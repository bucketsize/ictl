from os import getenv, walk
from os.path import exists, join, expanduser
from os.path import split as psplit
from json import load, dump
from subprocess import run, Popen, PIPE
from re import compile, match
from ictl.util import Logger, tmenu_select, sh, fork
from io import open
from ictl.config import ctrl_bin, pop_term, Cfg

logger = Logger()

USER = getenv("USER")
appcache = "/tmp/appcache.ictl.%s.json" % (USER)

def parsedesktopfile(f: str) -> [dict]:
    with open(f, "r") as h:
        n,e,bs = [],[],[]
        i = 0
        for l in h:
            name = match("^Name=([\w\s\-_\/]+)", l)
            if name:
                n.append(name.group(1).strip())
            exec = match("^Exec=(.+)", l)
            if exec:
                e.append(exec.group(1).strip())
        n0 = n[0]
        for exe in e:
            arg = exe.split("/")[-1]
            if arg != None and arg.strip() == "":
                print("parsedesktopfile, wierd entry:", exe)
            else:
                nam = "{} - {}".format(n0, arg) 
                bs.append({"name": nam, "exec": exe, "bin": nam})
                print("parsedesktopfile: {} - {}".format(f, nam))
    return bs


def find_apps(apps={}) -> {}:
    for path in Cfg["app_dirs"]:
        for root, _, files in walk(expanduser(path)):
            for file in files:
                if file.endswith(".desktop"):
                    for d in parsedesktopfile(join(root, file)):
                        apps[d['bin']] = d['exec'] 
                else:
                    apps[file] = join(root, file)
    return apps

fpre = compile('(\w+)\s+(\w+)\s+(.*)')
def find_flatpaks(apps={}) -> {}:
    try:
        h = run(["flatpak", "list"], stdout=PIPE)
    except Exception as e:
        print(e)
        return apps
    for line in h.stdout.decode().splitlines():
        m = fpre.match(line)
        if m:
            apps['fp>'+m.group(1)] = 'flatpak run '+m.group(2)
    return apps

def list_apps():
    apps = {}
    if not exists(appcache):
        find_apps(apps)
        find_flatpaks(apps)
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
    cmd = pmap[sela].split(" ")
    if cmd[-1].startswith("%"):
        fork(cmd[:-1])
    else:
        fork(cmd)

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

