#!/usr/bin/env python
__author__ = "Maximilian Werner"

from datetime import timedelta, datetime
from config import RMV_API_KEY
import requests
import json
from rmv_stations import stations

hkp = "3015020"
schloss = "3016016"
da_hbf = "3004734"
wb_hbf = "3006907"


def bahn():
    search_term = "markt"


def search_stations(search_term):
    tokens = search_term.split()
    number_of_tokens = len(tokens)
    results = []
    for key in stations.keys():
        count = 0
        for token in tokens:
            if token.lower() in key.lower():
                count += 1
        if (count / number_of_tokens) > 0.5:
            results.append(key)
    return results


def make_request(origin_id, destination_id, delta_mins=0):
    base_url = "https://www.rmv.de/hapi/trip"
    api_key = "?accessId=" + RMV_API_KEY
    response_format = "&format=json"

    origin_id = "&originId=" + origin_id
    dest = "&destId=" + destination_id

    now = datetime.now()
    delay = now + timedelta(minutes=delta_mins)
    delay = "&time=" + str(delay)[11:16]

    url = base_url + api_key + origin_id + dest + delay + response_format
    return requests.get(url)


def extract_from_request(request):
    schedule_raw = request.json()
    schedule = {"trips": []}
    for i in range(3):
        number_of_legs = len(schedule_raw['Trip'][i]['LegList']['Leg'])

        planned_ab = schedule_raw['Trip'][i]['LegList']['Leg'][0]['Origin']['time'][:-3]
        planned_ab_time = datetime(2020, 10, 10, int(planned_ab[:2]), int(planned_ab[3:]), 0)

        # actual_ab = schedule_raw['Trip'][i]['LegList']['Leg'][0]['Origin']['rtTime'][:-3]
        # actual_ab_time = datetime(2020, 10, 10, int(actual_ab[:2]), int(actual_ab[3:]), 0)

        tz = planned_ab_time + timedelta(minutes=10)
        tz = f"{tz.hour if len(str(tz.hour)) == 2 else '0' + str(tz.hour)}:{tz.minute if len(str(tz.minute)) == 2 else '0' + str(tz.minute)}"

        planned_an = schedule_raw['Trip'][i]['LegList']['Leg'][number_of_legs - 1]['Destination']['time'][:-3]
        planned_an_time = datetime(2020, 10, 10, int(planned_an[:2]), int(planned_an[3:]), 0)

        duration = str(planned_an_time - planned_ab_time)[:4]

        # delay = actual_ab_time - planned_ab_time
        # delay = (delay.seconds//60) % 60

        line = [schedule_raw['Trip'][i]['LegList']['Leg'][leg]['name'].strip() for leg in range(number_of_legs)]
        line = [line for line in line if line != ""]
        # line = line[0] if len(line) == 1 else line

        schedule['trips'].append({
            "id": i,
            "ab": planned_ab,
            "tz": tz,
            "an": planned_an,
            "duration": duration,
            # "delay": delay,
            "line": line
        })

    return schedule


def dump_schedule(file_url, schedule):
    with open(file_url, "w") as f:
        json.dump(schedule, f, indent=2)


def update_bahn():
    nahverkehr = extract_from_request(make_request(hkp, schloss, 10))
    dump_schedule("../data/timetable.json", nahverkehr)
    print("hi")
    regio = extract_from_request(make_request(da_hbf, wb_hbf, 25))
    dump_schedule("../data/timetable_regio.json", regio)
