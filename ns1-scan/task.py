import os, sys, requests
import logging
import json


def get_all_zones(headers):
    all_zones = []
    zones = get_zones(headers)
    all_zones += zones["zones"]
    if zones["link"] != None:
        link = zones["link"]
        while link != None:
            zones = get_zones(headers, link=link)
            all_zones += zones["zones"]
            link = zones["link"]
    return all_zones


def get_zones(headers, link=None):
    zones_response = None
    if link == None:
        zones_response = requests.get('https://api.nsone.net/v1/zones', headers=headers)
    else:
        zones_response = requests.get(link, headers=headers)
    
    if zones_response.links == {}:
        return { "status": zones_response.status_code, "zones": zones_response.json(), "link": None }
    else :
        return { "status": zones_response.status_code, "zones": zones_response.json(), "link": zones_response.links.get('next', None).get('url', None) }

def get_records(headers, zone):
    zone_response = requests.get(f'https://api.nsone.net/v1/zones/{zone}', headers=headers)
    return { "status": zone_response.status_code, "records": zone_response.json().get('records', None) }


def get_record_details(headers, zone_name, domain, type="CNAME"):
    record_response = requests.get(f"https://api.nsone.net/v1/zones/{zone_name}/{domain}/{type}", headers=headers)
    return record_response.json()

# Get apiKey and output file path
apiKey = os.environ.get("NSONE_API_KEY")
outputFile = os.environ.get("VOL_OUTPUT_DIR")
if apiKey == None or outputFile == None: 
    if apiKey == None:
        logging.exception("No NSONE_API_KEY env variable value provided")
        sys.exit("No NSONE_API_KEY env variable value provided")
    if outputFile == None:
        logging.exception("No VOL_OUTPUT_DIR env variable value provided")
        sys.exit("No VOL_OUTPUT_DIR env variable value provided")
else:
    headers={ "X-NSONE-Key": apiKey }
    # Get zones
    zones = get_all_zones(headers)

    zone_names = [z['zone'] for z in zones]
    print(zone_names)

    cname_records = []
    for name in zone_names:
        records = get_records(headers, name)
        for record in records.get('records'):
            if record.get('type').upper() in ("CNAME","A", "AAAA"):
                cname_records.append(get_record_details(headers, name, record.get('domain')))

    print(cname_records)
    # Save to file replace with save to storage account
    with open(outputFile, 'w') as f:
        json.dump(cname_records, f)
