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
        "parse": lambda s: logger.info("TODO %s" % s)
    }
}

def getwallpaper(provider='bing'):
    logger.info("#getwallpaper provider %s" % provider)
    pro = urlr[provider]
    status, _, body = httprequest("GET", pro["url"]())
    logger.info("getwallpaper response: [%s] [%s]" % (status, body))
    if status != 200:
        return
    url, name = pro["parse"](body.decode())
    logger.info("getwallpaper: [%s] [%s]" % (url, name))
    status,_,body = httprequest("GET", url)
    with open(wlprs + name, "wb") as file:
        file.write(body)
    if exists(wlprs + "wallpaper"):
        remove(wlprs + "wallpaper")
    link(wlprs + name, wlprs + "wallpaper")
    return wlprs + name

def selectwallpaper(dir):
    wps = listdir(dir)
    if not wps:
        return applywallpaper()
    return join(dir, rnd.choice(wps))

def applywallpaper():
    wp = None
    if Cfg["wallpapermode"] == "new":
        wp = getwallpaper()
    elif Cfg["wallpapermode"] == "fixed":
        wp = Home + "/" + Cfg["wallpaperfixd"]
    elif Cfg["wallpapermode"] == "folder":
        wp = selectwallpaper(Home + "/" + Cfg["wallpapersdir"])
    else:
        wp = selectwallpaper(wlprs)
    logger.info("applying wallpaper %s" % wp)
    sh(["feh", "--bg-scale", wp])

def tmenu_set_wallpaper():
    wps = {}
    for k,v in find(wlprs):
        wps[k] = v
    sel = tmenu_select(wps)
    if sel:
        sh(["feh", "--bg-scale", wps[sel]])

def dmenu_set_wallpaper():
    sh(pop_term(ctrl_bin(["tmenu_wallpaper"])))
