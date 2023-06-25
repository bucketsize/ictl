#!/usr/bin/env python

import os
from sys import argv, exit 

from control_app import tmenu_kill_proc, tmenu_run
from control_cmd import tmenu_misc
from control_exit import tmenu_exit
from control_wallpaper import tmenu_set_wallpaper
from control_x11 import tmenu_setup_video, tmenu_select_window
from control_pulseaudio import tmenu_select_pa_sinks

from control_app import dmenu_kill_proc, dmenu_run
from control_cmd import dmenu_misc
from control_exit import dmenu_exit
from control_wallpaper import dmenu_set_wallpaper
from control_x11 import dmenu_setup_video, dmenu_select_window
from control_pulseaudio import dmenu_select_pa_sinks, vol_unmute, vol_mute, vol_down, vol_up

fmapper = {
    "tmenu_run": tmenu_run,
    "tmenu_kill": tmenu_kill_proc,
    "tmenu_wallpaper": tmenu_set_wallpaper,
    "tmenu_exit": tmenu_exit,
    "tmenu_video": tmenu_setup_video,
    "tmenu_window": tmenu_select_window,
    "tmenu_audio_sink": tmenu_select_pa_sinks,
    "dmenu_run": dmenu_run,
    "dmenu_kill": dmenu_kill_proc,
    "dmenu_wallpaper": dmenu_set_wallpaper,
    "dmenu_exit": dmenu_exit,
    "dmenu_video": dmenu_setup_video,
    "dmenu_window": dmenu_select_window,
    "dmenu_audio_sink": dmenu_select_pa_sinks,
    "vol_up": vol_up,
    "vol_down": vol_down,
    "vol_mute": vol_mute,
    "vol_unmute": vol_unmute,
}

def print_help():
    print("usage:")
    for k,_ in fmapper.items():
        print('\t',k)

if __name__ == '__main__':
    if len(argv) < 2:
        print_help()
        exit(1)
    if fmapper.get(argv[1]) == None:
        print_help()
        exit(1)
    fmapper[argv[1]]()
    