import requests
import json

def getJobDetailsFromUrl(jenkinsUrl):
    url = f'{jenkinsUrl}/job/api/json?pretty=true&tree=builds[jobname,number,result,duration]'
    response = requests.get(url)
    
    # Print response text for debugging
    print(response.text)
    
    
    data = response.json()
    

    builds = data.get("builds", [])
    
    for build in builds:
        job_name = build.get("jobname", "N/A")
        number = build.get("number", "N/A")
        result = build.get("result", "N/A")
        duration = build.get("duration", "N/A")
        print(f'Build Number: {job_name}, {number}, Result: {result}, Duration: {duration}')

# Example usage
jenkinsUrl = "http://localhost:8080"
getJobDetailsFromUrl(jenkinsUrl)
