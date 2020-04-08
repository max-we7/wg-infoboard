from collections import defaultdict
from config import OPEN_WEATHER_MAP_API_KEY
from requests import get
import logging
import json
import time
from datetime import datetime
from babel.dates import format_date
from keyboards import create_weather_start_keyboard, create_weather_searchresult_keyboard, \
    kb_wetter_favoriten_bearbeiten
from telepot.namedtuple import ReplyKeyboardRemove


def weather(self):
    """
    general weather function to handle all input
    """
    if self.wetter_flag1 or self.wetter_flag3:
        self.wetter_flag1 = False
        if self.command[0] == "Suche":
            search_weather_skeleton(self)
        elif self.command[0] == "Favoriten" and self.command[1] == "bearbeiten":
            edit_weather_favorites(self)
        else:
            self.wetter_flag3 = False
            try:
                user_input = " ".join(self.command)
                self.destination = user_input
                with open("../data/weather_locations.json", "rb") as f:
                    data = json.load(f)
                    locations = [(entry['name'], entry['id']) for entry in data]
                location_id = [location[1] for location in locations if location[0] == user_input]
                return_weather(self, str(location_id[0]))
            except (KeyError, IndexError):
                self.sender.sendMessage("Ungültige Eingabe! Bitte starte die Anfrage noch einmal von vorne.",
                                        reply_markup=ReplyKeyboardRemove())
    else:
        self.wetter_flag1 = True
        keyboard = create_weather_start_keyboard(self)
        self.sender.sendMessage("Zum Abrufen von Wetterdaten bitte einen Standort auswählen:", reply_markup=keyboard)


def search_weather_skeleton(self):
    if self.wetter_flag2:
        search_result = search_locations(self.command)
        if len(search_result.keys()) > 0:
            keyboard = create_weather_searchresult_keyboard(search_result)
            self.wetter_flag2, self.wetter_flag3 = False, True
            self.sender.sendMessage("Bitte wähle einen Standort aus:", reply_markup=keyboard)
        else:
            self.sender.sendMessage("Kein Standort gefunden. Bitte erneut einen Suchbegriff eingeben:")
    else:
        self.wetter_flag2 = True
        self.sender.sendMessage("Bitte gib einen Suchbegriff ein (PLZs nicht unterstützt):",
                                reply_markup=ReplyKeyboardRemove())


def return_weather(self, location_id):
    """
    return weather results to user
    """
    if check_cache(location_id):
        data = load_from_cache(location_id)
    else:
        data = make_api_request(location_id)
        dump_to_cache(data, location_id)

    clocks = {
        "00": "\U0001F55B", "01": "\U0001F550", "02": "\U0001F551", "03": "\U0001F552", "04": "\U0001F553",
        "05": "\U0001F554", "06": "\U0001F555", "07": "\U0001F556", "08": "\U0001F557", "09": "\U0001F558",
        "10": "\U0001F559", "11": "\U0001F55A", "12": "\U0001F55B", "13": "\U0001F550", "14": "\U0001F551",
        "15": "\U0001F552", "16": "\U0001F553", "17": "\U0001F554", "18": "\U0001F555", "19": "\U0001F556",
        "20": "\U0001F557", "21": "\U0001F558", "22": "\U0001F559", "23": "\U0001F55A"
    }

    try:
        # Current
        msg = f"<b>Das Wetter heute in {self.destination}:</b>\n\n"
        msg += f"{data['current']['weather'][0]['description']}\n"
        msg += f"\U0001F321 {int(round(data['current']['temp']))}\u00B0C (gefühlt: " \
               f"{int(round(data['current']['feels_like']))}\u00B0C)\n\n"
        msg += f"\U0001F32B {data['current']['humidity']}%\n"
        msg += f"\U0001F32C {int(round(data['current']['wind_speed']))} km/h\n\n"
        msg += f"\U0001F304 {datetime.fromtimestamp(data['current']['sunrise']).strftime('%H:%M')} Uhr\n"
        msg += f"\U0001F307 {datetime.fromtimestamp(data['current']['sunset']).strftime('%H:%M')} Uhr\n\n\n"

        # Hourly (next 15 hours)
        msg += "<b>Stündlich:</b>\n\n"
        i = 15
        for entry in data['hourly']:
            if i != 0:
                time_hour = datetime.fromtimestamp(entry['dt']).strftime('%H')
                msg += f"{clocks[time_hour]} {time_hour}:00"
                msg += f"  \U0001F321 {int(round(entry['temp']))}\u00B0C -"
                msg += f" {entry['weather'][0]['description']}\n"
                i -= 1

        # Daily (next 7 days)
        msg += "\n\n<b>In den nächsten Tagen:</b>\n\n"
        i = 8
        for entry in data['daily']:
            if i != 0 and i != 8:
                msg += f"{format_date(datetime.fromtimestamp(entry['dt']), 'EEE, d.M.', locale='de_DE')}: "
                msg += f" \U0001F321 {int(round(entry['temp']['min']))}\u00B0C / "
                msg += f"{int(round(entry['temp']['max']))}\u00B0C -"
                msg += f" {entry['weather'][0]['description']}\n"
            i -= 1
        self.sender.sendMessage(msg, parse_mode='html', reply_markup=ReplyKeyboardRemove())
    except KeyError:
        logging.error("OpenWeatherMap API - Response hat unbekanntes Format!")
        self.sender.sendMessage("Wetterdaten konnten nicht abgerufen werden. Möglicherweise sind die Server der"
                                "OpenWeatherMap gerade offline.", reply_markup=ReplyKeyboardRemove())


