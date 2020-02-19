import telepot
from telepot.namedtuple import ReplyKeyboardRemove
import re
import logging
from python.keyboards import kb_finance_start, kb_teilnehmer, kb_ja_nein, kb_wg_bewohner
from python.sheets_connector import get_balances, get_history, add_entry, delete_entry, get_balances_raw
import random
from python.config import GROUP_ID


def geld(self):
    """
    show finance start dialogue
    """
    self.current_message_id = self.sender.sendMessage("Was möchtest du tun?", reply_markup=kb_finance_start)


def show_balance(self):
    """
    show balance of all users
    """
    self._editor = telepot.helper.Editor(self.bot, self.current_message_id)
    # noinspection PyBroadException
    try:
        balances = get_balances_raw()
    except Exception:
        logging.error("Error loading balances, #1003")
        self.sender.sendMessage("Fehler #1003")
        return
    self._editor.editMessageText(f"Aktuelle Kontostände:\n\n"
                                 f"Max: <b>{balances[0][1]}</b>\nNawid: <b>{balances[1][1]}</b>\n"
                                 f"Noah: <b>{balances[2][1]}</b>\nSeb: <b>{balances[3][1]}</b>", parse_mode='html')


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
                      f"({self.preis} €) </b>wurde angelegt!"
            self.sender.sendMessage(message, parse_mode='html')
            self._bot.sendMessage(GROUP_ID, message, parse_mode='html')
        else:
            self.sender.sendMessage("Ungültige Eingabe. Bitte im Format X,XX und ohne Währungssymbol eingeben:")
    elif self.empfaenger_flag:
        self.einkaeufer = msg['from']['first_name'] if msg['from']['first_name'] != "Simmy" else "Seb"
        if msg['text'] in ["Max", "Nawid", "Noah", "Seb"]:
            if msg['text'] != self.einkaeufer:
                self.empfaenger = msg['text']
                self.empfaenger_flag, self.betrag_flag = False, True
                self.sender.sendMessage("Wie viel Geld möchtest du überweisen?", reply_markup=ReplyKeyboardRemove())
            else:
                self.sender.sendMessage("Du kannst dir nicht selbst Geld überweisen ;) ...setze zurück...",
                                        reply_markup=ReplyKeyboardRemove())
                self.empfaenger_flag = False
        else:
            self.sender.sendMessage("Ungültige Eingabe! Setze zurück...", reply_markup=ReplyKeyboardRemove())
            self.empfaenger_flag = False
    else:
        self.empfaenger_flag = True
        self._editor3 = telepot.helper.Editor(self.bot, self.current_message_id)
        self._editor3.editMessageText("Was möchtest du tun?")
        self.sender.sendMessage("Neue Überweisung. An wen hast du Geld überwiesen?", reply_markup=kb_wg_bewohner)


def neuer_einkauf(self, msg):
    """
    create new financial transaction
    """
    if self.teilnehmer_flag:
        if msg['text'] not in ["Max", "Nawid", "Noah", "Seb", "Alle", "Fertig!"]:
            self.sender.sendMessage("Inkorrekter Name. setze Anfrage zurück...")
            self.teilnehmer_flag = False
            self.teilnehmer = []
        if msg['from']['first_name'] != "Simmy" and msg['from']['first_name'] not in self.teilnehmerliste:
            self.teilnehmerliste.append(msg['from']['first_name'])
        elif msg['from']['first_name'] == "Simmy" and "Seb" not in self.teilnehmerliste:
            self.teilnehmerliste.append("Seb")
        if msg['text'] != "Fertig!" and msg['text'] != "Alle":
            if msg['text'] not in self.teilnehmerliste:
                self.teilnehmerliste.append(msg['text'])
        else:
            if msg['text'] == "Alle":
                self.teilnehmerliste = ["Alle"]
            if len(self.teilnehmerliste) == 1 and "Alle" not in self.teilnehmerliste:
                self.sender.sendMessage("Bitte wähle außer dir selbst mindestens eine weitere Person aus!")
                return
            self.teilnehmer_flag = False
            self.sender.sendMessage(f"Eintrag wird angelegt... bitte warten", reply_markup=ReplyKeyboardRemove())
            # noinspection PyBroadException
            try:
                calculate_money(self)
            except Exception:
                logging.error("Error calculating transaction, #1001")
                self.sender.sendMessage("Fehler #1001")
                return
            self.sender.sendMessage(f"Finanzeintrag <b>{self.artikel} ({self.preis} €) </b>wurde angelegt!",
                                    parse_mode='html')
            self._bot.sendMessage(GROUP_ID, f"{self.einkaeufer} hat den Finanzeintrag <b>{self.artikel} "
                                            f"({self.preis} €) </b>angelegt!", parse_mode='html')
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
        self._editor2 = telepot.helper.Editor(self.bot, self.current_message_id)
        self._editor2.editMessageText("Neuer Eintrag:\nWas hast du eingekauft?")
        self.artikel_flag = True
        if msg['from']['first_name'] == "Simmy":
            self.einkaeufer = "Seb"
        else:
            self.einkaeufer = msg['from']['first_name']


