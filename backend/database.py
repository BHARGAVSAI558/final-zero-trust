import psycopg2
import psycopg2.extras
import os

def get_db():
    return psycopg2.connect(
        os.getenv("DATABASE_URL", "postgresql://zero_user:password@localhost/zero")
    )
