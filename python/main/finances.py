import telepot
from telepot import message_identifier
from telepot.namedtuple import ReplyKeyboardRemove
import re
import logging
from keyboards import kb_finance_start, kb_teilnehmer, kb_ja_nein, kb_wg_bewohner
from python.api.sheets_connector import get_balances, get_history, add_entry, delete_entry, get_balances_raw
import random
from python.main.config import GROUP_ID, wg_members, wg, finanz_spreadsheet_link, API_KEY
from datetime import datetime


def geld(self):
    """
    show finance start dialog
    """
    self.current_message_id = self.sender.sendMessage("Was möchtest du tun?", reply_markup=kb_finance_start)


def show_balance(self):
    """
    show balance of all users
    """
    # noinspection PyBroadException
    try:
        balances = get_balances_raw()
    except Exception:
        logging.error("Error loading balances, #1003")
        self.sender.sendMessage("Fehler #1003")
        return
    telepot.Bot(API_KEY).editMessageText(message_identifier(self.current_message_id),
                                         f"Aktuelle Kontostände:\n\n"
                                         f"{wg_members[0]}: \U0001F4B0<b>{balances[0][1]}</b>\n{wg_members[1]}: "
                                         f"\U0001F4B0<b>{balances[1][1]}</b>\n{wg_members[2]}: \U0001F4B0<b>"
                                         f"{balances[2][1]}</b>\n{wg_members[3]}: \U0001F4B0<b>{balances[3][1]}</b>",
                                         parse_mode='html')


def make_transaction(self, msg):
    """
    make a transaction from one account to another
    """
    if self.betrag_flag:
        if re.match('^[0-9]{1,3},[0-9]{2}$', msg['text']):
            self.preis = msg['text']
            self.betrag_flag = False
            self.sender.sendMessage(f"Eintrag wird angelegt... bitte warten")
            # noinspection PyBroadException
            try:
                calculate_transaction(self)
            except Exception:
                logging.error("Error calculating transaction, #1002")
                self.sender.sendMessage("Fehler #1002")
                return
            message = f"Überweisung von <b>{self.einkaeufer} </b>an<b> {self.empfaenger} " \
                      f"(\U0001F4B0{self.preis} €) </b>wurde angelegt!"
            self.sender.sendMessage(message, parse_mode='html')
            self._bot.sendMessage(GROUP_ID, message, parse_mode='html')
        else:
            self.sender.sendMessage("Ungültige Eingabe. Bitte den Betrag im Format X,XX und ohne Währungssymbol "
                                    "eingeben:")
    elif self.empfaenger_flag:
        self.einkaeufer = wg[str(msg['from']['id'])]
        if msg['text'] in wg_members:
            if msg['text'] != self.einkaeufer:
                self.empfaenger = msg['text']
                self.empfaenger_flag, self.betrag_flag = False, True
                self.sender.sendMessage("Wie viel Geld möchtest du überweisen?", reply_markup=ReplyKeyboardRemove())
            else:
                self.sender.sendMessage("Du kannst dir nicht selbst Geld überweisen \U0001F926",
                                        reply_markup=ReplyKeyboardRemove())
                self.empfaenger_flag = False
        else:
            self.sender.sendMessage("Ungültige Eingabe! Setze zurück...", reply_markup=ReplyKeyboardRemove())
            self.empfaenger_flag = False
    else:
        self.empfaenger_flag = True
        telepot.Bot(API_KEY).editMessageText(message_identifier(self.current_message_id), "Neue Überweisung.")
        self.sender.sendMessage("An wen möchtest du Geld überwiesen?", reply_markup=kb_wg_bewohner)


