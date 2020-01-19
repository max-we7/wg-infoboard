#!/usr/bin/env python
__author__ = "Maximilian Werner"

from datetime import datetime
import logging
import json
import re

logging.basicConfig(filename="zaw.log", filemode="a+", format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


# TODO: implement Garbage


def dump_to_json(data):
    """
    write to JSON file
    """
    path = "../data/zaw.json"
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
            logging.info("Successfully dumped timetable.json")
    except FileNotFoundError as exception:
        logging.critical("Error dumping data to JSON ...")
        logging.exception("Stack Trace:", exception)
