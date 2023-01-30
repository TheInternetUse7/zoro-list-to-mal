import xmlparser, requests, time, os, shutil

def main():
    for animeId in xmlparser.malIds:

        # ffs there's rate limit smh
        time.sleep(0.5)
        response = requests.get(f"https://api.jikan.moe/v4/anime/{animeId}")
        jsonResponse = response.json()

        if response.status_code == 200:
            malId = jsonResponse["data"]["mal_id"]
            title = jsonResponse["data"]["titles"][0]['title']
            seriesType = jsonResponse["data"]["type"]
            episodes = jsonResponse["data"]["episodes"]

            print(malId, seriesType, title, episodes)

            data = f"""<anime>
            <series_animedb_id>{malId}</series_animedb_id>
            <series_title><![CDATA[{title}]]></series_title>
            <series_type>{seriesType}</series_type>
            <series_episodes>{episodes}</series_episodes>
            <my_id>0</my_id>
            <my_watched_episodes>{episodes}</my_watched_episodes>
            <my_start_date>0000-00-00</my_start_date>
            <my_finish_date>0000-00-00</my_finish_date>
            <my_fansub_group><![CDATA[]]></my_fansub_group>
            <my_rated></my_rated>
            <my_score>0</my_score>
            <my_dvd></my_dvd>
            <my_storage></my_storage>
            <my_status>Completed</my_status>
            <my_comments><![CDATA[]]></my_comments>
            <my_times_watched>0</my_times_watched>
            <my_rewatch_value></my_rewatch_value>
            <my_downloaded_eps>0</my_downloaded_eps>
            <my_tags></my_tags>
            <my_rewatching>0</my_rewatching>
            <my_rewatching_ep>0</my_rewatching_ep>
            <update_on_import>1</update_on_import>
        </anime>"""
            with open('.temp.xml', 'a', encoding='utf-8') as f:
                f.write(data)

def prepend_line(file_name, line):
    """ Insert given string as a new line at the beginning of a file """
    # define name of temporary dummy file
    dummy_file = file_name + '.bak'
    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Write given line to the dummy file
        write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)

def append_line():
    with open('.temp.xml', 'a', encoding='utf-8') as f:
        f.write("</myanimelist>")

    shutil.copyfile(".temp.xml", "final.xml")
    os.remove(".temp.xml")
main()
prepend_line(".temp.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<myanimelist>')
append_line()
