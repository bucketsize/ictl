from os import getenv, walk, remove, link, listdir
from os.path import exists, join
from os.path import split as psplit
from json import load, dump
from subprocess import run, Popen, PIPE
from re import compile
from util import Logger, tmenu_select, sh, fork, httprequest, find
from io import open
from config import ctrl_bin, pop_term, Cfg, wminfo
from time import time
from random import Random
from control_x11_min import Cmds as Xcmd

LogoutCmds = {
    'bspwm': ['bspc', 'quit'] ,
    'lg3d': ['bspc', 'quit'] ,
    'i3wm': ['i3-msg', 'exit'] ,
    'openbox': ['openbox', '--exit'] ,
    'xmonad': [''] ,
}

def tmenu_exit():
    wminf = wminfo()
    print(wminf)
    exit_with = {
        'lock': Xcmd["scr_lock"],
        'logout': LogoutCmds[wminf["wm"]],
        'reboot': ['systemctl', 'reboot'] ,
        'shutdown': ['systemctl', 'poweroff', '-i'] ,
        'hibernate': ['systemctl', 'hibernate'] ,
        'suspend': ['systemctl', 'suspend'] ,
    }
    opt = tmenu_select(exit_with)
    if opt == None:
        return
    sh(exit_with[opt])

def dmenu_exit():
    sh(pop_term(ctrl_bin(['tmenu_exit'])))
