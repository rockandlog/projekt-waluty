import { Component, ChangeDetectorRef } from '@angular/core'; 
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
  
  tryb: string = 'zakres';
  wybranaWaluta: string = 'USD';
  
  wybranyRok: number = 2025;
  wybranyKwartal: string = '1';
  wybranyMiesiac: string = '01';

  dataOd: string = '2025-01-01';
  dataDo: string = '2025-01-31';

  status: string = '';
  isLoading: boolean = false;

  
  constructor(private http: HttpClient, private cd: ChangeDetectorRef) {}

  przeliczDaty() {
    if (this.tryb === 'rok') {
      this.dataOd = `${this.wybranyRok}-01-01`;
      this.dataDo = `${this.wybranyRok}-12-31`;
    } 
    else if (this.tryb === 'kwartal') {
      if (this.wybranyKwartal === '1') {
        this.dataOd = `${this.wybranyRok}-01-01`; this.dataDo = `${this.wybranyRok}-03-31`;
      } else if (this.wybranyKwartal === '2') {
        this.dataOd = `${this.wybranyRok}-04-01`; this.dataDo = `${this.wybranyRok}-06-30`;
      } else if (this.wybranyKwartal === '3') {
        this.dataOd = `${this.wybranyRok}-07-01`; this.dataDo = `${this.wybranyRok}-09-30`;
      } else {
        this.dataOd = `${this.wybranyRok}-10-01`; this.dataDo = `${this.wybranyRok}-12-31`;
      }
    } 
    else if (this.tryb === 'miesiac') {
      const ostatniDzien = new Date(this.wybranyRok, parseInt(this.wybranyMiesiac), 0).getDate();
      this.dataOd = `${this.wybranyRok}-${this.wybranyMiesiac}-01`;
      this.dataDo = `${this.wybranyRok}-${this.wybranyMiesiac}-${ostatniDzien}`;
    }
  }

  pobierzKursy() {
    this.przeliczDaty();
    
    this.isLoading = true;
    this.status = '⏳ Łączenie z NBP...';
    this.cd.detectChanges(); 

    const body = {
      currency: this.wybranaWaluta,
      start_date: this.dataOd,
      end_date: this.dataDo
    };

    this.http.post('http://localhost:8000/currencies/fetch', body).subscribe({
      next: (response: any) => {
        this.status = `✅ Sukces! ${response.message}`;
        
        this.odswiezListe();
      },
      error: (error) => {
        console.error(error);
        this.status = '❌ Błąd. Sprawdź konsolę (może NBP nie ma danych?)';
        this.isLoading = false;
        this.cd.detectChanges(); 
      }
    });
  }

  odswiezListe() {
    
    const url = `http://localhost:8000/currencies/filter/range?currency=${this.wybranaWaluta}&start_date=${this.dataOd}&end_date=${this.dataDo}`;

    this.http.get<any[]>(url).subscribe({
      next: (data) => {
        this.kursyWalut = data.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
        
        
        this.isLoading = false;
        
        
        setTimeout(() => { 
          if(!this.isLoading) {
             this.status = ''; 
             this.cd.detectChanges(); 
          }
        }, 3000);

        
        this.cd.detectChanges();
      },
      error: (error) => {
        console.error(error);
        this.isLoading = false;
        this.cd.detectChanges();
      }
    });
  }
}