from collections import defaultdict
from datetime import timedelta, datetime
from config import RMV_API_KEY
import requests
import json
from rmv_stations import stations
from keyboards import create_bahn_start_keyboard, create_bahn_searchresult_keyboard, create_bahn_destination_keyboard, \
    kb_favoriten_bearbeiten
from telepot.namedtuple import ReplyKeyboardRemove


def bahn(self):
    if self.bahn_destination_flag:
        self.bahn_destination_flag = False
        if self.command[0] == "Suche":
            self.bahn_search, self.search_dest_flag = True, True
            search_station(self)
        else:
            try:
                user_input = " ".join(self.command)
                self.destination = stations[user_input]
                return_search_results(self)
            except KeyError:
                self.sender.sendMessage("Ungültige Eingabe! Bitte starte die Anfrage noch einmal von vorne.",
                                        reply_markup=ReplyKeyboardRemove())
    elif self.bahn_start:
        self.bahn_start = False
        if self.command[0] == "Suche":
            search_station(self)
        elif self.command[0] == "Favoriten" and self.command[1] == "bearbeiten":
            favoriten_bearbeiten(self)
        else:
            try:
                user_input = " ".join(self.command)
                self.origin = stations[user_input]
                self.bahn_destination_flag = True
                self.sender.sendMessage("Wo möchtest du hin?", reply_markup=create_bahn_destination_keyboard(self))
            except KeyError:
                self.sender.sendMessage("Ungültige Eingabe! Bitte starte die Anfrage noch einmal von vorne.",
                                        reply_markup=ReplyKeyboardRemove())
    else:
        keyboard = create_bahn_start_keyboard(self)
        self.bahn_start = True
        self.sender.sendMessage("Von wo aus möchtest du starten?", reply_markup=keyboard)


def return_search_results(self):
    origin = [key for key in stations.keys() if stations[key] == self.origin][0]
    destination = [key for key in stations.keys() if stations[key] == self.destination][0]
    msg = f"Fahrplan für deine Fahrt von <b>{origin}</b> nach <b>{destination}</b>:\n\n"
    results = extract_from_api_request(make_api_request(self.origin, self.destination))
    for trip in results['trips']:
        msg += f"Ab: {trip['ab']} (+{trip['delay']}) An: {trip['an']} Dauer: {trip['duration']}\nLinie(n): " \
               f"{', '.join(trip['line'])}\n\n"
    self.sender.sendMessage(msg, reply_markup=ReplyKeyboardRemove(), parse_mode='html')


def search_station(self):
    if self.bahn_search3:
        self.bahn_search3 = False
        try:
            user_input = " ".join(self.command)
            if self.search_dest_flag:
                self.destination = stations[user_input]
                self.search_dest_flag = False
                return_search_results(self)
            else:
                self.origin = stations[user_input]
                self.bahn_destination_flag = True
                self.sender.sendMessage("Wo möchtest du hin?", reply_markup=create_bahn_start_keyboard(self))
        except KeyError:
            self.sender.sendMessage("Ungültige Eingabe! Bitte starte die Anfrage noch einmal von vorne.",
                                    reply_markup=ReplyKeyboardRemove())
    elif self.bahn_search2:
        keyboard = create_bahn_searchresult_keyboard(self, search_stations(self.command))
        self.bahn_search2, self.bahn_search3 = False, True
        self.sender.sendMessage("Bitte wähle eine Station aus:", reply_markup=keyboard)
    else:
        self.bahn_search, self.bahn_search2 = False, True
        self.sender.sendMessage("Bitte gib einen Suchbegriff ein:", reply_markup=ReplyKeyboardRemove())


def search_stations(tokens):
    number_of_tokens = len(tokens)
    results = defaultdict(str)
    for station, station_id in stations.items():
        count = 0
        for token in tokens:
            if token.lower() in station.lower():
                count += 1
        if (count / number_of_tokens) > 0.5:
            if len(results) < 200:
                results[station] = station_id
    return results


