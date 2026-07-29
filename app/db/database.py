from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.orm import Session

from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite:///database.db"

engine = create_engine(DATABASE_URL)
                            # engine ile db bağlantısı  oluşturulur
SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)   # şu 2si transactionda sıkıntı çıkmasın diye var
                                            # session db üzerine işlem demek her endpointe requesste işlem yapılabilir 
                                            # o yüzden merkezleştiriyoruz



class Base(DeclarativeBase):
    pass                        # base de burada çünkü butun tablolar-modeller bunu inherit edecek merkezi olması ideal



"""temeldeki model tableları kurduktan sonra eğer bunları geliştirmek istersek önce python kodu olarka
sonra da sqlalchemy ile database işlemeliyiz bu database i genişletmeye ekstra alanlar tablolar eklemeye  migration
denir git gibi düşün atılan her commit gibi 
alembic ise ptyhon kodu ile databesi karsşılaştırıyo bunlar birbirine uyuyo mu pythonda yazan db de var mı bakıyo
pythonda bio var userda db de yok o zaman migration oluşturuyo yani  dbyi güncelliyo 
crud işlemleri migrationdan sonra gelir çünkü önce uygun db lazım tablo falan

sıralama şu önce model oluştur sonra migration oluştur sonra db oluştur  sonra crud işlemleri yaz

bundan sonra artık Base.metadata.create_all(engine) kullanmayacağız.
 Gerçek projelerde tablo oluşturmayı Alembic yönetir"""

# alembic.ini url düzeltildi
#burdaki  alembic env düzeltildi ve  alembic revision --autogenerate -m "create users and posts" yapıldı 
"""migration dosyasyı oluşturuldu 


alembic upgrade head ile database tablo flan tamamen oluşacak sonmra da 

SessionLocal, get_db() dependency ve ilk CRUD endpoint'leri. Bunlar artık API'nin veritabanıyla konuşmasını sağlayacak. """

#request gelince yeni session oluşturuyo 

def get_db():
    db = SessionLocal()     #endpoint bunu kullanıyo

    try:
        yield db
    finally:
        db.close()



naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

Base = declarative_base(metadata=MetaData(naming_convention=naming_convention))