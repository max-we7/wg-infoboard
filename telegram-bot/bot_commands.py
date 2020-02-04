from putzplan import muell, glas, bad, kueche, saugen, handtuecher, duschvorhang
import json
from insults import insults
import random
import platform
import subprocess
from config import ADMIN_IDS
import telepot


def choose_command(bot, msg):
    if msg['text'].lower().startswith("/einkaufen"):
        einkaufen(bot, msg)
    if msg['text'].lower().startswith("/eingekauft"):
        eingekauft(bot, msg)
    if msg['text'].lower().startswith("/insult"):
        insult(bot, msg)
    if msg['text'].lower().startswith("/help"):
        help_commands(bot, msg)
    if msg['text'].lower().startswith("/muell"):
        muell(bot, msg)
    if msg['text'].lower().startswith("/glas"):
        glas(bot, msg)
    if msg['text'].lower().startswith("/bad"):
        bad(bot, msg)
    if msg['text'].lower().startswith("/kueche"):
        kueche(bot, msg)
    if msg['text'].lower().startswith("/saugen"):
        saugen(bot, msg)
    if msg['text'].lower().startswith("/handtuecher"):
        handtuecher(bot, msg)
    if msg['text'].lower().startswith("/duschvorhang"):
        duschvorhang(bot, msg)
    if msg['text'].lower().startswith("/loc"):
        loc(bot, msg)
    if msg['text'].lower().startswith("/bahn"):
        bahn(bot, msg)
    if msg['text'].lower().startswith("/reboot"):
        reboot(bot, msg)
    if msg['text'].lower().startswith("/reload"):
        reload(bot, msg)


def einkaufen(bot, msg):
    einkaufsliste = load_einkaufsliste()
    if len(msg['text']) == 10:
        return_einkaufsliste(bot, msg)
    else:
        item = msg['text'].lower()[11:].capitalize()
        if item in einkaufsliste:
            bot.sendMessage(msg['chat']['id'], f"<b>{item}</b> ist bereits auf der Einkaufsliste",
                            parse_mode='html')
        else:
            einkaufsliste.append(item)
            bot.sendMessage(msg['chat']['id'], f"{msg['from']['first_name']} hat <b>{item}</b> auf die Einkaufsliste "
                                               f"gesetzt", parse_mode='html')
            dump_einkaufsliste(einkaufsliste)


def return_einkaufsliste(bot, msg):
    """
    sends user the list of current items on shopping list
    """
    einkaufsliste = load_einkaufsliste()
    if len(einkaufsliste) > 0:
        liste_pretty = "<b>Einkaufsliste:</b>\n"
        for item in einkaufsliste:
            liste_pretty += (item + "\n")
        bot.sendMessage(msg['chat']['id'], liste_pretty, parse_mode='html')
    else:
        bot.sendMessage(msg['chat']['id'], "Die Einkaufsliste ist leer. Hinzufügen eines Artikels "
                                           "mit <b>/einkaufen X</b>", parse_mode='html')


def eingekauft(bot, msg):
    """
    removes given items from the shopping list
    """
    einkaufsliste = load_einkaufsliste()
    if len(msg['text']) == 11:
        bot.sendMessage(msg['chat']['id'], "Löschen eines Artikels von der Einkaufsliste mit <b>/eingekauft X"
                                           "</b>", parse_mode='html')
    else:
        item = msg['text'].lower()[12:].capitalize()
        if item not in einkaufsliste:
            if item == "All":
                einkaufsliste = []
                dump_einkaufsliste(einkaufsliste)
                bot.sendMessage(msg['chat']['id'], "Einkaufsliste wurde geleert")
            else:
                bot.sendMessage(msg['chat']['id'], f"<b>{item}</b> befindet sich nicht auf der Einkaufsliste",
                                parse_mode='html')
        else:
            einkaufsliste.remove(item)
            bot.sendMessage(msg['chat']['id'], f"{msg['from']['first_name']} hat <b>{item}</b> von der Einkaufsliste "
                                               f"entfernt", parse_mode='html')
            dump_einkaufsliste(einkaufsliste)


def bahn(bot, msg):
    """
    returns current train times to user
    TODO: test
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
    bot.sendMessage(msg['chat']['id'], message)
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
        lines_raw = [line for line in entry['line']] if len(entry['line']) == 2 else entry['line']
        lines = ", ".join(lines_raw)
        message += f"{entry['ab']}  {entry['an']}  {lines}\n"
    bot.sendMessage(msg['chat']['id'], message)


def load_einkaufsliste():
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
        print("Error - File Not Found")
    return einkaufsliste


def dump_einkaufsliste(einkaufsliste):
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
        print("Error - File Not Found")


def insult(bot, msg):
    """
    insults given person, usage "/insult person"
    """
    random_insult = random.choice(insults)
    bot.sendMessage(msg['chat']['id'], f"{msg['text'][8:]} du {random_insult}")


def help_commands(bot, msg):
    """
    TODO: update list of available commands
    """
    bot.sendMessage(msg['chat']['id'], f"Verfügbare Befehle:\n"
                                       f"<b>/einkaufen</b> - zeige Einkaufsliste an\n"
                                       f"<b>/einkaufen X</b> - setze X auf die Einkaufsliste\n"
                                       f"<b>/eingekauft X</b> - lösche X von der Einkaufsliste\n"
                                       f"<b>/eingekauft all</b> - lösche alle Artikel von der Einkaufsliste\n"
                                       f"<b>/bahn</b> - zeige aktuelle Zugverbindungen\n"
                                       f"<b>/muell, /glas, /bad, /kueche, /saugen, /handtuecher, /duschvorhang</b> - "
                                       f"abhaken mit 'erledigt', Intervall (in Tagen) anzeigen mit "
                                       f"'intervall', Intervall setzen mit 'intervall X', vergangene Tage "
                                       f"anzeigen mit 'vergangen', vergangene Tage setzen mit 'vergangen X'\n"
                                       f"<b>/loc</b> - zeige Anzahl Codezeilen des WG Infoboard Projekts\n"
                                       f"<b>/insult X</b> - Beleidige X mit zufälliger Beleidigung ;)"
                    , parse_mode="html")


def loc(bot, msg):
    """
    returns current Lines of Code of the WG-Infoboard project
    """
    try:
        with open("../data/loc.json", "r") as f:
            data = json.load(f)
            bot.sendMessage(msg['chat']['id'], f"Lines of Code: {data['header']['n_lines']}")
    except FileNotFoundError:
        print("Error - File Not Found")


def reboot(bot, msg):
    """
    reboot machine remotely via Telegram
    """
    if msg['from']['id'] in ADMIN_IDS:
        if platform.system() == "Linux":
            subprocess.run(["sudo", "reboot"])
        else:
            bot.sendMessage(msg['chat']['id'], "Platform does not seem to be Linux.")
    else:
        bot.sendMessage(msg['chat']['id'], "You do not have permission to use this command.")


def reload(bot, msg):
    """
    reload kiosk.sh service remotely via Telegram
    """
    if msg['from']['id'] in ADMIN_IDS:
        if platform.system() == "Linux":
            subprocess.run(["sudo", "service", "kiosk.sh", "restart"])
        else:
            bot.sendMessage(msg['chat']['id'], "Platform does not seem to be Linux.")
    else:
        bot.sendMessage(msg['chat']['id'], "You do not have permission to use this command.")
