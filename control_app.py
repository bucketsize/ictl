import os
import re
import io
import os.path
import subprocess
import json
import logging
import config
import util

Cfg = config.Cfg
logger = logging.getLogger()

USER = os.getenv("USER")
appcache = "/tmp/appcache.mxctl." + USER + ".json"

def hazapp(bs, b):
    for bi in bs:
        if bi['exec'] == b['exec']:
            return True
    return False

def buildapp(tag, bs, b):
    if b['name'] and b['exec'] and not hazapp(bs, b):
        bs.append(b)

def parsedesktopfile(f: str) -> [dict]:
    with io.open(f, "r") as h:
        bs, b = [], {}
        i = 0
        for l in h:
            if re.match("^%[(.+)%]", l):
                buildapp(str(i), bs, b)
                b = {'name': "na", 'exec': "na", 'bin': "na"}
                i += 1
            else:
                name = re.match("^Name=([\w\s\-_\/]+)", l)
                if name:
                    b['name'] = name.group(1)
                else:
                    exec = re.match("^Exec=(.+)", l)
                    if exec:
                        b['exec'] = exec.group(1).strip()
                        p = os.path.split(f)[-1].split(".")[0]
                        b['bin'] = p if p else b['exec']
        buildapp(str(i + 1), bs, b)
    return bs

def find() -> {}:
    apps = {}
    for path in Cfg["app_dirs"]:
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".desktop"):
                    for d in parsedesktopfile(os.path.join(root, file)):
                        apps[d['bin']] = d['exec'] 
                else:
                    apps[file] = os.path.join(root, file)
    logger.info("discovered [apps+exes] %s targets" % len(apps))
    with open(appcache, 'w') as f:
        json.dump(apps, f)
    return apps

def list_apps():
    if not os.path.exists(appcache):
        apps = find()
        with open(appcache, 'w') as f:
            json.dump(apps, f)
    else:
        with open(appcache) as f:
            apps = json.load(f)
    return apps

def tmenu_run():
    pmap = list_apps()
    sela = util.tmenu_select(pmap)
    if sela == None:
        return
    util.fork(pmap[sela].split(" ")) 

def dmenu_run():
    util.sh(config.pop_term(config.ctrl_bin(["tmenu_run"])))

def list_proc():
    pmap = {}
    output = subprocess.check_output("ps -xo pid,pcpu,pmem,stat,comm | grep '(%d+)%s+(%d+.%d+)%s+(%d+.%d+)%s+([%a%p]+)%s+([%a%p]+)'", shell=True)
    for x in output:
        if x:
            pmap[string.format("%d \t\t %s \t\t %s", x[1], x[4], x[5])] = x[1]
    return pmap

def tmenu_kill_proc():
    pmap = list_proc()
    output = util.tmenu_select(omap) 
    for x in output:
        for y in x:
            logger.info("tmenu_kill_proc, kill", y)
            subprocess.call(["kill", pmap[y]])

def dmenu_kill_proc():
    util.sh(config.pop_term(config.ctrl_bin(["tmenu_kill_proc"])))

