from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):

    email: str | None = None

class Usuario_registrado(BaseModel):
    user_id_ml: str

    email: str


class UserInDB(User):
    hashed_password: str
    
    