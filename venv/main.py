from http.client import HTTPException
from urllib import response
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine
from fastapi.templating import Jinja2Templates
from models import crud, user, feed
from config import db
from routers import auth as auth_router
from sqlalchemy.orm import Session

templates = Jinja2Templates(directory="templates")
user.Base.metadata.create_all(bind=db.engine)

app = FastAPI()
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/")
def read_root():
    return{"message": "Hello, world!" }



@app.get('/index/', response_class=HTMLResponse)
def index(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("index.html", context)

@app.get('/login/', response_class=HTMLResponse)
def index(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("login.html", context)

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )


