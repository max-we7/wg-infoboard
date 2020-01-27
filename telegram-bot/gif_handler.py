# import imageio
# import os
# import sys


def handle_gif(msg, bot):
    print("starting download")
    bot.download_file(msg['document']['file_id'], '../data/video.mp4')
    # convert_to_gif()
    print("downloaded")
    pass


def handle_img(msg, bot):
    pass


# def convert_to_gif():
#     inputpath = "../data/video.mp4"
#     target_format = ".gif"
#     outputpath = os.path.splitext(inputpath)[0] + target_format
#     print("converting\r\n\t{0}\r\nto\r\n\t{1}".format(inputpath, outputpath))
#
#     reader = imageio.get_reader(inputpath)
#     fps = reader.get_meta_data()['fps']
#
#     writer = imageio.get_writer(outputpath, fps=fps)
#     for i, im in enumerate(reader):
#         sys.stdout.write("\rframe {0}".format(i))
#         sys.stdout.flush()
#         writer.append_data(im)
#     print("\r\nFinalizing...")
#     writer.close()
#     print("Done.")