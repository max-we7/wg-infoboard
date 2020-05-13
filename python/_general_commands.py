import random
import json

import telepot
from insults import insults
import platform
import subprocess
from config import ADMIN_IDS, LEGIT_IDS, API_KEY, GROUP_ID, wg
import logging
from muddawitze import muddawitze


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
    if len(self.command) == 1:
        self.sender.sendMessage("Löschen eines Artikels von der Einkaufsliste mit <b>/eingekauft X"
                                "</b>", parse_mode='html')
    else:
        item = ' '.join(self.command[1:]).lower().capitalize()
        if item not in einkaufsliste:
            if item == "All":
                einkaufsliste = []
                dump_einkaufsliste(self, einkaufsliste)
                telepot.Bot(API_KEY).sendMessage(GROUP_ID, f"{msg['from']['first_name']} hat die Einkaufsliste geleert "
                                                           f"\U0001F4DC\u2705", parse_mode='html')
            else:
                self.sender.sendMessage(f"<b>{item}</b> befindet sich nicht auf der Einkaufsliste",
                                        parse_mode='html')
        else:
            einkaufsliste.remove(item)
            telepot.Bot(API_KEY).sendMessage(GROUP_ID, f"{msg['from']['first_name']} hat <b>{item}</b> von der "
                                                       f"Einkaufsliste entfernt \U0001F4DC\u2705", parse_mode='html')
            dump_einkaufsliste(self, einkaufsliste)


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
    self.sender.sendMessage(f"{msg['text'][8:]} du {random_insult}\U0001F595")


def impersonate(self, msg):
    """
    send message through bot account
    """
    if self.chatid in ADMIN_IDS:
        telepot.Bot(API_KEY).sendMessage(GROUP_ID, msg['text'][12:])


def deinemudda(self):
    """
    returns random deinemudda-joke
    """
    random_muddawitz = random.choice(muddawitze)
    self.sender.sendMessage(f"{random_muddawitz}\U0001F61C")


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
                                f"<b>/essen</b> - Zufälligen Essensvorschlag anzeigen\n\n"
                                f"<b>/essen liste</b> - Liste aller Essensvorschläge/Rezepte anzeigen\n\n"
                                f"<b>/essen add [X]</b> - Essen zur Essensliste hinzufügen\n\n"
                                f"<b>/essen remove [X]</b> - Essen von der Essensliste entfernen\n\n"
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
                                f"<b>/insult [Person]</b> - Beleidige Person mit zufälliger Beleidigung\n\n"
                                f"<b>/deinemudda</b> - zufälligen DeineMudda-Witz anzeigen\n\n"
                                f"<b>/reload</b> - WG-Infoboard neu laden\n\n\n"
                                f"<b>Admin-Befehle:</b>\n\n"
                                f"<b>/reboot</b> - WG-Infoboard-Server neustarten\n\n"
                                f"<b>/impersonate</b> - als Bot schreiben\n\n"
                                f"<b>/git pull</b> - Bot auf neuste Version aktualisieren"
                                , parse_mode="html")
    else:
        self.sender.sendMessage(f"\u2753<b>Öffentlich verfügbare Befehle</b>\u2753\n\n"
                                f"<b>/help</b> - zeige diesen Dialog\n\n"
                                f"<b>/bahn</b> - suche nach aktuellen Zugverbindungen im RMV-Gebiet (Beta)\n\n"
                                f"<b>/wetter</b> - Wettervorhersage für beliebigen Ort in Deutschland abrufen\n\n"
                                f"<b>/mensa</b> - zeige Speiseplan von versch. Mensen\n\n"
                                f"<b>/insult [Person]</b> - Beleidige Person mit zufälliger Beleidigung ;)\n\n"
                                , parse_mode="html")


def loc(self):
    """
    returns current Lines of Code of the WG-Infoboard project
    """
    try:
        with open("../data/loc.json", "r") as f:
            data = json.load(f)
            self.sender.sendMessage(f"Lines of Code: {data['header']['n_lines']}\u200D")
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
        self.sender.sendMessage("\U0001F504Reloading service kiosk.sh\U0001F504")
        subprocess.run(["sudo", "service", "kiosk.sh", "restart"])
    else:
        self.sender.sendMessage("Platform does not seem to be Linux.")


def essen(self):
    """
    manage recipe list
    """
    recipes = {"liste": []}
    try:
        with open("../data/recipes.json", "r") as f:
            recipes = json.load(f)
    except FileNotFoundError:
        pass
    if len(self.command) == 1:
        item = random.choice(recipes["liste"])
        self.sender.sendMessage(f"Wie wäre es mit:\n\n{item}?")
    elif self.command[1] == "liste":
        msg = "<b>Essenswünsche und Rezeptesammlung:</b>\n\n"
        for item in recipes["liste"]:
            msg += "\U0001F538" + item + "\n"
        self.sender.sendMessage(msg, parse_mode="html")
        pass
    elif self.command[1] == "add":
        item = ' '.join(self.command[2:])
        recipes["liste"].append(item)
        self.sender.sendMessage(f"Du hast <b>{item}</b> zur Essensliste hinzugefügt!", parse_mode="html")
        telepot.Bot(API_KEY).sendMessage(GROUP_ID, f"{wg[self.chatid]} hat <b>{item}</b> zur Essensliste hinzugefügt!",
                                         parse_mode="html")
    elif self.command[1] == "remove":
        pass
        # TODO: implement removal
    try:
        with open("../data/recipes.json", "w") as f:
            json.dump(recipes, f, indent=2)
    except FileNotFoundError:
        pass


