import os
import io
import subprocess
import util
import control_x11_min as x11_min
import control_x11 as x11
import control_wallpaper as cwall 

misc = {
    "kb led on": x11_min.Funs["kb_led_on"],
    "kb led off": x11_min.Funs["kb_led_off"],
    "setup display": x11.tmenu_setup_video,
    "set wallpaper": cwall.tmenu_set_wallpaper,
}

def tmenu_misc():
    sel = util.tmenu_select(misc)
    misc[sel]()

def dmenu_misc():
    util.sh(config.pop_term(config.ctrl_bin(["tmenu_misc"])))
