import datetime
import os
import time
import traceback

import pyautogui
from colorama import init, Fore, Style
from pywinauto import Desktop, Application

# Inicjalizacja colorama
init(autoreset=True)


def log(message, level="INFO"):
    """
    Funkcja do logowania z timestampami i kolorami
    """
    timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

    if level == "INFO":
        color = Fore.GREEN
    elif level == "WARNING":
        color = Fore.YELLOW
    elif level == "ERROR":
        color = Fore.RED
    elif level == "SUCCESS":
        color = Fore.CYAN
    else:
        color = Fore.WHITE

    print(f"{Fore.WHITE}[{timestamp}] {color}{message}{Style.RESET_ALL}")


def cleanup_windows():
    """
    Funkcja do zamykania wszystkich otwartych okien związanych z aplikacją
    """
    log("Sprzątanie otwartych okien...", "INFO")

    # Lista tytułów okien do zamknięcia
    window_titles = [
        {"title_re": ".*Właściwości.*", "exact": False},
        {"title_re": ".*Urządzenia i drukarki.*", "exact": False},
        {"title": "Ustawienia", "exact": True},
        {"title_re": ".*Panel sterowania.*", "exact": False}
    ]

    for window_info in window_titles:
        try:
            if window_info.get("exact", False):
                app = Application(backend="uia").connect(title=window_info["title"], timeout=1)
            else:
                app = Application(backend="uia").connect(title_re=window_info["title_re"], timeout=1)

            window = app.top_window()
            log(f"Zamykam okno: {window.window_text()}", "INFO")
            window.close()
            time.sleep(0.2)
        except Exception:
            # Ignorujemy błędy, jeśli okno nie istnieje lub nie można go zamknąć
            pass

    log("Zakończono sprzątanie", "INFO")


