import ffmpy


def handle_gif(msg, bot):
    print("starting download")
    bot.download_file(msg['document']['file_id'], '../data/video.mp4')
    ff = ffmpy.FFmpeg(
        inputs={"video.mp4": None},
        outputs={"animation.gif": None})

    ff.run
    print("downloaded")
    pass


def handle_img(msg, bot):
    pass

