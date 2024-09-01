import json
import re
import asyncio
import aiohttp
import logging
from lxml import etree as ET
from typing import Dict, List, Tuple
import yaml
import time
from datetime import datetime

# Load configuration
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(filename: str) -> Dict:
    with open(filename) as file:
        return json.load(file)

def id_fetch(status: List[Dict]) -> List[str]:
    return [re.findall(r'\d+', item['link'])[0] for item in status]

async def fetch_anime_data(session: aiohttp.ClientSession, animeId: str, retries: int = 3) -> Dict:
    url = f"{config['api_url']}/anime/{animeId}"
    for attempt in range(retries):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 429:
                    retry_after = int(response.headers.get('Retry-After', 5))
                    logging.warning(f"Rate limit hit for anime {animeId}. Retrying after {retry_after} seconds.")
                    await asyncio.sleep(retry_after)
                else:
                    logging.error(f"Error fetching anime {animeId}: {response.status}")
                    return None
        except aiohttp.ClientError as e:
            logging.error(f"Network error fetching anime {animeId}: {e}")
            await asyncio.sleep(1)
    logging.error(f"Failed to fetch anime {animeId} after {retries} attempts")
    return None

def create_cdata_element(parent, tag, text):
    elem = ET.SubElement(parent, tag)
    elem.text = ET.CDATA(text)
    return elem

async def process_anime(session: aiohttp.ClientSession, animeId: str, status: str, xml_root: ET.Element) -> None:
    data = await fetch_anime_data(session, animeId)
    if data:
        anime_data = data["data"]
        anime = ET.SubElement(xml_root, "anime")
        ET.SubElement(anime, "series_animedb_id").text = str(anime_data["mal_id"])
        create_cdata_element(anime, "series_title", anime_data['titles'][0]['title'])
        ET.SubElement(anime, "series_type").text = anime_data["type"]
        ET.SubElement(anime, "series_episodes").text = str(anime_data["episodes"])
        ET.SubElement(anime, "my_id").text = "0"
        ET.SubElement(anime, "my_watched_episodes").text = str(anime_data["episodes"] if status == "Completed" else 0)
        ET.SubElement(anime, "my_start_date").text = "0000-00-00"
        ET.SubElement(anime, "my_finish_date").text = "0000-00-00"
        ET.SubElement(anime, "my_rated")
        ET.SubElement(anime, "my_score").text = "0"
        ET.SubElement(anime, "my_storage")
        ET.SubElement(anime, "my_storage_value").text = "0.00"
        ET.SubElement(anime, "my_status").text = status
        create_cdata_element(anime, "my_comments", "")
        ET.SubElement(anime, "my_times_watched").text = "0"
        ET.SubElement(anime, "my_rewatch_value")
        ET.SubElement(anime, "my_priority").text = "LOW"
        create_cdata_element(anime, "my_tags", "")
        ET.SubElement(anime, "my_rewatching").text = "0"
        ET.SubElement(anime, "my_rewatching_ep").text = "0"
        ET.SubElement(anime, "my_discuss").text = "1"
        ET.SubElement(anime, "my_sns").text = "default"
        ET.SubElement(anime, "update_on_import").text = "1"
        logging.info(f"Processed anime: {anime_data['titles'][0]['title']}")
    else:
        logging.error(f"Failed to process anime: {animeId}")

async def process_chunk(session: aiohttp.ClientSession, chunk: List[str], status: str, xml_root: ET.Element) -> None:
    tasks = [process_anime(session, animeId, status, xml_root) for animeId in chunk]
    await asyncio.gather(*tasks)

async def main() -> None:
    data = load_data(config['input_file'])
    
    status_mapping: Dict[str, Tuple[str, List[Dict]]] = {
        'Watching': ('Watching', data['Watching']),
        'Completed': ('Completed', data['Completed']),
        'On-Hold': ('On-Hold', data['On-Hold']),
        'Dropped': ('Dropped', data['Dropped']),
        'Plan to watch': ('Plan to Watch', data['Plan to watch'])
    }

    xml_root = ET.Element("myanimelist")
    
    # Add myinfo section (optional)
    # myinfo = ET.SubElement(xml_root, "myinfo")
    # ET.SubElement(myinfo, "user_id").text = "YOUR_USER_ID"
    # ET.SubElement(myinfo, "user_name").text = "YOUR_USERNAME"
    # ET.SubElement(myinfo, "user_export_type").text = "1"
    # ET.SubElement(myinfo, "user_total_anime").text = str(sum(len(anime_list) for _, anime_list in status_mapping.values()))
    # ET.SubElement(myinfo, "user_total_watching").text = str(len(data['Watching']))
    # ET.SubElement(myinfo, "user_total_completed").text = str(len(data['Completed']))
    # ET.SubElement(myinfo, "user_total_onhold").text = str(len(data['On-Hold']))
    # ET.SubElement(myinfo, "user_total_dropped").text = str(len(data['Dropped']))
    # ET.SubElement(myinfo, "user_total_plantowatch").text = str(len(data['Plan to watch']))
    
    async with aiohttp.ClientSession() as session:
        for status, (mal_status, anime_list) in status_mapping.items():
            anime_ids = id_fetch(anime_list)
            chunk_size = config['chunk_size']
            for i in range(0, len(anime_ids), chunk_size):
                chunk = anime_ids[i:i+chunk_size]
                await process_chunk(session, chunk, mal_status, xml_root)
                await asyncio.sleep(1)  # Add a delay between chunks to help with rate limiting

    tree = ET.ElementTree(xml_root)
    
    # Add XML declaration and comments
    xml_declaration = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    comments = '''<!--
 Created by a wacky script from theinternetuser
-->

'''
    
    # Write the XML to a file with correct encoding
    with open(config['output_file'], 'wb') as f:  # Open in binary mode for utf-8 encoding
        f.write(xml_declaration.encode('utf-8'))
        f.write(comments.encode('utf-8'))
        tree.write(f, encoding='utf-8', pretty_print=True, xml_declaration=False)
    
    logging.info(f"Anime list exported to {config['output_file']}")

if __name__ == "__main__":
    asyncio.run(main())
