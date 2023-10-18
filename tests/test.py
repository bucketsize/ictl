import ictl.config as Con 
import ictl.app as Ctl
import ictl.x11 as Xx 
import ictl.brightness as Xb 
import ictl.wallpaper as Xw  
from time import sleep

apps = Ctl.find_apps()
assert(len(apps) >  0)
sleep(1)

app = Ctl.parsedesktopfile("tests/res/URxvtc.desktop")
sleep(1)

re = Con.get_renderer()
wm = Con.wminfo()
print("config:", re, wm)

def test_display():
    Xx.setup_video()
    sleep(1)

    Xb.brightness_down()
    sleep(2)

    Xb.brightness_up()
    sleep(2)

    Xw.applywallpaper()
    sleep(2)
