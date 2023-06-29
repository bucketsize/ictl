from os import getenv, walk, remove, link, listdir
from os.path import exists, join
from os.path import split as psplit
from json import load, dump
from subprocess import run, Popen, PIPE
from re import compile
from ictl.util import Logger, tmenu_select, sh, fork, httprequest, find
from io import open
from ictl.config import ctrl_bin, pop_term, Cfg
from time import time
from random import Random

logger = Logger()

def brightness(delta):
    logger.info("brightness", delta)
    bf = listdir("/sys/class/backlight")
    if bf:
        bf = bf[0]
        max = int(open(f"/sys/class/backlight/{bf}/max_brightness", "r").read())
        cur = int(open(f"/sys/class/backlight/{bf}/brightness", "r").read())
        tar = int(cur + delta * max / 100)
        if tar > max:
            tar = max
        if tar < 0:
            tar = cur
        logger.info("brightness", delta, bf, cur, tar, max)
        with open(f"/sys/class/backlight/{bf}/brightness", "w") as h:
            h.write(str(tar))

def brightness_up():
    brightness(Cfg["lux_step"])

def brightness_down():
    brightness(-Cfg["lux_step"])

