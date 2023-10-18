from os import getenv, walk, remove, link, listdir
from os.path import exists, join
from os.path import split as psplit
from json import load, dump
from subprocess import run, Popen, PIPE
from re import compile
from ictl.util import Logger, tmenu_select, sh, fork, httprequest, find, randstr
from io import open
from ictl.config import ctrl_bin, pop_term, Cfg
from time import time
from random import Random
from sys import argv
from ictl.config import get_renderer

logger = Logger()
rnd = Random()
rnd.seed(int(time()) + 19)

Home = getenv("HOME")            
wlprs = Home + "/.wlprs/"

urlr = {
    "bing": {
        "url": lambda: "https://www.bing.com/HPImageArchive.aspx?format=xml&idx=%s&n=1" % randstr(13),
        "parse": lambda s: (
            (lambda res: (
                "http://www.bing.com" + res,
                res[res.find("id=") + 3:res.find("jpg") + 3]
            ))(s[s.find("<url>") + 5:s.find("</url>") - 1])
        )
    },
    "nasa": {
        "url": lambda: "https://api.nasa.gov/planetary/apod?api_key=cRFIBE5eZnucIQxhm3jJGJopmXDBTQsTkAQal6Qu&count=1",
        "parse": lambda s: print("TODO %s" % s)
    }
}

def getwallpaper(provider='bing'):
    print("#getwallpaper provider %s" % provider)
    pro = urlr[provider]
    status, _, body = httprequest("GET", pro["url"]())
    print("#getwallpaper response: [%s] [%s]" % (status, body))
    if status != 200:
        return
    url, name = pro["parse"](body.decode())
    print("#getwallpaper: [%s] [%s]" % (url, name))
    status,_,body = httprequest("GET", url)
    with open(wlprs + name, "wb") as file:
        file.write(body)
    if exists(wlprs + "wallpaper"):
        remove(wlprs + "wallpaper")
    link(wlprs + name, wlprs + "wallpaper")
    return wlprs + name

def selectwallpaper(dir):
    wps = listdir(dir)
    if wps:
        return join(dir, rnd.choice(wps))

def applywallpaper():
    if Cfg["wallpapermode"] == "new":
        try:
            wp = getwallpaper()
        except e as Exception:
            print("could not get wallpaper", e)
            wp = selectwallpaper(wlprs)
    elif Cfg["wallpapermode"] == "fixed":
        wp = Home + "/" + Cfg["wallpaperfixd"]
    elif Cfg["wallpapermode"] == "folder":
        wp = selectwallpaper(Home + "/" + Cfg["wallpapersdir"])
    else:
        wp = selectwallpaper(wlprs)
    print("applying wallpaper %s" % wp)
    applywallpaperCmd(wp)

def applywallpaperCmd(wp):
    r = get_renderer()
    if r.find('wayland') > -1:
        sh(["killall", "-q","swaybg"])
        fork(["swaybg", "-m", "center", "-i", wp])
    else:
        sh(["feh", "--bg-scale", wp])

def tmenu_set_wallpaper():
    wps = {}
    for k,v in find(wlprs):
        wps[k] = v
    sel = tmenu_select(wps)
    if sel:
        applywallpaperCmd(wps[sel])

def dmenu_set_wallpaper():
    sh(pop_term(ctrl_bin(["tmenu_wallpaper"])))

if __name__ == '__main__':
    mf = {
        '-t': tmenu_set_wallpaper,
        '-d': dmenu_set_wallpaper,
        '-get': getwallpaper,
        '-set': applywallpaper}
    mf[argv[1]]()
