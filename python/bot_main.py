import platform
import subprocess
import time
import telepot
import schedule
import logging
import telepot.helper
from datetime import datetime
from telepot.loop import MessageLoop
from telepot.delegate import create_open, pave_event_space, include_callback_query_chat_id, per_chat_id
from _putzplan import update_putzplan
from zaw_query import update_muell
from rmv import update_bahn
import json
from read_rss import update_news
from config import API_KEY, LEGIT_IDS, GROUP_ID, ADMIN_IDS
from media_handler import handle_img, handle_gif
from _commandhandler import choose_command, choose_callback_command

# TODO: git_pull(), handle_img()

logging.basicConfig(filename="wg-infoboard.log", filemode="a+", format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class MessageHandler(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)
        self.command = ""
        self.query_data = ""
        self.current_message_id = ""
        self.chatid = ""
        self.cookies = {}

        # Finance state variables
        self.betrag_flag = False
        self.empfaenger_flag = False
        self.delete_flag = False
        self.artikel_flag = False
        self.preis_flag = False
        self.teilnehmer_flag = False
        self.artikel = ""
        self.preis = ""
        self.einkaeufer = ""
        self.empfaenger = ""
        self.teilnehmerliste = []

        # Bahn state variables
        self.bahn_start = False
        self.bahn_search = False
        self.bahn_search2 = False
        self.bahn_search3 = False
        self.bahn_destination_flag = False
        self.search_dest_flag = False
        self.fav_flag1 = False
        self.fav_flag2 = False
        self.fav_flag3 = False
        self.origin = ""
        self.destination = ""
        self.fav_to_be_modified = ""

    def on_chat_message(self, msg):
        content_type, chat_type, cid = telepot.glance(msg)
        self.chatid = str(cid)
        if chat_type == "private": self.load_cookies(msg)
        if self.chatid in LEGIT_IDS:
            if content_type == "document":
                handle_gif(self, msg)
            if content_type == "photo":
                handle_img(self, msg)
        if content_type == 'text':
            self.command = msg['text'].split(" ")
            choose_command(self, msg)
        if chat_type == "private": self.dump_cookies()

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        self.query_data = query_data
        choose_callback_command(self, msg)

    def load_cookies(self, msg):
        fileurl = f"../data/cookies/{self.chatid}.json"
        try:
            with open(fileurl, "r", encoding='utf-8') as f:
                self.cookies = json.load(f)
                self.cookies['info']['last_seen'] = str(datetime.now())
        except FileNotFoundError:
            self.sender.sendMessage(f"Hallo {msg['from']['first_name']}!\n\n>> /help <<")
            self.cookies = {
                "info": {
                    "first_name": msg['from']['first_name'],
                    "username": msg['from']['username'],
                    "last_seen": str(datetime.now()),
                    "language_code": msg['from']['language_code']
                },
                "bahn": {
                    "fav1": {},
                    "fav2": {},
                    "fav3": {}
                }
            }

    def dump_cookies(self):
        fileurl = f"../data/cookies/{self.chatid}.json"
        try:
            with open(fileurl, "w") as f:
                json.dump(self.cookies, f, indent=4)
        except FileNotFoundError:
            logging.error("Error dumping Cookie!, #0003")
            self.sender.sendMessage("Fehler #0003")


bot = telepot.DelegatorBot(API_KEY, [
    include_callback_query_chat_id(
        pave_event_space())(
        per_chat_id(), create_open, MessageHandler, timeout=30),
])


def reload_service():
    if platform.system() == "Linux":
        subprocess.run(["sudo", "service", "kiosk.sh", "restart"])


# noinspection PyBroadException
try:
    MessageLoop(bot).run_as_thread()

    # Define Scheduled Jobs
    # noinspection PyBroadException
    try:
        schedule.every().day.at("00:02").do(update_putzplan)
        schedule.every().day.at("00:02").do(update_muell)
        schedule.every(4).minutes.do(update_bahn)
        schedule.every(10).minutes.do(update_news)
        schedule.every(50).minutes.do(reload_service)
    except Exception:
        logging.error("Error running scheduled tasks in main, #0002")
        telepot.Bot(API_KEY).sendMessage(ADMIN_IDS[0], "Error running scheduled tasks, #0002")

    while 1:
        time.sleep(10)
        schedule.run_pending()
except Exception:
    telepot.Bot(API_KEY).sendMessage(ADMIN_IDS[0], "Error: program failure, #0001")
    logging.exception("Program Crash in main, #0001")
