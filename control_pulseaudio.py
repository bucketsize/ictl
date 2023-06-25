from os import getenv, walk
from os.path import exists
from os.path import split as psplit
from json import load, dump
from subprocess import run, Popen, PIPE
from re import compile
from util import Logger, tmenu_select, sh, fork
from io import open
from config import ctrl_bin, pop_term, Cfg
from time import time
from random import Random

logger = Logger()

rnd = Random()
rnd.seed(int(time()) + 19)

Pactl = "/usr/bin/pactl"

PactlCmd = {
    'vol_up': [Pactl, 'set-sink-volume', '@DEFAULT_SINK@', '+10%'] ,
    'vol_down': [Pactl, 'set-sink-volume', '@DEFAULT_SINK@', '-10%'] ,
    'vol_mute': [Pactl, 'set-sink-mute', '@DEFAULT_SINK@', 'toggle'] ,
    'vol_unmute': [Pactl, 'set-sink-mute', '@DEFAULT_SINK@', 'toggle'] ,
}

def pa_sinks() -> {}:
    v = {}
    h = run([Pactl, "list", "sinks"], stdout=PIPE)
    for line in h.stdout.decode().splitlines():
        if "Name: " in line:
            name = line.split("Name: ")[1]
            v[name] = name
    return v

def tmenu_select_pa_sinks():
    sinks = pa_sinks()
    id = tmenu_select(sinks)
    if id:
        sh([Pactl, "set-default-sink", id])

def dmenu_select_pa_sinks():
    sh(pop_term(ctrl_bin(["tmenu_audio_sink"])))

def vol_up():
    sh(PactlCmd["vol_up"])

def vol_down():
    sh(PactlCmd["vol_down"])

def vol_mute():
    sh(PactlCmd["vol_mute"])

def vol_unmute():
    sh(PactlCmd["vol_unmute"])
