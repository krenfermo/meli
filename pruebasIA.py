from openai import OpenAI

from os.path import join, dirname
from dotenv import load_dotenv
import os


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

OPENIA_KEY = os.environ.get("OPENIA_KEY")
 

print(OPENIA_KEY)
client = OpenAI(api_key=OPENIA_KEY)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo", 
  messages=[
    {"role": "user", "content": "Can you tell me 5 countries in Latin America?"}
  ],
  max_tokens=30
)

print(completion.choices[0].message.content)

