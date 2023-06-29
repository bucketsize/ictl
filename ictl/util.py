from os import getenv, walk, remove, link, listdir
from os.path import exists, join
from os.path import split as psplit
from json import load, dump
from subprocess import run, Popen, PIPE, check_output
from re import compile
from io import open
from time import time,asctime,sleep
from random import Random
from urllib.request import urlparse
from http.client import HTTPSConnection

class Logger:
    def info(self, m):
        print("INFO - ", m)

logger = Logger()

def find(path) -> [(str, str)]:
    for root, _, files in walk(path):
        for file in files:
            yield file, join(root, file)
            
def randstr(n: int):
    return asctime().replace(":", "_").replace(" ", "_") 

def httprequest(method, url, headers={}, body=None):
    urls = urlparse(url)
    print(url, urls)
    conn = HTTPSConnection(urls.netloc)
    conn.request(method, urls.path+'?'+urls.query,urls.params, headers)
    res = conn.getresponse()
    return res.status, res.headers, res.read()

def tmenu_select(omap):
    with open("/tmp/mxcmd.out", "w") as f:
        for k in omap.keys():
            f.write(k)
            f.write("\n")
            print("tmenu_select, opt:", k)
    try:
        sel = check_output("fzf < /tmp/mxcmd.out", shell=True)
    except:
        return None
    logger.info("tmenu_select: %s" % sel)
    return sel.decode().strip()

def sh(cmd: [str]):
    print("#sh: ", cmd)
    run(cmd, stdout=PIPE)

def mksh(cmd: [str]):
    return lambda cmd: run(cmd, stdout=PIPE)

def fork(cmd: [str]):
    print("#fork: ", cmd)
    Popen(["nohup"] + cmd, stdout=PIPE)
    sleep(2)