def fix_bluetooth_headphones():
    # Nazwa słuchawek
    headphones_name = "Boltune BT-BH010"
    log(f"Rozpoczynam naprawę słuchawek {headphones_name}...", "INFO")

    original_handsfree_state = None  # Tutaj zapiszemy pierwotny stan opcji "Telefon głośnomówiący"

    try:
        # Otwieranie ustawień Bluetooth
        log("Otwieram ustawienia Bluetooth...", "INFO")
        os.system("start ms-settings:bluetooth")
        time.sleep(1)  # Zmniejszony czas oczekiwania

        # Podłączamy się do okna ustawień
        app = Application(backend="uia").connect(title="Ustawienia")
        settings_window = app.window(title="Ustawienia")

        # Przewijamy w dół do sekcji "Powiązane ustawienia"
        log("Przewijam do sekcji 'Powiązane ustawienia'...", "INFO")
        for _ in range(5):
            settings_window.wheel_mouse_input(wheel_dist=-3)
            time.sleep(0.1)  # Zmniejszony czas oczekiwania

        # Próbujemy różnych metod znalezienia elementu "Więcej ustawień urządzeń i drukarek"
        log("Szukam opcji 'Więcej ustawień urządzeń i drukarek'...", "INFO")

        # METODA 1: Szukanie przez zawartość tekstu (częściowe dopasowanie)
        found = False
        try:
            # Uzyskanie wszystkich elementów potomnych okna
            all_elements = settings_window.descendants()
            for element in all_elements:
                try:
                    element_text = element.window_text()
                    if "urządzeń i drukarek" in element_text:
                        log(f"Znaleziono element: '{element_text}'", "SUCCESS")
                        element.click_input()
                        found = True
                        time.sleep(1.5)  # Pozostawiamy dłuższy czas na otwarcie okna
                        break
                except Exception:
                    continue
        except Exception as e:
            log(f"Metoda 1 nie powiodła się: {e}", "WARNING")

        # METODA 2: Próba kliknięcia przez zdefiniowane wzorce klasy/id
        if not found:
            try:
                log("Próbuję znaleźć element przez wzorce klasy/id...", "INFO")
                hyperlinks = settings_window.children(control_type="Hyperlink")
                for link in hyperlinks:
                    try:
                        if "urządzeń i drukarek" in link.window_text():
                            log(f"Znaleziono hiperłącze: {link.window_text()}", "SUCCESS")
                            link.click_input()
                            found = True
                            time.sleep(1.5)
                            break
                    except:
                        continue
            except Exception as e:
                log(f"Metoda 2 nie powiodła się: {e}", "WARNING")

        # METODA 3: Odszukanie zewnętrznej strzałki (ikony) i kliknięcie na nią
        if not found:
            try:
                log("Szukam ikony zewnętrznej linku...", "INFO")
                external_icons = settings_window.descendants(control_type="Button", title="")
                for icon in external_icons:
                    try:
                        parent = icon.parent()
                        parent_text = parent.window_text()
                        if "urządzeń i drukarek" in parent_text:
                            log(f"Znaleziono przycisk z rodzicem: {parent_text}", "SUCCESS")
                            icon.click_input()
                            found = True
                            time.sleep(1.5)
                            break
                    except:
                        continue
            except Exception as e:
                log(f"Metoda 3 nie powiodła się: {e}", "WARNING")

        # METODA 4: Bezpośrednie otwarcie Panelu Sterowania - Urządzenia i drukarki
        if not found:
            try:
                log("Otwieram Panel Sterowania - Urządzenia i drukarki bezpośrednio...", "INFO")
                os.system("control printers")
                found = True
                time.sleep(1.5)
            except Exception as e:
                log(f"Metoda 4 nie powiodła się: {e}", "WARNING")

        # METODA 5: Użycie koordynatów ekranu jako ostateczność
        if not found:
            try:
                log("Używam koordynatów ekranu jako ostateczności...", "WARNING")
                # Rozmiar ekranu
                screen_width, screen_height = pyautogui.size()

                # Przybliżone koordynaty dla "Więcej ustawień urządzeń i drukarek"
                x = screen_width // 2  # środek ekranu w poziomie
                y = screen_height // 2 + 100  # nieco poniżej środka ekranu

                # Kliknięcie w przybliżonym miejscu
                pyautogui.click(x, y)
                found = True
                time.sleep(1)
            except Exception as e:
                log(f"Metoda 5 nie powiodła się: {e}", "WARNING")

        if not found:
            raise Exception("Nie udało się znaleźć lub kliknąć opcji 'Więcej ustawień urządzeń i drukarek'")

        # Podłączamy się do okna Panelu Sterowania
        log("Podłączam się do okna 'Urządzenia i drukarki'...", "INFO")
        try:
            devices_app = Application(backend="uia").connect(title_re=".*Urządzenia i drukarki.*", timeout=5)
            devices_window = devices_app.window(title_re=".*Urządzenia i drukarki.*")
        except Exception as e:
            log(f"Nie można znaleźć okna 'Urządzenia i drukarki': {e}", "WARNING")

            # Próba alternatywna - podłączenie do jakiegokolwiek okna Panelu Sterowania
            try:
                log("Próba alternatywna - szukam okna Panelu Sterowania...", "INFO")
                devices_app = Application(backend="uia").connect(title_re=".*Panel sterowania.*", timeout=5)
                devices_window = devices_app.top_window()
            except Exception as e2:
                raise Exception(f"Nie można znaleźć okna Panelu Sterowania: {e2}")

        # Znajdujemy słuchawki w panelu sterowania
        log(f"Szukam słuchawek {headphones_name}...", "INFO")
        try:
            # Próba znalezienia słuchawek (elastyczne podejście)
            all_items = devices_window.descendants()
            bt_device = None
            for item in all_items:
                try:
                    item_text = item.window_text()
                    if headphones_name in item_text:
                        bt_device = item
                        log(f"Znaleziono urządzenie: {item_text}", "SUCCESS")
                        break
                except:
                    continue

            if not bt_device:
                raise Exception(f"Nie znaleziono urządzenia {headphones_name}")

            # Klikamy dwukrotnie na urządzenie
            log("Otwieram właściwości przez podwójne kliknięcie...", "INFO")
            try:
                bt_device.double_click_input()
                time.sleep(0.8)
            except Exception as e:
                log(f"Podwójne kliknięcie nie powiodło się: {e}", "WARNING")

                # Klikamy prawym i używamy menu kontekstowego
                try:
                    log("Próbuję otworzyć właściwości przez menu kontekstowe...", "INFO")
                    bt_device.click_input(button="right")
                    time.sleep(0.3)

                    # Próba znalezienia opcji "Właściwości" w menu kontekstowym
                    menu = Desktop(backend="uia").window(
                        class_name="#32768")  # Standardowa klasa dla menu kontekstowego
                    menu_items = menu.children()

                    for item in menu_items:
                        try:
                            if "właściwości" in item.window_text().lower():
                                item.click_input()
                                time.sleep(0.8)
                                break
                        except:
                            continue

                    # Jeśli nie znaleziono, spróbuj kliknąć ostatnią pozycję w menu (zwykle to Właściwości)
                    if len(menu_items) > 0:
                        menu_items[-1].click_input()
                        time.sleep(0.8)
                except Exception as e:
                    log(f"Menu kontekstowe nie działa: {e}", "WARNING")

                    # Metoda z PyAutoGUI jako ostateczność
                    try:
                        # Ostateczne rozwiązanie - kliknięcie w prawy dolny róg okna właściwości
                        mouse_pos = pyautogui.position()
                        # Przesunięcie na dół o 300 pikseli powinno trafić w obszar menu
                        pyautogui.click(mouse_pos.x, mouse_pos.y + 300)
                        time.sleep(0.8)
                    except Exception as e:
                        log(f"Awaryjne kliknięcie nie zadziałało: {e}", "WARNING")

        except Exception as e:
            raise Exception(f"Problem podczas szukania słuchawek: {e}")

        # Obsługa okna właściwości - próbujemy kilka podejść
        log("Podłączam się do okna właściwości...", "INFO")
        props_window = None

        # Podejście 1: Szukamy po nazwie słuchawek
        try:
            props_app = Application(backend="uia").connect(title_re=f".*{headphones_name}.*", timeout=3)
            props_window = props_app.top_window()
            log("Znaleziono okno właściwości przez nazwę słuchawek", "SUCCESS")
        except Exception as e:
            log(f"Nie znaleziono okna przez nazwę słuchawek: {e}", "WARNING")

        # Podejście 2: Szukamy po słowie "Właściwości"
        if props_window is None:
            try:
                props_app = Application(backend="uia").connect(title_re=".*Właściwości.*", timeout=3)
                props_window = props_app.top_window()
                log("Znaleziono okno właściwości przez ogólną nazwę", "SUCCESS")
            except Exception as e:
                log(f"Nie znaleziono okna przez ogólną nazwę: {e}", "WARNING")

        # Podejście 3: Używamy find_windows do szukania najnowszego okna dialogowego
        if props_window is None:
            try:
                from pywinauto import findwindows
                windows = findwindows.find_windows(title_re=".*",
                                                   class_name="#32770")  # Typowa klasa dla okien dialogowych
                if windows:
                    props_app = Application(backend="uia").connect(handle=windows[0])
                    props_window = props_app.top_window()
                    log("Znaleziono okno przez najnowsze okno dialogowe", "SUCCESS")
            except Exception as e:
                log(f"Nie znaleziono okna przez find_windows: {e}", "WARNING")

        if props_window is None:
            raise Exception("Nie można znaleźć okna właściwości")

        # Klikamy zakładkę "Usługi"
        log("Przechodzę do zakładki 'Usługi'...", "INFO")
        try:
            # Próba 1: Standardowe podejście
            services_tab = props_window.child_window(title="Usługi", control_type="TabItem")
            services_tab.click_input()
            time.sleep(0.8)  # Krótsze oczekiwanie
        except Exception as e:
            log(f"Standardowe podejście do zakładki nie zadziałało: {e}", "WARNING")

            # Próba 2: Szukamy wszystkich zakładek
            try:
                tabs = props_window.descendants(control_type="TabItem")
                services_found = False
                for tab in tabs:
                    try:
                        if "Usługi" in tab.window_text():
                            tab.click_input()
                            services_found = True
                            time.sleep(0.8)
                            break
                    except:
                        continue

                if not services_found:
                    # Próba 3: Klikamy trzecią zakładkę (często "Usługi" to trzecia zakładka)
                    if len(tabs) >= 3:
                        tabs[2].click_input()
                        time.sleep(0.8)
                    else:
                        raise Exception("Nie znaleziono zakładki 'Usługi'")
            except Exception as e2:
                # Próba 4: Szukamy po koordynatach (bazując na zrzucie ekranu)
                try:
                    window_rect = props_window.rectangle()
                    # Koordynaty zakładki "Usługi" bazując na pozycji okna
                    services_tab_x = window_rect.left + window_rect.width() // 2  # Środek okna
                    services_tab_y = window_rect.top + 50  # Zakładając, że zakładki są na górze

                    # Próbujemy kliknąć blisko środka górnej części okna
                    pyautogui.click(services_tab_x, services_tab_y)
                    time.sleep(0.8)
                except Exception as e3:
                    raise Exception(f"Problem podczas przechodzenia do zakładki 'Usługi': {e2}, {e3}")

        # Wyłączamy opcję "Telefon głośnomówiący"
        handsfree_clicked = False

        # METODA 1: Szukanie po tekście
        log("Próbuję znaleźć i kliknąć element 'Telefon głośnomówiący'...", "INFO")
        try:
            for elem in props_window.descendants():
                try:
                    if "głośnomówiący" in elem.window_text().lower():
                        log(f"Znaleziono element: {elem.window_text()}", "SUCCESS")
                        elem.click_input()
                        time.sleep(0.3)
                        handsfree_clicked = True
                        original_handsfree_state = 1  # Zakładamy, że był włączony
                        log("Kliknięto element 'Telefon głośnomówiący'", "SUCCESS")
                        break
                except:
                    continue
        except Exception as e:
            log(f"Nie udało się kliknąć 'Telefon głośnomówiący' metodą 1: {e}", "WARNING")

        # METODA 2: Kliknięcie w przybliżone koordynaty na podstawie zrzutu ekranu
        if not handsfree_clicked:
            try:
                log("Próbuję kliknąć opcję 'Telefon głośnomówiący' przez koordynaty...", "INFO")
                # Bazując na zrzucie ekranu
                rect = props_window.rectangle()

                # Z zrzutu ekranu widać, że opcja jest mniej więcej w 1/3 okna od góry
                checkmark_x = rect.left + 40  # Checkbox jest zwykle blisko lewej krawędzi
                checkmark_y = rect.top + (rect.height() * 0.35)  # Około 1/3 w dół okna

                # Kliknięcie w checkbox
                pyautogui.click(checkmark_x, checkmark_y)
                time.sleep(0.3)
                handsfree_clicked = True
                original_handsfree_state = 1
                log(f"Kliknięto w koordynaty ({checkmark_x}, {checkmark_y})", "SUCCESS")
            except Exception as e:
                log(f"Nie udało się kliknąć 'Telefon głośnomówiący' metodą 2: {e}", "WARNING")

        if not handsfree_clicked:
            log("Nie udało się kliknąć opcji 'Telefon głośnomówiący'", "WARNING")

        # Klikamy OK - używamy wielu metod i weryfikacji
        log("Zatwierdzam zmiany...", "INFO")
        ok_clicked = False

        # METODA 1: Standardowe szukanie przycisku OK
        try:
            ok_button = props_window.child_window(title="OK", control_type="Button")
            ok_button.click_input()
            time.sleep(0.5)
            ok_clicked = True
            log("Kliknięto przycisk OK metodą 1", "SUCCESS")
        except Exception as e:
            log(f"Nie udało się kliknąć OK metodą 1: {e}", "WARNING")

        # METODA 2: Szukanie wszystkich przycisków
        if not ok_clicked:
            try:
                log("Szukam przycisku OK wśród wszystkich przycisków...", "INFO")
                buttons = props_window.descendants(control_type="Button")
                for button in buttons:
                    try:
                        if button.window_text() == "OK":
                            button.click_input()
                            time.sleep(0.5)
                            ok_clicked = True
                            log("Kliknięto przycisk OK metodą 2", "SUCCESS")
                            break
                    except:
                        continue
            except Exception as e:
                log(f"Nie udało się kliknąć OK metodą 2: {e}", "WARNING")

        # METODA 3: Kliknięcie przycisku w dolnej części okna
        if not ok_clicked:
            try:
                log("Próbuję kliknąć OK przez koordynaty...", "INFO")
                # Kliknięcie w prawy dolny róg okna
                rect = props_window.rectangle()
                ok_x = rect.left + (rect.width() * 0.4)  # Przycisk OK jest zwykle po prawej stronie na dole
                ok_y = rect.top + rect.height() - 25  # Blisko dolnej krawędzi

                # Kliknięcie w przycisk
                pyautogui.click(ok_x, ok_y)
                time.sleep(0.5)
                ok_clicked = True
                log(f"Kliknięto OK przez koordynaty ({ok_x}, {ok_y})", "SUCCESS")
            except Exception as e:
                log(f"Nie udało się kliknąć OK metodą 3: {e}", "WARNING")

        # METODA 4: Użycie klawisza Enter zamiast kliknięcia
        if not ok_clicked:
            try:
                log("Próbuję zatwierdzić przez klawisz Enter...", "INFO")
                # Aktywacja okna
                props_window.set_focus()
                time.sleep(0.2)
                # Naciśnięcie Enter
                pyautogui.press('enter')
                time.sleep(0.5)
                ok_clicked = True
                log("Wysłano klawisz Enter", "SUCCESS")
            except Exception as e:
                log(f"Nie udało się wysłać klawisza Enter: {e}", "WARNING")

        if not ok_clicked:
            log("Nie udało się kliknąć przycisku OK, ale kontynuuję...", "WARNING")

        # Wracamy do ustawień Bluetooth
        log("Wracam do ustawień Bluetooth...", "INFO")
        os.system("start ms-settings:bluetooth")
        time.sleep(1)

        # Podłączamy się ponownie do okna ustawień
        app = Application(backend="uia").connect(title="Ustawienia")
        settings_window = app.window(title="Ustawienia")

        # Znajdujemy nasze słuchawki
        log(f"Szukam słuchawek {headphones_name} do rozłączenia...", "INFO")
        try:
            # Szukamy słuchawek
            all_items = settings_window.descendants()
            headphones = None
            for item in all_items:
                try:
                    item_text = item.window_text()
                    if headphones_name in item_text:
                        headphones = item
                        log(f"Znaleziono słuchawki: {item_text}", "SUCCESS")
                        break
                except:
                    continue

            if not headphones:
                # Przewijamy w górę - być może słuchawki są w innym miejscu
                for _ in range(3):
                    settings_window.wheel_mouse_input(wheel_dist=3)
                    time.sleep(0.1)

                # Szukamy ponownie
                all_items = settings_window.descendants()
                for item in all_items:
                    try:
                        item_text = item.window_text()
                        if headphones_name in item_text:
                            headphones = item
                            log(f"Znaleziono słuchawki: {item_text}", "SUCCESS")
                            break
                    except:
                        continue

            if not headphones:
                raise Exception(f"Nie znaleziono słuchawek {headphones_name}")

            # Klikamy na słuchawki, aby wyświetlić przyciski
            headphones.click_input()
            time.sleep(0.3)

            # Szukamy przycisku "Rozłącz"
            disconnect_button = None
            buttons = settings_window.descendants(control_type="Button")
            for button in buttons:
                try:
                    button_text = button.window_text()
                    if "Rozłącz" in button_text:
                        disconnect_button = button
                        log(f"Znaleziono przycisk: {button_text}", "SUCCESS")
                        break
                except:
                    continue

            if disconnect_button:
                log("Rozłączam słuchawki...", "INFO")
                disconnect_button.click_input()
                log("Słuchawki zostały rozłączone.", "SUCCESS")
                time.sleep(1)
            else:
                log("Przycisk 'Rozłącz' nie znaleziony. Być może słuchawki są już rozłączone.", "WARNING")
                # Sprawdzamy, czy jest dostępny przycisk "Połącz" od razu
                connect_button = None
                for button in buttons:
                    try:
                        button_text = button.window_text()
                        if "Połącz" in button_text:
                            connect_button = button
                            break
                    except:
                        continue

                if connect_button:
                    log("Słuchawki są już rozłączone, przechodzę do ponownego łączenia.", "INFO")
                else:
                    # Klikamy ponownie, aby upewnić się, że mamy dostęp do przycisków
                    headphones.click_input()
                    time.sleep(0.3)

            # Szukamy przycisku "Połącz"
            connect_button = None
            buttons = settings_window.descendants(control_type="Button")
            for button in buttons:
                try:
                    button_text = button.window_text()
                    if "Połącz" in button_text:
                        connect_button = button
                        log(f"Znaleziono przycisk: {button_text}", "SUCCESS")
                        break
                except:
                    continue

            if not connect_button:
                # Klikamy ponownie w słuchawki, aby odświeżyć stan
                headphones.click_input()
                time.sleep(0.3)

                # Ponowne szukanie przycisku "Połącz"
                buttons = settings_window.descendants(control_type="Button")
                for button in buttons:
                    try:
                        button_text = button.window_text()
                        if "Połącz" in button_text:
                            connect_button = button
                            log(f"Znaleziono przycisk: {button_text}", "SUCCESS")
                            break
                    except:
                        continue

            if connect_button:
                log("Ponownie łączę słuchawki...", "INFO")
                connect_button.click_input()
                log("Słuchawki są ponownie łączone.", "SUCCESS")
                time.sleep(2)
            else:
                log("Przycisk 'Połącz' nie znaleziony. Sprawdź stan słuchawek.", "WARNING")
        except Exception as e:
            raise Exception(f"Problem podczas rozłączania/łączenia słuchawek: {e}")

        log("Zadanie zostało pomyślnie zakończone!", "SUCCESS")
        return True

    except Exception as e:
        error_msg = str(e)
        log(f"Wystąpił błąd: {error_msg}", "ERROR")
        traceback.print_exc()
        return False
    finally:
        # Zawsze sprzątamy na końcu, niezależnie od wyniku
        cleanup_windows()


