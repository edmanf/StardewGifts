import json
import requests

API_URL = "https://stardewvalleywiki.com/mediawiki/api.php"


def action_query_category(category, continueid=None):
    """
        Query the wiki for categorymembers of the given category
        and return the result.
    """

    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": category,
        "format": "json"}
    if continueid:
        params["cmcontinue"] = continueid

    response = requests.get(API_URL, params)
    return json.loads(response.text)


def action_parse_pageid(pageid):
    params = {
        "action": "parse",
        "pageid": pageid,
        "format": "json"
    }

    response = requests.get(API_URL, params)
    return json.loads(response.text)
