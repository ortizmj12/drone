#!/usr/bin/env python

'''
This script is used to find the Drone agent that executed a past build/deploy.

Example:
    python get-drone-agent.py https://drone.example.net/SERVICE/frontend-service/173
'''

import argparse
import yaml
import os
import requests
import json

args = ''
drone_build = ''
headers = ''
DRONE_API_URL = 'https://drone.example.net/api/repos/{}/{}/builds/{}'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('drone_build',
                        help='URL of the Drone build',
                        type=str)
    args = parser.parse_args()
    return args

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

def create_api_url(url):
    project = url.split('/')[3]
    repo = url.split('/')[4]
    build = url.split('/')[5]

    api_url = DRONE_API_URL.format(project, repo, build)
    return api_url

def main():
    args = get_args()
    token = get_token()
    headers = {'Authorization': 'Bearer ' + token}
    api_url = create_api_url(args.drone_build)
    r = requests.get(api_url, headers=headers)
    data = r.json()
    print('Build agent: ' + data['procs'][0]['machine'])


if __name__ == '__main__':
    main()
