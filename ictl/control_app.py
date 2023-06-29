from os import getenv, walk
from os.path import exists, join
from os.path import split as psplit
from json import load, dump
from subprocess import run, Popen, PIPE
from re import compile, match
from ictl.util import Logger, tmenu_select, sh, fork
from io import open
from ictl.config import ctrl_bin, pop_term, Cfg

logger = Logger()

USER = getenv("USER")
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
    with open(f, "r") as h:
        bs, b = [], {}
        i = 0
        for l in h:
            if match("^%[(.+)%]", l):
                buildapp(str(i), bs, b)
                b = {'name': "na", 'exec': "na", 'bin': "na"}
                i += 1
            else:
                name = match("^Name=([\w\s\-_\/]+)", l)
                if name:
                    b['name'] = name.group(1)
                else:
                    exec = match("^Exec=(.+)", l)
                    if exec:
                        b['exec'] = exec.group(1).strip()
                        p = psplit(f)[-1].split(".")[0]
                        b['bin'] = p if p else b['exec']
        buildapp(str(i + 1), bs, b)
    return bs

def find() -> {}:
    apps = {}
    for path in Cfg["app_dirs"]:
        for root, _, files in walk(path):
            for file in files:
                if file.endswith(".desktop"):
                    for d in parsedesktopfile(join(root, file)):
                        apps[d['bin']] = d['exec'] 
                else:
                    apps[file] = join(root, file)
    logger.info("discovered [apps+exes] %s targets" % len(apps))
    with open(appcache, 'w') as f:
        dump(apps, f)
    return apps

def list_apps():
    if not exists(appcache):
        apps = find()
        with open(appcache, 'w') as f:
            dump(apps, f)
    else:
        with open(appcache) as f:
            apps = load(f)
    return apps

def tmenu_run():
    pmap = list_apps()
    sela = tmenu_select(pmap)
    if sela == None:
        return
    fork(pmap[sela].split(" ")) 

def dmenu_run():
    sh(pop_term(ctrl_bin(["tmenu_run"])))

psre = compile('\s+(\d+)\s+(\d+.\d+)\s+(\d+.\d+)\s+([\w\-_]+)\s+([\w\-_]+)')
def procs() -> {}:
    pmap = {}
    h = run(["ps", "-xo", "pid,pcpu,pmem,stat,comm"], stdout=PIPE)
    for p in h.stdout.decode().splitlines():
        m = psre.match(p)
        print("m:", p, m)
        if m:
            pid,pcpu,pmem,stat,comm = m.groups()
            pmap["%s - %s - %s" % (comm, pid, pmem)] = pid
    return pmap

def tmenu_kill_proc():
    pmap = procs()
    opt  = tmenu_select(pmap) 
    if opt == None:
        return
    sh(["/usr/bin/kill", "-9", pmap[opt]])

def dmenu_kill_proc():
    sh(pop_term(ctrl_bin(["tmenu_kill"])))

