from fastapi import FastAPI, Depends, HTTPException
import requests
from datetime import date as date_type
from sqlalchemy.orm import Session
# Importujemy rzeczy z naszego nowego pliku database.py
from database import engine, SessionLocal, Base, CurrencyRate

# To tworzy tabelę w bazie danych (jeśli jeszcze nie istnieje)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Funkcja pomocnicza do pobierania sesji bazy danych (otwiera i zamyka połączenie)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "System walutowy działa!"}

# Endpoint 1: Pobierz z NBP i zapisz do bazy
@app.post("/currencies/fetch")
def fetch_currency(currency_code: str = "USD", db: Session = Depends(get_db)):
    # 1. Pobieramy z NBP
    url = f"http://api.nbp.pl/api/exchangerates/rates/A/{currency_code}/?format=json"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Nie znaleziono waluty w NBP")
    
    data = response.json()
    kurs = data['rates'][0]['mid']
    data_kursu = date_type.fromisoformat(data['rates'][0]['effectiveDate'])
    
    # 2. Tworzymy nowy rekord do bazy
    nowy_wpis = CurrencyRate(
        currency_code=data['code'],
        rate=kurs,
        date=data_kursu
    )
    
    # 3. Zapisujemy w bazie
    db.add(nowy_wpis)
    db.commit()      # Zatwierdź zmiany
    db.refresh(nowy_wpis) # Odśwież, żeby dostać ID
    
    return {"message": "Zapisano w bazie!", "data": nowy_wpis}

# Endpoint 2: Odczytaj wszystko, co mamy w bazie
@app.get("/currencies")
def get_currencies(db: Session = Depends(get_db)):
    # SELECT * FROM kursy_walut
    kursy = db.query(CurrencyRate).all()
    return kursy