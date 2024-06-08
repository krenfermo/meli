from flask import Flask, render_template,request,jsonify
from funciones import creaToken
from os.path import join, dirname
from dotenv import load_dotenv
from flask_socketio import SocketIO
import os
import time
from asgiref.sync import sync_to_async
import asyncio
from funciones import get_me,get_last_token,get_info_users,get_orders_users
import nest_asyncio
import json
import ast



nest_asyncio.apply()


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

APP_ID=os.environ.get("APP_ID")
re_url=os.environ.get("redirect")
CLIENT_SECRET=os.environ.get("CLIENT_SECRET")


from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)


CORS(app, support_credentials=True)


@app.route('/')
def sessions():
    return render_template('session.html')

@app.route('/autoriza')
def index():
    print(APP_ID,re_url)
    return render_template('index.html',appID=APP_ID,redirect=re_url)

 
@app.route('/callback', methods=['GET'])
#@cross_origin(supports_credentials=True)
async def respond():
    code = request.args.get("code")
   
    token=creaToken(code)
 
    
    if token:
        print("token CREADO")
    
    return render_template('callback.html')



@app.route('/me', methods=['GET'])
#@cross_origin(supports_credentials=True)
async def me():
    token=get_last_token('40137874')
    reaultado=get_me(token)
    
    return reaultado


@app.route('/info_user', methods=['GET'])
#@cross_origin(supports_credentials=True)
async def info_user():
    token=get_last_token('40137874')
    reaultado=get_info_users(token)
    
    return reaultado

@app.route('/orders_user', methods=['GET'])
#@cross_origin(supports_credentials=True)
async def orders_user():
    token=get_last_token('40137874')
    reaultado=get_orders_users(token)
    
    return reaultado

 

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8000,ssl_context='adhoc')