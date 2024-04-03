import requests
from bs4 import BeautifulSoup
import re
import json

def get_xml_links(file='html'):
    response = open('html').read()
    soup = BeautifulSoup(response, 'html.parser')

    xml_links = {}
    for link in soup.find_all('a', href=True):
        if 'Welsh language' not in link.text:
            if re.match(r'https:\/\/ratings\.food\.gov\.uk\/api\/open-data-files\/.*\.xml', link['href']):
                xml_links[link.text.replace(' (English language)', '')] = link['href']

    return xml_links

# Use the function
xml_links = get_xml_links()
with open('input.json', 'w') as json_file:
    json.dump(xml_links, json_file, indent=4)