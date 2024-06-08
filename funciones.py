 
import os
import requests
from selenium import webdriver
import time
 
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
from urllib.parse import parse_qs
import subprocess
import asyncio
from os.path import join, dirname
from dotenv import load_dotenv
from mercadolibre.client import Client
import ast
from run_ml import runner as runml
import json
from init_db import get_db_connection
    
    
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

APP_ID=os.environ.get("APP_ID")
re_url=os.environ.get("redirect")
CLIENT_SECRET=os.environ.get("CLIENT_SECRET")
#https://github.com/GearPlug/mercadolibre-python/tree/master
client = Client(APP_ID, CLIENT_SECRET, site='MLM')
user_id=""
url = 'https://auth.mercadolibre.com.mx/authorization?response_type=code&client_id={}&redirect_uri={}'.format(APP_ID,re_url)
 

def get_code():
    print("va por codigo")
    debugger_address = 'localhost:8989'

    c_options = Options()
    c_options.add_experimental_option("debuggerAddress", debugger_address)

    driver = webdriver.Chrome(options=c_options)

    driver.get(url)

    get_url = driver.current_url
    print("The current url is:"+str(get_url))
    time.sleep(5)
    parsed_url = urlparse(get_url)
    code = parse_qs(parsed_url.query)['code'][0]
    driver.quit() 
    return code

 

def get_me(token):
    
    print(token)
    client.set_token(token)
    
    usuario=client.me()
 
    try:
        if usuario["status"]==401:
            print("entra REFRESH")
            client.refresh_token(token)
            usuario=client.me()
        
    except:
        pass 
    return usuario

def get_info_users(token):
    
    print(token)
    client.set_token(token)
    usua=get_me(token)
    usuario=client.get_info_users('MLM',usua["nickname"])
    
    try:
        if usuario["status"]==401:
            print("entra REFRESH")
            client.refresh_token(token)
            usuario=client.get_info_users('MLM',usua["nickname"])
    except:
        pass     
    return usuario

def get_orders_users(token):
    
    print(token)
    client.set_token(token)
    usua=get_me(token)
     

    usuario=client.get_orders(usua["id"])
    try:
        if usuario["status"]==401:
            print("entra REFRESH")
            client.refresh_token(token)
            usuario=client.get_orders(usua["id"])
    except:
        pass    
    return usuario

def get_last_token(userid):
    
    conn=get_db_connection()
    cur = conn.cursor()
    print("select json_data  from tokens t where user_id ='{}' ORDER BY created  DESC LIMIT 1 ".format(userid))
    cur.execute("select json_data  from tokens t where user_id ='{}' ORDER BY created  DESC LIMIT 1 ".format(userid))
     
    usuario=cur.fetchone()
    cur.close()
    conn.close()
    resultado=[]
    for i in usuario:
        #print(i)
        resultado.append(i)
    
    json_data = ast.literal_eval(resultado[0])
     
    return json_data
    
    
    return resultado
    
def refreshToken():
    
    token = client.refresh_token()
    print("token:",token)
    crea_json('token.json',token)
    client.set_token(token)

def crea_json(filename,data):
    
    with open(filename, 'w') as f:
        json.dump(data, f)
#runml()
 
def lee_json(filename,campo=None):
    f = open(filename)
 
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    
    # Iterating through the json
    # list
    if campo != None:
        for i in data[campo]:
            print(i)
            f.close()
            return i
    else: 
        print("lee JSON")
        return data
    # Closing file
    return False

def creaToken(codigo):
    #codigo=get_code()
 
    token = client.exchange_code(re_url, codigo)
 
    #crea_json('token_{}.json'.format(token["user_id"]),token)
    conn=get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO tokens (user_id, json_data)'
            'VALUES (%s, %s)',
            (token["user_id"],
                '{}'.format(token))
            )

    conn.commit()

    cur.close()
    conn.close()

    return True
if __name__ == "__main__":
    #user_id=creaToken()

    user_id="40137874"
    token=lee_json('token_{}.json'.format(user_id))
    print("token:",token)
    #crea_json('token.json',token)
    client.set_token(token)
     
    
    usuario=client.get_info_users('MLM','krenfermo')
    
    #crea_json('info_user.json',usuario)
    
    print(client.get_orders(usuario["seller"]["id"]))
    
    exit()
    url = 'https://api.mercadolibre.com/oauth/token'
    payload = {'grant_type': 'authorization_code',
            'client_id': APP_ID,
            'client_secret': CLIENT_SECRET,
            'code': 'TG-666267a63d29bb0001cef362-40137874',
            'redirect_uri': redirect}
    headers = {'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, headers=headers, data=payload)
    print(response)