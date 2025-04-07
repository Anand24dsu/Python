import requests
import mysql.connector
import re
from datetime import datetime

# MySQL Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "$dop@123",
    "database": "devops"
}

# Prometheus Node Exporter URL
PROMETHEUS_URL = "http://localhost:9100/metrics"

# Connect to MySQL Database
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Create a more comprehensive table to store metrics with labels
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS node_metrics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            metric_name VARCHAR(255),
            metric_labels JSON,
            metric_value DOUBLE,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

except mysql.connector.Error as err:
    print(f"MySQL Connection Error: {err}")
    exit()

# Parse Prometheus metrics
def parse_metric_line(line):
    # Match pattern for metrics with labels: name{label="value",...} value
    match = re.match(r'^([a-zA-Z0-9_:]+)(\{[^}]+\})?\s+(.+)$', line)
    if not match:
        return None
    
    metric_name = match.group(1)
    labels_str = match.group(2) or ""
    value_str = match.group(3)
    
    # Parse labels into a dictionary
    labels = {}
    if labels_str:
        # Strip the curly braces
        labels_str = labels_str[1:-1]
        label_pairs = re.findall(r'([a-zA-Z0-9_]+)="([^"]*)"', labels_str)
        for key, value in label_pairs:
            labels[key] = value
    
    # Parse value
    try:
        value = float(value_str)
        return (metric_name, labels, value)
    except ValueError:
        return None

# Fetch metrics from Node Exporter
try:
    response = requests.get(PROMETHEUS_URL)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print(response.text)
    else:
        lines = response.text.split("\n")
        metrics_count = 0
        
        for line in lines:
            if line and not line.startswith("#"):  # Ignore comments
                parsed = parse_metric_line(line)
                if parsed:
                    metric_name, labels, value = parsed
                    
                    # Convert labels dict to JSON string
                    import json
                    labels_json = json.dumps(labels)
                    
                    # Insert data into MySQL
                    cursor.execute(
                        "INSERT INTO node_metrics (metric_name, metric_labels, metric_value) VALUES (%s, %s, %s)",
                        (metric_name, labels_json, value)
                    )
                    metrics_count += 1
        
        conn.commit()
        print(f"✅ {metrics_count} metrics stored in MySQL successfully!")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
finally:
    # Close MySQL connection
    cursor.close()
    conn.close()