#FastAPI kütüphanesinden FastAPI ve Dependency modüllerini içe aktarıyoruz
from fastapi import FastAPI, Depends, HTTPException
# veritabanı işlemleri için gerekli olan SessionLocal sınıfını içe aktarıyoruz
from db import SessionLocal
# ORM için gerekli olan modelleri içe aktarıyoruz
import models
# veritabanı motorunu içe aktarıyoruz
from db import engine
# SQLAlchemy ORM kütüphanesinden session sınıfını içe aktarıyoruz
from sqlalchemy.orm import Session

from pydantic import BaseModel, Field
from typing import Optional
#FastAPI uygulamasını oluşturuyoruz
app = FastAPI()

# ORM ile oluşturulan modellerin tablo oluşumunu gerçekleştiriyoruz
models.Base.metadata.create_all(bind=engine)

# veritabanı bağlantısını açıp kapatmak için fonksiyon oluşturuyoruz
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




# ana sayfada tüm verileri döndüren route
@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    # veritabanındaki tüm todos bilgilerini döndürüyoruz
    return db.query(models.Todos).all()

# db:Session=Depends(get_db) bu kod parçacığı, 
# FastAPI tarafından sağlanan "dependency injection" 
# (bağımlılık enjeksiyonu) özelliğini kullanıyor. 
# Bu, fonksiyonun bağımlı olduğu bir "Session" nesnesini 
# sağlamak için kullanılır. Bu nesne veritabanı işlemleri 
# için kullanılabilir. get_db fonksiyonu ise bu "Session" 
# nesnesinin nasıl oluşturulduğunu tanımlıyor.
@app.get("/todo/{todo_id}")
async def read_all(todo_id:int ,db: Session = Depends(get_db)):
    # veritabanındaki belirli bir todo bilgisini döndürüyoruz
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is not None:
        # eğer belirli bir todo bulunmuşsa bu todo bilgisini döndürüyoruz
        return todo_model
    # eğer todo bulunmamışsa hata döndürüyoruz
    raise HTTPException(status_code=404, details="Todo not found") 

@app.post("/")
async def create_todo(todo: Todos,db:Session=Depends(get_db)):
    # Todo modelini oluşturalım
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complate = todo.complate
    
    # Oluşan todo modelini veritabanına ekleyelim
    db.add(todo_model)
    
    # Veritabanında yapılan değişikliği commit edelim
    db.commit()

    return {
        "status":200,
        "transaction": "Başarılı"
    }
@app.post("/{todo_id}")
async def update_todo(todo_id:int,todo: Todos,db:Session=Depends(get_db)):
    # Bu fonksiyon içerisinde, veritabanından todo_id ile eşleşen ilk kaydı alıyoruz.
    todo_model = db.query(models.Todos).filter(models.Todos.id== todo_id).first()
    # Eğer kayıt bulunamazsa, bir hata fırlatıyoruz.
    if todo_model is None:
        raise HTTPException()
    
    # Veri modeline gönderilen yeni verileri atıyoruz.
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complate = todo.complate
    # Değişiklikleri veritabanına ekliyoruz.
    db.add(todo_model)
    db.commit()

    # İşlem başarılı ise kullanıcıya 200 status kodu ve "Başarılı" mesajı döndürüyoruz.
    return {
        "status":200,
        "transaction": "Başarılı"
    }


@app.delete("/{todo_id}")
async def delete_todo(todo_id:int,todo: Todos,db:Session=Depends(get_db)):
    # todo_id ile belirtilen görevi veritabanından sorguluyoruz
    todo_model = db.query(models.Todos).filter(models.Todos.id== todo_id).first()
    
    # eğer sorgulama sonucunda hiçbir sonuç dönmüyorsa hata fırlatıyoruz
    if todo_model is None:
        raise HTTPException()
    
    # veritabanından sorguladığımız görevi siliniyoruz
    db.query(models.Todos).filter(models.Todos.id== todo_id).delete()
    # veritabanındaki değişikliği kaydediyoruz
    db.commit()

    # Kullanıcıya başarılı bir işlem olduğunu bildiriyoruz
    return {
        "status":200,
        "transaction": "Başarılı"
    }


# uvicorn main:app --reload
