# zoro-list-to-mal

## wip: i have no idea what i'm doing yet again, but i wanted to help a friend

## info:
**CURRENTLY ONLY WORKS WITH ANILIST** (use anilist :P )<BR>
uhh this uses https://jikan.moe/ and they 3 request/sec limit so it might feel slow.<br>
there's a similar tool at https://github.com/Adaptz/Zoro_Export_to_MAL which i found out about after i finished this :skull:

## installation:

- make sure you have the latest Python.
- you also need `requests` so install that.
- you need `pip` ig
- download this repo as a zip and extract or `git clone https://github.com/TheInternetUse7/zoro-list-to-mal`
- go to into `zoro-list-to-mal` folder and run `pip install -r requirements.txt`


## instructions:

1. Export your list by going to https://zoro.to/user/mal?tab=export make sure it like in the picture below, enable "Group by folder"
<img src="https://theinternetuser.is-from.space/r/chrome_JU8MsCpPUj.png">

2. you should get a file named `export.json` if not, name it that. put that file in the same folder as `mainjson.py`

3. run the file: `python mainjson.py`

## things to fix:
- ~~make it use `.json` files as input bc zoro.to gives more info with that (like watch status)~~
- ~~i forgor :skull:~~
- fix the xml import(?)

## features:
- bad code
- ~~set all of your list as "Completed"~~ fixed. instead, you get to have all your ep progress set to 0 bc zoro doesnt give that info on the json
