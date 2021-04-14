# get work logs tutorial:
# https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-worklogs/#api-rest-api-3-worklog-list-post

# get story points tutorial:
# https://community.atlassian.com/t5/Answers-Developer-Questions/Story-Points-using-JIRA-Agile-REST-API/qaq-p/511133

import requests
from requests.auth import HTTPBasicAuth
import json
import datetime

import globals

auth = HTTPBasicAuth(globals.jira_user, globals.jira_api_token)

def getSprintStartDate():
    
    # get most recent Monday for sprint start date 
    today = datetime.date.today()
    sprint_start_date = today - datetime.timedelta(days=today.weekday()) - datetime.timedelta(days=7) - datetime.timedelta(days=7)
    
    timestamp = datetime.datetime(
        sprint_start_date.year, 
        sprint_start_date.month, 
        sprint_start_date.day).timestamp()
    
    return int(timestamp)*1000 # convert to mS

def getWorklogIds(start_date):
    url = globals.base_url + "/rest/api/3/worklog/updated"

    headers = {
       "Accept": "application/json"
    }
    
    query = {
       'since': start_date
    }
    
    response = requests.request(
       "GET",
       url,
       headers=headers,
       params=query,
       auth=auth
    )
    
    response_dict = response.json() 

    values_dict = response_dict["values"]

    worklog_dict = {}
    for worklog in values_dict: #values_dict.keys():
        
        worklog_dict[ worklog["worklogId"] ] = None
        
    return list(worklog_dict.keys())



def getWorkLogsHelper(ID_list):
    url = globals.base_url + "/rest/api/3/worklog/list"

    headers = {
       "Accept": "application/json",
       "Content-Type": "application/json"
    }

    payload = json.dumps( {
      "ids": ID_list
    } )

    response = requests.request(
       "POST",
       url,
       data=payload,
       headers=headers,
       auth=auth
    )

    response_list = response.json()
    
    worklog_dict = {}
    for workLog in response_list:
        worklog_dict[ workLog['id'] ] = workLog
    
    return worklog_dict
        
        
def getWorklogs():
    start_date = getSprintStartDate()
    worklog_IDs = getWorklogIds(start_date)
    worklogs = getWorkLogsHelper(worklog_IDs)
    return worklogs
        
        
def getAccountIds():
    
    url = globals.base_url + "/rest/api/3/users"

    headers = {
       "Accept": "application/json"
    }

    response = requests.request(
       "GET",
       url,
       headers=headers,
       auth=auth
    )
    
    response_list = response.json()
    
    account_ids = []
    for item in response_list:
        account_ids = account_ids + [item['accountId']]
        
    return account_ids


def getTeam():
    account_ids = getAccountIds()
    print(account_ids)
    
    url = globals.base_url + "/rest/api/3/user/bulk"

    headers = {
       "Accept": "application/json"
    }

    query = {
       'accountId': account_ids[9] #'{accountId}'
    }

    response = requests.request(
       "GET",
       url,
       headers=headers,
       params=query,
       auth=auth
    )

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))



def getIssue(issue_id):
    url = "https://wardenclyffeorganization.atlassian.net/rest/api/3/issue/" + issue_id
    
    headers = {
       "Accept": "application/json"
    }

    response = requests.request(
       "GET",
       url,
       headers=headers,
       auth=auth
    )

    return response.json()

def getStoryPoints(issue_id):
    story_points_field_id = 'customfield_10026'
    issue = getIssue(issue_id)
    return str(int(issue['fields'][story_points_field_id]))
    

#if __name__ == '__main__':
    
    