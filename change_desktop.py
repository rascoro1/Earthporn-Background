import os
import sys
import time
from subprocess import check_output, CalledProcessError

# This Script was make by Rascoro1 4/11/2016
# This script will only work on Mac computers

# Pull URLs from restful API that will update every 15 minutes
# Download images found from reddit.com/r/earthporn
# Cycle through images updating the Desktop Background

# User can decide where to download the images
# User can decide the frequency of background upgrade

#@TODO Enable this script for Linux and Windows


WEBSITE = ''
SCRIPT_HOME = os.getcwd() + '/'
IMG_PATH = ''
DELAY = 60 # Default is 60 mins
PICTURE_NUM = 0

def parse_config():
    """ Parse Config File """
    global PICTURE_NUM
    global DELAY
    global WEBSITE
    global IMG_PATH
    if not os.path.exists(SCRIPT_HOME + 'config.cfg'):
        print SCRIPT_HOME
        print "CONFIG.CFG DOES NOT EXISTS!"
        sys.exit(1)
    else:
        f = open(SCRIPT_HOME + 'config.cfg', 'r')
        cfg_lines = f.readlines()
        f.close()
        for line in cfg_lines:
            line = line.replace('\n', '')
            if not "#" in line[0]:
                if line.startswith('URL'):
                    WEBSITE = line.split('=', 2)[1]
                    print "FOUND URL IN CONFIG:", WEBSITE
                elif line.startswith('IMG_PATH'):
                    IMG_PATH = line.split('=', 2)[1]
                    print "FOUND IMG_PATH IN CONFIG:", IMG_PATH
                elif line.startswith('PICTURE_NUM'):
                    PICTURE_NUM = int(line.split('=', 2)[1])
                    print "FOUND PICTURE_NUM IN CONFIG:", PICTURE_NUM
                elif line.startswith('DELAY'):
                    DELAY = int(line.split('=', 2)[1])
                    print "FOUND DELAY IN CONFIG:", DELAY, "min"
                    DELAY = DELAY * 60
    print "Parsing Config File Complete"


def get_pictures():
    """ Install Pictures into IMG_PATH """
    res = check_output(('curl', WEBSITE, '-s'))
    res = res.split('},')
    for line in res:
        line =  line.replace('{', '')
        link, name = line.split('",', 2)
        link = link.split(': "')[1]
        name = name.split(': "')[1]
        name = name.replace('\n"', '')
        name =  name[:-8]
        name = name.replace(' ', '_')
        if not os.path.exists(IMG_PATH):
            print "Creating image path"
            os.mkdir(IMG_PATH)
        name = name.split('[OC]', 2)[0]
        name = IMG_PATH + name + '.jpg'
        args = ['wget', link, '-O',name, '-q']
        print "wget arguments:", args
        try:
            check_output(args)
        except CalledProcessError as e:
            print e.output
    print "Picture Downloads Complete."

def select_picture():
    """ Select Which Picture, will cycle through pictures in IM_PATH directory """
    pics = os.listdir(IMG_PATH)
    print "PICTURE_NUM:", PICTURE_NUM
    pic = pics[PICTURE_NUM]
    pwd = os.getcwd()
    pwd = pwd + '/'
    print pwd
    return IMG_PATH + pic

def change_desktop():
    """ This will Change the Mac Desktop """
    pic_path = select_picture()
    print pic_path
    print "New pic_path:", pic_path.replace('\n', '')
    args = ['osascript', '-e', ]
    last_arg = 'tell application "Finder" to set desktop picture to POSIX file "'
    last_arg = last_arg + pic_path + '"'
    args.append(last_arg)
    print args
    try:
        check_output(args)
        print "Successfully change Desktop"
    except CalledProcessError as e:
        print e.output

def change_picture_number():
    """ Add one to the PICTURE_NUM in the config.cfg file """
    f = open('config.cfg', 'r')
    in_lines = f.readlines()
    f.close()
    out_lines = []
    NEXT_PICTURE_NUM = PICTURE_NUM+1
    if NEXT_PICTURE_NUM >= len(os.listdir(IMG_PATH)):
        NEXT_PICTURE_NUM = 0
    for line in in_lines:
        if line.startswith('PICTURE_NUM'):
            out_lines.append('PICTURE_NUM='+str(NEXT_PICTURE_NUM) + '\n')
        else:
            out_lines.append(line)
    f = open('config.cfg', 'w')
    for line in out_lines:
        f.write(line)
    f.close()
    print "Successfully Changed Config File Picture Number"


if __name__ == "__main__":
    """ Infinite loop, can be thrown in background """
    while True:
        parse_config()
        get_pictures()
        change_desktop()
        change_picture_number()
        print "Program Finsihed!"
        print "Change Desktop will occur in", str(DELAY)
        time.sleep(DELAY)



