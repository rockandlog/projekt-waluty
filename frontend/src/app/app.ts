import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class AppComponent {
  kursyWalut: any[] = [];
  
  wybranaWaluta: string = 'USD';
  dataOd: string = '2024-01-01';
  dataDo: string = '2024-01-10';

  constructor(private http: HttpClient) {}

  pobierzKursy() {
    const body = {
      currency: this.wybranaWaluta,
      start_date: this.dataOd,
      end_date: this.dataDo
    };

    this.http.post('http://localhost:8000/currencies/fetch', body).subscribe({
      next: (response: any) => {
        alert(response.message);
        this.odswiezListe();
      },
      error: (error) => {
        console.error(error);
        alert('Blad pobierania danych');
      }
    });
  }

  odswiezListe() {
    this.http.get<any[]>('http://localhost:8000/currencies').subscribe({
      next: (data) => {
        this.kursyWalut = data.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
      },
      error: (error) => {
        console.error(error);
      }
    });
  }
}