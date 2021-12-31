from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

con_url = 'postgresql://postgres:password@localhost:5432/meal_builder'
engine = create_engine(con_url)
Session = sessionmaker(bind=engine)


Base = declarative_base()
