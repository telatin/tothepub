import json
import requests
import xmltodict
import csv

with open('input.json', 'r') as file:
    data = json.load(file)
    all_locations = [] 
    valid_businesses = ['Restaurant/Cafe/Canteen', 'Pub/bar/nightclub']
    fields = ['BusinessName', 'BusinessType', 'AddressLine1', 'AddressLine2', 'AddressLine3', 'PostCode', 'RatingValue', 'RatingDate', 'LocalAuthorityName', 'Latitude', 'Longitude'] 
    for authority,xml  in data.items():
        print(f"Authority: {authority}, XML: {xml}")

        response = requests.get(xml)
        if response.status_code == 200:
            xml_data = xmltodict.parse(response.text)
            locations = xmltodict.parse(response.text)['FHRSEstablishment']["EstablishmentCollection"]['EstablishmentDetail']
            for location in locations:
                if location.get('Geocode') and location['BusinessType'] in valid_businesses:
                    filtered_location = {field: location.get(field, None) for field in fields}
                    filtered_location['Latitude'] = location['Geocode'].get('Latitude')
                    filtered_location['Longitude'] = location['Geocode'].get('Longitude')
                    all_locations.append(filtered_location)
                    

        else:
            print(f"Failed to fetch XML from {xml}")

    with open('tothepub.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        writer.writeheader()
        for location in all_locations:
            writer.writerow(location)