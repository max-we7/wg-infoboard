import sys
sys.path.insert(1, '../../')
import platform
import subprocess
import time
import telepot
import schedule
import logging
import json
import telepot.helper
from datetime import datetime
from telepot.loop import MessageLoop
from telepot.delegate import create_open, pave_event_space, include_callback_query_chat_id, per_chat_id
from putzplan import update_putzplan
from zaw_query import update_muell, check_muell_due
from python.api.rmv import update_infoboard_bahn
from config import API_KEY, LEGIT_IDS, ADMIN_IDS
from python.media_handler import handle_img, handle_gif
from commandhandler import choose_command, choose_callback_command

logging.basicConfig(filename="main/wg-infoboard.log", filemode="a+", format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


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

        # Speiseplan state variables
        self.speiseplan_flag1 = False
        self.speiseplan_flag2 = False
        self.speiseplan_flag3 = False
        self.fav_flag1_speiseplan = False
        self.fav_flag2_speiseplan = False
        self.fav_flag3_speiseplan = False

        # Wetter state variables
        self.wetter_flag1 = False
        self.wetter_flag2 = False
        self.wetter_flag3 = False
        self.fav_flag1_wetter = False
        self.fav_flag2_wetter = False
        self.fav_flag3_wetter = False

        # Einkauf state variables
        self.eingekauft_flag1 = False

    def on_chat_message(self, msg):
        logging.debug(f"{msg}")
        print(msg)
        content_type, chat_type, cid = telepot.glance(msg)
        logging.debug(f"{content_type}, {chat_type}, {cid}")
        self.chatid = str(cid)
        if chat_type == "private": self.load_cookies(msg)
        if self.chatid in LEGIT_IDS:
            if content_type == "document":
                handle_gif(self, msg)
            if content_type == "photo":
                handle_img(self, msg)
        else:
            logging.info(f"Not in legit IDs: {self.chatid}")
        if content_type == 'text':
            self.command = msg['text'].split(" ")
            choose_command(self, msg)
        if chat_type == "private": self.dump_cookies()

    def on_callback_query(self, msg):
        print(msg)
        logging.debug(f"{msg}")
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        self.query_data = query_data
        choose_callback_command(self, msg)

    def load_cookies(self, msg):
        fileurl = f"../../data/cookies/{self.chatid}.json"
        logging.debug(f"Cookie file path (load): {fileurl}")
        try:
            with open(fileurl, "r", encoding='utf-8') as f:
                self.cookies = json.load(f)
                self.cookies['info']['last_seen'] = str(datetime.now())
        except FileNotFoundError:
            logging.info("no cookie file found. Creating cookie dictionary!")
            self.sender.sendMessage(f"Hallo {msg['from']['first_name']}!\n\n>> /help <<")
            logging.debug("Welcome message sent")
            try:
                username = msg['from']['username']
            except KeyError:
                username = "None"
            self.cookies = {
                "info": {
                    "first_name": msg['from']['first_name'],
                    "username": username,
                    "last_seen": str(datetime.now()),
                    "language_code": msg['from']['language_code']
                },
                "bahn": {
                    "fav1": {},
                    "fav2": {},
                    "fav3": {}
                },
                "mensa": {
                    "fav1": {},
                    "fav2": {}
                }
            }
            logging.debug("New cookie dictionary created")

    def dump_cookies(self):
        fileurl = f"../../data/cookies/{self.chatid}.json"
        logging.debug(f"Cookie file path (dump): {fileurl}")
        try:
            with open(fileurl, "w") as f:
                json.dump(self.cookies, f, indent=4)
                logging.debug("dumped cookie. no errors.")
        except FileNotFoundError:
            logging.error("Error dumping Cookie!, #0003")
            self.sender.sendMessage("Fehler #0003")


bot = telepot.DelegatorBot(API_KEY, [
    include_callback_query_chat_id(
        pave_event_space())(
        per_chat_id(), create_open, MessageHandler, timeout=60),
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
        schedule.every().day.at("00:01").do(update_putzplan)
        schedule.every().day.at("00:02").do(update_muell)
        schedule.every().day.at("22:00").do(check_muell_due)
        schedule.every(4).minutes.do(update_infoboard_bahn)
        # TODO: run news updating with schedule instead of cronjob

        # check if weather widget still updates
        #schedule.every(50).minutes.do(reload_service)
    except Exception:
        logging.error("Error running scheduled tasks in main, #0002")
        telepot.Bot(API_KEY).sendMessage(ADMIN_IDS[0], "Error running scheduled tasks, #0002")

    while 1:
        time.sleep(10)
        schedule.run_pending()
except Exception:
    telepot.Bot(API_KEY).sendMessage(ADMIN_IDS[0], "Error: program failure, #0001")
    logging.exception("Program Crash in main, #0001")
