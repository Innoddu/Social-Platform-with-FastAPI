from http.client import HTTPException
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine
from fastapi.templating import Jinja2Templates
from models.user import Base as UserBase
from models.feed import Base as FeedBase
from models.comment import Base as CommentBase
from routers import auth_router, feed_router, comment_router
import os

templates = Jinja2Templates(directory="templates")
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

UserBase.metadata.create_all(bind=engine)
FeedBase.metadata.create_all(bind=engine)
CommentBase.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
app.include_router(feed_router.router, prefix="/api/feed", tags=["feed"])
app.include_router(comment_router.router, prefix="/api/comment", tags=['comment'])
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


