from collections import defaultdict
from json import JSONDecodeError
import requests
import logging
import time
from datetime import datetime, timedelta
from python.api.openmensa_canteens import canteens
from python.main.keyboards import create_canteen_start_keyboard, create_canteen_searchresult_keyboard, \
    kb_canteen_favoriten_bearbeiten
from telepot.namedtuple import ReplyKeyboardRemove


def speiseplan(self):
    if self.speiseplan_flag1 or self.speiseplan_flag3:
        self.speiseplan_flag1 = False
        if self.command[0] == "Suche":
            search_canteen_skeleton(self)
        elif self.command[0] == "Favoriten" and self.command[1] == "bearbeiten":
            edit_canteen_favorites(self)
        else:
            self.speiseplan_flag3 = False
            try:
                user_input = " ".join(self.command)
                canteen_id = canteens[user_input]
                send_meal_plan(self, canteen_id)
            except KeyError:
                self.sender.sendMessage("Ungültige Eingabe! Bitte starte die Anfrage noch einmal von vorne.",
                                        reply_markup=ReplyKeyboardRemove())
    else:
        self.speiseplan_flag1 = True
        keyboard = create_canteen_start_keyboard(self)
        self.sender.sendMessage("Zum Abrufen des Speiseplans bitte eine Mensa auswählen:", reply_markup=keyboard)


def search_canteen_skeleton(self):
    if self.speiseplan_flag2:
        search_result = search_canteens(self.command)
        if len(search_result.keys()) > 0:
            keyboard = create_canteen_searchresult_keyboard(search_result)
            self.speiseplan_flag2, self.speiseplan_flag3 = False, True
            self.sender.sendMessage("Bitte wähle eine Mensa aus:", reply_markup=keyboard)
        else:
            self.sender.sendMessage("Keine Mensa gefunden. Bitte erneut einen Suchbegriff eingeben:")
    else:
        self.speiseplan_flag2 = True
        self.sender.sendMessage("Bitte gib einen Suchbegriff ein:", reply_markup=ReplyKeyboardRemove())


def send_meal_plan(self, canteen_id):
    """
    make API request to OpenMensa, format response and send response message to user
    """
    current_time = datetime.now()
    if int(datetime.now().strftime("%H")) > 14:
        tomorrow = current_time + timedelta(days=1)
        date = tomorrow.strftime("%Y-%m-%d")
        msg = f"Speiseplan für morgen, den {tomorrow.strftime('%d.%m.%Y')}: \n\n"
    else:
        date = "today"
        msg = f"Speiseplan für heute, den {current_time.strftime('%d.%m.%Y')}: \n\n"
    meal_plan = extract_from_api_request(make_api_request(str(canteen_id), date))
    if meal_plan == -2:
        msg = msg + "Leider kein Angebot!"
    elif meal_plan == -1:
        msg = msg + "Fehler beim Abrufen des Speiseplans!"
    else:
        for key in meal_plan.keys():
            msg += f"<b>{key}:</b>\n\n"
            for meal, price in meal_plan[key].items():
                msg += f"{meal}\n<b>{price}</b>\n\n"
            msg += "\n"
    self.sender.sendMessage(msg, parse_mode='html', reply_markup=ReplyKeyboardRemove())


def search_canteens(tokens):
    """
    search for a canteen
    :param tokens: list of search terms
    :return: dictionary of matching canteens and their id
    """
    results = defaultdict(str)
    for canteen, canteen_id in canteens.items():
        count = 0
        for token in tokens:
            if token.lower() in canteen.lower():
                count += 1
        if count > 0 and len(results) < 200:
            results[canteen] = canteen_id
    return results


def edit_canteen_favorites(self):
    """
    edit the list of 2 favorite canteens saved in the cookie file
    """
    favs = {"Favorit 1": "fav1", "Favorit 2": "fav2"}
    if self.fav_flag3_speiseplan:
        try:
            self.cookies['mensa']
        except KeyError:
            self.cookies.update({
                "mensa": {
                    "fav1": {},
                    "fav2": {}
                }
            })
        canteen_name = " ".join(self.command)
        if canteen_name in canteens.keys():
            canteen_id = canteens[canteen_name]
            self.cookies['mensa'][self.fav_to_be_modified].clear()
            self.cookies['mensa'][self.fav_to_be_modified].update({canteen_name: canteen_id})
            self.fav_flag3_speiseplan = False
            self.sender.sendMessage("Favorit wurde erfolgreich aktualisiert!", reply_markup=ReplyKeyboardRemove())
        else:
            self.fav_flag3_speiseplan = False
            self.sender.sendMessage("Vorgang wurde abgebrochen.", reply_markup=ReplyKeyboardRemove())
    elif self.fav_flag2_speiseplan:
        search_result = search_canteens(self.command)
        if len(search_result.keys()) > 0:
            keyboard = create_canteen_searchresult_keyboard(search_result)
            self.fav_flag2_speiseplan, self.fav_flag3_speiseplan = False, True
            self.sender.sendMessage("Bitte wähle eine Mensa aus:", reply_markup=keyboard)
        else:
            self.sender.sendMessage("Keine Mensa gefunden. Bitte erneut einen Suchbegriff eingeben:")
    elif self.fav_flag1_speiseplan:
        entry = " ".join(self.command)
        if entry in favs.keys():
            self.fav_to_be_modified = favs[entry]
            self.fav_flag1_speiseplan, self.fav_flag2_speiseplan = False, True
            self.sender.sendMessage("Bitte gib einen Suchbegriff ein:", reply_markup=ReplyKeyboardRemove())
        else:
            self.fav_flag1_speiseplan = False
            self.sender.sendMessage("Vorgang wurde abgebrochen.", reply_markup=ReplyKeyboardRemove())
    else:
        self.fav_flag1_speiseplan = True
        self.sender.sendMessage("Welchen Eintrag möchtest du bearbeiten?", reply_markup=kb_canteen_favoriten_bearbeiten)


def make_api_request(canteen_id, date="today"):
    """
    make API request to the OpenMensa API
    :param canteen_id: ID of the canteen to search
    :param date: date on which to search for meal plan
    :return: request object
    """
    base_url = "https://openmensa.org/api/v2/canteens/"
    now = datetime.now()
    day = now.strftime("%Y-%m-%d") if date == "today" else date
    url = base_url + canteen_id + "/days/" + day + "/meals"

    result, i, request = False, 0, -1
    while not result and i < 300:
        # noinspection PyBroadException
        try:
            request = requests.get(url)
            result = True
        except Exception:
            logging.exception(f"OpenMensa API request failed! Used query URL: {url}")
            i += 1
            time.sleep(0.01)

    return request


def extract_from_api_request(request):
    if request == -1: return -1

    try:
        meal_plan_raw = request.json()
    except JSONDecodeError:
        # kein Essensangebot
        return -2

    meals = defaultdict(dict)

    for meal in meal_plan_raw:
        try:
            price = float(meal['prices']['students'])
            if price > 1:
                category = meal['category']
                if len(str(price).rsplit('.')[-1]) == 2:
                    meals[category].update({meal['name']: f"{price}€"})
                else:
                    meals[category].update({meal['name']: f"{price}0€"})
        except TypeError:
            category = meal['category']
            meals[category].update({meal['name']: "?.??€"})

    return meals if meals else -2
