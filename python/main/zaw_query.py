#!/usr/bin/env python
__author__ = "Maximilian Werner"

from datetime import *
import logging
import json
import telepot
from config import API_KEY, GROUP_ID
from keyboards import kb_muell_due

# UPDATING TO NEW YEAR
# save ical file from zaw website to a textfile
# run: cat zaw.txt | grep 'DTSTART\|SUMMARY'
# do regex magic in pycharm:

# replace DTSTART;VALUE=DATE: with {\n      "date": "
# replace \nSUMMARY: with ",\n      "category": "
# replace  -alle Größen- (with leading space) with "\n    },
# replace  Tonnen und Container 14-täglich (with leading space) with "
# replace  Tonnen und Container (with leading space) with "
# replace Restmüll" with Restmüll"\n    },
# replace Papier" with Papier"\n    },
# replace ü with \\u00fc


def load_raw():
    try:
        with open("../../data/zaw_raw.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error("Error - File Not Found")
    return data


def dump_to_json(data):
    """
    write to JSON file
    """
    path = "../../data/zaw.json"
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
            logging.info("Successfully dumped zaw.json")
    except FileNotFoundError as exception:
        logging.error("Error dumping data to JSON ...")
        logging.exception("Stack Trace:", exception)


def update_muell():
    plan = load_raw()

    muell_dates = []
    for muell_art in ["Gelber Sack", "Biomüll", "Restmüll", "Papier"]:
        for entry in plan["muell"]:
            if str(entry["category"]).startswith(muell_art):
                year = int(entry["date"][:4])
                month = int(entry["date"][4:6])
                day = int(entry["date"][6:])
                today = date.today()
                future = date(year, month, day)
                diff = future - today
                if diff.days > -1:
                    muell_dates.append({
                        "art": muell_art,
                        "date": future,
                        "days_remaining": diff.days
                    })

    gelb = [entry for entry in muell_dates if entry["art"].startswith("Gelber Sack")]
    schwarz = [entry for entry in muell_dates if entry["art"].startswith("Restmüll")]
    blau = [entry for entry in muell_dates if entry["art"].startswith("Papier")]
    gruen = [entry for entry in muell_dates if entry["art"].startswith("Biomüll")]

    muell_upcoming = {}

    muell_upcoming.update({
        "gelb": str(gelb[0]["days_remaining"]),
        "schwarz": str(schwarz[0]["days_remaining"]),
        "blau": str(blau[0]["days_remaining"]),
        "gruen": str(gruen[0]["days_remaining"])
    })

    dump_to_json(muell_upcoming)


def check_muell_due():
    dic = {
        "gelb": "Gelber Sack",
        "schwarz": "Restmüll",
        "blau": "Papiermüll",
        "gruen": "Biomüll"
    }

    attempts = 0
    while attempts < 50:
        # noinspection PyBroadException
        try:
            with open("../../data/zaw.json", "r") as f:
                muell = json.load(f)
            for item in ["gelb", "schwarz", "blau", "gruen"]:
                if int(muell[item]) == 1:
                    telepot.Bot(API_KEY).sendMessage(GROUP_ID, f"Erinnerung: {dic[item]} wird morgen abgeholt!",
                                                     reply_markup=kb_muell_due)
                    logging.info("Garbage notification message successfully sent")
            break
        except Exception:
            attempts += 1
            logging.error("Could not send garbage notification message")
