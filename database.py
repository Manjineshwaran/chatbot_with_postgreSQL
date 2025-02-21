import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

def create_tables():

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_goals (
                id SERIAL PRIMARY KEY,
                username TEXT,
                goal TEXT,
                weightage INTEGER
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_info (
                id SERIAL PRIMARY KEY,
                username TEXT,
                name TEXT,
                email TEXT,
                phone TEXT,
                country TEXT
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error creating tables:", e)

def save_data(table_name, data):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        columns = ', '.join(data.keys())
        values = tuple(data.values())
        placeholders = ', '.join(['%s'] * len(values))

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, values)

        conn.commit()
        cursor.close()
        conn.close()
        print(f"Data saved to '{table_name}' successfully!")
    except Exception as e:
        print("Database error:", e)

def fetch_user_data(username):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("SELECT username, goal, weightage FROM user_goals WHERE username = %s", (username,))
        goals = cursor.fetchall()

        cursor.execute("SELECT name, email, phone, country FROM user_info WHERE username = %s", (username,))
        user_info = cursor.fetchone()

        conn.close()

        goals_text = "; ".join([f"{username}{goal} ({weightage}%)" for username, goal, weightage in goals]) if goals else "No goals found."
        user_info_text = f"Name: {user_info[0]}, Email: {user_info[1]}, Phone: {user_info[2]},country:{user_info[3]}" if user_info else "No user info found."
        #print("goals_text",goals_text)
        #print("user_info_text",user_info_text)
        return goals_text, user_info_text

    except Exception as e:
        return f"Error retrieving data: {e}", None
