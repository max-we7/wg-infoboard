import imageio
import os
import sys
import telepot
import subprocess
import platform


def handle_gif(self, msg):
    self._bot.download_file(msg['document']['file_id'], '../data/video.mp4')
    self.sender.sendMessage("downloading file... done!")
    convert_to_gif(self)
    if platform.system() == "Linux":
        subprocess.run(["sudo", "rm", "-rf", "/home/pi/.cache/chromium"])
        subprocess.run(["sudo", "service", "kiosk.sh", "restart"])
        self.sender.sendMessage("flushing browser cache... done!")
    else:
        self.sender.sendMessage("cache flushing failed.")


def handle_img(self, msg):
    # TODO: implement
    pass


def convert_to_gif(self):
    # noinspection PyBroadException
    try:
        inputpath = "../data/video.mp4"
        target_format = ".gif"
        outputpath = os.path.splitext(inputpath)[0] + target_format
        sent_message = self.sender.sendMessage("starting conversion to GIF...")
        self._editor5 = telepot.helper.Editor(self.bot, sent_message)

        reader = imageio.get_reader(inputpath)
        fps = reader.get_meta_data()['fps']

        writer = imageio.get_writer(outputpath, fps=fps)
        total_frames = -1
        for j in enumerate(reader):
            total_frames += 1
        for i, im in enumerate(reader):
            self._editor5.editMessageText(f"Converting to GIF: Frame {i} of {total_frames}...")
            sys.stdout.write("\rframe {0}".format(i))
            sys.stdout.flush()
            writer.append_data(im)
        writer.close()
    except Exception as e:
        self.sender.sendMessage("error converting GIF")
        pass
