def handle_gif(msg, bot):
    print("starting download")
    bot.download_file(msg['document']['file_id'], '../data/gif.mp4')
    print("downloaded")
    pass


def handle_img(msg, bot):
    pass

