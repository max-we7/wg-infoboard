import json
import logging


def load_putzplan():
    try:
        with open("../data/putzplan.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error - File Not Found")
    return data


def dump_putzplan(plan):
    try:
        with open("../data/putzplan.json", "w") as f:
            json.dump(plan, f, indent=4)
    except FileNotFoundError:
        print("Error - File Not Found")


def muell(bot, msg):
    putzplan = load_putzplan()
    if msg['text'].lower()[7:] == "erledigt":
        index = putzplan["muell"]["reihenfolge"].index(putzplan["muell"]["dran"])
        putzplan["muell"]["dran"] = putzplan["muell"]["reihenfolge"][(index + 1) % 4]
        bot.sendMessage(msg['chat']['id'], f"Müll wurde rausgebracht. <b>{putzplan['muell']['dran']}</b> ist als "
                                           f"nächster dran.", parse_mode="html")
        dump_putzplan(putzplan)
    elif len(msg['text']) == 6:
        bot.sendMessage(msg['chat']['id'], f"<b>{putzplan['muell']['dran']}</b> ist aktuell mit Müll rausbringen "
                                           f"dran.", parse_mode="html")
    else:
        bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Wenn du den Müll rausgebracht hast, bestätige '
                                           'das bitte mit dem Befehl "/muell erledigt".')


def glas(bot, msg):
    putzplan = load_putzplan()
    if msg['text'].lower()[6:] == "erledigt":
        index = putzplan["glas"]["reihenfolge"].index(putzplan["glas"]["dran"])
        putzplan["glas"]["dran"] = putzplan["glas"]["reihenfolge"][(index + 1) % 4]
        bot.sendMessage(msg['chat']['id'], f"Glas wurde weggebracht. <b>{putzplan['glas']['dran']}</b> ist als "
                                           f"nächster dran.", parse_mode="html")
        dump_putzplan(putzplan)
    elif len(msg['text']) == 5:
        bot.sendMessage(msg['chat']['id'], f"<b>{putzplan['glas']['dran']}</b> ist aktuell mit Glas wegbringen "
                                           f"dran.", parse_mode="html")
    else:
        bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Wenn du Glas weggebracht hast, bestätige '
                                           'das bitte mit dem Befehl "/glas erledigt".')


def bad(bot, msg):
    putzplan = load_putzplan()
    if msg['text'].lower()[5:] == "erledigt":
        index = putzplan["bad"]["reihenfolge"].index(putzplan["bad"]["dran"])
        putzplan["bad"]["dran"] = putzplan["bad"]["reihenfolge"][(index + 1) % 4]
        putzplan["bad"]["tage_vergangen"] = 0
        bot.sendMessage(msg['chat']['id'], f"Bäder wurden geputzt. <b>{putzplan['bad']['dran']}</b> ist als "
                                           f"nächster dran.", parse_mode="html")
    elif len(msg['text']) == 4:
        bot.sendMessage(msg['chat']['id'], f"<b>{putzplan['bad']['dran']}</b> ist aktuell mit Bäder putzen "
                                           f"dran.", parse_mode="html")
    elif msg['text'].lower()[5:14] == "intervall":
        try:
            days = int(msg['text'].lower()[14:])
            putzplan["bad"]["intervall_tage"] = days
            bot.sendMessage(msg['chat']['id'], f"Intervall der Aufgabe Bad putzen wurde auf <b>"
                                               f"{days}</b> Tage gesetzt.",
                            parse_mode="html")
        except ValueError:
            bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Intervall setzen mit "/bad intervall X".')
    elif msg['text'].lower()[5:14] == "vergangen":
        try:
            days = int(msg['text'].lower()[14:])
            putzplan["bad"]["tage_vergangen"] = days
            bot.sendMessage(msg['chat']['id'], f"Vergangene Tage der Aufgabe Bad putzen wurden auf <b>"
                                               f"{putzplan['bad']['tage_vergangen']}</b> Tage gesetzt.",
                            parse_mode="html")
        except ValueError:
            bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Vergangene Tage setzen mit "/bad vergangen X".')
    else:
        bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Wenn du die Bäder geputzt hast, bestätige '
                                           'das bitte mit dem Befehl "/bad erledigt".')
    dump_putzplan(putzplan)


