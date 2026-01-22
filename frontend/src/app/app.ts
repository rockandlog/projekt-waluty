import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.html',  // Wskazujemy Twój plik HTML
  styleUrl: './app.css'       // Wskazujemy Twój plik stylów
})
export class AppComponent {
  // Lista, w której będziemy trzymać pobrane waluty
  kursyWalut: any[] = [];

  constructor(private http: HttpClient) {}

  // Metoda 1: Wysyła żądanie do Twojego Backendu, żeby pobrał dane z NBP
  pobierzDolara() {
    this.http.post('http://127.0.0.1:8000/currencies/fetch', {}).subscribe({
      next: (response) => {
        console.log('Backend odpowiedział:', response);
        alert('Sukces! Pobrano kurs dolara z NBP do Twojej bazy.');
        this.odswiezListe(); // Automatycznie odśwież tabelkę
      },
      error: (error) => {
        console.error('Błąd:', error);
        alert('Błąd! Sprawdź czy backend (czarne okno) jest włączony.');
      }
    });
  }

  // Metoda 2: Pobiera to, co już mamy zapisane w bazie danych
  odswiezListe() {
    this.http.get<any[]>('http://127.0.0.1:8000/currencies').subscribe({
      next: (data) => {
        console.log('Dane z bazy:', data);
        this.kursyWalut = data;
      },
      error: (error) => {
        console.error('Nie udało się pobrać listy:', error);
      }
    });
  }
}