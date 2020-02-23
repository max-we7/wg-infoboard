import random
import json
from insults import insults
import platform
import subprocess
from config import ADMIN_IDS, LEGIT_IDS
import logging


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
            self.sender.sendMessage(f"{msg['from']['first_name']} hat <b>{item}</b> auf die Einkaufsliste "
                                    f"gesetzt", parse_mode='html')
            dump_einkaufsliste(self, einkaufsliste)


def return_einkaufsliste(self):
    """
    send user the list of current items on shopping list
    """
    einkaufsliste = load_einkaufsliste(self)
    if len(einkaufsliste) > 0:
        liste_pretty = "<b>Einkaufsliste:</b>\n"
        for item in einkaufsliste:
            liste_pretty += (item + "\n")
        self.sender.sendMessage(liste_pretty, parse_mode='html')
    else:
        self.sender.sendMessage("Die Einkaufsliste ist leer. Hinzufügen eines Artikels "
                                "mit <b>/einkaufen X</b>", parse_mode='html')


def eingekauft(self, msg):
    """
    remove given items from the shopping list
    """
    einkaufsliste = load_einkaufsliste(self)
    if len(self.command) == 1:
        self.sender.sendMessage("Löschen eines Artikels von der Einkaufsliste mit <b>/eingekauft X"
                                "</b>", parse_mode='html')
    else:
        item = ' '.join(self.command[1:]).lower().capitalize()
        if item not in einkaufsliste:
            if item == "All":
                einkaufsliste = []
                dump_einkaufsliste(self, einkaufsliste)
                self.sender.sendMessage("Einkaufsliste wurde geleert")
            else:
                self.sender.sendMessage(f"<b>{item}</b> befindet sich nicht auf der Einkaufsliste",
                                        parse_mode='html')
        else:
            einkaufsliste.remove(item)
            self.sender.sendMessage(f"{msg['from']['first_name']} hat <b>{item}</b> von der Einkaufsliste "
                                    f"entfernt", parse_mode='html')
            dump_einkaufsliste(self, einkaufsliste)


def bahn(self):
    """
    returns current train times to user
    """
    train_times = []
    try:
        with open("../data/timetable.json", "r") as f:
            data = json.load(f)
            for item in data['trips']:
                train_times.append(item)
    except FileNotFoundError:
        print("Error - File Not Found")
    message = "Griesheim --> DA:\n"
    for entry in train_times:
        if type(entry['line']) == type(str()):
            lines = entry['line']
        else:
            lines_raw = [line for line in entry['line']]
            lines = ", ".join(lines_raw)
        message += f"{entry['ab']}  {entry['an']}  {lines}\n"
    self.sender.sendMessage(message)
    regio_times = []
    try:
        with open("../data/timetable_regio.json", "r") as f:
            data = json.load(f)
            for item in data['trips']:
                regio_times.append(item)
    except FileNotFoundError:
        print("Error - File Not Found")
    message = "DA --> Wiesbaden:\n"
    for entry in regio_times:
        if type(entry['line']) == type(str()):
            lines = entry['line']
        else:
            lines_raw = [line for line in entry['line'] if line != ""]
            lines = ", ".join(lines_raw)
        message += f"{entry['ab']}  {entry['an']}  {lines}\n"
    self.sender.sendMessage(message)


def load_einkaufsliste(self):
    """
    load einkaufsliste from JSON file
    """
    einkaufsliste = []
    try:
        with open("../data/einkaufsliste.json", "r") as f:
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
        with open("../data/einkaufsliste.json", "w") as f:
            json.dump(data, f, indent=2)
    except FileNotFoundError as exception:
        logging.error("Error - File Not Found, #3002")
        self.sender.sendMessage("Fehler #3002")


def insult(self, msg):
    """
    insults given person, usage "/insult person"
    """
    random_insult = random.choice(insults)
    self.sender.sendMessage(f"{msg['text'][8:]} du {random_insult}")


