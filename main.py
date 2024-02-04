from fastapi import FastAPI
from routers import products,users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/url")
async def url():
    return {"url": "https://sordotravel.com"}

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}



#Correr el servidor --> uvicorn "name_file":app --reload
#Doc Swagger --> http://127.0.0.1:8000/docs
#Doc Redoc --> http://127.0.0.1:8000/redoc