def check_cache(location_id):
    """
    check if there is cached data newer than 10 minutes ago
    """
    try:
        with open(f"../data/weather_cache/{location_id}.json", "r", encoding='utf-8') as f:
            data = json.load(f)
            time_of_cache = data['current']['dt']
            current_time = int(time.time())
            if current_time > (time_of_cache + 600):
                return False
            return True
    except FileNotFoundError:
        return False


def search_locations(tokens):
    """
    search for a location
    :param tokens: list of search terms
    :return: dictionary of matching locations and their id
    """
    results = defaultdict(str)
    with open("../data/weather_locations.json", "rb") as f:
        data = json.load(f)
    locations = [(entry['name'], entry['id']) for entry in data]
    for i in range(len(locations)):
        count = 0
        for token in tokens:
            if token.lower() in str(locations[i][0]).lower():
                count += 1
        if count > 0 and len(results) < 200:
            results[locations[i][0]] = locations[i][1]
    return results


def edit_weather_favorites(self):
    """
    edit the list of 2 favorite locations saved in the cookie file
    """
    favs = {"Favorit 1": "fav1", "Favorit 2": "fav2"}
    if self.fav_flag3_wetter:
        try:
            self.cookies['wetter']
        except KeyError:
            self.cookies.update({
                "wetter": {
                    "fav1": {},
                    "fav2": {}
                }
            })
        location_name = " ".join(self.command)
        with open("../data/weather_locations.json", "rb") as f:
            data = json.load(f)
            locations = [(entry['name'], entry['id']) for entry in data]
        if location_name in [location[0] for location in locations]:
            location_id = [location[1] for location in locations if location[0] == location_name][0]
            self.cookies['wetter'][self.fav_to_be_modified].clear()
            self.cookies['wetter'][self.fav_to_be_modified].update({location_name: str(location_id)})
            self.fav_flag3_wetter = False
            self.sender.sendMessage("Favorit wurde erfolgreich aktualisiert!", reply_markup=ReplyKeyboardRemove())
        else:
            self.fav_flag3_wetter = False
            self.sender.sendMessage("Vorgang wurde abgebrochen.", reply_markup=ReplyKeyboardRemove())
    elif self.fav_flag2_wetter:
        search_result = search_locations(self.command)
        if len(search_result.keys()) > 0:
            keyboard = create_weather_searchresult_keyboard(search_result)
            self.fav_flag2_wetter, self.fav_flag3_wetter = False, True
            self.sender.sendMessage("Bitte wähle einen Standort aus:", reply_markup=keyboard)
        else:
            self.sender.sendMessage("Kein Standort gefunden. Bitte erneut einen Suchbegriff eingeben:")
    elif self.fav_flag1_wetter:
        entry = " ".join(self.command)
        if entry in favs.keys():
            self.fav_to_be_modified = favs[entry]
            self.fav_flag1_wetter, self.fav_flag2_wetter = False, True
            self.sender.sendMessage("Bitte gib einen Suchbegriff ein:", reply_markup=ReplyKeyboardRemove())
        else:
            self.fav_flag1_wetter = False
            self.sender.sendMessage("Vorgang wurde abgebrochen.", reply_markup=ReplyKeyboardRemove())
    else:
        self.fav_flag1_wetter = True
        self.sender.sendMessage("Welchen Eintrag möchtest du bearbeiten?", reply_markup=kb_wetter_favoriten_bearbeiten)


def make_api_request(location_id):
    """
    get weather data for given location
    """
    try:
        with open("../data/weather_locations.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error("weather_locations.json not found!")
    location = [entry for entry in data if str(entry['id']) == str(location_id)][0]
    lat = location['coord']['lat']
    lon = location['coord']['lon']

    base_url = "https://api.openweathermap.org/data/2.5/onecall?"
    url = f"{base_url}lat={lat}&lon={lon}&units=metric&lang=de&appid={OPEN_WEATHER_MAP_API_KEY}"
    return get(url).json()


def load_from_cache(location_id):
    """
    load query data from cache
    :param location_id: location for which the query data is loaded
    """
    try:
        with open(f"../data/weather_cache/{location_id}.json", "r", encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return False


def dump_to_cache(query_result, location_id):
    """
    dump query result to cache
    """
    try:
        with open(f"../data/weather_cache/{location_id}.json", "w") as f:
            json.dump(query_result, f, indent=4)
    except FileNotFoundError:
        logging.error("Error - File Not Found! weather.py, dump_to_cache()")
