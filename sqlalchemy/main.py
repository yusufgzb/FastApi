from fastapi import FastAPI, Depends, HTTPException
from db import SessionLocal
import models
from db import engine
from sqlalchemy.orm import Session

from pydantic import BaseModel, Field
from typing import Optional
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Todos(BaseModel):
    title: str
    description: Optional[str]
    priority: int= Field(gt=0, lt=6, description="1 le 5 arası veri")
    complate: bool




@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@app.get("/todo/{todo_id}")
async def read_all(todo_id:int ,db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, details="Todo not found") 

@app.post("/")
async def create_todo(todo: Todos,db:Session=Depends(get_db)):
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complate = todo.complate
    
    db.add(todo_model)
    
    db.commit()

    return {
        "status":200,
        "transaction": "Başarılı"
    }
@app.post("/{todo_id}")
async def update_todo(todo_id:int,todo: Todos,db:Session=Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id== todo_id).first()
    if todo_model is None:
        raise HTTPException()
    
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complate = todo.complate
    db.add(todo_model)
    db.commit()

    return {
        "status":200,
        "transaction": "Başarılı"
    }


@app.delete("/{todo_id}")
async def delete_todo(todo_id:int,todo: Todos,db:Session=Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id== todo_id).first()
    
    if todo_model is None:
        raise HTTPException()
    
    db.query(models.Todos).filter(models.Todos.id== todo_id).delete()
    db.commit()

    return {
        "status":200,
        "transaction": "Başarılı"
    }


# uvicorn main:app --reload
