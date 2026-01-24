from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import date as date_type
from sqlalchemy.orm import Session
from sqlalchemy import distinct
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

# 1. Endpoint zgodny z wymaganiami: GET /currencies
# Zwraca liste dostepnych walut w bazie
@app.get("/currencies")
def get_available_currencies(db: Session = Depends(get_db)):
    # Pobieramy unikalne kody walut z bazy
    waluty = db.query(CurrencyRate.currency_code).distinct().all()
    # Wynik to lista krotek, zamieniamy na prosta liste stringow: ['USD', 'EUR']
    return [w[0] for w in waluty]

# 2. Endpoint zgodny z wymaganiami: GET /currencies/<date>
# Zwraca kursy z konkretnego dnia
@app.get("/currencies/{date_str}")
def get_currency_by_date(date_str: str, db: Session = Depends(get_db)):
    try:
        szukana_data = date_type.fromisoformat(date_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Zly format daty (uzyj YYYY-MM-DD)")

    kursy = db.query(CurrencyRate).filter(CurrencyRate.date == szukana_data).all()
    return kursy

# Endpoint pomocniczy do filtrowania (dla tabeli z zakresem)
# Nie jest wprost w wymaganiach, ale jest niezbedny do wyswietlania historii
@app.get("/currencies/filter/range")
def get_currencies_range(currency: str, start_date: str, end_date: str, db: Session = Depends(get_db)):
    d_start = date_type.fromisoformat(start_date)
    d_end = date_type.fromisoformat(end_date)
    
    kursy = db.query(CurrencyRate).filter(
        CurrencyRate.currency_code == currency,
        CurrencyRate.date >= d_start,
        CurrencyRate.date <= d_end
    ).all()
    return kursy

# 3. Endpoint zgodny z wymaganiami: POST /currencies/fetch
@app.post("/currencies/fetch")
def fetch_currency(request: FetchRequest, db: Session = Depends(get_db)):
    url = f"http://api.nbp.pl/api/exchangerates/rates/A/{request.currency}/{request.start_date}/{request.end_date}/?format=json"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Blad NBP (brak danych lub limit 367 dni)")
    
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