def favoriten_bearbeiten(self):
    favs = {"Favorit 1": "fav1", "Favorit 2": "fav2", "Favorit 3": "fav3"}
    if self.fav_flag3:
        station_name = " ".join(self.command)
        station_id = stations[station_name]
        self.cookies['bahn'][self.fav_to_be_modified].clear()
        self.cookies['bahn'][self.fav_to_be_modified].update({station_name: station_id})
        self.fav_flag3 = False
        self.sender.sendMessage("Favorit wurde erfolgreich aktualisiert!", reply_markup=ReplyKeyboardRemove())
    elif self.fav_flag2:
        keyboard = create_bahn_searchresult_keyboard(self, search_stations(self.command))
        self.fav_flag2, self.fav_flag3 = False, True
        self.sender.sendMessage("Bitte wähle eine Station aus:", reply_markup=keyboard)
    elif self.fav_flag1:
        entry = " ".join(self.command)
        if entry in favs.keys():
            self.fav_to_be_modified = favs[entry]
            self.fav_flag1, self.fav_flag2 = False, True
            self.sender.sendMessage("Bitte gib einen Suchbegriff ein:", reply_markup=ReplyKeyboardRemove())
        else:
            self.fav_flag1 = False
            self.sender.sendMessage("Vorgang wurde abgebrochen.", reply_markup=ReplyKeyboardRemove())
    else:
        self.fav_flag1 = True
        self.sender.sendMessage("Welchen Eintrag möchtest du bearbeiten?", reply_markup=kb_favoriten_bearbeiten)


def make_api_request(origin_id, destination_id, delta_mins=0):
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


def extract_from_api_request(request):
    schedule_raw = request.json()
    # check if response is internal server error!
    schedule = {"trips": []}
    for i in range(5):
        number_of_legs = len(schedule_raw['Trip'][i]['LegList']['Leg'])

        planned_ab_time = schedule_raw['Trip'][i]['LegList']['Leg'][0]['Origin']['time'][:-3]
        planned_ab_date = schedule_raw['Trip'][i]['LegList']['Leg'][0]['Origin']['date']
        planned_ab = datetime(int(planned_ab_date[:4]), int(planned_ab_date[5:7]), int(planned_ab_date[8:10]),
                              int(planned_ab_time[:2]), int(planned_ab_time[3:]), 0)

        try:
            actual_ab_time = schedule_raw['Trip'][i]['LegList']['Leg'][0]['Origin']['rtTime'][:-3]
            actual_ab = datetime(2020, 10, 10, int(actual_ab_time[:2]), int(actual_ab_time[3:]), 0)
            delay = actual_ab - planned_ab
            delay = (delay.seconds // 60) % 60
        except KeyError:
            delay = 0

        tz = planned_ab + timedelta(minutes=10)
        tz = f"{tz.hour if len(str(tz.hour)) == 2 else '0' + str(tz.hour)}:{tz.minute if len(str(tz.minute)) == 2 else '0' + str(tz.minute)}"

        planned_an_time = schedule_raw['Trip'][i]['LegList']['Leg'][number_of_legs - 1]['Destination']['time'][:-3]
        planned_an_date = schedule_raw['Trip'][i]['LegList']['Leg'][number_of_legs - 1]['Destination']['date']
        planned_an = datetime(int(planned_an_date[:4]), int(planned_an_date[5:7]), int(planned_an_date[8:10]),
                              int(planned_an_time[:2]), int(planned_an_time[3:]), 0)
        duration = str(planned_an - planned_ab)[:4]

        line = [schedule_raw['Trip'][i]['LegList']['Leg'][leg]['name'].strip() for leg in range(number_of_legs)]
        line = [line for line in line if line != ""]

        schedule['trips'].append({
            "id": i,
            "ab": planned_ab_time,
            "tz": tz,
            "an": planned_an_time,
            "duration": duration,
            "delay": delay,
            "line": line
        })
    return schedule


def dump_schedule(file_url, schedule):
    with open(file_url, "w") as f:
        json.dump(schedule, f, indent=2)


def update_bahn():
    hkp = "3015020"
    schloss = "3016016"
    da_hbf = "3004734"
    wb_hbf = "3006907"
    nahverkehr = extract_from_api_request(make_api_request(hkp, schloss, 8))
    dump_schedule("../data/timetable.json", nahverkehr)
    regio = extract_from_api_request(make_api_request(da_hbf, wb_hbf, 25))
    dump_schedule("../data/timetable_regio.json", regio)
