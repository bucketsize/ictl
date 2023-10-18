#!/usr/bin/env python

import os
from sys import argv, exit 

from ictl.app import tmenu_kill_proc, tmenu_run
from ictl.cmd import tmenu_misc
from ictl.exit import tmenu_exit
from ictl.wallpaper import tmenu_set_wallpaper
from ictl.x11 import tmenu_setup_video, tmenu_select_window
from ictl.pulseaudio import tmenu_select_pa_sinks
from ictl.brightness import brightness_up, brightness_down 

from ictl.app import dmenu_kill_proc, dmenu_run
from ictl.cmd import dmenu_misc
from ictl.exit import dmenu_exit
from ictl.wallpaper import dmenu_set_wallpaper, applywallpaper
from ictl.x11 import dmenu_setup_video, dmenu_select_window, setup_video
from ictl.pulseaudio import dmenu_select_pa_sinks, vol_unmute, vol_mute, vol_down, vol_up

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
    "brightness_up": brightness_up,
    "brightness_down": brightness_down,
    "applywallpaper": applywallpaper,
    "getwallpaper": getwallpaper,
    "setup_video": setup_video,
}

def print_help():
    print("usage:")
    for k,_ in fmapper.items():
        print('\t',k)

def main():
    if len(argv) < 2:
        print_help()
        return 1
    if fmapper.get(argv[1]) == None:
        print_help()
        return 1
    fmapper[argv[1]]()
    return 0

