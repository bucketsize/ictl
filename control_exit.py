import util
import config
import control_x11_min

Xcmd = control_x11_min.Funs
Cfg = config.Cfg
LogoutCmds = {
    'bspwm': ['bspc', 'quit'] ,
    'lg3d': ['bspc', 'quit'] ,
    'i3wm': ['i3-msg', 'exit'] ,
    'openbox': ['openbox', '--exit'] ,
    'xmonad': [''] ,
}

def tmenu_exit():
    wminf = util.wminfo()
    exit_with = {
        'lock': xcmd["scr_lock_cmd"](),
        'logout': LogoutCmds[wminf.wm.lower()],
        'reboot': ['systemctl', 'reboot'] ,
        'shutdown': ['systemctl', 'poweroff', '-i'] ,
        'hibernate': ['systemctl', 'hibernate'] ,
        'suspend': ['systemctl', 'suspend'] ,
    }
    opt = util.tmenu_select(exit_with)
    util.sh(exit_with[opt])

def dmenu_exit():
    util.sh(config.pop_term(config.ctrl_bin(['tmenu_exit'])))
