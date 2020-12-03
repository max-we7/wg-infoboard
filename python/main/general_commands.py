import json
import telepot
from telepot.namedtuple import ReplyKeyboardRemove
import platform
import subprocess
from config import ADMIN_IDS, LEGIT_IDS, API_KEY, GROUP_ID, wg
import logging
from keyboards import create_eingekauft_keyboard


def einkaufen(self, msg):
    """
    add item to shopping list. If no argument is given, return shopping list
    """
    einkaufsliste = load_einkaufsliste(self)
    if len(self.command) == 1:
        return_einkaufsliste(self)
    else:
        item = ' '.join(self.command[1:]).lower().capitalize()
        if item in einkaufsliste:
            self.sender.sendMessage(f"<b>{item}</b> ist bereits auf der Einkaufsliste",
                                    parse_mode='html')
        else:
            einkaufsliste.append(item)
            telepot.Bot(API_KEY).sendMessage(GROUP_ID, f"{msg['from']['first_name']} hat <b>{item}</b> auf die "
                                                       f"Einkaufsliste gesetzt \U0001F4C4\U0001F6D2", parse_mode='html')
            dump_einkaufsliste(self, einkaufsliste)


def return_einkaufsliste(self):
    """
    send user the list of current items on shopping list
    """
    einkaufsliste = load_einkaufsliste(self)
    if len(einkaufsliste) > 0:
        liste_pretty = "\U0001F4C4\U0001F6D2 <b>Einkaufsliste</b> \U0001F6D2\U0001F4C4\n\n"
        for item in einkaufsliste:
            liste_pretty += ("\U0001F538" + item + "\n")
        self.sender.sendMessage(liste_pretty, parse_mode='html')
    else:
        self.sender.sendMessage("Die Einkaufsliste ist leer. Hinzufügen eines Artikels "
                                "mit <b>/einkaufen X</b>", parse_mode='html')


def eingekauft(self, msg):
    """
    remove given items from the shopping list
    """
    einkaufsliste = load_einkaufsliste(self)
    if self.eingekauft_flag1:
        item = " ".join(self.command)
        if item == "Alle":
            einkaufsliste = []
            dump_einkaufsliste(self, einkaufsliste)
            self.sender.sendMessage("Einkaufsliste wurde geleert!", reply_markup=ReplyKeyboardRemove())
            telepot.Bot(API_KEY).sendMessage(GROUP_ID, f"{msg['from']['first_name']} hat die Einkaufsliste geleert "
                                                       f"\U0001F4DC\u2705", parse_mode='html')
        elif item == "Abbrechen":
            self.sender.sendMessage("Vorgang abgebrochen.", reply_markup=ReplyKeyboardRemove())
        else:
            try:
                einkaufsliste.remove(item)
                dump_einkaufsliste(self, einkaufsliste)
                self.sender.sendMessage(f"{item} wurde von der Einkaufsliste entfernt!",
                                        reply_markup=ReplyKeyboardRemove())
                telepot.Bot(API_KEY).sendMessage(GROUP_ID, f"{msg['from']['first_name']} hat <b>{item}</b> von der "
                                                           f"Einkaufsliste entfernt \U0001F4DC\u2705",
                                                 parse_mode='html')
            except ValueError:
                {}
        self.eingekauft_flag1 = False
    else:
        if len(einkaufsliste) == 0:
            self.sender.sendMessage("Einkaufsliste ist leer!")
            return
        self.eingekauft_flag1 = True
        self.sender.sendMessage("Welchen Artikel möchtest du entfernen?",
                                reply_markup=create_eingekauft_keyboard(einkaufsliste))


def load_einkaufsliste(self):
    """
    load einkaufsliste from JSON file
    """
    einkaufsliste = []
    try:
        with open("../../data/einkaufsliste.json", "r") as f:
            data = json.load(f)
            for item in data['liste']:
                einkaufsliste.append(item)
    except FileNotFoundError:
        logging.error("Error - File Not Found, #3003")
        self.sender.sendMessage("Fehler #3003")
        return
    return einkaufsliste


def dump_einkaufsliste(self, einkaufsliste):
    """
    write einkaufsliste to JSON file
    """
    data = {"liste": []}
    for i in range(len(einkaufsliste)):
        data["liste"].append(einkaufsliste[i])
    try:
        with open("../../data/einkaufsliste.json", "w") as f:
            json.dump(data, f, indent=2)
    except FileNotFoundError as exception:
        logging.error("Error - File Not Found, #3002")
        self.sender.sendMessage("Fehler #3002")


