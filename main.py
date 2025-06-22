from fastapi import FastAPI, APIRouter
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import  declarative_base, sessionmaker

engine = create_engine('sqlite:///mydb.db')
session = sessionmaker(engine)()
class Sellers(declarative_base()):
    __tablename__ = 'Sellers'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)

app = FastAPI()
@app.on_event('startup')
async def startup():
    Sellers.metadata.create_all(engine)

sellers = APIRouter()
@sellers.get('')
def show():
    return session.query(Sellers).all()
@sellers.get('/{sell_id}')
def show(sell_id):
    return session.query(Sellers).get(sell_id)
@sellers.put('/{sell_id}/update')
def update(sell_id, name):
    seller = session.query(Sellers).get(sell_id)
    if seller:
        seller.Name = name
        session.commit()
    return seller

app.include_router(sellers, tags=['Sellers'], prefix='/sellers')
