from collections import defaultdict
import requests
from datetime import datetime

tu_stadtmitte = "173"
tu_lichtwiese = "174"


def speiseplan(self):
    if len(self.command) == 2 and self.command[1] == "liwi":
        get_food(self, tu_lichtwiese)
    elif len(self.command) == 1:
        get_food(self, tu_stadtmitte)


def get_food(self, mensa_id, date="today"):
    base_url = "https://openmensa.org/api/v2/canteens/"

    now = datetime.now()
    day = now.strftime("%Y-%m-%d") if date == "today" else date
    request = requests.get(base_url + mensa_id + "/days/" + day + "/meals")

    meal_plan_raw = request.json()

    meals = defaultdict(list)

    for meal in meal_plan_raw:
        if float(meal['prices']['students'] > 1):
            category = meal['category']
            meals[category].append(f"{meal['name']}\n<b>Preis: {meal['prices']['students']}0€</b>\n")

    message = "-- Das gibt es heute zu essen --\n\n"
    for key in meals.keys():
        message += f"<b>{key}:</b>\n\n"
        for i in range(len(meals[key])):
            message += f"{meals[key][i]}\n"
        message += "\n"

    self.sender.sendMessage(message, parse_mode='html')
