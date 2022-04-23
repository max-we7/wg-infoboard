import json
import logging
import telepot
from config import GROUP_ID, API_KEY, ADMIN_IDS
logging.basicConfig(filename="../wg-infoboard.log", filemode="a+", format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def load_putzplan():
    """
    load putzplan from JSON file
    :return: putzplan in dictionary format
    """
    try:
        with open("../../data/putzplan.json", "r", encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
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
        pass


def update_putzplan():
    """
    increment passed days of all chores. Run this function once every day
    """
    putzplan = load_putzplan()
    # noinspection PyBroadException
    try:
        for chore in ["bad", "kueche", "saugen", "handtuecher", "duschvorhang", "garten"]:
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


update_putzplan()
