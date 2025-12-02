# SafeChat - Bezpieczny Czat Szyfrowany

Aplikacja czatu wykorzystująca bibliotekę Flask oraz Socket.IO, implementująca szyfrowanie hybrydowe (RSA + AES) po stronie klienta. Serwer pośredniczy w komunikacji, ale nie ma dostępu do treści wiadomości.

## 1. Wymagania i Instalacja

Upewnij się, że masz zainstalowany Python. Następnie zainstaluj niezbędne biblioteki:

```bash
pip install flask flask-socketio
```
## 2. Struktura plików
Aby aplikacja działała poprawnie z frameworkiem Flask, utwórz foldery i rozmieść pliki w następujący sposób:

```text
projekt/
│
├── .env
├── app.py                # Twój główny plik serwera
├── templates/            # Folder na pliki HTML
│   ├── login.html
│   └── chat.html
└── static/               # Folder na pliki statyczne
    └── styles.css        # Plik stylów (musi istnieć)
```

## 2. Instalacja wymagań
Upewnij się, że masz zainstalowanego Pythona. Następnie zainstaluj wymagane biblioteki:
```bash
pip install flask flask-socketio python-dotenv
```
## 3. Konfiguracja środowiska
Przed uruchomieniem aplikacji utwórz w głównym folderze plik o nazwie .env i wklej do niego poniższą treść (możesz zmienić klucz na własny):
```ini
FLASK_SECRET_KEY="SEKRETNY-KLUCZ"
```

## 4. Uruchomienie serwera
W terminalu, będąc w folderze projektu, wpisz:

```bash
python app.py
```
Serwer wystartuje domyślnie pod adresem: http://127.0.0.1:5000.

## 5. Scenariusz: Uruchomienie 3 klientów
Ponieważ czat działa w przeglądarce, możesz symulować wielu użytkowników, otwierając nowe okna incognito.

### Krok 1: Pierwszy użytkownik (Inicjator pokoju)

Otwórz przeglądarkę i wejdź na http://127.0.0.1:5000.

Wpisz nick, np. Kacper i kliknij "Połącz".

Co się dzieje: Kacper jest sam w pokoju, więc generuje losowy klucz szyfrujący AES dla tego pokoju.

### Krok 2: Drugi użytkownik

Otwórz nowe okno incognito/prywatne (aby uniknąć konfliktów pamięci podręcznej) pod tym samym adresem.

Wpisz nick, np. Kamil i kliknij "Połącz".

Co się dzieje: Kacper wykrywa Kamila, szyfruje klucz AES używając klucza publicznego Kamila i wysyła mu go. Teraz mogą pisać ze sobą bezpiecznie.

### Krok 3: Trzeci użytkownik

Otwórz kolejną kartę (trzecie okno).

Wpisz nick, np. Patryk i kliknij "Połącz".

Co się dzieje: Obecni użytkownicy (Kacper lub Kamil) przesyłają zaszyfrowany klucz AES do Patryka.

Wszyscy trzej użytkownicy widzą się na liście "Użytkownicy online" i mogą wymieniać zaszyfrowane wiadomości.

## Dodatkowe informacje
Komendy: Wpisz /help w oknie czatu, aby zobaczyć dostępne polecenia.

Rozłączanie: Możesz użyć przycisku "Wyjdź" lub wpisać /quit.

Historia: Serwer przechowuje ostatnie 10 wiadomości (w formie zaszyfrowanej).