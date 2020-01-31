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
        # TODO: test
        if len(msg['text']) == 14:
            bot.sendMessage(msg['chat']['id'], f"Intervall der Aufgabe Bad putzen ist aktuell auf <b>"
                                               f"{putzplan['bad']['intervall_tage']}</b> Tage gesetzt.",
                            parse_mode="html")
        else:
            try:
                days = int(msg['text'].lower()[14:])
                putzplan["bad"]["intervall_tage"] = days
                bot.sendMessage(msg['chat']['id'], f"Intervall der Aufgabe Bad putzen wurde auf <b>"
                                                   f"{days}</b> Tage gesetzt.",
                                parse_mode="html")
            except ValueError:
                bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Intervall setzen mit "/bad intervall X".')
    elif msg['text'].lower()[5:14] == "vergangen":
        # TODO: test
        if len(msg['text']) == 14:
            bot.sendMessage(msg['chat']['id'], f"Vergangene Tage der Aufgabe Bad putzen sind aktuell auf <b>"
                                               f"{putzplan['bad']['tage_vergangen']}</b> Tage gesetzt.",
                            parse_mode="html")
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
        # TODO: test Intervallabfrage
        if len(msg['text']) == 16:
            bot.sendMessage(msg['chat']['id'], f"Intervall der Aufgabe Küche putzen ist aktuell auf <b>"
                                               f"{putzplan['kueche']['intervall_tage']}</b> Tage gesetzt.",
                            parse_mode="html")
        else:
            try:
                days = int(msg['text'].lower()[17:])
                putzplan["kueche"]["intervall_tage"] = days
                bot.sendMessage(msg['chat']['id'], f"Intervall der Aufgabe Küche putzen wurde auf <b>"
                                                   f"{days}</b> Tage gesetzt.",
                                parse_mode="html")
            except ValueError:
                bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Intervall setzen mit "/kueche intervall X".')
    elif msg['text'].lower()[8:17] == "vergangen":
        # TODO: test Abfrage
        if len(msg['text']) == 16:
            bot.sendMessage(msg['chat']['id'], f"Vergangene Tage der Aufgabe Küche putzen sind aktuell auf <b>"
                                               f"{putzplan['kueche']['tage_vergangen']}</b> Tage gesetzt.",
                            parse_mode="html")
        else:
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
        # TODO: test Intervallabfrage
        if len(msg['text']) == 16:
            bot.sendMessage(msg['chat']['id'], f"Intervall der Aufgabe Staubsaugen ist aktuell auf <b>"
                                               f"{putzplan['saugen']['intervall_tage']}</b> Tage gesetzt.",
                            parse_mode="html")
        else:
            try:
                days = int(msg['text'].lower()[17:])
                putzplan["saugen"]["intervall_tage"] = days
                bot.sendMessage(msg['chat']['id'], f"Intervall der Aufgabe Staubsaugen wurde auf <b>"
                                                   f"{days}</b> Tage gesetzt.",
                                parse_mode="html")
            except ValueError:
                bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Intervall setzen mit "/saugen intervall X".')
    elif msg['text'].lower()[8:17] == "vergangen":
        # TODO: test Abfrage
        if len(msg['text']) == 16:
            bot.sendMessage(msg['chat']['id'], f"Vergangene Tage der Aufgabe Staubsaugen ist aktuell auf <b>"
                                               f"{putzplan['saugen']['tage_vergangen']}</b> Tage gesetzt.",
                            parse_mode="html")
        else:
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
    putzplan = load_putzplan()
    if msg['text'].lower()[13:] == "erledigt":
        index = putzplan["handtuecher"]["reihenfolge"].index(putzplan["handtuecher"]["dran"])
        putzplan["handtuecher"]["dran"] = putzplan["handtuecher"]["reihenfolge"][(index + 1) % 4]
        putzplan["handtuecher"]["tage_vergangen"] = 0
        bot.sendMessage(msg['chat']['id'], f"Handtücher waschen wurde erledigt. <b>{putzplan['handtuecher']['dran']}"
                                           f"</b> ist als nächster dran.", parse_mode="html")
    elif len(msg['text']) == 7:
        bot.sendMessage(msg['chat']['id'], f"<b>{putzplan['handtuecher']['dran']}</b> ist aktuell mit Handtücher "
                                           f"waschen dran.", parse_mode="html")
    elif msg['text'].lower()[13:22] == "intervall":
        # TODO: test Intervallabfrage
        if len(msg['text']) == 21:
            bot.sendMessage(msg['chat']['id'], f"Intervall der Aufgabe Handtücher waschen ist aktuell auf <b>"
                                               f"{putzplan['handtuecher']['intervall_tage']}</b> Tage gesetzt.",
                            parse_mode="html")
        else:
            try:
                days = int(msg['text'].lower()[22:])
                putzplan["handtuecher"]["intervall_tage"] = days
                bot.sendMessage(msg['chat']['id'], f"Intervall der Aufgabe Handtücher waschen wurde auf <b>"
                                                   f"{days}</b> Tage gesetzt.",
                                parse_mode="html")
            except ValueError:
                bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Intervall setzen mit "/handtuecher '
                                                   'intervall X".')
    elif msg['text'].lower()[13:22] == "vergangen":
        # TODO: test Abfrage
        if len(msg['text']) == 21:
            bot.sendMessage(msg['chat']['id'], f"Vergangene Tage der Aufgabe Handtücher waschen ist aktuell auf <b>"
                                               f"{putzplan['handtuecher']['tage_vergangen']}</b> Tage gesetzt.",
                            parse_mode="html")
        else:
            try:
                days = int(msg['text'].lower()[22:])
                putzplan["handtuecher"]["tage_vergangen"] = days
                bot.sendMessage(msg['chat']['id'], f"Vergangene Tage der Aufgabe Handtücher waschen wurden auf <b>"
                                                   f"{putzplan['handtuecher']['tage_vergangen']}</b> Tage gesetzt.",
                                parse_mode="html")
            except ValueError:
                bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Vergangene Tage setzen mit "/handtuecher '
                                                   'vergangen X".')
    else:
        bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Wenn du die Aufgabe Handtücher waschen erledigt '
                                           'hast, bestätige das bitte mit dem Befehl "/handtuecher erledigt".')
    dump_putzplan(putzplan)


