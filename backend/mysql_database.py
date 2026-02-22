import psycopg2
import psycopg2.extras
import os

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "postgres"),
        port=os.getenv("DB_PORT", "5432")
    )