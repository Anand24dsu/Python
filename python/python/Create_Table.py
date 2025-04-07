import mysql.connector
import os, sys
import requests

db_connection = mysql.connector.connect(
    host="localhost",       # e.g., "localhost" or IP address
    user="root",
    password="$dop@123",
    database="devops"
)

def getJobDetailsFromUrl(jenkinsUrl, jobName):
    url = f'{jenkinsUrl}/job/{jobName}/api/json?pretty=true&tree=builds[number,result,duration]'
   
    for _ in range(5):
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
       
    print(f"The request timed out for {url}. Response was {response}.")
    return None

def printJobDetails(result):
    if result is not None:
        for buildRec in result["builds"]:
            print(buildRec["number"], buildRec["result"], buildRec["duration"])

def insertJobDetails(db_connection, jobDetails):
    cursor = db_connection.cursor()
    insert_query = "INSERT INTO jenkins_bulid_details_tables (number, result, duration) VALUES (%s, %s, %s)"
    data = [(build["number"], build["result"], build["duration"]) for build in jobDetails["builds"]]
    
    try:
        cursor.executemany(insert_query, data)
        db_connection.commit()
        print(f"{cursor.rowcount} records inserted successfully into jenkins_bulid_details_tables table.")
    except mysql.connector.Error as error:
        print(f"Failed to insert record into jenkins_bulid_details_tables table: {error}")
    finally:
        cursor.close()

jobNme = "MY_FIRST_JOB_WITH_GIT"
result = getJobDetailsFromUrl(jenkinsUrl="http://localhost:8080", jobName=jobNme)

if result is not None:
    printJobDetails(result)
    insertJobDetails(db_connection, result)

db_connection.close()