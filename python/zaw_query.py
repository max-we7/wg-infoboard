#!/usr/bin/env python
__author__ = "Maximilian Werner"

from datetime import *
import logging
import json
import telepot
from config import API_KEY, GROUP_ID


def load_raw():
    try:
        with open("../data/zaw_raw.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error("Error - File Not Found")
    return data


def dump_to_json(data):
    """
    write to JSON file
    """
    path = "../data/zaw.json"
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
    for muell_art in ["Gelber Sack", "Biomüll", "Restmüll", "Papiertonne"]:
        for entry in plan["muell"]:
            if str(entry["category"]).startswith(muell_art):
                month = int(entry["date"][:2])
                day = int(entry["date"][2:])
                today = date.today()
                future = date(2020, month, day)
                diff = future - today
                if diff.days > -1:
                    muell_dates.append({
                        "art": muell_art,
                        "date": future,
                        "days_remaining": diff.days
                    })

    gelb = [entry for entry in muell_dates if entry["art"].startswith("Gelber Sack")]
    schwarz = [entry for entry in muell_dates if entry["art"].startswith("Restmüll")]
    blau = [entry for entry in muell_dates if entry["art"].startswith("Papiertonne")]
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
    # noinspection PyBroadException
    try:
        with open("../data/zaw.json", "r") as f:
            muell = json.load(f)
        for item in ["gelb", "schwarz", "blau", "gruen"]:
            if int(muell[item]) == 1:
                telepot.Bot(API_KEY).sendMessage(GROUP_ID, f"Erinnerung: {dic[item]} wird morgen abgeholt!")
    except Exception:
        logging.error("Error sending garbage notification message: in check_muell_due")
