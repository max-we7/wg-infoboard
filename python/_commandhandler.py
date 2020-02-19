from _putzplan import chores
from _general_commands import insult, einkaufen, eingekauft, bahn, help_commands, reload, reboot, git_pull, loc
from _finances import geld, show_balance, make_transaction, neuer_einkauf, show_history, delete_last_record
import logging
from speiseplan import speiseplan


def choose_command(self, msg):
    """
    route chat message to corresponding function
    """
    if self.artikel_flag or self.preis_flag or self.teilnehmer_flag:
        neuer_einkauf(self, msg)
        return
    if self.delete_flag:
        delete_last_record(self, msg)
        return
    if self.empfaenger_flag or self.betrag_flag:
        make_transaction(self, msg)
        return
    if self.command[0] == "/einkaufen":
        # noinspection PyBroadException
        try:
            einkaufen(self, msg)
        except Exception:
            logging.error("General error in einkaufen(), #2006")
            self.sender.sendMessage("Fehler #2006")
            return
    if self.command[0] == "/eingekauft":
        # noinspection PyBroadException
        try:
            eingekauft(self, msg)
        except Exception:
            logging.error("General error in eingekauft(), #2007")
            self.sender.sendMessage("Fehler #2007")
            return
    if self.command[0] == "/insult":
        # noinspection PyBroadException
        try:
            insult(self, msg)
        except Exception:
            logging.error("General error in insult(), #2008")
            self.sender.sendMessage("Fehler #2008")
            return
    if self.command[0] == "/help":
        # noinspection PyBroadException
        try:
            help_commands(self)
        except Exception:
            logging.error("General error in help_commands(), #2009")
            self.sender.sendMessage("Fehler #2009")
            return
    if self.command[0] in ["/muell", "/glas", "/bad", "/kueche", "/saugen", "/handtuecher", "/duschvorhang"]:
        # noinspection PyBroadException
        try:
            chores(self)
        except Exception:
            logging.error("General error in chores(), #2010")
            self.sender.sendMessage("Fehler #2010")
            return
    if self.command[0] == "/loc":
        # noinspection PyBroadException
        try:
            loc(self)
        except Exception:
            logging.error("General error in loc(), #2011")
            self.sender.sendMessage("Fehler #2011")
            return
    if self.command[0] == "/bahn":
        # noinspection PyBroadException
        try:
            bahn(self)
        except Exception:
            logging.error("General error in bahn(), #2012")
            self.sender.sendMessage("Fehler #2012")
            return
    if self.command[0] == "/reboot":
        # noinspection PyBroadException
        try:
            reboot(self, msg)
        except Exception:
            logging.error("General error in reboot(), #2013")
            self.sender.sendMessage("Fehler #2013")
            return
    if self.command[0] == "/reload":
        # noinspection PyBroadException
        try:
            reload(self, msg)
        except Exception:
            logging.error("General error in reload(), #2014")
            self.sender.sendMessage("Fehler #2014")
            return
    if self.command[0] == "/git pull":
        # noinspection PyBroadException
        try:
            git_pull(self, msg)
        except Exception:
            logging.error("General error in git_pull(), #2015")
            self.sender.sendMessage("Fehler #2015")
            return
    if self.command[0] == "/geld":
        # noinspection PyBroadException
        try:
            geld(self)
        except Exception:
            logging.error("General error in geld(), #2016")
            self.sender.sendMessage("Fehler #2016")
            return
    if self.command[0] == "/mensa":
        # noinspection PyBroadException
        try:
            speiseplan(self)
        except Exception:
            logging.error("General error in mensa(), #2017")
            self.sender.sendMessage("Fehler #2017")
            return


def choose_callback_command(self, msg):
    """
    route callback query to corresponding function
    """
    if self.query_data == "balance":
        # noinspection PyBroadException
        try:
            show_balance(self)
        except Exception:
            logging.error("General error in show_balance(), #2001")
            self.sender.sendMessage("Fehler #2001")
            return
    if self.query_data == "transaction":
        # noinspection PyBroadException
        try:
            make_transaction(self, msg)
        except Exception:
            logging.error("General error in make_transaction(), #2002")
            self.sender.sendMessage("Fehler #2002")
            return
    if self.query_data == "billing":
        # noinspection PyBroadException
        try:
            neuer_einkauf(self, msg)
        except Exception:
            logging.error("General error in neuer_einkauf(), #2003")
            self.sender.sendMessage("Fehler #2003")
            return
    if self.query_data == "history":
        # noinspection PyBroadException
        try:
            show_history(self)
        except Exception:
            logging.error("General error in show_history(), #2004")
            self.sender.sendMessage("Fehler #2004")
            return
    if self.query_data == "delete":
        # noinspection PyBroadException
        try:
            delete_last_record(self, msg)
        except Exception:
            logging.error("General error in delete_last_record(), #2005")
            self.sender.sendMessage("Fehler #2005")
            return
