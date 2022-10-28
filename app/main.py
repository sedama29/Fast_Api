from typing import Optional
from xml.dom import xmlbuilder
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import sqlite3
import time
app = FastAPI()

class Details(BaseModel):
    name: str
    email: str
    phoneNumber: str

def get_one(id:int): 
    cursor.execute("""select * from details""")
    detail = cursor.fetchall() 
    print(detail)    
    for i in detail:
        x = i[0]
        if x == id:
            index1= x
            return index1

while True:
    try:
        conn = sqlite3.connect('db\detail.db', check_same_thread=False)
        cursor =conn.cursor()
        print('Database connection was succesful!')
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)

            
@app.get("/")
def read_root():
    return {"message": "root"}

@app.get("/data1")
def get_posts():
    cursor.execute("""select * from details""")
    detail = cursor.fetchall()
    print(len(detail))
    print(detail)
    return{"data":detail}

@app.get("/data1/{id}")
def get_posts():
    index = get_one(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post with id: {index} does not exist')
    cursor.execute("""select * from details where id = ?""",(index,))
    data3 = cursor.fetchone()
    return{"data":data3}


@app.post("/data1", status_code=status.HTTP_201_CREATED)
def create_posts(detail: Details):
    cursor.execute("""INSERT INTO details(name, email, phoneNumber) VALUES(?,?,?)""",(detail.name, detail.email, detail.phoneNumber))
    conn.commit()
    return{"data was added succesfully"}

@app.put("/data1/{id}")
def update_posts(id : int, detail2: Details):
    print(detail2)
    print(id)
    index = get_one(id)
    print(type(index))
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post with id: {id} does not exist')
    cursor.execute("""update details set name = ? where id = ?""",(detail2.name, index,))
    conn.commit()
    cursor.execute("""select * from details where id = ?""", (index,))
    data = cursor.fetchone()
    return {'sucessfully updated':data}

@app.delete('/data1/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id : int):
    index = get_one(id)
    print(type(index))
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post with id: {id} does not exist')
    cursor.execute("""delete from details where id = ?;""",(index,))
    conn.commit()
    return {'details with id were deleted'}
