import os
import psycopg2
from dotenv import load_dotenv
import logging
from fastapi import HTTPException
from psycopg2 import IntegrityError

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
Will need to make sure we have a db set up with the following:

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE inventory (
    user_id INTEGER REFERENCES users(id),
    item TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    expiration_date DATE NOT NULL,
    PRIMARY KEY (user_id, item)
);

'''

def get_db_connection():
    """
    Establish a connection to the PostgreSQL database.
    Returns a connection object.
    """
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        logger.info("Database connection established successfully.")
        return connection
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

def get_db():
    """
    Dependency that provides a database connection for each request.
    Closes the connection after the request is complete.
    """
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()
        logger.info("Database connection closed.")

