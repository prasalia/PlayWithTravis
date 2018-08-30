#!/usr/bin/env python2.7
import json
import requests
import base64
import os

REST_URL = 'https://api.travis-ci.com'
id = '3177861'

AUTH_HEADER = \
    {
        'Travis-API-Version': '3',
        'User-Agent': 'API Explorer',
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'token gqKQVjzU-RFzycYj-GA7DA'
    }

res = requests.get(REST_URL + '/owner/ConnectedHomes/repos?limit=10', headers = AUTH_HEADER)
#res = requests.get(REST_URL + '/user', headers = AUTH_HEADER)
if res.ok:
    json_result = res.json()
    print json.dumps(json_result,indent=4)
else:
    res.raise_for_status()

/repo/3177861/builds?limit=10
