import mysql.connector
import requests
import sys

def create_db_connection(job_name):
    db_name = "devops"
    table_name = f"job_{job_name}"
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="$dop@123",
        auth_plugin="mysql_native_password"  # Added to fix authentication issue
    )
    cursor = db_connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.execute(f"USE {db_name}")
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (number INT, result VARCHAR(255), duration INT)")
    cursor.close()
    return db_connection, table_name

def get_job_details_from_url(jenkins_url, job_name):
    url = f'{jenkins_url}/job/{job_name}/api/json?pretty=true&tree=builds[number,result,duration]'
    auth = requests.auth.HTTPBasicAuth('admin', '11755eb213bad5ff76bb746c99621105b9')

    for _ in range(5):
        try:
            response = requests.get(url, auth=auth, timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")

    print(f"The request timed out for {url}.")
    return None

def print_job_details(result):
    if result is not None:
        for build_rec in result["builds"]:
            print(build_rec["number"], build_rec["result"], build_rec["duration"])

def insert_job_details(job_name, job_details, jenkins_url):
    db_connection, table_name = create_db_connection(job_name)
    cursor = db_connection.cursor()
    insert_query = f"INSERT INTO {table_name} (number, result, duration) VALUES (%s, %s, %s)"
    data = [(build["number"], build["result"], build["duration"]) for build in job_details["builds"]]

    try:
        cursor.executemany(insert_query, data)
        db_connection.commit()
        print(f"{cursor.rowcount} records inserted successfully into {table_name} table.")
    except mysql.connector.Error as error:
        print(f"Failed to insert record into {table_name} table: {error}")
    finally:
        cursor.close()
        db_connection.close()

# Correct function call with appropriate parameter names
job_name = "01_BUILD_JOB"
jenkins_url ="http://localhost:8080"

result = get_job_details_from_url(jenkins_url=jenkins_url, job_name=job_name)

if result is not None:
    print_job_details(result)
    insert_job_details(job_name, result, jenkins_url)
