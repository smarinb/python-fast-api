# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=14094

### Users API con autorización OAuth2 básica ###

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login") #Lo que vamos a poner en la ruta(path) para el metodo que haga el login


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
        "password": "123456"
    },
    "creyes": {
        "username": "creyes",
        "full_name": "Cristina Reyes",
        "email": "creyesg86@gmail.com",
        "disabled": True,
        "password": "654321"
    }
}


def search_user_db(username: str): #Devuelvo un objeto UserDB que tenga el username que le paso
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str): #Igual pero devuelvo un objeto de clase User
    if username in users_db:
        return User(**users_db[username]) #Le pueden llegar varios parametros


async def current_user(token: str = Depends(oauth2)): #En este ejemplo el token es el username, cuando el usuario esté
    ##autorizado el token será el username por eso usamos el metodo search_user
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )

    return user


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username) #simulamos la bbdd con una lista de usuarios, y preguntamos si en la
    #lista está el usuario capaturado del formulario 
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username) 
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user