import logging
import os
from hubspot import HubSpot
import json
from pprint import pprint

"""
This is the definition we are expecting back from the hubspot contacts:
https://github.com/HubSpot/hubspot-api-python/blob/master/hubspot/crm/contacts/models/simple_public_object_with_associations.py

[{'archived': False,
'archived_at': None,
'associations': None,
'created_at': datetime.datetime(2021, 11, 29, 18, 36, 2, 998000, tzinfo=tzutc()),
'id': '1',
'properties': {'createdate': '2021-11-29T18:36:02.998Z',
'email': 'emailmaria@hubspot.com',
'firstname': 'Maria',
'hs_object_id': '1',
'lastmodifieddate': '2022-12-14T03:54:41.361Z',
'lastname': 'Johnson (Sample Contact)'},
'properties_with_history': None,
'updated_at': datetime.datetime(2022, 12, 14, 3, 54, 41, 361000, tzinfo=tzutc())},
{'archived': False,
'archived_at': None,
'associations': None,
'created_at': datetime.datetime(2021, 11, 29, 18, 36, 3, 340000, tzinfo=tzutc()),
'id': '51',
'properties': {'createdate': '2021-11-29T18:36:03.340Z',
'email': 'bh@hubspot.com',
'firstname': 'Brian',
'hs_object_id': '51',
'lastmodifieddate': '2022-09-12T16:37:49.931Z',
'lastname': 'Halligan (Sample Contact)'},
'properties_with_history': None,
'updated_at': datetime.datetime(2022, 9, 12, 16, 37, 49, 931000, tzinfo=tzutc())}]

"""

def main():
    logging.basicConfig(level=logging.INFO)
    sdk_key = os.environ['HUBSPOT_KEY']

    logging.info(f"got sdk key {sdk_key}".format())

    api_client = HubSpot(access_token=sdk_key)

    all_contacts = api_client.crm.contacts.get_all()

    pprint(all_contacts)


    print(json.dumps(all_contacts, sort_keys=True, indent=4))

if __name__ == '__main__':
    main()
