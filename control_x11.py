import os
import math
import random
import os
import subprocess
import re


import time
import config 
import util

logger = util.Logger()
rnd = random.Random()
rnd.seed(int(time.time()) + 19)

Cfg = config.Cfg
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
    h = subprocess.run(["/usr/bin/xrandr", "-q"], stdout=subprocess.PIPE)
    ots = {}
    ot = None
    for line in h.stdout.decode().splitlines():
        logger.info("xrandr_info: %s" % line)
        otc = line.strip().split()[0]
        if "connected" in line:
            logger.info("xrandr_info, parse connected %s" % otc)
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
    for m in o["modes"]:
        k = mk_key([o["name"], str(m["x"]),str(m["y"])])
        logger.info("outgrid_config: %s" % k)
        if outgrid.get(k) is None:
            outgrid[k] = {"name": o["name"], "x": m["x"], "y": m["y"], "active": False, "on": "", "off": "", "modes":[]}
        outgrid[k]["modes"].append(m)

def outgrid_controls_config(outgrid, outgrid_ctl, o):
    for m in o["modes"]:
        k = mk_key([o["name"], str(m["x"]), str(m["y"])])
        logger.info("outgrid__controls_config: %s" % k)
        if outgrid_ctl.get(k) is None:
            outgrid_ctl[k] = {"name": o["name"], "active": False, "on": None, "off": None}
        outgrid_ctl[k]["on" ] = (DISPLAY_ON % (o["name"], m["x"], m["y"], 0, 0, "")).split()
        outgrid_ctl[k]["off"] = (DISPLAY_OFF % o["name"]).split()
        if m["active"]:
            outgrid_ctl[k]["active" ] = True


def xrandr_configs():
    outputs = xrandr_info()
    outgrid = {}
    for otc, o in outputs.items():
        logger.info("xrandr_configs, item %s, %s" % (otc, o["name"]))
        outgrid_config(outgrid, o)
    logger.info("xrandr_configs, outgrid: %s" % outgrid)
    outgrid_ctl = {}
    for o in outputs.values():
        outgrid_controls_config(outgrid, outgrid_ctl, o)
    logger.info("xrandr_configs, outgrid_ctl: %s" % outgrid_ctl)
    return outgrid, outgrid_ctl

def setup_video():
    _, outgrid_ctl = xrandr_configs()
    for d in outgrid_ctl.values():
        if d["active"]:
            util.sh(d["on"])

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
    opt = util.tmenu_select(vgridctl)
    if opt == None:
        return 
    util.sh(vgridctl[opt].on)

def dmenu_setup_video():
    util.sh(config.pop_term(config.ctrl_bin(["tmenu_setup_video"])))


reps = re.compile("(\w+)\s+(\d+)\s+([\w_\-]+)\s+(.*)")

def tmenu_select_window():
    ws = {}
    pc = subprocess.run("wmctrl -l", stdout=subprocess.PIPE)
    plines = pc.stdout.decode().splitlines()
    for i in plines:
        id,wx,name = reps.match(i).groups()
        print(id,wx,name)
        ws[name] = id
    wid = util.tmenu_select(ws)
    util.sh(["wmctrl", "-ia", ws[wid]])

def dmenu_select_window():
    util.sh(config.pop_term(config.ctrl_bin(["tmenu_select_window"])))

def scr_lock_if():
    iv = None
    # Pr.pipe().add(Sh.exec("pactl list sinks")).add(Sh.grep("RUNNING")).add(Sh.echo()).add(lambda x: iv = x if x else None).run()
    # if iv == None:
    #     Sh.sh(xcmd.scr_lock())
