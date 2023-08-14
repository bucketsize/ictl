from os import getenv, walk, remove, link, listdir
from os.path import exists, join
from os.path import split as psplit
from json import load, dump
from subprocess import run, Popen, PIPE
from re import compile
from ictl.util import Logger, tmenu_select, sh, fork, httprequest, find
from io import open
from ictl.config import ctrl_bin, pop_term, Cfg
from time import time
from random import Random

logger = Logger()
rnd = Random()
rnd.seed(int(time()) + 19)

DISPLAYS = Cfg["displays"]
DISPLAY_ON = """
    xrandr \
        --output %s \
        --mode %dx%d \
        --rotate normal \
        --pos %dx%d \
        %s
"""
DISPLAY_OFF = """
    xrandr \
        --output %s \
        --off
"""

def xrandr_info():
    h = run(["/usr/bin/xrandr", "-q"], stdout=PIPE)
    ots = {}
    ot = None
    for line in h.stdout.decode().splitlines():
        logger.info("xrandr_info: %s" % line)
        otc = line.strip().split()[0]
        if "connected" in line:
            logger.info("xrandr_info, parse (dis)connected %s" % otc)
            ot = otc
            if ots.get(ot) is None:
                ots[ot] = {"modes": [], "name": ot}
        elif ot is not None:
            mode = line.split()[0] if 'x' in line else ""
            mx, my = [int(i) for i in mode.split('x')]
            logger.info("xrandr_info, mode (%s,%s,%s)" % (ot, mx, my))
            ots[ot]["modes"].append({"x": mx, "y": my, "active": False})
    return ots

def mk_key(l: [str]) -> str:
    return "_".join(l)

def outgrid_config(outgrid, o):
    vcfg = None
    for cfg in Cfg['displays']:
        if cfg['name'] == o['name']:
            vcfg = cfg
            break
    print("#outgrid_config: ", vcfg)
    for m in o["modes"]:
        k = mk_key([o["name"], str(m["x"]),str(m["y"])])
        if outgrid.get(k) is None:
            outgrid[k] = {"name": o["name"], "x": m["x"], "y": m["y"], "active": False, "on": "", "off": "", "modes":[]}
        if vcfg and vcfg['mode']['y'] == m['y'] and vcfg['mode']['x'] == m['x']:
            outgrid[k]['active'] = True
        logger.info("#outgrid_config: %s, %s" % (k, outgrid[k]))
        outgrid[k]["modes"].append(m)

def outgrid_controls_config(outgrid, outgrid_ctl, o):
    for m in o["modes"]:
        k = mk_key([o["name"], str(m["x"]), str(m["y"])])
        oc = outgrid[k]
        if outgrid_ctl.get(k) is None:
            outgrid_ctl[k] = {"name": o["name"], "active": oc['active'], "on": None, "off": None}
        outgrid_ctl[k]["on" ] = (DISPLAY_ON % (o["name"], m["x"], m["y"], 0, 0, "")).split()
        outgrid_ctl[k]["off"] = (DISPLAY_OFF % o["name"]).split()
        if m["active"]:
            outgrid_ctl[k]["active" ] = True
        logger.info("#outgrid__controls_config: %s, %s" % (k, outgrid_ctl[k]))


def xrandr_configs():
    outputs = xrandr_info()
    outgrid = {}
    for otc, o in outputs.items():
        logger.info("#xrandr_configs, item %s, %s" % (otc, o["name"]))
        outgrid_config(outgrid, o)
    outgrid_ctl = {}
    for o in outputs.values():
        outgrid_controls_config(outgrid, outgrid_ctl, o)
    return outgrid, outgrid_ctl

def setup_video():
    _, outgrid_ctl = xrandr_configs()
    for d in outgrid_ctl.values():
        if d["active"]:
            print("#setup_video:", d)
            sh(d["on"])

# -- local function get2dElem(t, i, j)
# -- 	if t[i] == nil then
# -- 		return nil
# -- 	else
# -- 		return t[i][j]
# -- 	end
# -- end
# --
# -- local function getElem(t, indexes)
# -- 	if indexes[1] == nil then
# -- 		return nil
# -- 	else
# -- 		if indexes[2] == nil then
# -- 			return t
# -- 		else
# -- 			return getElem(t[indexes[1]], {})
# -- 		end
# -- 	end
# -- end

def tmenu_setup_video():
    _, vgridctl = xrandr_configs()
    opt = tmenu_select(vgridctl)
    if opt == None:
        return 
    sh(vgridctl[opt]["on"])

def dmenu_setup_video():
    sh(pop_term(ctrl_bin(["tmenu_video"])))

reps = compile("(\w+)\s+(\d+)\s+([\w_\-]+)\s+(.*)")

def tmenu_select_window():
    ws = {}
    pc = run(["/usr/bin/wmctrl", "-l"], stdout=PIPE)
    for i in pc.stdout.decode().splitlines():
        id,wx,name,titl = reps.match(i).groups()
        ws[name+"::"+titl] = id
    wid = tmenu_select(ws)
    if wid == None:
        return 
    sh(["/usr/bin/wmctrl", "-ia", ws[wid]])

def dmenu_select_window():
    sh(pop_term(ctrl_bin(["tmenu_window"])))

def scr_lock_if():
    iv = None
    # Pr.pipe().add(Sh.exec("pactl list sinks")).add(Sh.grep("RUNNING")).add(Sh.echo()).add(lambda x: iv = x if x else None).run()
    # if iv == None:
    #     Sh.sh(xcmd.scr_lock())