def kueche(bot, msg):
    putzplan = load_putzplan()
    if msg['text'].lower()[8:] == "erledigt":
        index = putzplan["kueche"]["reihenfolge"].index(putzplan["kueche"]["dran"])
        putzplan["kueche"]["dran"] = putzplan["kueche"]["reihenfolge"][(index + 1) % 4]
        putzplan["kueche"]["tage_vergangen"] = 0
        bot.sendMessage(msg['chat']['id'], f"Küche wurde geputzt. <b>{putzplan['kueche']['dran']}</b> ist als "
                                           f"nächster dran.", parse_mode="html")
    elif len(msg['text']) == 7:
        bot.sendMessage(msg['chat']['id'], f"<b>{putzplan['kueche']['dran']}</b> ist aktuell mit Küche putzen "
                                           f"dran.", parse_mode="html")
    elif msg['text'].lower()[8:17] == "intervall":
        try:
            days = int(msg['text'].lower()[17:])
            putzplan["kueche"]["intervall_tage"] = days
            bot.sendMessage(msg['chat']['id'], f"Intervall der Aufgabe Küche putzen wurde auf <b>"
                                               f"{days}</b> Tage gesetzt.",
                            parse_mode="html")
        except ValueError:
            bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Intervall setzen mit "/kueche intervall X".')
    elif msg['text'].lower()[8:17] == "vergangen":
        try:
            days = int(msg['text'].lower()[17:])
            putzplan["kueche"]["tage_vergangen"] = days
            bot.sendMessage(msg['chat']['id'], f"Vergangene Tage der Aufgabe Bad putzen wurden auf <b>"
                                               f"{putzplan['kueche']['tage_vergangen']}</b> Tage gesetzt.",
                            parse_mode="html")
        except ValueError:
            bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Vergangene Tage setzen mit "/kueche '
                                               'vergangen X".')
    else:
        bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Wenn du die Küche geputzt hast, bestätige '
                                           'das bitte mit dem Befehl "/kueche erledigt".')
    dump_putzplan(putzplan)


def saugen(bot, msg):
    # TODO: implement
    putzplan = load_putzplan()
    if msg['text'].lower()[8:] == "erledigt":
        index = putzplan["saugen"]["reihenfolge"].index(putzplan["saugen"]["dran"])
        putzplan["saugen"]["dran"] = putzplan["saugen"]["reihenfolge"][(index + 1) % 4]
        putzplan["saugen"]["tage_vergangen"] = 0
        bot.sendMessage(msg['chat']['id'], f"Staubsaugen wurde erledigt. <b>{putzplan['saugen']['dran']}</b> ist als "
                                           f"nächster dran.", parse_mode="html")
    elif len(msg['text']) == 7:
        bot.sendMessage(msg['chat']['id'], f"<b>{putzplan['saugen']['dran']}</b> ist aktuell mit Staubsaugen "
                                           f"dran.", parse_mode="html")
    elif msg['text'].lower()[8:17] == "intervall":
        try:
            days = int(msg['text'].lower()[17:])
            putzplan["saugen"]["intervall_tage"] = days
            bot.sendMessage(msg['chat']['id'], f"Intervall der Aufgabe Staubsaugen wurde auf <b>"
                                               f"{days}</b> Tage gesetzt.",
                            parse_mode="html")
        except ValueError:
            bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Intervall setzen mit "/saugen intervall X".')
    elif msg['text'].lower()[8:17] == "vergangen":
        try:
            days = int(msg['text'].lower()[17:])
            putzplan["saugen"]["tage_vergangen"] = days
            bot.sendMessage(msg['chat']['id'], f"Vergangene Tage der Aufgabe Staubsaugen wurden auf <b>"
                                               f"{putzplan['saugen']['tage_vergangen']}</b> Tage gesetzt.",
                            parse_mode="html")
        except ValueError:
            bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Vergangene Tage setzen mit "/saugen '
                                               'vergangen X".')
    else:
        bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Wenn du die Aufgabe Staubsaugen erledigt hast, '
                                           'bestätige das bitte mit dem Befehl "/saugen erledigt".')
    dump_putzplan(putzplan)


def handtuecher(bot, msg):
    # TODO: implement
    return 0


def duschvorhang(bot, msg):
    # TODO: implement
    return 0


def update_putzplan():
    putzplan = load_putzplan()
    # noinspection PyBroadException
    try:
        putzplan['bad']['tage_vergangen'] += 1
        putzplan['kueche']['tage_vergangen'] += 1
        putzplan['saugen']['tage_vergangen'] += 1
        putzplan['handtuecher']['tage_vergangen'] += 1
        putzplan['duschvorhang']['tage_vergangen'] += 1
        dump_putzplan(putzplan)
    except Exception:
        logging.error("Error incrementing 'tage_vergangen'")
