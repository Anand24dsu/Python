import os
import sys
import requests
import mysql.connector
from mysql.connector import Error
import plotly.graph_objects as go
import plotly.express as px

def getJobDetailsFromUrl(jenkinsUrl, jobName):
    url = f'{jenkinsUrl}/job/{jobName}/api/json?pretty=true&tree=builds[number,result,duration]'

    for _ in range(5):
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()

    print(f"The request timed out for {url}. Response as {response}.")
    return None

def insertBuildDetailsToDB(job_name, build_number, build_status, build_duration):
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='devops',
            user='root',
            password='$dop@123'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            insert_query = """
                INSERT INTO jenkins_build_details_table (job_name, build_number, build_status, build_duration)
                VALUES (%s, %s, %s, %s)
            
            """
            cursor.execute(insert_query, (job_name, build_number, build_status, build_duration))
            connection.commit()
            print(f"Inserted/Updated build details for job: {job_name}, build number: {build_number}")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def plotBuildData(job_name, builds_data):
    # Pie Chart - Success vs Failure
    success_count = sum(1 for build in builds_data if build['status'] == 1)
    failure_count = len(builds_data) - success_count
    pie_chart = go.Figure(data=[go.Pie(labels=["Success", "Failure"], values=[success_count, failure_count])])
    pie_chart.update_layout(title=f"{job_name} - Build Success vs Failure")

    # Bar Chart - Build Duration
    build_numbers = [str(build['number']) for build in builds_data]
    build_durations = [build['duration'] / 1000 for build in builds_data]  # Convert ms to seconds

    bar_chart = px.bar(
        x=build_numbers,
        y=build_durations,
        labels={'x': 'Build Number', 'y': 'Duration (seconds)'},
        title=f"{job_name} - Build Duration for Each Build"
    )

    # Show the charts
    pie_chart.show()
    bar_chart.show()

def main():
    jobNme = input("Enter job name: ")
    result = getJobDetailsFromUrl(jenkinsUrl="http://localhost:8080", jobName=jobNme)

    if result:
        builds_data = []
        for buildRec in result["builds"]:
            build_number = buildRec["number"]
            build_status = 1 if buildRec["result"] == "SUCCESS" else 0 
            build_duration = buildRec["duration"]

            print(f"Build Number: {build_number}, Status: {build_status}, Duration: {build_duration}")

            # Save to DB
            insertBuildDetailsToDB(jobNme, build_number, build_status, build_duration)
            
            # Collect the build data for visualization
            builds_data.append({'number': build_number, 'status': build_status, 'duration': build_duration})

        # Plot the data with job name as part of the graph
        plotBuildData(jobNme, builds_data)

if __name__ == '__main__':
    main()
