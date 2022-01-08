from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:12345678@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi',user='postgres', password='12345678',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Connected to database")
#         break
#     except Exception as e:
#         print(e)
#         time.sleep(2)