def help_commands(self):
    """
    show user available commands
    """
    if self.chatid in LEGIT_IDS:
        self.sender.sendMessage(f"Verfügbare Befehle:\n\n"
                                f"<b>/help</b> - zeige diesen Dialog\n\n"
                                f"<b>/einkaufen</b> - Einkaufsliste einsehen und Artikel hinzufügen\n\n"
                                f"<b>/einkaufen [Artikel]</b> - setze Artikel auf die Einkaufsliste\n\n"
                                f"<b>/eingekauft [Artikel]</b> - lösche Artikel von der Einkaufsliste\n\n"
                                f"<b>/eingekauft all</b> - lösche alle Artikel von der Einkaufsliste\n\n"
                                f"<b>/geld</b> - Finanzeintrag erstellen, Kontostände abrufen, Überweisung tätigen\n\n"
                                f"<b>/bahn</b> - suche nach aktuellen Zugverbindungen im RMV-Gebiet (Beta)\n\n"
                                f"<b>/mensa</b> - zeige heutigen Speiseplan, TU Stadtmitte\n\n"
                                f"<b>/mensa liwi</b> - zeige heutigen Speiseplan, TU Lichtwiese\n\n"
                                f"<b>/[Aufgabe]</b> - zeige, wer gerade mit einer Aufgabe dran ist, + Fälligkeit\n\n"
                                f"<b>/[Aufgabe] erledigt</b> - eine Aufgabe abhaken\n\n"
                                f"<b>/[Aufgabe] intervall</b> - Intervall einer Aufgabe anzeigen\n\n"
                                f"<b>/[Aufgabe] vergangen</b> - Vergangene Tage einer Aufgabe anzeigen\n\n"
                                f"<b>/[Aufgabe] intervall [Tage]</b> - Intervall einer Aufgabe setzen\n\n"
                                f"<b>/[Aufgabe] vergangen [Tage]</b> - Vergangene Tage einer Aufgabe setzen\n\n"
                                f"<b>/loc</b> - Anzahl Codezeilen des WG Infoboard Projekts anzeigen\n\n"
                                f"<b>/insult [Person]</b> - Beleidige Person mit zufälliger Beleidigung ;)\n\n"
                                f"<b>/reload</b> - WG-Infoboard neu laden\n\n"
                                f"<b>/reboot</b> - WG-Infoboard-Server neustarten\n\n"
                                , parse_mode="html")
    else:
        self.sender.sendMessage(f"Öffentlich verfügbare Befehle:\n\n"
                                f"<b>/help</b> - zeige diesen Dialog\n\n"
                                f"<b>/bahn</b> - suche nach aktuellen Zugverbindungen im RMV-Gebiet (Beta)\n\n"
                                f"<b>/mensa</b> - zeige heutigen Speiseplan, TU Stadtmitte\n\n"
                                f"<b>/mensa liwi</b> - zeige heutigen Speiseplan, TU Lichtwiese\n\n"
                                , parse_mode="html")


def loc(self):
    """
    returns current Lines of Code of the WG-Infoboard project
    """
    try:
        with open("../data/loc.json", "r") as f:
            data = json.load(f)
            self.sender.sendMessage(f"Lines of Code: {data['header']['n_lines']}")
    except FileNotFoundError:
        logging.error("Error - File Not Found, #3001")
        self.sender.sendMessage("Fehler #3001")


def git_pull(self, msg):
    # TODO: implement
    """
    pull current version remotely via Telegram
    """
    # if str(msg['from']['id']) in ADMIN_IDS:
    #     if platform.system() == "Linux":
    #         message_id = bot.sendMessage(msg['chat']['id'], "Pulling Git Repository...")
    #         # os.chdir("/var/www/rmw/wg-infoboard")
    #         subprocess.Popen(["sudo", "git", "pull", "https://github.com/max-we7/wg-infoboard.git"],
    #         cwd="/var/www/rmw/wg-infoboard")
    #         bot.editMessageText(message_id, "Pulling Git Repository... Done!")
    #     else:
    #         bot.sendMessage(msg['chat']['id'], "Platform does not seem to be Linux.")
    # else:
    #     bot.sendMessage(msg['chat']['id'], "You do not have permission to use this command.")
    pass


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
    reload kiosk.sh service remotely via Telegram
    """
    if platform.system() == "Linux":
        self.sender.sendMessage("Reloading service kiosk.sh...")
        subprocess.run(["sudo", "service", "kiosk.sh", "restart"])
    else:
        self.sender.sendMessage("Platform does not seem to be Linux.")
