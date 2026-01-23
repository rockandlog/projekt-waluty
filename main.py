from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import date as date_type
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base, CurrencyRate
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FetchRequest(BaseModel):
    currency: str
    start_date: str
    end_date: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "System walutowy dziala"}

@app.post("/currencies/fetch")
def fetch_currency(request: FetchRequest, db: Session = Depends(get_db)):
    url = f"http://api.nbp.pl/api/exchangerates/rates/A/{request.currency}/{request.start_date}/{request.end_date}/?format=json"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Blad polaczenia z NBP lub zly zakres dat")
    
    data = response.json()
    rates = data['rates']
    
    licznik = 0
    for rate in rates:
        kurs = rate['mid']
        data_kursu = date_type.fromisoformat(rate['effectiveDate'])
        
        istnieje = db.query(CurrencyRate).filter(
            CurrencyRate.currency_code == data['code'],
            CurrencyRate.date == data_kursu
        ).first()
        
        if not istnieje:
            nowy_wpis = CurrencyRate(
                currency_code=data['code'],
                rate=kurs,
                date=data_kursu
            )
            db.add(nowy_wpis)
            licznik += 1
    
    db.commit()
    return {"message": f"Pobrano {licznik} nowych kursow"}

@app.get("/currencies")
def get_currencies(db: Session = Depends(get_db)):
    kursy = db.query(CurrencyRate).all()
    return kursy