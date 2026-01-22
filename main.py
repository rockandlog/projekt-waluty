from fastapi import FastAPI
import requests

# Tworzymy aplikację
app = FastAPI()

# To jest nasza strona startowa (żeby sprawdzić, czy działa)
@app.get("/")
def read_root():
    return {"message": "Witaj! Twój backend działa poprawnie."}

# To jest endpoint do pobierania kursu dolara
@app.get("/kurs-dolara")
def pobierz_dolara():
    url = "http://api.nbp.pl/api/exchangerates/rates/A/USD/?format=json"
    response = requests.get(url)
    
    if response.status_code == 200:
        dane = response.json()
        return {
            "waluta": dane['code'],
            "kurs": dane['rates'][0]['mid'],
            "data": dane['rates'][0]['effectiveDate']
        }
    else:
        return {"error": "Nie udało się pobrać danych z NBP"}