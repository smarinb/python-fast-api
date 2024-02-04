from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib .context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 #1 minuto
SECRET = "01f97bb95eaa61a442f27a65193377fdd466b47d55f39e516923581361fcacca" #openssl rand -hex 32 (Generarlo)

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "smarin": {
        "username": "smarin",
        "full_name": "Sergio Marín",
        "email": "sergemb87@gmail.com",
        "disabled": False,
        "password": "$2a$12$N64WB5DUCUeEz1BAYKlHt.GbXEOZBEQ1wnqN/7xLMiKi2FLdXZhYm"
    },
    "creyes": {
        "username": "creyes",
        "full_name": "Cristina Reyes",
        "email": "creyesg86@gmail.com",
        "disabled": True,
        "password": "$2a$12$V7NmoCqw0WdAGq7VNQnX8uCAwlrYwg02igEGhV5evipuKAzK7IgNK"
    }
}

def search_user_db(username: str): #Devuelvo un objeto UserDB que tenga el username que le paso
    if username in users_db:
        return UserDB(**users_db[username])

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username) #simulamos la bbdd con una lista de usuarios, y preguntamos si en la
    #lista está el usuario capaturado del formulario 
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username) 

    if not crypt.verify(form.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    


    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION) #Esto sera un minuto más desde la generación del token
    }


    return {"access_token": jwt.encode(access_token, SECRET, algorithm = ALGORITHM), "token_type": "bearer"}