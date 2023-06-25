from os import getenv, walk, remove, link, listdir
from os.path import exists, join
from os.path import split as psplit
from json import load, dump
from subprocess import run, Popen, PIPE
from re import compile
from util import Logger, tmenu_select, sh, fork, httprequest, find
from io import open
from config import ctrl_bin, pop_term, Cfg
from time import time
from random import Random
from control_x11_min import Funs
from control_x11 import tmenu_setup_video
from control_wallpaper import tmenu_set_wallpaper

misc = {
    "kb led on": Funs["kb_led_on"],
    "kb led off": Funs["kb_led_off"],
    "setup display": tmenu_setup_video,
    "set wallpaper": tmenu_set_wallpaper,
}

def tmenu_misc():
    sel = tmenu_select(misc)
    misc[sel]()

def dmenu_misc():
    sh(pop_term(ctrl_bin(["tmenu_misc"])))
