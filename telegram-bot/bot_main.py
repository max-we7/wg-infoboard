import time
import telepot
import schedule
import logging
from telepot.loop import MessageLoop
from bot_commands import choose_command
from putzplan import update_putzplan
from config import API_KEY, LEGIT_IDS
from gif_handler import handle_gif, handle_img

logging.basicConfig(filename="bot.log", filemode="a+", format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

bot = telepot.Bot(API_KEY)


def handle(msg):
    """
    handle all incoming messages
    """
    print(msg)  # print all incoming messages for easy debugging
    content_type, chat_type, chat_id = telepot.glance(msg)
    if str(chat_id) in LEGIT_IDS:
        try:
            if msg['animation']:
                handle_gif(msg, bot)
        except KeyError:
            pass
        try:
            if msg['photo']:
                handle_img(msg, bot)
        except KeyError:
            pass
        if content_type == 'text':
            choose_command(bot, msg)
        else:
            logging.debug(f"Invalid input given: {msg}")
    else:
        bot.sendMessage(msg['chat']['id'], f"It seems you do not have access rights to this bot.\n\nYour Telegram ID "
                                           f"is: <b>{msg['from']['id']}</b>.\n\nUse it to ask for permission to use "
                                           f"this bot.", parse_mode="html")
        logging.info(f"Not in legit IDs: {msg['from']['first_name']}, {msg['from']['id']}")


# noinspection PyBroadException
try:
    MessageLoop(bot, handle).run_as_thread()
    schedule.every().day.at("00:02").do(update_putzplan)
    # schedule.every().day.at("14:00").do(testf)
    while True:
        schedule.run_pending()
        time.sleep(10)
except Exception as e:
    logging.error("Program failure!")


def testf():
    pass
