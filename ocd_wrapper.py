import json
from pprint import pprint

import requests

from sunlight_api_key import SUNLIGHT_API_KEY


BASE_URL = "https://api.opencivicdata.org/"
header = {"X-APIKEY": SUNLIGHT_API_KEY}


def lookup(ocd_id):
    ''' Look up objects based on their UID '''

    # Check for errors in the ID parameter
    if type(ocd_id) is not str:
        raise AssertionError("OCD ID must be a string")

    # Make request to server
    url = BASE_URL + ocd_id
    response = requests.get(url, headers=header)
    response.raise_for_status()
    
    # Parse response text and return the object
    response_object = json.loads(response.text)
    return response_object


def search(ocd_type, search_terms):
    ''' Search for objects of a given type '''

    # Check for errors in the search parameters
    if type(search_terms) is not dict:
        raise AssertionError("Search terms must be provided in a dictionary")

    VALID_OCD_TYPES = [
            "jurisdictions",
            "divisions",
            "organizations",
            "people",
            "bills",
            "votes",
            "events"
            ]
    if ocd_type not in VALID_OCD_TYPES:
        raise AssertionError(
                "OCD type must be one of: {}".format(VALID_OCD_TYPES)
                )

    # Extract the results from every page of server responses
    url = BASE_URL + ocd_type

    page_to_retrieve = 1
    last_page = False
    results = []

    while not last_page:
        search_terms["page"] = page_to_retrieve
        
        response = requests.get(url, params=search_terms, headers=header)
        response.raise_for_status()

        response_object = json.loads(response.text)
        results.extend(response_object["results"])

        if response_object["meta"]["page"] == \
                response_object["meta"]["max_page"]:
            last_page = True
        else:
            page_to_retrieve = page_to_retrieve + 1

    return results


# Test the functionality of this module
if __name__ == "__main__":
    # EXAMPLE_PERSON_ID = "ocd-person/d4bcb1e7-5956-4432-9111-ab25c9ff3fd7"
    # person = lookup(EXAMPLE_PERSON_ID)
    # pprint(person)

    # EXAMPLE_PEOPLE_SEARCH_PARAMETERS = {"name": "John Smith"}
    # people = search("people", EXAMPLE_PEOPLE_SEARCH_PARAMETERS)
    # pprint(people)

    EXAMPLE_ORGANIZATIONS_SEARCH_PARAMETERS = {
            "jurisdiction_id": "ocd-jurisdiction/country:us/state:mi/government"
            }
    organizations = \
            search("organizations", EXAMPLE_ORGANIZATIONS_SEARCH_PARAMETERS)
    pprint(organizations)

