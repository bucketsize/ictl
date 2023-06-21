import os
import math
import random
import os
import subprocess
import http.client
import urllib.request

import time
import config 
import util

logger = util.Logger()
rnd = random.Random()
rnd.seed(int(time.time()) + 19)

Cfg = config.Cfg
Home = os.getenv("HOME")            
wlprs = Home + "/.wlprs/"
pop_term = config.build_pop_term
menu_sel = config.build_menu_sel
ctrl_bin = config.build_ctrl_bin

urlr = {
    "bing": {
        "url": lambda: "https://www.bing.com/HPImageArchive.aspx?format=xml&idx=%s&n=1" % util.randstr(13),
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
    status, _, body = util.httprequest("GET", pro["url"]())
    logger.info("getwallpaper response: [%s] [%s]" % (status, body))
    if status != 200:
        return
    url, name = pro["parse"](body.decode())
    logger.info("getwallpaper: [%s] [%s]" % (url, name))
    status,_,body = util.httprequest("GET", url)
    with open(wlprs + name, "wb") as file:
        file.write(body)
    if os.path.exists(wlprs + "wallpaper"):
        os.remove(wlprs + "wallpaper")
    os.link(wlprs + name, wlprs + "wallpaper")
    return wlprs + name

def selectwallpaper(dir):
    wps = os.listdir(dir)
    if not wps:
        return applywallpaper()
    return os.path.join(dir, rnd.choice(wps))

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
    subprocess.call(["feh", "--bg-scale", wp])

def tmenu_set_wallpaper():
    wps = {}
    for k,v in util.find(wlprs):
        wps[k] = v
    sel = util.tmenu_select(wps)
    subprocess.call(["feh", "--bg-scale", wps[sel]])

def dmenu_set_wallpaper():
    subprocess.run(["sh", pop_term(ctrl_bin("tmenu_set_wallpaper"))])
