 
import os
import psycopg2
from dotenv import load_dotenv
from os.path import join, dirname


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def get_db_connection():
    conn = psycopg2.connect(host=os.environ['DB_HOSTNAME'],
                            database=os.environ['DB_NAME'],
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'],
                            port=os.environ['DB_PORT'])
    return conn


 

