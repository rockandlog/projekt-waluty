from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Tworzymy plik bazy danych (będzie się nazywał 'waluty.db')
DATABASE_URL = "sqlite:///./waluty.db"

# To jest silnik bazy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# To jest sesja - czyli nasze "połączenie" z bazą
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Baza dla modeli (nie przejmuj się tym, to wymóg techniczny)
Base = declarative_base()

# 2. Definiujemy Tabelę (Tak jak w Excelu)
class CurrencyRate(Base):
    __tablename__ = "kursy_walut"

    id = Column(Integer, primary_key=True, index=True) # Unikalny numer wpisu
    currency_code = Column(String, index=True)         # Np. "USD"
    rate = Column(Float)                               # Np. 4.02
    date = Column(Date)                                # Np. 2024-01-22