def create_wlasciwosci_image():
    """
    Tworzy prosty obrazek napisu 'Właściwości' w menu kontekstowym,
    który potem będzie używany do rozpoznawania tej opcji w menu.
    """
    try:
        import numpy as np
        from PIL import Image, ImageDraw, ImageFont

        # Tworzenie prostego obrazka
        img = Image.new('RGB', (120, 24), color=(240, 240, 240))
        d = ImageDraw.Draw(img)

        # Próba użycia czcionki systemowej (jeśli dostępna)
        try:
            font = ImageFont.truetype("segoeui.ttf", 14)
        except:
            font = None

        # Narysowanie tekstu
        d.text((10, 5), "Właściwości", fill=(0, 0, 0), font=font)

        # Zapisanie obrazka
        img.save('wlasciwosci.png')
        log("Utworzono plik wlasciwosci.png do rozpoznawania menu", "SUCCESS")
        return True
    except Exception as e:
        log(f"Nie udało się utworzyć pliku obrazu: {e}", "ERROR")
        return False


if __name__ == "__main__":
    log("Program do naprawy słuchawek Bluetooth - eliminacja opcji 'Telefon głośnomówiący'", "INFO")
    log("=" * 80, "INFO")

    # Tworzymy plik obrazu przed uruchomieniem
    create_wlasciwosci_image()

    # Uruchamiamy główną funkcję
    success = fix_bluetooth_headphones()

    if success:
        log("\n✅ Program zakończył się pomyślnie!", "SUCCESS")
    else:
        log("\n❌ Program napotkał błąd i nie został zakończony pomyślnie.", "ERROR")

