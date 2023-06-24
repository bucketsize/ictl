import os
import time
import subprocess
import http.client
import urllib.request

class Logger:
    def info(self, m):
        print("INFO - ", m)

logger = Logger()

def find(path) -> [(str, str)]:
    for root, _, files in os.walk(path):
        for file in files:
            yield file, os.path.join(root, file)
            
def randstr(n: int):
    return time.asctime().replace(":", "_").replace(" ", "_") 

def httprequest(method, url, headers={}, body=None):
    urls = urllib.request.urlparse(url)
    print(url, urls)
    conn = http.client.HTTPSConnection(urls.netloc)
    conn.request(method, urls.path+'?'+urls.query,urls.params, headers)
    res = conn.getresponse()
    return res.status, res.headers, res.read()

def tmenu_select(omap):
    with open("/tmp/mxcmd.out", "w") as f:
        for k in omap.keys():
            f.write(k)
            f.write("\n")
    try:
        sel = subprocess.check_output("fzf < /tmp/mxcmd.out", shell=True)
    except: 
        return None
    logger.info("tmenu_select: %s" % sel)
    return sel.decode().strip()

def sh(cmd: [str]):
    print("#sh: ", cmd)
    subprocess.run(cmd, stdout=subprocess.PIPE)

def mksh(cmd: [str]):
    return lambda cmd: subprocess.run(cmd, stdout=subprocess.PIPE)

def fork(cmd: [str]):
    print("#fork: ", cmd)
    subprocess.Popen(cmd, stdout=subprocess.PIPE)
    time.sleep(2)
