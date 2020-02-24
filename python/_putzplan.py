import json
import logging


def load_putzplan():
    """
    load putzplan from JSON file
    :return: putzplan in dictionary format
    """
    try:
        with open("../data/putzplan.json", "r", encoding='utf-8') as f:
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
        with open("../data/putzplan.json", "w") as f:
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
            aufgabe_erledigen(self, putzplan, chore)
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
        if days == 0: faellig = "heute"
        elif days == 1: faellig = "morgen"
        elif days == -1: faellig = "gestern"
        elif days > 1: faellig = f"in {days} Tagen"
        else:
            days = days * -1
            faellig = f"seit {days} Tagen"
    self.sender.sendMessage(f"<b>{putzplan[chore]['dran']}</b> ist aktuell mit {putzplan[chore]['bezeichnung']} "
                            f"dran. Fällig: {faellig}", parse_mode="html")


def aufgabe_erledigen(self, putzplan, chore):
    """
    check off a chore and show who's turn it is next
    """
    putzplan[chore]["tage_vergangen"] = 0
    index = putzplan[chore]["reihenfolge"].index(putzplan[chore]["dran"])
    putzplan[chore]["dran"] = putzplan[chore]["reihenfolge"][(index + 1) % 4]
    dump_putzplan(putzplan)
    self.sender.sendMessage(f"Aufgabe {putzplan[chore]['bezeichnung']} wurde erledigt. <b>"
                            f"{putzplan[chore]['dran']}</b> ist als nächster dran.", parse_mode="html")


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
    self.sender.sendMessage(f"Intervall der Aufgabe {putzplan[chore]['bezeichnung']} wurde auf {days} Tage"
                            f"gesetzt.")
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
    self.sender.sendMessage(f"Vergangene Tage der Aufgabe {putzplan[chore]['bezeichnung']} wurde auf {days} Tage"
                            f"gesetzt.")
    dump_putzplan(putzplan)


def update_putzplan():
    """
    increment passed days of all chores. Run this function once every day
    """
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
        logging.error("Error incrementing 'tage_vergangen', #4003")
