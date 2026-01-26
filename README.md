# System Analizy Kursów Walut (NBP Currency Analyzer)

Profesjonalna aplikacja internetowa typu SPA (Single Page Application) służąca do pobierania, archiwizacji i analizy kursów walut z API NBP. Projekt zrealizowany w architekturze mikroserwisowej z pełną konteneryzacją Docker.

---

## Cel i Zakres Projektu

Aplikacja integruje się z zewnętrznym API Narodowego Banku Polskiego, pobiera dane historyczne, zapisuje je w lokalnej bazie danych SQL i umożliwia ich analizę poprzez dedykowany interfejs webowy.

### Kluczowe funkcjonalności:
* **Integracja API:** Pobieranie kursów średnich walut (`api.nbp.pl`).
* **Persistence:** Trwały zapis danych w bazie relacyjnej (SQLite).
* **Analiza:** Filtrowanie danych wg lat, kwartałów, miesięcy i zakresów dat.
* **Frontend:** Responsywny interfejs w Angularze (v19) z dynamicznym odświeżaniem.

---

## 🛠️ Technologie (Tech Stack)

* **Frontend:** Angular 19, TypeScript, Bootstrap 5, Jasmine/Karma.
* **Backend:** FastAPI (Python 3.11), SQLAlchemy, Pytest.
* **DevOps:** Docker, Docker Compose (Multi-stage builds).

---

## Instrukcja Uruchomienia

Wymagane jest środowisko **Docker Desktop**. Cały proces odbywa się w trzech krokach:

1.  **Pobranie repozytorium**
    ```bash
    git clone <adres-twojego-repozytorium>
    cd projekt-waluty
    ```

2.  **Uruchomienie aplikacji**
    Budowanie obrazów i start kontenerów w trybie tła:
    ```bash
    docker-compose up --build -d
    ```

3.  **Dostęp do usług**
    * **Aplikacja Frontend:** [http://localhost:4200](http://localhost:4200)
    * **Dokumentacja API:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Testy Jednostkowe

Projekt posiada pełne pokrycie testami, które uruchamiane są wewnątrz odizolowanych kontenerów.

1.  **Testy Backend (Pytest)**
    Sprawdzają endpointy API, logikę biznesową oraz operacje na bazie danych.
    ```bash
    docker-compose exec backend pytest
    ```

2.  **Testy Frontend (Jasmine/Karma)**
    Sprawdzają komponenty Angulara w trybie Headless (bez okna przeglądarki).
    ```bash
    docker-compose exec frontend ng test --watch=false
    ```

---

## Endpoints API (Backend)

| Metoda | Endpoint | Opis |
| :--- | :--- | :--- |
| `GET` | `/currencies` | Lista dostępnych walut. |
| `GET` | `/currencies/{date}` | Pobranie kursu dla konkretnej daty. |
| `GET` | `/currencies/filter/range` | Filtrowanie kursów po zakresie dat. |
| `POST` | `/currencies/fetch` | Pobranie danych z NBP i zapis do bazy. |

---

## Struktura Projektu

```text
projekt-waluty/
├── docker-compose.yml       # Orkiestracja (Frontend + Backend)
├── README.md                # Dokumentacja techniczna
├── backend/                 # API (FastAPI + SQLite)
│   ├── main.py
│   ├── database.py
│   ├── test_main.py
│   └── Dockerfile
└── frontend/                # UI (Angular)
    ├── src/app/
    ├── karma.conf.js
    └── Dockerfile