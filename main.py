# Time,Schedule and instabot imported
import os
import shutil

from instabot import Bot
import schedule
import time
import random

# login
usr = "terminal__shoes"  # username
pwd = "mefeK3ws"  # password
# dirs paths
POSTS_DIR = './PostsToUpload'
POSTED_DIR = './Posted'
STORY_DIR = './Story'
# text
Post_Text_Path = './postText.txt'

def clean_up():
    dir = "config"
    # checking whether config folder exists or not
    if os.path.exists(dir):
        try:
            # removing it so we can upload new image
            shutil.rmtree(dir)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

def getMultiPics(image_path, images_dir_list):
    name = image_path[:image_path.index('_UTC')]
    multiPicsList = []
    for pic in images_dir_list:
        if name in pic:
            multiPicsList.append(pic)
    multiPicsList.sort()
    return multiPicsList

def random_picture():
    clean_up()
    bot = Bot()

    bot.login(username=usr, password=pwd)
    images_dir_list = os.listdir(POSTS_DIR)
    image_path = random.choice(images_dir_list) # take random image from dir

    success = False
    while not success:
        album_list = getMultiPics(image_path, images_dir_list) # get a package of images associated with the selected image
        album_path = ['{}/{}'.format(POSTS_DIR, pic) for pic in album_list]
        text = open(Post_Text_Path, 'r').read() # post caption text
        image_name = album_path.__getitem__(0) # get the first image in list
        album_path.remove(image_name)
        success = bot.upload_photo(image_name, caption=text)
        if not success:
            os.rename(image_name, '{}/{}'.format(STORY_DIR, os.path.basename(image_name)))
    # clean up the image we upload and related pack of photos
    remove_me = "{}.REMOVE_ME".format(image_name)
    if os.path.exists(remove_me):
        src = '{}/{}'.format(POSTED_DIR, os.path.basename(image_name))
        os.rename(remove_me, src)
    for image in album_list:
        os.rename('{}/{}'.format(POSTS_DIR, image), '{}/{}'.format(POSTED_DIR, image))

if __name__ == '__main__':
    schedule.every(1).second.do(random_picture)
    while True:
        schedule.run_pending()  # waiting for schedule
        time.sleep(1)  # countdown 1 second
