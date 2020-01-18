#!/usr/bin/env python
__author__ = "Maximilian Werner"

from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
from datetime import datetime
import logging
import json

logging.basicConfig(filename="rmv.log", filemode="a+", format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


def web_request():
    """
    creates BS object of a timetable request for current time
    """
    now = datetime.now()
    hour = int(now.strftime("%H"))
    mins = int(now.strftime("%M"))
    # add 12 mins to current time
    mins += 8
    # check for time overflow
    if mins > 59:
        mins %= 60
        hour += 1
    if hour == 24:
        hour, mins = 23, 59
    url = f"https://www.rmv.de/auskunft/bin/jp/query.exe/dn?start=1&s=hans-karl-platz&z=Darmstadt%20" \
          f"Schlo%C3%9F&time={hour}%3A{mins}&timesel=depart"
    logging.info(f"Searching with query: {url} ...")
    try:
        with urlopen(url) as response:
            source = response.read()
        return BS(source, features="html.parser")
    except ConnectionError as exception:
        logging.critical("Connection Error ... could not reach given URL: ", url, "...")
        logging.exception("Stack Trace:", exception)


def get_schedule():
    """
    extract features from the request and same them in schedule dictionary
    """
    request = web_request()
    schedule_raw = request.find_all("div", class_="planed")
    durations_raw = request.find_all("td", class_="duration")
    lines_raw = request.find_all("td", class_="products")
    schedule = {"trips": []}
    if len(schedule_raw) < 3 or len(durations_raw) < 3 or len(lines_raw) < 3:
        logging.error("Less than 3 trips detected")
    for i in range(len(schedule_raw)):
        tram_index = str(lines_raw[i]).index("Tram")
        abfahrt = str(schedule_raw[i])[21:26]
        ankunft = str(schedule_raw[i])[35:40]
        duration = str(durations_raw[i])[-10:-6]
        hour, mins = int(abfahrt[:2]), int(abfahrt[3:])
        mins += 10
        if mins > 59:
            mins %= 60
            if -1 < mins < 10:
                mins = "0" + str(mins)
            hour += 1
        if hour > 23:
            hour %= 24
            if hour == 0:
                hour = str(hour) + "0"
        tz_ankunft = f"{hour}:{mins}"
        # check if there is an additional bus in the connection, usually Tram only
        no_bus = False
        try:
            bus_index = str(lines_raw[i]).index("Bus")
        except ValueError:
            no_bus = True
        if no_bus:
            line = str(lines_raw[i])[tram_index:tram_index + 6]
        else:
            line = str(lines_raw[i])[tram_index:tram_index + 6], \
                   str(lines_raw[i])[bus_index:bus_index + 7]
        schedule["trips"].append({
            "id": i,
            "ab": abfahrt,
            "tz": tz_ankunft,
            "an": ankunft,
            "duration": duration,
            "line": line
        })
    return schedule


def dump_to_json(data):
    """
    write timetable to JSON file
    """
    try:
        with open("../data/timetable.json", "w") as f:
            json.dump(data, f, indent=2)
    except FileNotFoundError as exception:
        logging.critical("Error dumping data to JSON ...")
        logging.exception("Stack Trace:", exception)


if __name__ == '__main__':
    dump_to_json(get_schedule())
