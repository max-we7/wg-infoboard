#!/usr/bin/env python
__author__ = "Maximilian Werner"

from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
from datetime import datetime
import logging
import json
import re

logging.basicConfig(filename="xkcd.log", filemode="a+", format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def web_request():
    """
    creates BS object of a timetable request for current time
    """
    url = "https://xkcd.com"
    try:
        with urlopen(url) as response:
            source = response.read()
        return BS(source, features="html.parser")
    except ConnectionError as exception:
        logging.critical("Connection Error ... could not reach given URL: ", url, "...")
        logging.exception("Stack Trace:", exception)


def extract_data():
    request = web_request()
    pic = request.find(id="comic")
    start_index = str(pic).index("imgs.xkcd.com")
    end_index = str(pic).index("srcset=")
    url = str(pic)[start_index:end_index - 2]
    dump_to_json(url)


def dump_to_json(data):
    """
    write to JSON file
    """
    path = "../data/xkcd.txt"
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
            logging.info("Successfully dumped xkcd.json")
    except FileNotFoundError as exception:
        logging.critical("Error dumping data to JSON ...")
        logging.exception("Stack Trace:", exception)


extract_data()