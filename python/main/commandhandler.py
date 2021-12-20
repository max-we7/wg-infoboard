from putzplan import chores, show_putzplan
from general_commands import einkaufen, help_commands, reload, reboot, \
    impersonate, eingekauft
from finances import geld, show_balance, make_transaction, neuer_einkauf, show_history, delete_last_record
import logging
from python.api.rmv import bahn, search_station, edit_station_favorites
from python.api.speiseplan import speiseplan, search_canteen_skeleton, edit_canteen_favorites
from python.api.weather import weather, search_weather_skeleton, edit_weather_favorites
from config import LEGIT_IDS


def choose_command(self, msg):
    """
    route chat messages to corresponding functions
    """
    # --------------- FLAGS ----------------
    if self.artikel_flag or self.preis_flag or self.teilnehmer_flag:
        neuer_einkauf(self, msg)
        return
    if self.delete_flag:
        delete_last_record(self, msg)
        return
    if self.empfaenger_flag or self.betrag_flag:
        make_transaction(self, msg)
        return
    if self.bahn_start or self.bahn_destination_flag:
        bahn(self)
        return
    if self.bahn_search or self.bahn_search2 or self.bahn_search3:
        search_station(self)
    if self.fav_flag1 or self.fav_flag2 or self.fav_flag3:
        edit_station_favorites(self)
    if self.fav_flag1_speiseplan or self.fav_flag2_speiseplan or self.fav_flag3_speiseplan:
        edit_canteen_favorites(self)
    if self.speiseplan_flag3:
        speiseplan(self)
    if self.speiseplan_flag2:
        search_canteen_skeleton(self)
    if self.speiseplan_flag1:
        speiseplan(self)
    if self.fav_flag1_wetter or self.fav_flag2_wetter or self.fav_flag3_wetter:
        edit_weather_favorites(self)
    if self.wetter_flag3:
        weather(self)
    if self.wetter_flag2:
        search_weather_skeleton(self)
    if self.wetter_flag1:
        weather(self)
    if self.eingekauft_flag1:
        eingekauft(self, msg)

    # ---------------- COMMANDS ---------------------
    if self.command[0] == "/einkaufen" and self.chatid in LEGIT_IDS:
        # noinspection PyBroadException
        try:
            einkaufen(self, msg)
        except Exception:
            logging.error("General error in einkaufen(), #2006")
            self.sender.sendMessage("Fehler #2006")
    if self.command[0] == "/eingekauft" and self.chatid in LEGIT_IDS:
        # noinspection PyBroadException
        try:
            eingekauft(self, msg)
        except Exception:
            logging.error("General error in eingekauft(), #2007")
            self.sender.sendMessage("Fehler #2007")
    if self.command[0] == "/impersonate":
        impersonate(self, msg)
    if self.command[0] == "/help" or self.command[0] == "/start":
        # noinspection PyBroadException
        try:
            help_commands(self)
        except Exception:
            logging.error("General error in help_commands(), #2009")
            self.sender.sendMessage("Fehler #2009")
    if self.command[0] == "/putzplan":
        show_putzplan(self)
    if self.command[0] in ["/muell", "/müll", "/glas", "/bad", "/kueche", "/küche", "/saugen", "/handtuecher",
                           "/handtücher", "/duschvorhang"] and \
            self.chatid in LEGIT_IDS:
        # noinspection PyBroadException
        try:
            if self.command[0] == "/müll":
                self.command[0] = "/muell"
            if self.command[0] == "/küche":
                self.command[0] = "/kueche"
            if self.command[0] == "/handtücher":
                self.command[0] = "/handtuecher"
            chores(self)
        except Exception:
            logging.error("General error in chores(), #2010")
            self.sender.sendMessage("Fehler #2010")
    if self.command[0] == "/bahn":
        # noinspection PyBroadException
        try:
            bahn(self)
        except Exception:
            logging.error("General error in bahn(), #2012")
            self.sender.sendMessage("Fehler #2012")
    if self.command[0] == "/reboot" and self.chatid in LEGIT_IDS:
        # noinspection PyBroadException
        try:
            reboot(self, msg)
        except Exception:
            logging.error("General error in reboot(), #2013")
            self.sender.sendMessage("Fehler #2013")
    if self.command[0] == "/reload" and self.chatid in LEGIT_IDS:
        # noinspection PyBroadException
        try:
            reload(self)
        except Exception:
            logging.error("General error in reload(), #2014")
            self.sender.sendMessage("Fehler #2014")
    if self.command[0] in ["/geld", "/Geld"] and self.chatid in LEGIT_IDS:
        # noinspection PyBroadException
        try:
            geld(self)
        except Exception:
            logging.error("General error in geld(), #2016")
            self.sender.sendMessage("Fehler #2016")
    if self.command[0] == "/mensa":
        # noinspection PyBroadException
        try:
            speiseplan(self)
        except Exception:
            self.sender.sendMessage("Fehler #2017, bitte erneut versuchen!")
            logging.exception("General error in speiseplan(), #2017")
    if self.command[0] == "/wetter":
        # noinspection PyBroadException
        try:
            weather(self)
        except Exception:
            self.sender.sendMessage("Fehler #2018, bitte erneut versuchen!")
            logging.exception("General error in weather(), #2018")


def choose_callback_command(self, msg):
    """
    route callback query to corresponding function
    """
    if self.query_data == "balance":
        # noinspection PyBroadException
        try:
            show_balance(self)
        except Exception:
            logging.exception("General error in show_balance(), #2001")
            self.sender.sendMessage("Fehler #2001")
            return
    if self.query_data == "transaction":
        # noinspection PyBroadException
        try:
            make_transaction(self, msg)
        except Exception:
            logging.exception("General error in make_transaction(), #2002")
            self.sender.sendMessage("Fehler #2002")
            return
    if self.query_data == "billing":
        # noinspection PyBroadException
        try:
            neuer_einkauf(self, msg)
        except Exception:
            logging.exception("General error in neuer_einkauf(), #2003")
            self.sender.sendMessage("Fehler #2003")
            return
    if self.query_data == "history":
        # noinspection PyBroadException
        try:
            show_history(self)
        except Exception:
            logging.exception("General error in show_history(), #2004")
            self.sender.sendMessage("Fehler #2004")
            return
    if self.query_data == "delete":
        # noinspection PyBroadException
        try:
            delete_last_record(self, msg)
        except Exception:
            logging.exception("General error in delete_last_record(), #2005")
            self.sender.sendMessage("Fehler #2005")
            return
    if self.query_data == "garbage_take_responsibility":
        # noinspection PyBroadException
        try:
            self.sender.sendMessage(f"{msg['from']['first_name']} übernimmt. Ehre!")
        except Exception:
            logging.exception("General error , #20005")
            self.sender.sendMessage("Fehler #2005")
            return
    if self.query_data == "garbage_not_full":
        # noinspection PyBroadException
        try:
            self.sender.sendMessage(f"{msg['from']['first_name']} meint: Müll ist noch nicht voll.")
        except Exception:
            logging.exception("General error , #20005")
            self.sender.sendMessage("Fehler #2005")
            return
    if self.query_data == "garbage_already_done":
        # noinspection PyBroadException
        try:
            self.sender.sendMessage(f"{msg['from']['first_name']} meint: Müll ist schon draußen. Nice!")
        except Exception:
            logging.exception("General error , #20005")
            self.sender.sendMessage("Fehler #2005")
            return