def neuer_einkauf(self, msg):
    """
    create new financial transaction
    """
    if self.teilnehmer_flag:
        if msg['text'] not in wg_members and msg['text'] not in ["Alle", "Fertig!"]:
            self.sender.sendMessage("Inkorrekte Eingabe. setze Anfrage zurück...")
            self.teilnehmer_flag = False
            self.teilnehmer = []
        if msg['text'] not in ["Alle", "Fertig!"] and msg['text'] not in self.teilnehmerliste and "Alle" not \
                in self.teilnehmerliste:
            self.teilnehmerliste.append(msg['text'])
        elif msg['text'] == "Alle":
            self.teilnehmerliste = ["Alle"]
        elif msg['text'] == "Fertig!":
            if len(self.teilnehmerliste) == 1 and wg[str(msg['from']['id'])] in self.teilnehmerliste:
                self.sender.sendMessage("Bitte wähle außer dir selbst mindestens eine weitere Person aus!")
            elif len(self.teilnehmerliste) == 0:
                self.sender.sendMessage("Bitte wähle mindestens eine Person aus!")
            else:
                if len(self.teilnehmerliste) == 4: self.teilnehmerliste = ["Alle"]
                self.teilnehmer_flag = False
                self.sender.sendMessage(f"Eintrag wird angelegt... bitte warten", reply_markup=ReplyKeyboardRemove())
                # noinspection PyBroadException
                try:
                    calculate_money(self)
                except Exception:
                    # noinspection PyBroadException
                    try:
                        logging.error("Error calculating transaction, #1001")
                        self.sender.sendMessage("Fehler #1001")
                        return
                    except Exception:
                        pass
                logging.debug("breakpoint 1")
                self.sender.sendMessage(f"Finanzeintrag <b>{self.artikel} (\U0001F4B0{self.preis} €) "
                                        f"</b>wurde angelegt!", parse_mode='html')
                teilnehmer = ""
                for person in self.teilnehmerliste:
                    teilnehmer = teilnehmer + person + ", "
                self._bot.sendMessage(GROUP_ID, f"{self.einkaeufer} hat den Finanzeintrag <b>{self.artikel} "
                                                f"(\U0001F4B0{self.preis} €) </b>für {teilnehmer[:-2]} angelegt!",
                                      parse_mode='html')
                self.teilnehmerliste.clear()
    elif self.preis_flag:
        if re.match('^[0-9]{1,3},[0-9]{2}$', msg['text']):
            self.preis = msg['text']
        else:
            self.sender.sendMessage("Ungültige Eingabe. Bitte im Format X,XX und ohne Währungssymbol eingeben:")
            return
        self.preis_flag, self.teilnehmer_flag = False, True
        self.current_message_id = self.sender.sendMessage("Für wen hast du eingekauft?", reply_markup=kb_teilnehmer)
    elif self.artikel_flag:
        self.artikel = str(msg['text'])
        self.artikel_flag, self.preis_flag = False, True
        self.sender.sendMessage(f"Was hast du für <b>{self.artikel}</b> bezahlt?", parse_mode='html')
    else:
        telepot.Bot(API_KEY).editMessageText(message_identifier(self.current_message_id), "Neuer Eintrag:\nWas hast "
                                                                                          "du eingekauft?")
        self.artikel_flag = True
        self.einkaeufer = wg[str(msg['from']['id'])]


def calculate_money(self):
    """
    helper function for neuer_einkauf(), calculates new balances
    """
    balances = get_balances()
    item_preis = int(self.preis.replace(',', ''))
    beteiligte = []

    if "Alle" in self.teilnehmerliste:
        beteiligte = wg_members[:]
    else:
        for teilnehmer in self.teilnehmerliste:
            beteiligte.append(teilnehmer)
    preis_anteil = len(beteiligte)

    rest = 0
    while item_preis % preis_anteil != 0:
        item_preis -= 1
        rest += 1

    if self.einkaeufer not in beteiligte:
        balances[self.einkaeufer] += item_preis
    for person in beteiligte:
        if person == self.einkaeufer:
            balances[person] += (item_preis / preis_anteil * (preis_anteil - 1))
        else:
            balances[person] -= (item_preis / preis_anteil)

    if rest != 0:
        losers = []
        for i in range(rest):
            loser = random.choice(beteiligte)
            losers.append(loser)
            beteiligte.remove(loser)
        for loser in losers:
            if loser == self.einkaeufer:
                rest -= 1
            else:
                balances[loser] -= 1
        balances[self.einkaeufer] += rest

    # Integrity Variable
    integrity = 0

    for person in balances.keys():
        integrity += balances[person]
        balances[person] = str(int(balances[person]))
        if re.match('^[0-9]{2}$', balances[person]):
            balances[person] = f"0{balances[person]}"
        if re.match('^-[0-9]{2}$', balances[person]):
            balances[person] = f"-0{balances[person][1:]}"
        balances[person] = f"{balances[person][:-2]},{balances[person][-2:]} €"

    # Integrity Check
    if integrity != 0:
        self.sender.sendMessage("Integritätscheck fehlgeschlagen. Bitte Transaktionen prüfen!")

    anteilig_wert = str(int(item_preis / preis_anteil))
    if re.match('^[0-9]{2}$', anteilig_wert):
        anteilig_wert = f"0{anteilig_wert}"
    anteilig_wert = f"{anteilig_wert[:-2]},{anteilig_wert[-2:]} €"

    teilnehmer_formatted = ""
    self.teilnehmerliste.sort()
    for teilnehmer in self.teilnehmerliste:
        teilnehmer_formatted += f"{teilnehmer}, "

    new_row = [datetime.now().strftime("%d.%m.%Y"), self.einkaeufer, self.artikel, f"{self.preis} €",
               teilnehmer_formatted[:-2], anteilig_wert, balances[wg_members[0]], balances[wg_members[1]],
               balances[wg_members[2]], balances[wg_members[3]]]
    add_entry(new_row)


