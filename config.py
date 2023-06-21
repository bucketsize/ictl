import os
import json
import logging

logger = logging.getLogger()

Home = os.getenv("HOME")
Cfg = {
    "termopts" : {
        "st"    : '-f monospace:size=10',
        "stterm": '-f monospace:size=10 -g 108x24'
    },
    "pop_termopts" : {
        "alacritty": '--class Popeye -o window.dimensions.columns=64 -o window.dimensions.lines=16 -e',
        "xterm": '-name Popeye -geom 64x16 -e',
        "urxvt": '-name Popeye -geometry 64x16 -e',
        "urxvtc": '-name Popeye -geometry 64x16 -e',
        "st": '-c Popeye -g 64x16 -e',
        "stterm": '-c Popeye -g 64x16 -e',
        "qterminal": '--profile Popeye -e',
        "foot     ": '--app-id Popeye --title Popeye --window-size-chars 64x16'
    }
}

if os.path.exists(Home + "/.config/mxctl/config.json"):
    logger.info("config << ~/.config/mxctl/config.json")
    with open(Home + "/.config/mxctl/config.json") as f:
        _cfg = json.load(f)
else:
    logger.info("config << default")
    with open("config.json") as f:
        _cfg = json.load(f)

Cfg.update(_cfg)   

def get_renderer():
    wl_dev = os.getenv("WAYLAND_DISPLAY")
    if wl_dev:
        print("get_renderer:", wl_dev)
        return "wayland"
    else:
        print("get_renderer:", "xorg")
        return "xorg"

def get_pop_term():
    return Cfg["pop_term"][get_renderer()]

def build_pop_term(cmd):
    pop_term = get_pop_term()
    if pop_term not in Cfg["termopts"]:
        Cfg["termopts"][pop_term] = ''
    return f"{pop_term} {Cfg['termopts'][pop_term]} {Cfg['pop_termopts'][pop_term]} {cmd}"

def build_term(t):
    if t not in Cfg["termopts"]:
        Cfg["termopts"][t] = ''
    return f"{t} {Cfg['termopts'][t]}"

def build_menu_sel(lst):
    return f"{lst} | {Cfg['menu_sel']} "

def build_ctrl_bin(cmd):
    return f"{Cfg['ctrl_bin']} {cmd} "