def impersonate(self, msg):
    """
    send message through bot account
    """
    if self.chatid in ADMIN_IDS:
        telepot.Bot(API_KEY).sendMessage(GROUP_ID, msg['text'][12:])


def help_commands(self):
    """
    show user available commands
    """
    if self.chatid in LEGIT_IDS:
        self.sender.sendMessage(f"\u2753<b>Verfügbare Befehle</b>\u2753\n\n"
                                f"<b>/help</b> - Hilfe-Dialog anzeigen\n\n"
                                f"<b>/einkaufen</b> - Einkaufsliste einsehen und Artikel hinzufügen\n\n"
                                f"<b>/einkaufen [Artikel]</b> - Artikel auf die Einkaufsliste setzen\n\n"
                                f"<b>/eingekauft [Artikel]</b> - Artikel von der Einkaufsliste löschen\n\n"
                                f"<b>/eingekauft all</b> - alle Artikel von der Einkaufsliste löschen\n\n"
                                f"<b>/geld</b> - Finanzeintrag erstellen, Kontostände abrufen, Überweisung tätigen\n\n"
                                f"<b>/bahn</b> - nach aktuellen Zugverbindungen im RMV-Gebiet suchen\n\n"
                                f"<b>/wetter</b> - Wettervorhersage für beliebigen Ort in Deutschland abrufen\n\n"
                                f"<b>/mensa</b> - zeige heutigen Mensa-Speiseplan. Unterstützt alle Mensen, deren "
                                f"Speiseplan über OpenMensa verfügbar ist\n\n"
                                f"<b>/putzplan</b> - Putzplan anzeigen\n\n"
                                f"Verfügbare Aufgaben: <b>muell | müll, glas, bad, kueche | küche, saugen, handtuecher"
                                f" | handtücher, duschvorhang</b>\n\n"
                                f"<b>/[Aufgabe]</b> - anzeigen, wer gerade mit einer Aufgabe dran ist + Fälligkeit\n\n"
                                f"<b>/[Aufgabe] erledigt</b> - eine Aufgabe abhaken\n\n"
                                f"<b>/[Aufgabe] intervall</b> - Intervall einer Aufgabe anzeigen\n\n"
                                f"<b>/[Aufgabe] vergangen</b> - Vergangene Tage einer Aufgabe anzeigen\n\n"
                                f"<b>/[Aufgabe] intervall [Tage]</b> - Intervall einer Aufgabe setzen\n\n"
                                f"<b>/[Aufgabe] vergangen [Tage]</b> - Vergangene Tage einer Aufgabe setzen\n\n"
                                f"<b>/putzplan</b> - Putzplan anzeigen\n\n"
                                f"<b>/loc</b> - Anzahl Codezeilen des WG Infoboard Projekts anzeigen\n\n"
                                f"<b>/reload</b> - Cache leeren und WG-Infoboard neu laden\n\n\n"
                                f"<b>Admin-Befehle:</b>\n\n"
                                f"<b>/reboot</b> - WG-Infoboard-Server neustarten\n\n"
                                f"<b>/impersonate</b> - als Bot schreiben\n\n"
                                , parse_mode="html")
    else:
        self.sender.sendMessage(f"\u2753<b>Öffentlich verfügbare Befehle</b>\u2753\n\n"
                                f"<b>/help</b> - zeige diesen Dialog\n\n"
                                f"<b>/bahn</b> - suche nach aktuellen Zugverbindungen im RMV-Gebiet (Beta)\n\n"
                                f"<b>/wetter</b> - Wettervorhersage für beliebigen Ort in Deutschland abrufen\n\n"
                                f"<b>/mensa</b> - zeige Speiseplan von versch. Mensen\n\n"
                                , parse_mode="html")


def reboot(self, msg):
    """
    reboot machine remotely via Telegram
    """
    if str(msg['from']['id']) in ADMIN_IDS:
        if platform.system() == "Linux":
            self.sender.sendMessage("Rebooting...")
            subprocess.run(["sudo", "reboot"])
        else:
            self.sender.sendMessage("Platform does not seem to be Linux.")
    else:
        self.sender.sendMessage("You do not have permission to use this command.")


def reload(self):
    """
    clear chromium cache and reload kiosk.sh service remotely via Telegram
    """
    if platform.system() == "Linux":
        self.sender.sendMessage("\U0001F504Reloading service kiosk.sh\U0001F504")
        subprocess.run(["sudo", "rm", "-rf", "/home/pi/.cache/chromium"])
        subprocess.run(["sudo", "service", "kiosk.sh", "restart"])
    else:
        self.sender.sendMessage("Platform does not seem to be Linux, reloading not possible.")