def calculate_transaction(self):
    """
    helper function for new_transaction(), calculates new balances
    """
    balances = get_balances()
    transaction_value = int(self.preis.replace(',', ''))
    balances[self.einkaeufer] += transaction_value
    balances[self.empfaenger] -= transaction_value

    # Integrity Variable
    integrity = 0
    for person in balances.keys():
        integrity += balances[person]
        balances[person] = str(int(balances[person]))
        if re.match('^[0-9]{2}$', balances[person]):
            balances[person] = f"0{balances[person]}"
        if re.match('^-[0-9]{2}$', balances[person]):
            balances[person] = f"-0{balances[person][1:]}"
        balances[person] = f"{balances[person][:-2]},{balances[person][-2:]} €"

    # Integrity Check
    if integrity != 0:
        self.sender.sendMessage("Integritätscheck fehlgeschlagen. Bitte Transaktionen prüfen!")

    if re.match('^[0-9]{2}$', str(transaction_value)):
        transaction_value = f"0{transaction_value}"
    transaction_value = f"{str(transaction_value)[:-2]},{str(transaction_value)[-2:]} €"

    new_row = [datetime.now().strftime("%d.%m.%Y"), self.einkaeufer, "ÜBERWEISUNG", f"{transaction_value}",
               self.empfaenger, transaction_value, balances[wg_members[0]], balances[wg_members[1]],
               balances[wg_members[2]], balances[wg_members[3]]]
    add_entry(new_row)


def show_history(self):
    """
    return the three most recent transactions for the user to see
    """
    telepot.Bot(API_KEY).editMessageText(message_identifier(self.current_message_id), "Rufe Daten ab ... bitte warten")
    # noinspection PyBroadException
    try:
        histories = get_history()
    except Exception:
        logging.error("Error retrieving history, #1004")
        self.sender.sendMessage("Fehler #1004")
        return
    for history in histories:
        self.sender.sendMessage(f"{history[0]}: {history[1]} hat <b>{history[2]}</b> für {history[4]} gekauft\n"
                                f"Preis: {history[3]} - anteilig: {history[5]}\n\naktualisierte Kontostände:\n"
                                f"{wg_members[0]}: \U0001F4B0{history[6]} - {wg_members[1]}: \U0001F4B0{history[7]}\n"
                                f"{wg_members[2]}: \U0001F4B0{history[8]} - {wg_members[3]}: \U0001F4B0{history[9]}",
                                parse_mode='html')
    telepot.Bot(API_KEY).editMessageText(message_identifier(self.current_message_id), "Kürzliche Transaktionen "
                                                                                      "(neuste zuerst):")
    self.sender.sendMessage(f"Kompletter Verlauf verfügbar unter: {finanz_spreadsheet_link}")


def delete_last_record(self, msg):
    """
    delete the last transaction made
    """
    if self.delete_flag:
        if msg['text'] == "JA":
            # noinspection PyBroadException
            try:
                delete_entry()
            except Exception:
                logging.error("Error deleting entry, #1005")
                self.sender.sendMessage("Fehler #1005")
                return
            self.sender.sendMessage("Letzer Finanzeintrag wurde gelöscht!", reply_markup=ReplyKeyboardRemove())
            self._bot.sendMessage(GROUP_ID, f"{wg[str(msg['from']['id'])]} hat den letzten Finanzeintrag gelöscht",
                                  parse_mode='html')
            self.delete_flag = False
        else:
            self.sender.sendMessage("Vorgang abgebrochen.", reply_markup=ReplyKeyboardRemove())
            self.delete_flag = False
    else:
        self.delete_flag = True
        telepot.Bot(API_KEY).deleteMessage(message_identifier(self.current_message_id))
        self.sender.sendMessage("Bist du sicher, dass du den letzten Eintrag löschen möchtest?",
                                reply_markup=kb_ja_nein)
