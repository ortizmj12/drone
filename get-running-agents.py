#!/usr/bin/env python

'''
This script is used to find all of the drone agents that are currently running jobs.

Example command and output:
    $ python drone-get-running-agents.py
    TeamA/frontend-service #646: drone-agent006.example.net
    TeamB/backend-service #4063: drone-agent003.example.net
    TeamC/machine-learning #2455: drone-agent002.example.net
    TeamD/core-components #4179: drone-agent009.example.net
'''

import yaml
import os
import requests
import json

DRONE_BUILDS = 'https://drone.example.net/api/builds'
DRONE_BUILDS_API_URL = 'https://drone.example.net/api/repos/{}/{}/builds/{}'
headers = ''

def get_token():
    home = os.path.expanduser('~')
    credentials_file = home + '/.credentials'
    if os.path.isfile(credentials_file):
        credentials = yaml.load(open(credentials_file))
        token = credentials['drone']['token']
        return token
    else:
        token = raw_input('Enter Drone Token: ')
        return token

def get_token():
    home = os.path.expanduser('~')
    credentials_file = home + '/.credentials'
    if os.path.isfile(credentials_file):
        credentials = yaml.load(open(credentials_file))
        token = credentials['drone']['token']
        return token
    else:
        token = raw_input('Enter Drone Token: ')
        return token

def main():
    token = get_token()
    headers = {'Authorization': 'Bearer ' + token}
    builds_request = requests.get(DRONE_BUILDS, headers=headers)
    builds_data = builds_request.json()
    for num in range(0, len(builds_data)):
        status = builds_data[num]['status']
        owner = builds_data[num]['owner']
        name = builds_data[num]['name']
        number = builds_data[num]['number']

        if status == 'running':
            api_url = DRONE_BUILDS_API_URL.format(owner, name, number)
            build_request = requests.get(api_url, headers=headers)
            build_data = build_request.json()
            build_agent = build_data['procs'][0]['machine']
            print(owner + '/' + name + ' #' + str(number) + ': ' + build_agent)


if __name__ == '__main__':
    main()

