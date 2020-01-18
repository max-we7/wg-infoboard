from putzplan import muell, glas, bad, kueche, saugen, handtuecher, duschvorhang
import json


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
    bot.sendMessage(msg['chat']['id'], f"{msg['text'].lower()[8:]} ist ein kleiner Hurensohn")


def help_commands(bot, msg):
    bot.sendMessage(msg['chat']['id'], f"Available commands:\n/help\n/einkaufen\n/eingekauft\n/insult")


def loc(bot, msg):
    # TODO: run cloc on Linux to count LOC
    bot.sendMessage(msg['chat']['id'], f"Lines of Code (as per 17.01.2020): 705")
