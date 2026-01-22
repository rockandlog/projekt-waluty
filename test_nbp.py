import requests
import json

# 1. Adres API NBP (pytamy o kurs dolara USD w formacie JSON)
url = "http://api.nbp.pl/api/exchangerates/rates/A/USD/?format=json"

print("Wysyłam zapytanie do NBP...")

# 2. Wysyłamy żądanie do NBP
response = requests.get(url)

# 3. Sprawdzamy, czy się udało (kod 200 oznacza OK)
if response.status_code == 200:
    print("Sukces! Odebrano dane.")
    
    # 4. Odczytujemy dane
    dane = response.json()
    
    # Wyciągamy sam kurs i datę z tego, co przyszło
    waluta = dane['code']
    kurs = dane['rates'][0]['mid']
    data = dane['rates'][0]['effectiveDate']
    
    print("--------------------------------")
    print(f"Waluta: {waluta}")
    print(f"Data: {data}")
    print(f"Kurs średni: {kurs} zł")
    print("--------------------------------")
else:
    print("Błąd! Nie udało się połączyć z NBP.")