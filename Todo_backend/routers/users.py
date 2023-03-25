import sys

from routers.auth import get_current_user, get_password_hash, get_user_exception, verify_password
sys.path.append("..")
from fastapi import  Depends,HTTPException,status,APIRouter
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext



from sqlalchemy.orm import Session
from db import SessionLocal,engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError

SCRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM  = "HS256"
class CreateUser(BaseModel):
    username: str  
    email: Optional[str]  
    firs_name: str  
    last_name: str  
    password: str  

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str
     
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={401: {"user":"Not fount"}}
)

@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

@router.get("/user/{user_id}")
def get_by_path(user_id:int,db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()

    if user_id is not None:
        return user
    raise HTTPException(status_code=404, details="user not found") 

@router.get("/user/")
def get_by_query(user_id:int,db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()

    if user_id is not None:
        return user
    raise HTTPException(status_code=404, details="user not found") 
    
@router.put("/user/password")
async def user_password_change(user_verification: UserVerification,db: Session = Depends(get_db), user:dict = Depends(get_current_user)):
    if user is None:
        raise get_user_exception()
    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()
    if user_model is not None:
        if user_verification.username == user_model.username and verify_password(
            user_verification.password,user_model.hashed_password):
            user_model.hashed_password = get_password_hash(user_verification.new_password)
            db.add(user_model)
            db.commit()
            return "successful"
    return "Invalid user or request"

@router.delete("/{todo_id}")
async def user_password_change(db: Session = Depends(get_db), user:dict = Depends(get_current_user)):
    if user is None:
        raise get_user_exception()
    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException()
    
    # veritabanından sorguladığımız görevi siliniyoruz
    db.query(models.Users).filter(models.Users.id== user.get("id")).delete()
    # veritabanındaki değişikliği kaydediyoruz
    db.commit()

    # Kullanıcıya başarılı bir işlem olduğunu bildiriyoruz
    return {
        "status":200,
        "transaction": "Başarılı"
    }
