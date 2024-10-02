import os
import mysql.connector
from flask import Flask
import random
from datetime import datetime
import threading
import time

app = Flask(__name__)

# MySQL connection details from environment variables
DB_HOST = os.getenv('MYSQL_HOST', 'localhost')
DB_NAME = os.getenv('MYSQL_DB', 'random_data')
DB_USER = os.getenv('MYSQL_USER', 'user')
DB_PASS = os.getenv('MYSQL_PASSWORD', 'password')

# Initialize the database
def init_db():
    conn = mysql.connector.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            userid VARCHAR(255),
            timestamp VARCHAR(255),
            value FLOAT
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Insert random data into MySQL
def insert_row(userid, timestamp, value):
    conn = mysql.connector.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO data (userid, timestamp, value) VALUES (%s, %s, %s)
    ''', (userid, timestamp, value))
    conn.commit()
    cursor.close()
    conn.close()

# Function to generate random data
def generate_random_data():
    while True:
        userid = f"user_{random.randint(1, 100)}"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        value = round(random.uniform(10.0, 100.0), 2)
        insert_row(userid, timestamp, value)
        time.sleep(1)

# Start data generation in a separate thread
def start_data_generation():
    thread = threading.Thread(target=generate_random_data)
    thread.daemon = True
    thread.start()

@app.route('/')
def home():
    return "Data is being generated every second and saved to the MySQL database."

if __name__ == '__main__':
    init_db()  # Initialize the database
    start_data_generation()  # Start generating data
    app.run(host='0.0.0.0', port=5000)
