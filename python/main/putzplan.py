import json
import logging
import telepot
from config import GROUP_ID, API_KEY, ADMIN_IDS


def load_putzplan():
    """
    load putzplan from JSON file
    :return: putzplan in dictionary format
    """
    try:
        with open("../../data/putzplan.json", "r", encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error("Error - File Not Found, #4001")
        return
    return data


def dump_putzplan(plan):
    """
    dump putzplan to JSON file
    :param plan: putzplan in dictionary format
    """
    try:
        with open("../../data/putzplan.json", "w") as f:
            json.dump(plan, f, indent=4)
    except FileNotFoundError:
        logging.error("Error - File Not Found, #4002")


def chores(self):
    """
    main function to accept putzplan queries and delegate them
    """
    putzplan = load_putzplan()
    chore = self.command[0][1:]
    arg1 = self.command[1] if len(self.command) > 1 else ""
    if len(self.command) == 1:
        wer_ist_dran(self, putzplan, chore)
    elif len(self.command) == 2:
        if arg1 == "erledigt":
            aufgabe_erledigen(putzplan, chore)
        elif arg1 == "intervall":
            show_intervall(self, putzplan, chore)
        elif arg1 == "vergangen":
            show_vergangene_tage(self, putzplan, chore)
        else:
            self.sender.sendMessage(f"Ungültiger Parameter! Wenn du die Aufgabe {putzplan[chore]['bezeichnung']} "
                                    f"erledigt hast, benutze den Parameter \"erledigt\", um sie abzuhaken.")
    elif len(self.command) == 3:
        if arg1 == "intervall":
            set_intervall(self, putzplan, chore)
        elif arg1 == "vergangen":
            set_vergangene_tage(self, putzplan, chore)
        else:
            self.sender.sendMessage("Ungültige Eingabe - Parameter 1 ungültig")
    else:
        self.sender.sendMessage("Ungültige Eingabe - zu viele Parameter!")


def wer_ist_dran(self, putzplan, chore):
    """
    given a chore, return who's turn it is
    """
    if chore in ["muell", "glas"]:
        faellig = "bei Bedarf"
    else:
        days = int(putzplan[chore]['intervall_tage']) - int(putzplan[chore]['tage_vergangen'])
        if days == 0:
            faellig = "heute"
        elif days == 1:
            faellig = "morgen"
        elif days == -1:
            faellig = "gestern"
        elif days > 1:
            faellig = f"in {days} Tagen"
        else:
            days = days * -1
            faellig = f"seit {days} Tagen"
    self.sender.sendMessage(f"<b>{putzplan[chore]['dran']}</b> ist aktuell mit {putzplan[chore]['bezeichnung']} "
                            f"dran. Fällig: {faellig}", parse_mode="html")


def aufgabe_erledigen(putzplan, chore):
    """
    check off a chore and show who's turn it is next
    """
    putzplan[chore]["tage_vergangen"] = 0
    index = putzplan[chore]["reihenfolge"].index(putzplan[chore]["dran"])
    putzplan[chore]["dran"] = putzplan[chore]["reihenfolge"][(index + 1) % 4]
    dump_putzplan(putzplan)
    telepot.Bot(API_KEY).sendMessage(GROUP_ID, f"\u2705Aufgabe {putzplan[chore]['bezeichnung']} wurde erledigt\u2705\n"
                                               f"\n<b>{putzplan[chore]['dran']}</b> ist als nächster dran.",
                                     parse_mode="html")


def show_intervall(self, putzplan, chore):
    """
    show current interval of a chore
    """
    if chore not in ["muell", "glas"]:
        self.sender.sendMessage(f"Intervall der Aufgabe {putzplan[chore]['bezeichnung']} ist auf <b>"
                                f"{putzplan[chore]['intervall_tage']}</b> Tage gesetzt.", parse_mode="html")
    else:
        self.sender.sendMessage(f"Die Aufgabe {putzplan[chore]['bezeichnung']} ist nur bei Bedarf fällig!")


def show_vergangene_tage(self, putzplan, chore):
    """
    show current passed days of a chore
    """
    if chore not in ["muell", "glas"]:
        self.sender.sendMessage(f"Vergangene Tage der Aufgabe {putzplan[chore]['bezeichnung']} sind auf <b>"
                                f"{putzplan[chore]['intervall_tage']}</b> Tage gesetzt.", parse_mode="html")
    else:
        self.sender.sendMessage(f"Die Aufgabe {putzplan[chore]['bezeichnung']} ist nur bei Bedarf fällig!")


def set_intervall(self, putzplan, chore):
    """
    set interval of a chore
    """
    arg2 = self.command[2]
    if chore in ["muell", "glas"]:
        self.sender.sendMessage(f"Die Aufgabe {putzplan[chore]['bezeichnung']} ist nur bei Bedarf fällig!")
        return
    try:
        days = int(arg2)
    except ValueError:
        self.sender.sendMessage("Ungültige Eingabe - Parameter 2 ungültig")
        return
    putzplan[chore]['intervall_tage'] = days
    telepot.Bot(API_KEY).sendMessage(GROUP_ID, f"Intervall der Aufgabe {putzplan[chore]['bezeichnung']} wurde auf "
                                               f"{days} Tage gesetzt.")
    dump_putzplan(putzplan)


def set_vergangene_tage(self, putzplan, chore):
    """
    set passed days of a chore
    """
    arg2 = self.command[2]
    if chore in ["muell", "glas"]:
        self.sender.sendMessage(f"Die Aufgabe {putzplan[chore]['bezeichnung']} ist nur bei Bedarf fällig!")
        return
    try:
        days = int(arg2)
    except ValueError:
        self.sender.sendMessage("Ungültige Eingabe - Parameter 2 ungültig")
        return
    putzplan[chore]['tage_vergangen'] = days
    telepot.Bot(API_KEY).sendMessage(GROUP_ID, f"Vergangene Tage der Aufgabe {putzplan[chore]['bezeichnung']} wurde "
                                               f"auf {days} Tage gesetzt.")
    dump_putzplan(putzplan)


def show_putzplan(self):
    putzplan = load_putzplan()
    msg = "\U0001F9F9\U0001F9F9<b>Putzplan</b>\U0001F9F9\U0001F9F9\n\n"
    for chore in ["muell", "glas", "bad", "kueche", "saugen", "handtuecher", "duschvorhang"]:
        try:
            days = int(putzplan[chore]['intervall_tage']) - int(putzplan[chore]['tage_vergangen'])
            if days == 0:
                faellig = "heute"
            elif days == 1:
                faellig = "morgen"
            elif days == -1:
                faellig = "gestern\u2757"
            elif days > 1:
                faellig = f"in {days} Tagen"
            else:
                days = days * -1
                faellig = f"seit {days} Tagen\u203C"
        except KeyError:
            faellig = "bei Bedarf"
        msg += f"<b>{putzplan[chore]['bezeichnung']}:</b> {putzplan[chore]['dran']}, fällig: {faellig}\n\n"
    self.sender.sendMessage(msg, parse_mode='html')


def update_putzplan():
    """
    increment passed days of all chores. Run this function once every day
    """
    putzplan = load_putzplan()
    # noinspection PyBroadException
    try:
        for chore in ["bad", "kueche", "saugen", "handtuecher", "duschvorhang"]:
            logging.info(f"... incrementing chore {chore} ...")
            putzplan[chore]['tage_vergangen'] += 1
            logging.info(f"... incremented chore {chore} ...")
            if putzplan[chore]['tage_vergangen'] == putzplan[chore]['intervall_tage']:
                attempts = 0
                while attempts < 5:
                    try:
                        chore = putzplan[chore]['bezeichnung']
                        who = putzplan[chore]['dran']
                        telepot.Bot(API_KEY).sendMessage(GROUP_ID, f"\u2757Folgende Aufgabe ist heute fällig: "
                                                                   f"{chore} ({who})\u2757")
                        break
                    except Exception:
                        attempts += 1
                        logging.error(f"Error sending message << chore due >>")
        dump_putzplan(putzplan)
    except Exception:
        logging.critical("Error updating chores")
        try:
            telepot.Bot(API_KEY).sendMessage(ADMIN_IDS[0], "Error updating chores, #4003")
        except Exception:
            pass
