#!/usr/bin/env python

import os
import sys
import control_app as capp 
import control_cmd as ccmd 
import control_exit as cexe 
import control_wallpaper as cwall
import control_x11 as cx11 

fmapper = {
    "dmenu_run": capp.dmenu_run,
    "tmenu_run": capp.tmenu_run,
    "dmenu_kill": capp.dmenu_run,
    "tmenu_kill": capp.tmenu_run,
    "dmenu_set_wallpaper": cwall.dmenu_set_wallpaper,
    "tmenu_set_wallpaper": cwall.dmenu_set_wallpaper,
    "dmenu_exit": cexe.dmenu_exit,
    "tmenu_exit": cexe.tmenu_exit,
    "tmenu_setup_video": cx11.tmenu_setup_video
}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)
    if fmapper.get(sys.argv[1]) == None:
        sys.exit(1)
    fmapper[sys.argv[1]]()
    
