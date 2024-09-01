# zoro-list-to-mal

## wip: i have no idea what i'm doing

## info
- this will convert a list exported from zoro.to/aniwatch.to/hianime.to to a MAL export format that you can import to your AniList or MyAnimeList account. 
- uses <https://jikan.moe/> and they have 3 requests per second limit so it might be a bit slow.
- there's a similar tool at <https://github.com/Adaptz/Zoro_Export_to_MAL> which i found out about after i finished this 💀
- zoro/hianime doesnt provide your episode progress on the file so your ep count will be set to 0, except Completed list.

## installation

- make sure you have the latest Python along with `pip`.
- download this repo as a zip and extract or `git clone https://github.com/TheInternetUse7/zoro-list-to-mal`
- go to into `zoro-list-to-mal` folder and run `pip install -r requirements.txt`

## instructions

1. Export your list by going to ~~<https://zoro.to/user/mal?tab=export>~~ <https://hianime.to/user/mal?tab=export> make sure it like in the picture below, enable "Group by folder"
![Screenshot of export settings](https://theinternetuser.is-from.space/r/chrome_JU8MsCpPUj.png)

2. you should get a file named `export.json` if not, name it that. put that file in the same folder as `main.py`

3. run the file: `python main.py`

## features

- bad code
- ~~set all of your list as "Completed"~~ fixed. instead, you get to have all your ep progress set to 0 bc zoro doesnt give that info on the json
