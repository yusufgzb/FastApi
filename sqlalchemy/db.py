from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Veritabanı bağlantı dizesi.
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db" # kullanarak SQLite ile çalışabilirsiniz.
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# user ve password kısımlarını kendi kullanıcı adınız ve şifreniz ile değiştirin.
# postgresserver kısmını ise kendi postgres sunucunuzun adresi ile değiştirin.
# db kısmı ise kullanacağınız veritabanının adıdır.

# Veritabanı motorunu oluştur
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Oturum yönetimini yapmak için sessionmaker nesnesini oluştur
# autocommit=False ve autoflush=False yaparak otomatik kaydetme ve flush ayarlarını kapatıyoruz.
# bind=engine parametresi ile oluşturduğumuz motoru oturum yönetimine bağlıyoruz
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tablo temellerini tanımlayan Base nesnesini oluşturuyoruz
Base = declarative_base()