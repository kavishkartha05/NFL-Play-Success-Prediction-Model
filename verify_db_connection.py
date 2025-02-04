import pandas as pd
import psycopg2

# Filling in psql parameters and credentials 
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "newpassword"
DB_NAME = "nfl_data"

# Querying data from PostgreSQL
query = "SELECT * FROM play_by_play LIMIT 5;"

# Connecting to PostgreSQL and fetching data
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    df = pd.read_sql_query(query, conn)
    print(f"Data fetched successfully. Shape: {df.shape}")
    print(df.head()) 
    conn.close()
except Exception as e:
    print(f"An error occurred: {e}")
