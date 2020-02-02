import imageio
import os
import sys
import telepot
import subprocess
import platform


def handle_gif(msg, bot):
    bot.download_file(msg['document']['file_id'], '../data/video.mp4')
    bot.sendMessage(msg['chat']['id'], "downloading file... done!")
    convert_to_gif(msg, bot)
    if platform.system() == "Linux":
        subprocess.run(["sudo", "service", "kiosk.sh", "restart"])
        bot.sendMessage(msg['chat']['id'], "flushing browser cache... done!")
    else:
        bot.sendMessage(msg['chat']['id'], "cache flushing failed.")


def handle_img(msg, bot):
    pass


def convert_to_gif(msg, bot):
    try:
        inputpath = "../data/video.mp4"
        target_format = ".gif"
        outputpath = os.path.splitext(inputpath)[0] + target_format
        sent_message = bot.sendMessage(msg['chat']['id'], "starting conversion to GIF...")
        message_id = telepot.message_identifier(sent_message)

        reader = imageio.get_reader(inputpath)
        fps = reader.get_meta_data()['fps']

        writer = imageio.get_writer(outputpath, fps=fps)
        total_frames = -1
        for j in enumerate(reader):
            total_frames += 1
        for i, im in enumerate(reader):
            bot.editMessageText(message_id, f"Converting to GIF: Frame {i} of {total_frames}...")
            sys.stdout.write("\rframe {0}".format(i))
            sys.stdout.flush()
            writer.append_data(im)
        writer.close()
    except Exception as e:
        bot.sendMessage(msg['chat']['id'], "error converting GIF")
