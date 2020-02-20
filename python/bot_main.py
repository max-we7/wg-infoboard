import time
import telepot
import schedule
import logging
import random
import telepot.helper
from telepot.loop import MessageLoop
from telepot.delegate import create_open, pave_event_space, include_callback_query_chat_id, per_chat_id
from _putzplan import update_putzplan
from insults import insults
from zaw_query import update_muell
from rmv import update_bahn
from read_rss import update_news
from config import API_KEY, LEGIT_IDS, GROUP_ID
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

    def on_chat_message(self, msg):
        content_type, chat_type, cid = telepot.glance(msg)
        self.chatid = str(cid)
        if str(self.chatid) in LEGIT_IDS:
            if content_type == "document":
                handle_gif(self, msg)
            if content_type == "photo":
                handle_img(self, msg)
        if content_type == 'text':
            self.command = msg['text'].split(" ")
            choose_command(self, msg)

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        print(msg)
        self.query_data = query_data
        choose_callback_command(self, msg)


bot = telepot.DelegatorBot(API_KEY, [
    include_callback_query_chat_id(
        pave_event_space())(
        per_chat_id(), create_open, MessageHandler, timeout=30),
])


def dinner_poll():
    insults_plural = []
    for insulty in insults:
        if str(insulty).endswith("er") or str(insulty).endswith("en"):
            insults_plural.append(insulty)
    random_insult = random.choice(insults_plural)
    telepot.Bot(API_KEY).sendMessage(GROUP_ID, f"Hallo ihr {random_insult}! Wer ist heute beim Abendessen am Start?")


# noinspection PyBroadException
try:
    MessageLoop(bot).run_as_thread()

    # Define Scheduled Jobs
    # noinspection PyBroadException
    try:
        schedule.every().day.at("00:02").do(update_putzplan)
        schedule.every().day.at("00:02").do(update_muell)
        schedule.every().monday.at("14:00").do(dinner_poll)
        schedule.every().tuesday.at("14:00").do(dinner_poll)
        schedule.every(4).minutes.do(update_bahn)
        schedule.every(10).minutes.do(update_news)
    except Exception:
        logging.error("Error running scheduled tasks in main, #0002")
        telepot.Bot(API_KEY).sendMessage("341986116", "Error running scheduled tasks, #0002")

    while 1:
        time.sleep(10)
        schedule.run_pending()
except Exception:
    telepot.Bot(API_KEY).sendMessage("341986116", "Error: program failure, #0001")
    logging.critical("Program Crash in main, #0001")
    raise
