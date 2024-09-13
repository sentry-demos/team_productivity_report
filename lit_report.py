import requests
import sys
import json
import urllib.parse
from datetime import datetime, timezone
import time

if len(sys.argv) < 6:
    print("Exisitng the script: Expecting 5 parameters: <sentry_project (string)>, <start_date (datetime)>, <end_date (datetime)>, <top_n_issues (int)>, <api_key (string)>")
    exit()

sentry_project = sys.argv[1]
start_date = urllib.parse.quote(datetime.strptime(sys.argv[2], "%m/%d/%Y").isoformat())
end_date = urllib.parse.quote(datetime.strptime(sys.argv[3], "%m/%d/%Y").isoformat())
top_n_issues = int(sys.argv[4])
api_key = sys.argv[5]

TIME_OUT = 10
get_project_api = f'https://sentry.io/api/0/projects/{your_org_slug}/{sentry_project}/'

print(get_project_api)

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

data = None

project_results = {
    "id": "",
    "slug": "",
    "name": "",
    "teams": []
}
response = requests.get(get_project_api, headers=headers)

if response is not None and response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    project_results["id"] = data["id"]
    project_results["slug"] = data["slug"]
    project_results["name"] = data["name"]
else:
    # Print an error message if the request failed
    print(f"Failed to retrieve project: {response.status_code}")
    exit()

project_id = data["id"]

get_project_issues_api = 'https://us.sentry.io/api/0/organizations/{your_org_slug}/issues/?collapse=unhandled&end={end_date}&project={project_id}&query=is%3Aunresolved%20assigned%3A%23{team_slug}&shortIdLookup=1&start={start_date}&sort=freq'

issues = []
top_issues = []
events_count = 0

for team in data["teams"]:
    teamIssuesUrl = get_project_issues_api.format(project_id = project_id, team_slug = team['slug'], start_date = start_date, end_date = end_date)
    time.sleep(0.01)
    issuesResponse = requests.get(teamIssuesUrl, headers=headers, timeout=TIME_OUT)
    if issuesResponse is not None and response.status_code == 200:
        issues = issues + issuesResponse.json()
        top_issues = issues[:top_n_issues]
        next = issuesResponse.links.get('next', {}).get('results') == 'true'
        while next:
            teamIssuesUrl = issuesResponse.links.get('next', {}).get('url')
            issuesResponse = requests.get(teamIssuesUrl, headers=headers)
            next = issuesResponse.links.get('next', {}).get('results') == 'true'
            issues = issues + issuesResponse.json()
        
        for issue in issues:
            events_count = events_count + int(issue["count"])


        project_results["teams"].append({
            "name": team['slug'],
            "number_of_issues": len(issues),
            "number_of_events": events_count,
            "top_issues": top_issues
        })

        issues = []
        top_issues = []
        events_count = 0

    else:
        # Print an error message if the request failed
        print(f"Failed to retrieve team issues: {response.status_code}")

print(json.dumps(project_results))
