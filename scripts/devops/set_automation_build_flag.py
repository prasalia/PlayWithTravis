#!/usr/bin/env python2.7
""" Script to determine whether to run an automation build and if yes set
    an environment variable in Travis configuration to true
"""
import sys
import json
import requests
import utils
import re
from subprocess import check_output, CalledProcessError
from datetime import datetime

REST_URL = 'https://api.travis-ci.com'
NGA_TRAVIS_REPO_ID = '3177861'
TRAVIS_TOKEN = 'gqKQVjzU-RFzycYj-GA7DA'
AUTH_HEADER = \
    {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Travis-API-Version': '3',
        'User-Agent': 'API Explorer',
        'Authorization' : 'token ' + TRAVIS_TOKEN
    }

if __name__ == '__main__':

    def initAutomationBuildFlag():
        """ Checks for the AUTOMATION_<ENV> configuration setting in Travis and creates one if it doesn't already exist
        """
        global env_var_id, env_var_value
        print 'Checking if the %s setting exists in Travis' % (env_var_name)
        res = requests.get('%s/repo/%s/env_vars' % (REST_URL, NGA_TRAVIS_REPO_ID), headers = AUTH_HEADER)
        if res.ok:
            json_result = res.json()
            if json_result['env_vars']:
                for item in json_result['env_vars']:
                    if item['name'] == env_var_name:
                        env_var_id = item['id'] if 'id' in item and item['id'] else None
                        env_var_value = item['value'] if 'value' in item and item['value'] else None
                        break
        else:
            res.raise_for_status()
        if not env_var_id:
            env_var_value = "off"
            print 'Setting %s not found. Creating one and setting it to %s' % (env_var_name, env_var_value)
            req_params = \
                {
                    "env_var.name" : env_var_name,
                    "env_var.value" : env_var_value,
                    "env_var.public" : True
                }
            res = requests.post('%s/repo/%s/env_vars' % (REST_URL, NGA_TRAVIS_REPO_ID), headers = AUTH_HEADER, params = req_params)
            if res.ok:
                json_result = res.json()
                if 'id' not in json_result or 'value' not in json_result or not json_result['id'] or not json_result['value']:
                    raise ValueError('Error: Failed to initialize the %s setting in Travis' % (env_var_name))
                else:
                    env_var_id = json_result['id']
            else:
                res.raise_for_status()
        else:
            print 'Setting %s found. Value is set to %s' % (env_var_name, env_var_value)

    def setEnvVarInTravis(id, name, value, public = True):
        """ Sets an environment variable setting in Travis
        """
        print 'Setting %s to %s in Travis' % (name, value)
        req_params = \
            {
                "env_var.name" : name,
                "env_var.value" : value,
                "env_var.public" : public
            }
        res = requests.patch('%s/repo/%s/env_var/%s' % (REST_URL, NGA_TRAVIS_REPO_ID, id), headers = AUTH_HEADER, params = req_params)
        if res.ok:
            json_result = res.json()
            if 'id' not in json_result or 'value' not in json_result or not json_result['id'] or not json_result['value']:
                raise ValueError('Error: Failed to initialize the %s setting in Travis' % (env_var_name))
        else:
            res.raise_for_status()

    env_var_id = env_var_value = None
    if sys.argv[1].lower() == 'develop':
        env_var_name = 'AUTOMATION_DEVELOP'
    elif sys.argv[1].lower() == 'release':
        env_var_name = 'AUTOMATION_RELEASE'
    initAutomationBuildFlag()
    if env_var_value.lower() != 'on':
        print 'Checking the time of the second last commit on this branch'
        cmd1 = 'git log -n 2 --format="%cd" --date=local --first-parent --merges | tail -1'
        print 'Checking the time of the last commit on this branch'
        cmd2 = 'git log -n 2 --format="%cd" --date=local --first-parent --merges | head -1'
        cmd_output1 = check_output(cmd1, shell = True)
        cmd_output2 = check_output(cmd2, shell = True)
        if cmd_output1 and cmd_output2:
            commit_date_second_last = datetime.strptime(cmd_output1.strip(), '%a %b %d %H:%M:%S %Y')
            commit_date_last = datetime.strptime(cmd_output2.strip(), '%a %b %d %H:%M:%S %Y')
            print 'Last commit made at %s' % (commit_date_last)
            print 'Second to Last commit made at %s' % (commit_date_second_last)
            days = utils.getdays(commit_date_second_last.strftime('%Y-%m-%d'))
            diff = utils.timediff(commit_date_second_last.strftime('%Y-%m-%dT%H:%M:%SZ'), commit_date_last.strftime('%Y-%m-%dT%H:%M:%SZ'))
            diff_hrs = float(diff) / 3600
            if int(diff) > 900:
                if days > 0:
                    print 'Setting %s to "preprod,mock" if not set already' % (env_var_name)
                    if env_var_value.lower() != 'preprod,mock':
                        setEnvVarInTravis(env_var_id, env_var_name, "preprod,mock")   
                else:   
                    if diff_hrs >= 12:
                        print 'Setting %s to "preprod,mock" if not set already' % (env_var_name)
                        if env_var_value.lower() != 'preprod,mock':
                            setEnvVarInTravis(env_var_id, env_var_name, "preprod,mock")   
                    elif diff_hrs >= 6 and diff_hrs < 12:
                        print 'Setting %s to "preprod" if not set already' % (env_var_name)
                        if env_var_value.lower() != 'preprod':
                            setEnvVarInTravis(env_var_id, env_var_name, "preprod")    
                    else:
                        print 'Setting %s to off if not set already' % (env_var_name)
                        if env_var_value.lower() != 'off':
                            setEnvVarInTravis(env_var_id, env_var_name, "off")
            else:
                print 'Time difference between both commits is less than 15 min. Nothing to be done'
        else:
            raise ValueError('Error: Failed to determine the second to last commit date in Travis')
