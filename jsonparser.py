import json, re

filename = open("export.json")

data = json.load(filename)
watching = data['Watching']
completed = data['Completed']
onhold = data['On-Hold']
dropped = data['Dropped']
planning = data['Plan to watch']

watc_id = []
comp_id = []
hold_id = []
drop_id = []
ptw_id = []

def id_fetch(status, id_type):
    for item in status:
        mal_url = item['link']
        id_type = id_type + (re.findall(r'\d+', mal_url))
    return id_type

watching_id = id_fetch(watching, watc_id)
completed_id = id_fetch(completed, comp_id)
onhold_id = id_fetch(onhold, hold_id)
dropped_id = id_fetch(dropped, drop_id)
planning_id = id_fetch(planning, ptw_id)