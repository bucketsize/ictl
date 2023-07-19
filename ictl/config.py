from os import getenv
from os.path import exists, join
from json import load
from subprocess import run, Popen, PIPE
from re import compile
from ictl.util import Logger

logger = Logger()

Home = getenv("HOME")
print("Home:", Home)
Cfg = {
    "pop_terms" : {
        "alacritty": ['/usr/bin/alacritty', '--class', 'Popeye', '-o', 'window.dimensions.columns=64', '-o', 'window.dimensions.lines=16', '-e'],
        'xterm': ['/usr/bin/xterm', '-name', 'Popeye', '-geom', '64x16', '-e'],
        'urxvt': ['/usr/bin/urxvt', '-name', 'Popeye', '-geometry', '64x16', '-e'],
        'urxvtc': ['/usr/bin/urxvtc', '-name', 'Popeye', '-geometry', '64x16', '-e'],
        'st': ['/usr/bin/st', '-c', 'Popeye', '-g', '64x16', '-f', 'monospace:size=10', '-e'],
        'stterm': ['/usr/bin/stterm', '-c', 'Popeye', '-g', '64x16', '-f', 'monospace:size=10', '-e'],
        'qterminal': ['/usr/bin/qterminal', '--profile', 'Popeye', '-e'],
        'foot': ['/usr/bin/foot', '--app-id', 'Popeye', '--title', 'Popeye', '--window-size-chars', '64x16']
    }
}

if exists(Home + "/.config/ictl/config.json"):
    with open(Home + "/.config/ictl/config.json") as f:
        _cfg = load(f)
elif exists("config.json"):
    print("using cwd config.json")
    with open("config.json") as f:
        _cfg = load(f)
else:
    print("config.json missing, please create ~/.config/ictl/config.json")

Cfg.update(_cfg)

def get_renderer():
    wl_dev = getenv("WAYLAND_DISPLAY")
    if wl_dev:
        print("get_renderer:", wl_dev)
        return "wayland"
    else:
        print("get_renderer:", "xorg")
        return "xorg"

wmre = compile("Name:\s+(\w+)")
def wminfo() -> {}:
    h = run(["wmctrl", "-m"], stdout=PIPE)
    wm = None
    for line in h.stdout.decode().splitlines():
        wm = wmre.match(line).groups()[0]
        if wm != None:
            break
    return {"wm": wm}

def pop_term(cmd: [str]) -> [str]:
    pt = Cfg["pop_term"][get_renderer()]
    print("pop_term:", pt)
    if pt not in Cfg["pop_terms"]:
        raise f"pop_term {pt} not defined in config.pop_terms"
    return Cfg['pop_terms'][pt] + cmd

def ctrl_bin(cmd: [str]) -> [str]:
    return [Home + "/.local/bin/ictl"]+ cmd
