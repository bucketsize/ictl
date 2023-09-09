import ictl.control_app as Ctl
import ictl.control_x11 as Xx 
import ictl.control_brightness as Xb 
import ictl.control_wallpaper as Xw  
from time import sleep

apps = Ctl.find()
assert(len(apps) >  0)
sleep(1)

app = Ctl.parsedesktopfile("tests/res/URxvtc.desktop")
sleep(1)

Xx.setup_video()
sleep(1)

Xb.brightness_down()
sleep(2)

Xb.brightness_up()
sleep(2)

Xw.applywallpaper()
sleep(2)
