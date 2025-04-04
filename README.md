# 🎧 Naprawiacz Słuchawek Bluetooth 🔧

<div align="center">
  <img src="https://img.shields.io/badge/Wersja-1.0-blue.svg" alt="Wersja" />
  <img src="https://img.shields.io/badge/Platforma-Windows%2010%2F11-brightgreen.svg" alt="Platforma" />
  <img src="https://img.shields.io/badge/Licencja-MIT-orange.svg" alt="Licencja" />
  <br><br>
  <img width="180" src="bluetooth_fix.ico" alt="Logo aplikacji" />
  <br><br>
  <p><strong>Automatyczne rozwiązanie problemu "Telefon głośnomówiący" w słuchawkach Bluetooth</strong></p>
</div>

## 📋 Spis treści

- [🔍 O programie](#-o-programie)
- [✨ Funkcje](#-funkcje)
- [📥 Instalacja](#-instalacja)
- [🚀 Jak używać](#-jak-używać)
- [🛠️ Wymagania techniczne](#️-wymagania-techniczne)
- [❓ FAQ](#-faq)

## 🔍 O programie

**Bluetooth Headphones Fixer** to narzędzie stworzone, aby rozwiązać powszechny problem z słuchawkami Bluetooth w systemie Windows 10/11. 

### ❗ Problem

> Windows często traktuje słuchawki Bluetooth jako urządzenie z mikrofonem (gdy go nie mają), co powoduje:
> - Brak dźwięku w grach
> - Problemy z automatycznym przełączaniem między urządzeniami
> - Konieczność ręcznego wyłączania opcji "Telefon głośnomówiący" po każdym połączeniu

### ✅ Rozwiązanie

Program automatycznie wykonuje sekwencję działań, które zwykle musiałbyś wykonać ręcznie:

1. Otwiera ustawienia urządzenia Bluetooth
2. Przechodzi do właściwości słuchawek
3. Wyłącza opcję "Telefon głośnomówiący"
4. Rozłącza i ponownie łączy słuchawki
5. Zamyka wszystkie otwarte okna

## ✨ Funkcje

- 🤖 **W pełni automatyczny proces** - nie wymaga interakcji użytkownika
- ⚡ **Szybkie działanie** - cały proces trwa kilka sekund
- 🔄 **Automatyczne rozłączanie i łączenie** - zrestartuje połączenie Bluetooth
- 🖥️ **Elegancki interfejs** - czytelne kolorowe logi i powiadomienia o statusie
- 🛡️ **Bezpieczny** - działa tylko na wskazanym urządzeniu, bez modyfikacji systemowych
- 📊 **Szczegółowe logi** - informacje o każdym kroku i ewentualnych problemach

## 📥 Instalacja

### Metoda 1: Gotowy plik wykonywalny

1. Pobierz najnowszą wersję programu z [sekcji Releases](https://github.com/philornot/HeadphoneFixer/releases/latest)
2. Rozpakuj archiwum do wybranego katalogu
3. Uruchom plik `bluetooth_fix.exe`

### Metoda 2: Kompilacja ze źródeł

Jeśli chcesz skompilować program samodzielnie:

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/philornot/HeadphoneFixer.git
   cd bluetooth-headphones-fixer
   ```

2. Zainstaluj wymagane zależności:
   ```bash
   pip install -r requirements.txt
   ```

3. Skompiluj program do pliku EXE:
   ```bash
   python build.py
   ```

4. Gotowy plik znajdziesz w katalogu `dist`

## 🚀 Jak używać

### Szybki start

1. **Upewnij się, że Twoje słuchawki są połączone** z komputerem
2. **Uruchom program** `bluetooth_fix.exe`
3. **Poczekaj** na zakończenie procesu
4. **Gotowe!** Po zakończeniu zobaczysz komunikat potwierdzający sukces

### Rozwiązywanie problemów

Jeśli napotkasz problemy:

- Upewnij się, że słuchawki są włączone i sparowane z komputerem
- Sprawdź, czy nazwa Twoich słuchawek odpowiada tej w programie (domyślnie "Boltune BT-BH010")
- Spróbuj uruchomić program jako administrator

## 🛠️ Wymagania techniczne

- **System operacyjny**: Windows 10 lub Windows 11
- **Uprawnienia**: Standardowe konto użytkownika
- **Dodatkowe oprogramowanie**: Nie wymagane
- **Bluetooth**: Wbudowany lub zewnętrzny adapter

## ❓ FAQ

<details>
  <summary><b>Czy mogę zmienić nazwę urządzenia, którego szuka program?</b></summary>
  
  Tak, możesz edytować plik `main.py` i zmienić wartość zmiennej `headphones_name` na nazwę Twoich słuchawek. Następnie musisz ponownie skompilować program używając `build.py`.
</details>

<details>
  <summary><b>Czy program działa z każdymi słuchawkami Bluetooth?</b></summary>
  
  Program powinien działać z większością słuchawek Bluetooth, które Windows nieprawidłowo rozpoznaje jako urządzenia z mikrofonem. Jeśli Twoje słuchawki faktycznie mają mikrofon, wyłączenie opcji "Telefon głośnomówiący" może zablokować jego funkcjonalność.
</details>

<details>
  <summary><b>Czy program jest bezpieczny?</b></summary>
  
  Tak, program wykonuje tylko standardowe operacje interfejsu użytkownika, które mógłbyś wykonać ręcznie. Nie modyfikuje rejestru Windows ani innych krytycznych ustawień systemowych.
</details>

---

<div align="center">
<p><3</p>
  <sub>© 2025 | <a href="https://github.com/philornot">philornot</a></sub>
</div>