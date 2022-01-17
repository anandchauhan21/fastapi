from logging import exception
from operator import index
from sqlite3 import Cursor
from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()

class Post(BaseModel):
    title: str
    content:str
    published:bool = True

while True:
    try:
        conn= psycopg2.connect(host='localhost',database='fastapidb',user='postgres',
        password='anand8791',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('data base conncted...:)')
        break  
    except Exception as error:
        print('conncetion is failed..:(')
        print("Error:",error)
        time.sleep(2)

my_post = [{"title":"new post", "content":"no content yet","id":1},{"title":"fav food", "content":"checcken","id":2}]

def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello fuccerrr"}

@app.get("/post")
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
                    (post.title,post.content,post.published))
    new_post = cursor.fetchall()
    conn.commit()
    return{"data":new_post}
    
'''
@app.get("/post/newadded")
def get_new_post():
    post= my_post[len(my_post) - 1]
    return {"New Added post":post}
'''
@app.get("/post/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * from posts WHERE id = %s""",(str(id)))
    post =  cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail= f"post with id: {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"massege":f"post with {id} not found"}
    return {"post detile":post}

@app.delete("/post/{id}",status_code = status.HTTP_204_NO_CONTENT)
def del_post(id: int):
    cursor.execute("""DELETE from posts WHERE id = %s RETURNING *""",(str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} note avelabel")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update
@app.put("/post/{id}")
def update_post(id:int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                    (post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} note avelabel")

    return {"data":updated_post} 