def duschvorhang(bot, msg):
    putzplan = load_putzplan()
    if msg['text'].lower()[14:] == "erledigt":
        index = putzplan["duschvorhang"]["reihenfolge"].index(putzplan["duschvorhang"]["dran"])
        putzplan["duschvorhang"]["dran"] = putzplan["duschvorhang"]["reihenfolge"][(index + 1) % 4]
        putzplan["duschvorhang"]["tage_vergangen"] = 0
        bot.sendMessage(msg['chat']['id'], f"Duschvorhänge waschen wurde erledigt. <b>"
                                           f"{putzplan['duschvorhang']['dran']}</b> ist als nächster dran.",
                        parse_mode="html")
    elif len(msg['text']) == 7:
        bot.sendMessage(msg['chat']['id'], f"<b>{putzplan['duschvorhang']['dran']}</b> ist aktuell mit Duschvorhänge "
                                           f"waschen dran.", parse_mode="html")
    elif msg['text'].lower()[14:23] == "intervall":
        # TODO: test Intervallabfrage
        if len(msg['text']) == 22:
            bot.sendMessage(msg['chat']['id'], f"Intervall der Aufgabe Duschvorhänge waschen ist aktuell auf <b>"
                                               f"{putzplan['duschvorhang']['intervall_tage']}</b> Tage gesetzt.",
                            parse_mode="html")
        else:
            try:
                days = int(msg['text'].lower()[23:])
                putzplan["duschvorhang"]["intervall_tage"] = days
                bot.sendMessage(msg['chat']['id'], f"Intervall der Aufgabe Duschvorhänge waschen wurde auf <b>"
                                                   f"{days}</b> Tage gesetzt.",
                                parse_mode="html")
            except ValueError:
                bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Intervall setzen mit "/duschvorhang '
                                                   'intervall X".')
    elif msg['text'].lower()[14:23] == "vergangen":
        # TODO: implement Abfrage
        if len(msg['text']) == 22:
            bot.sendMessage(msg['chat']['id'], f"Vergangene Tage der Aufgabe Duschvorhänge waschen ist aktuell auf <b>"
                                               f"{putzplan['duschvorhang']['tage_vergangen']}</b> Tage gesetzt.",
                            parse_mode="html")
        else:
            try:
                days = int(msg['text'].lower()[23:])
                putzplan["duschvorhang"]["tage_vergangen"] = days
                bot.sendMessage(msg['chat']['id'], f"Vergangene Tage der Aufgabe Duschvorhang waschen wurden auf <b>"
                                                   f"{putzplan['duschvorhang']['tage_vergangen']}</b> Tage gesetzt.",
                                parse_mode="html")
            except ValueError:
                bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Vergangene Tage setzen mit "/duschvorhang '
                                                   'vergangen X".')
    else:
        bot.sendMessage(msg['chat']['id'], 'Unbekannter Parameter. Wenn du die Aufgabe Duschvorhänge waschen erledigt '
                                           'hast, bestätige das bitte mit dem Befehl "/duschvorhang erledigt".')
    dump_putzplan(putzplan)


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
