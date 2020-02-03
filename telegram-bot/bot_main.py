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
    handles all incoming messages
    """
    print(msg)
    content_type, chat_type, chat_id = telepot.glance(msg)
    if str(chat_id) not in LEGIT_IDS:
        bot.sendMessage(msg['chat']['id'], f"It seems you do not have access rights to this bot.\n\nYour Telegram ID "
                                           f"is: <b>{msg['from']['id']}</b>.\n\nUse it to ask for permission to use "
                                           f"this bot.", parse_mode="html")
    try:
        if msg['animation']:
            print("Animation detected!")
            handle_gif(msg, bot)
    except KeyError:
        pass
    try:
        if msg['photo']:
            print("Image detected!")
            # print(msg['photo'][0]['file_id'])
            handle_img(msg, bot)
    except KeyError:
        pass
    if content_type == 'text' and chat_type == "private":
        if str(chat_id) in LEGIT_IDS:
            choose_command(bot, msg)
        else:
            logging.info(f"Not in legit IDs: {msg['chat']['first_name']}, {msg['chat']['id']}")
    elif content_type == 'text' and chat_type == "group":
        try:
            if msg['entities'][0]['type'] == 'mention' or msg['entities'][0]['type'] == 'bot_command':
                if str(chat_id) in LEGIT_IDS:
                    choose_command(bot, msg)
                else:
                    logging.info(f"Not in legit IDs: {msg['chat']['title']}, {msg['chat']['id']}")
        except KeyError:
            pass
    elif str(chat_id) not in LEGIT_IDS:
        bot.sendMessage(msg['chat']['id'], f"It seems you do not have access rights to this bot.\n\nYour Telegram ID "
                                           f"is: <b>{msg['from']['id']}</b>.\n\nUse it to ask for permission to use "
                                           f"this bot.", parse_mode="html")
    else:
        logging.debug("Invalid input given")


MessageLoop(bot, handle).run_as_thread()
schedule.every().day.at("00:02").do(update_putzplan)


while True:
    schedule.run_pending()
    time.sleep(10)
