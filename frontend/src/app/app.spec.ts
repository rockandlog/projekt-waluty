import { TestBed } from '@angular/core/testing';
import { AppComponent } from './app';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';

describe('AppComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      // Importujemy Twój komponent
      imports: [AppComponent],
      // Dostarczamy "udawany" internet, żeby testy nie próbowały naprawdę łączyć się z backendem
      providers: [
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    }).compileComponents();
  });

  // Test 1: Sprawdza, czy aplikacja w ogóle się tworzy (czy nie ma błędów w kodzie)
  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  // Test 2: Sprawdza, czy tytuł w kodzie HTML jest poprawny
  it('should render title', () => {
    const fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    // Sprawdzamy czy w nagłówku h1 jest tekst "Projekt Waluty"
    expect(compiled.querySelector('h1')?.textContent).toContain('Projekt Waluty');
  });
});