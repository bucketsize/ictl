import ictl.control_app as Ctl
import ictl.control_x11 as X11 

def test_findapps():
   apps = Ctl.find()

def test_parsedesktopfile():
   app = Ctl.parsedesktopfile(nil, "tests/res/URxvtc.desktop")

# def test_tmenu_run():
#    app = Ctl.tmenu_run()

X11.setup_video()