def calculate_money(self):
    """
    helper function for neuer_einkauf(), calculates new balances
    """
    balances, date = get_balances()
    item_preis = int(self.preis.replace(',', ''))
    beteiligte = []
    if "Alle" in self.teilnehmerliste:
        beteiligte = ["Max", "Nawid", "Noah", "Seb"]
    else:
        for teilnehmer in self.teilnehmerliste:
            beteiligte.append(teilnehmer)
    preis_anteil = len(beteiligte)

    rest = 0
    while item_preis % preis_anteil != 0:
        item_preis -= 1
        rest += 1

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
    if integrity != 0: self.sender.sendMessage("Integritätscheck fehlgeschlagen. Bitte Transaktionen prüfen!")

    anteilig_wert = str(int(item_preis / preis_anteil))
    if re.match('^[0-9]{2}$', anteilig_wert):
        anteilig_wert = f"0{anteilig_wert}"
    anteilig_wert = f"{anteilig_wert[:-2]},{anteilig_wert[-2:]} €"

    if len(self.teilnehmerliste) == 4 or "Alle" in self.teilnehmerliste:
        self.teilnehmerliste = ["Alle"]
    teilnehmer_formatted = ""
    self.teilnehmerliste.sort()
    for teilnehmer in self.teilnehmerliste:
        teilnehmer_formatted += f"{teilnehmer}, "

    new_row = [date, self.einkaeufer, self.artikel, f"{self.preis} €", teilnehmer_formatted[:-2], anteilig_wert,
               balances['Max'], balances['Nawid'], balances['Noah'], balances['Seb']]

    add_entry(new_row)
    self.teilnehmerliste = []


def calculate_transaction(self):
    """
    helper function for new_transaction(), calculates new balances
    """
    balances, date = get_balances()

    transaction_value = int(self.preis.replace(',', ''))
    transaction_recipient = self.empfaenger
    transaction_sender = self.einkaeufer
    balances[transaction_sender] -= transaction_value
    balances[transaction_recipient] += transaction_value

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
    if integrity != 0: self.sender.sendMessage("Integritätscheck fehlgeschlagen. Bitte Transaktionen prüfen!")

    print(transaction_value)
    if re.match('^[0-9]{2}$', str(transaction_value)):
        transaction_value = f"0{transaction_value}"
    transaction_value = f"{str(transaction_value)[:-2]},{str(transaction_value)[-2:]} €"

    new_row = [date, transaction_sender, "ÜBERWEISUNG", f"{transaction_value}", transaction_recipient,
               transaction_value, balances['Max'], balances['Nawid'], balances['Noah'], balances['Seb']]
    # noinspection PyBroadException
    add_entry(new_row)


def show_history(self):
    """
    return the three most recent transactions for the user to see
    """
    self._editor3 = telepot.helper.Editor(self.bot, self.current_message_id)
    self._editor3.editMessageText("Querying Google Sheets ... please wait")
    # noinspection PyBroadException
    try:
        histories = get_history()
    except Exception:
        logging.error("Error retrieving history, #1004")
        self.sender.sendMessage("Fehler #1004")
        return
    for history in histories:
        self.sender.sendMessage(f"{history[0]}: {history[1]} hat {history[2]} für {history[4]} gekauft\n"
                                f"Preis: {history[3]} - anteilig: {history[5]}\n\n"
                                f"aktualisierte Kontostände:\nMax: {history[6]} - Nawid: {history[7]} - "
                                f"Noah: {history[8]} - Seb: {history[9]}")
    self._editor3.editMessageText("Kürzliche Transaktionen:")


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
            if msg['from']['first_name'] == "Simmy":
                self.einkaeufer = "Seb"
            else:
                self.einkaeufer = msg['from']['first_name']
            self._bot.sendMessage(GROUP_ID, f"{self.einkaeufer} hat den letzten Finanzeintrag gelöscht",
                                  parse_mode='html')
            self.delete_flag = False
        else:
            self.sender.sendMessage("Vorgang abgebrochen.", reply_markup=ReplyKeyboardRemove())
            self.delete_flag = False
    else:
        self.delete_flag = True
        self._editor = telepot.helper.Editor(self.bot, self.current_message_id)
        self._editor.deleteMessage()
        self.sender.sendMessage("Bist du sicher, dass du den letzten Eintrag löschen möchtest?",
                                reply_markup=kb_ja_nein)
