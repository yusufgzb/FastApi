import sys
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
        

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user":"Not Auth"}}
)

def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password,hash_password):
    return bcrypt_context.verify(plain_password,hash_password)

def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.username == username).first()

    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id:int, expires_delta:Optional[timedelta]=None):
    encode = {"sub":username,"id":user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp":expire})
    return jwt.encode(encode, SCRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str =Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token,SCRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            raise get_current_user()
        return {"username": username, "id":user_id}
    except JWTError:
        raise HTTPException(status_code=404, detail="User not Found")


@router.post("/create/user")
async def create_new_user(create_user:CreateUser, db: Session = Depends(get_db)):
    existing_user_by_username = db.query(models.Users).filter_by(username=create_user.username).first()
    existing_user_by_email = db.query(models.Users).filter_by(email=create_user.email).first()

    if existing_user_by_username and existing_user_by_email:
        return {"message": "Bu kullanıcı adı ve mail daha önce alınmış"}
    elif existing_user_by_username:
        return {"message": "Bu kullanıcı adı  daha önce alınmış"}
    elif existing_user_by_email:
        return {"message": "Bu email adresi daha önce kayıt edilmiş"}
   
    create_user_model = models.Users()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.first_name = create_user.firs_name
    hash_password = get_password_hash(create_user.password)
    create_user_model.hashed_password = hash_password
    create_user_model.is_activate = True

    db.add(create_user_model) 
    db.commit()
    return {"Başarılı":"Kayıt olundu"}

@router.post("/token")
async def login_for_access_token(from_data:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(from_data.username,from_data.password,db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username,
                                user.id,
                                expires_delta=token_expires)
    return {"token":token}


def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Cloud not validate credentials",
        headers={"www-Authenticate":"Bearer"}
    )
    return credentials_exception

def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"www-Authenticate":"Bearer"}
    )
    return token_exception_response


# uvicorn auth:app --reload
