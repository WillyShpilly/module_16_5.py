from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/', tags=["Пользователи🧑‍🧑‍🧒‍🧒"], summary="Список всех пользователей")
def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/users/{user_id}')
def get_user(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'user': users[user_id-1]})


@app.delete('/user/{user_id}')
def delete_user(user_id: int):
    try:
        user = users.pop(user_id - 1)
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.post('/user/{username}/{age}')
def post_user(user: User, username: str, age: int):
    user.id = 1 if not users else users[-1].id + 1
    user.username = username
    user.age = age
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
def update_user(user_id: int, username: str, age: int):
    try:
        edit_user = users[user_id - 1]
        edit_user.username = username
        edit_user.age = age
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')



if __name__ == "__main__":
    uvicorn.run("urban:app", reload=True)

