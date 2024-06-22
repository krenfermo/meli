import datetime  # to calculate expiration of the JWT
from fastapi import FastAPI, Depends, HTTPException, Security, Request,status
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyCookie  # this is the part that puts the lock icon to the docs
from fastapi_sso.sso.google import GoogleSSO  # pip install fastapi-sso
from fastapi_sso.sso.base import OpenID
from jose import jwt  # pip install python-jose[cryptography]
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from os.path import join, dirname
from dotenv import load_dotenv
import os
import ssl
from funciones_api import creaUser,get_orders,getUser,post_user, post_login,pass_md5

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
 
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Annotated
from api_models import *
from fastapi.responses import JSONResponse


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI(
    title="API MELI",
    # if not custom domain
    openapi_prefix="/api"
)

security = HTTPBasic()


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('./certMELI.pem', keyfile='./keyMELI.pem')
SECRET_KEY="t103855291032928390605"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080
ALGORITHM = "HS256"


#openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
#uvicorn main:app --ssl-keyfile keyMELI.pem --ssl-certfile certMELI.pem
#{"id":"103855291032928390605","email":"morakurt@gmail.com","first_name":"joaquin","last_name":"mora","display_name":"joaquin mora",
# "picture":"https://lh3.googleusercontent.com/a/ACg8ocKp5Sofix9_6dFPz5u2uGh734gEk90V203IsO8PjTpohi8z86w=s96-c","provider":"google"}

CLIENT_ID = os.environ.get("google_CLIENTEID") # <-- paste your client id here
CLIENT_SECRET = os.environ.get("google_CLIENT_SECRET") # <-- paste your client secret here



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)




def get_google_sso() -> GoogleSSO:
    return GoogleSSO(CLIENT_ID, CLIENT_SECRET, redirect_uri="https://meli.mi-mercado.xyz/api/google/callback")



     
    

def get_user(username: str):
    datos_form={}
    datos_form['username']=username.rstrip().lstrip()
    #datos_form['password']=pass_md5(password.rstrip().lstrip()) 
    print("va check")
    oUser = post_user(datos_form)
    print(oUser)
    return oUser


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    datos_form={}
    datos_form['username']=username.rstrip().lstrip()
    datos_form['password']=pass_md5(password.rstrip().lstrip()) 

    login=post_login(datos_form)
    print("login",login)
    if not login:
        return False
    
    return login


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    print(current_user)
    if current_user==None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    datos_form={}
    datos_form['username']=credentials.username.rstrip().lstrip()
    datos_form['password']=pass_md5(credentials.password.rstrip().lstrip()) 

    login=post_login(datos_form)
    


    print(login)
    return login




@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    print(user)
    print(user[4])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user[4]}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



@app.get("/users/me/", response_model=Usuario_registrado)
async def read_users_me(username: Annotated[str, Depends(get_current_username)]):
    print("MEEE",username)
    try:
        #current_user=json.loads(json.dumps(dict(current_user), default=str))
        print("/me/",type(username))
        return JSONResponse(status_code=status.HTTP_200_OK, content={"user":username[4],"display_name":username[5]} )
    except:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"error":"error"})


@app.get('/api')
def sessions():
    return {"API    ":"run"}


@app.get("/google/login")
async def google_login(google_sso: GoogleSSO = Depends(get_google_sso)):
    return await google_sso.get_login_redirect()


async def get_logged_user(cookie: str = Security(APIKeyCookie(name="token"))) -> OpenID:
    """Get user's JWT stored in cookie 'token', parse it and return the user's OpenID."""
    try:
        claims = jwt.decode(cookie, key=SECRET_KEY, algorithms=["HS256"])
        return OpenID(**claims["pld"])
    except Exception as error:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials") from error



@app.get("/protected")
async def protected_endpoint(user: OpenID = Depends(get_logged_user)):
    """This endpoint will say hello to the logged user.
    If the user is not logged, it will return a 401 error from `get_logged_user`."""
    return {
        "message": f"{user.email}!",
    }
    
@app.get("/orders/{user_idML}")
async def protected_endpoint(user_idML: str,user: OpenID = Depends(get_logged_user)):
    """This endpoint will say hello to the logged user.
    If the user is not logged, it will return a 401 error from `get_logged_user`."""
     
 
    return get_orders(user_idML)
    
         
@app.get("/google/callback")
async def google_callback(request: Request, google_sso: GoogleSSO = Depends(get_google_sso)):
    openid = await google_sso.verify_and_process(request)
    if not openid:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    expiration = datetime.now(tz=timezone.utc) + timedelta(days=1)
    token = jwt.encode({"pld": openid.dict(), "exp": expiration, "sub": openid.id}, key=SECRET_KEY, algorithm="HS256")
    response = RedirectResponse(url="/api/protected")
    response.set_cookie(
        key="token", value=token, expires=expiration
    )  # This cookie will make sure /protected knows the user
    
    
    if getUser(openid.email)==None:
       
        if creaUser(openid.dict(),'Google',openid.email,openid.display_name):
            
            return response
        else:
            raise HTTPException(status_code=401, detail="error al crear usuario con Google")
    else:
        return response
    
    #return response


