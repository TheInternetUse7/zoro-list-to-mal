import xml.etree.ElementTree as ET
import sys, re

# filename = f'{sys.argv[1]}'
filename = "export.xml"

# get mal links
tree = ET.parse(filename)
root = tree.getroot()

#get mal ids
malIds = []
for item in root.findall('item'):
    malUrls = item[1].text
    malIds = malIds + (re.findall(r'\d+', malUrls))