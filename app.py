from flask import Flask, render_template,request,jsonify,session
from funciones import creaToken,creaRefreshToken
from os.path import join, dirname
from dotenv import load_dotenv
from flask_socketio import SocketIO
import os
import time
from asgiref.sync import sync_to_async
import asyncio
from funciones import get_me,get_last_token,get_info_users,get_orders_users,update_orders_users
import nest_asyncio
import json
import ast
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


import uvicorn

nest_asyncio.apply()


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

APP_ID=os.environ.get("APP_ID")
re_url=os.environ.get("redirect")
CLIENT_SECRET=os.environ.get("CLIENT_SECRET")


from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
socketio = SocketIO(app)
scheduler = BackgroundScheduler()

CORS(app, support_credentials=True)


def orders_updateJOB(user_id):
    print("ACTUALIZANDO")
    token=get_last_token(user_id)
    #creaRefreshToken(token)
    #exit()
    
    
    reaultado=update_orders_users(token)
    
 
 
    
scheduler.add_job(
   orders_updateJOB, 'interval',args=['1118811075'], minutes=30
)
scheduler.add_job(
   creaRefreshToken, 'interval',args=['1118811075'], minutes=1
)


# Start the scheduler
scheduler.start()


    
@app.route('/')
def sessions():
    return {"app":"run"}

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
        print(token)
        session['user_id']=session['token']["access_token"].split('-')[-1]
        
    return render_template('callback.html')



@app.route('/me', methods=['GET'])
#@cross_origin(supports_credentials=True)
async def me():
    
    token=get_last_token(session['user_id'])
    reaultado=get_me(token)
    #if 'user_id' not in session.keys():
        
    return jsonify(reaultado)



@app.route('/info_user', methods=['GET'])
#@cross_origin(supports_credentials=True)
async def info_user():
    token=get_last_token('1118811075')
    reaultado=get_info_users(token)
    
    return jsonify(reaultado)

@app.route('/orders_user', methods=['GET'])
#@cross_origin(supports_credentials=True)
async def orders_user():
    token=get_last_token('1118811075')
    #creaRefreshToken('1118811075')
    #exit()
    
    
    reaultado=get_orders_users(token)
    
    
            
    return reaultado

 

@app.route('/update_orders', methods=['GET'])
#@cross_origin(supports_credentials=True)
async def orders_update():
    token=get_last_token('1118811075')
    print(token)
    #creaRefreshToken(token)
    #exit()
    
    
    reaultado=update_orders_users(token)

            
    return reaultado


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=8000)