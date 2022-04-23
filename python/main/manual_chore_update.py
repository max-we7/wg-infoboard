import json


def load_putzplan():
    """
    load putzplan from JSON file
    :return: putzplan in dictionary format
    """
    try:
        with open("../../data/putzplan.json", "r", encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return
    return data


def dump_putzplan(plan):
    """
    dump putzplan to JSON file
    :param plan: putzplan in dictionary format
    """
    try:
        with open("../../data/putzplan.json", "w") as f:
            json.dump(plan, f, indent=4)
    except FileNotFoundError:
        pass


def update_putzplan():
    """
    increment passed days of all chores. Run this function once every day
    """
    putzplan = load_putzplan()
    # noinspection PyBroadException
    try:
        for chore in ["bad", "kueche", "saugen", "handtuecher", "duschvorhang", "garten"]:
            putzplan[chore]['tage_vergangen'] += 1
        dump_putzplan(putzplan)
    except Exception:
        pass
