import os
import sys
import shutil
import subprocess
from colorama import init, Fore, Style

# Inicjalizacja colorama
init(autoreset=True)


def log(message, level="INFO"):
    """
    Funkcja do logowania z kolorami
    """
    if level == "INFO":
        color = Fore.CYAN
    elif level == "WARNING":
        color = Fore.YELLOW
    elif level == "ERROR":
        color = Fore.RED
    elif level == "SUCCESS":
        color = Fore.GREEN
    else:
        color = Fore.WHITE

    print(f"{color}{message}{Style.RESET_ALL}")


def check_dependencies():
    """
    Sprawdza, czy wymagane zależności są zainstalowane
    """
    required_packages = ["pyinstaller", "pyautogui", "pywinauto", "colorama", "pillow"]
    missing_packages = []

    log("Sprawdzam wymagane zależności...", "INFO")

    for package in required_packages:
        try:
            __import__(package)
            log(f"✓ {package} jest zainstalowany", "SUCCESS")
        except ImportError:
            missing_packages.append(package)
            log(f"✗ {package} nie jest zainstalowany", "ERROR")

    if missing_packages:
        log("\nBrakujące pakiety. Instaluję je teraz:", "WARNING")
        for package in missing_packages:
            log(f"Instaluję {package}...", "INFO")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            log(f"Zainstalowano {package}", "SUCCESS")

    return True


def build_executable():
    """
    Buduje plik wykonywalny za pomocą PyInstaller
    """
    log("\nRozpoczynanie budowy pliku .exe...", "INFO")

    # Upewnij się, że plik main.py istnieje
    if not os.path.exists("main.py"):
        log("Błąd: Nie znaleziono pliku main.py", "ERROR")
        return False

    # Usuń poprzednie katalogi build i dist
    for dir_name in ["build", "dist"]:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                log(f"Usunięto katalog {dir_name}", "INFO")
            except Exception as e:
                log(f"Nie można usunąć katalogu {dir_name}: {e}", "WARNING")

    # Usuń poprzedni plik .spec
    spec_file = "bluetooth_fix.spec"
    if os.path.exists(spec_file):
        try:
            os.remove(spec_file)
            log(f"Usunięto plik {spec_file}", "INFO")
        except Exception as e:
            log(f"Nie można usunąć pliku {spec_file}: {e}", "WARNING")

    # Konfiguracja parametrów PyInstaller
    pyinstaller_cmd = [
        "pyinstaller",
        "--name=bluetooth_fix",
        "--onefile",  # Pojedynczy plik EXE
        "--windowed",  # Aplikacja okienkowa bez konsoli
        "--add-data=wlasciwosci.png;.",  # Dodanie pliku obrazu
        "--icon=NONE",  # Można tu dodać ścieżkę do ikony, jeśli jest dostępna
        "main.py"
    ]

    # Wykonanie komendy PyInstaller
    log("Uruchamiam PyInstaller...", "INFO")
    log(" ".join(pyinstaller_cmd), "INFO")

    try:
        subprocess.run(pyinstaller_cmd, check=True)
        log("\nBudowanie pliku .exe zakończone pomyślnie!", "SUCCESS")

        # Sprawdź, czy plik został utworzony
        exe_path = os.path.join("dist", "bluetooth_fix.exe")
        if os.path.exists(exe_path):
            log(f"Plik EXE jest dostępny pod ścieżką: {os.path.abspath(exe_path)}", "SUCCESS")
            return True
        else:
            log("Nie można znaleźć wygenerowanego pliku EXE", "ERROR")
            return False

    except subprocess.CalledProcessError as e:
        log(f"Błąd podczas budowania pliku .exe: {e}", "ERROR")
        return False
    except Exception as e:
        log(f"Nieoczekiwany błąd: {e}", "ERROR")
        return False


def main():
    """
    Główna funkcja programu
    """
    log("===== Generator pliku EXE dla naprawiacza słuchawek Bluetooth =====", "INFO")

    # Sprawdź zależności
    if not check_dependencies():
        log("Nie można kontynuować z powodu brakujących zależności", "ERROR")
        return

    # Upewnij się, że plik obrazu istnieje lub go utwórz
    if not os.path.exists("wlasciwosci.png"):
        log("Tworzę plik wlasciwosci.png...", "INFO")
        try:
            from main import create_wlasciwosci_image
            create_wlasciwosci_image()
        except Exception as e:
            log(f"Nie można utworzyć pliku wlasciwosci.png: {e}", "WARNING")
            log("Kontynuuję mimo to...", "WARNING")

    # Buduj plik wykonywalny
    if build_executable():
        log("\nPomyślnie utworzono plik EXE!", "SUCCESS")
        log("\nMożesz teraz uruchomić bluetooth_fix.exe z katalogu dist.", "INFO")
    else:
        log("\nNie udało się utworzyć pliku EXE.", "ERROR")

    log("\nNaciśnij Enter, aby zakończyć...", "INFO")
    input()


if __name__ == "__main__":
    main()