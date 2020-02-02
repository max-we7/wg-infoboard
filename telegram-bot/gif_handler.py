import imageio
import os
import sys


def handle_gif(msg, bot):
    bot.download_file(msg['document']['file_id'], '../data/video.mp4')
    bot.sendMessage(msg['chat']['id'], "downloading... done")
    convert_to_gif(msg, bot)
    bot.sendMessage(msg['chat']['id'], "done.")


def handle_img(msg, bot):
    pass


def convert_to_gif(msg, bot):
    try:
        inputpath = "../data/video.mp4"
        target_format = ".gif"
        outputpath = os.path.splitext(inputpath)[0] + target_format
        bot.sendMessage(msg['chat']['id'], "converting to GIF... please wait...")

        reader = imageio.get_reader(inputpath)
        fps = reader.get_meta_data()['fps']

        writer = imageio.get_writer(outputpath, fps=fps)
        for i, im in enumerate(reader):
            sys.stdout.write("\rframe {0}".format(i))
            sys.stdout.flush()
            writer.append_data(im)
        writer.close()
    except Exception as e:
        bot.sendMessage(msg['chat']['id'], "error converting GIF")
