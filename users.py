from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel): #Nos da la capacidad de crear una entidad 
    id: int
    name: str 
    surname: str 
    url: str | None = None
    age: int
    


users_list = [
    User(id=0, name="Sergio", surname="Marín", age=36),
    User(id=1, name="Victor", surname="Pariente", url="https://edreams.com", age=34),
    User(id=2, name="Cristina", surname="Reyes", url="https://sordotravel.com", age=37)
    ]






@app.get("/users_json")
async def users_json():
    return [{
        "name": "Sergio",
        "surname": "Marín",
        "url": "https://marca.com"
        },
        {
        "name": "Cristina",
        "surname": "Reyes",
        "url": "https://sordotravel.com" 
        },
        {
        "name": "Victor",
        "surname": "Pariente",
        "url": "https://edreams.com" 
        }
        
        
        ]

print(users_list)

@app.get("/users")
async def users():
    return users_list



#Path Parameters
@app.get("/users/{id}")
async def user(id: int):
    return search_user(id)



#Query Parameters
@app.get("/user/")
async def read_item(id: int = 0):
    return search_user(id)


@app.post("/user/")
async def user(user: User):
    if type(search_user(user.id)) == User:
            return {"Error" : "El usuario ya existe"}     
    else:
        users_list.append(user)
        return user

@app.put("/user/")
async def user(user: User): #Se le pasa un usuario complero a actualizar
    found: bool = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id: #El id tiene que existir (no es un nuevo usuario con nuevo id, seria un post si no)
            users_list[index] = user
            found = True
            return user
    if not found:
        return {"Error" : "Usuario no encontrado"}

@app.delete("/user/{id}")
async def user(id: int):
    if type(search_user(id)) == User:
        user : User = search_user(id)
        users_list.remove(user)
    else:
        return {"Error": "El usuario no existe"}

    



def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list) #funcion lambda si el user que le pasamos su id coincide , con el filter de toda la lista saca la que se cumpla
    try:
        return list(users)[0] #Lo devuelve como una lista y a mi me interesa el elemento (objeto), como en mi lista no sé vana  repetir los indices se que solo es un elemento
    except:
        return {"error": "No se ha encontrado el usuario"}
