#from openai import OpenAI

from os.path import join, dirname
from dotenv import load_dotenv
import os
 

from langchain.llms import OpenAI
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain



dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

OPENIA_KEY = os.environ.get("OPENIA_KEY")
print(OPENIA_KEY)
DB_HOSTNAME = os.environ.get("DB_HOSTNAME")
DB_NAME = os.environ.get("DB_NAME")
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT = os.environ.get("DB_PORT")

 

db = SQLDatabase.from_uri("postgresql+psycopg2://{}:{}@{}:{}/{}".format(DB_USERNAME,DB_PASSWORD,DB_HOSTNAME,DB_PORT,DB_NAME),
)

 
# setup llm
llm = OpenAI(temperature=0, openai_api_key=OPENIA_KEY)

# Create db chain
 


QUERY2 = """
Given an input question, first create a syntactically correct postgresql query to run, then look at the results of the query and return the answer.
Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

{question}
"""
 

QUERY = """
Data una pregunta del usuario:
1. crea una consulta de postgres
2. revisa los resultados
3. devuelve el dato
4. si tienes que hacer alguna aclaración o devolver cualquier texto que sea siempre en español
#{question}
"""
# Setup the database chain
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)


#question = QUERY.format(question="cual es el articulo mas vendido de la tabla orders_items?")
question = QUERY.format(question="cuales son los productos top 10 mas vendidos de la tabla orders_datos del userid=1118811075?")
print(db_chain.run(question))
