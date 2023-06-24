import os
import math
import random
import os
import subprocess

import time
import config 
import util

logger = util.Logger()
rnd = random.Random()
rnd.seed(int(time.time()) + 19)

Cfg = config.Cfg

_PA_CMD = {
    "vol_up": "pactl set-sink-volume @DEFAULT_SINK@ +10%",
    "vol_down": "pactl set-sink-volume @DEFAULT_SINK@ -10%",
    "vol_mute": "pactl set-sink-mute   @DEFAULT_SINK@ toggle",
    "vol_unmute": "pactl set-sink-mute   @DEFAULT_SINK@ toggle",
}

def pa_sinks():
    iv = []
    subprocess.run(["pactl", "list", "sinks"], capture_output=True)
    .stdout.decode().split("\n")
    for line in output:
        if "Name: " in line:
            iv.append(line.split("Name: ")[1])
    return iv

class Fn:
    def tmenu_select_pa_sinks(self):
        opts = [v[0] for v in pa_sinks().values()]
        opss = "\n".join(opts)
        subprocess.run(["echo", opss], capture_output=True)
        .stdout.decode().split("\n")
        id = output[0]
        if id:
            subprocess.run(["pactl", "set-default-sink", id], capture_output=True)

    def dmenu_select_pa_sinks(self):
        subprocess.run(["pop_term", ctrl_bin("tmenu_select_pa_sinks")], capture_output=True)

    def vol_up(self):
        subprocess.run(_PA_CMD["vol_up"], shell=True)

    def vol_down(self):
        subprocess.run(_PA_CMD["vol_down"], shell=True)

    def vol_mute(self):
        subprocess.run(_PA_CMD["vol_mute"], shell=True)

    def vol_unmute(self):
        subprocess.run(_PA_CMD["vol_unmute"], shell=True)
