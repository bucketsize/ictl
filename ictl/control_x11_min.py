from ictl.util import mksh

Cmds = {
    'kb_led_on': ['xset', 'led', 'on'],
    'kb_led_off': ['xset', 'led', 'off'],
    'win_left': ['xdotool', 'getactivewindow', 'windowmove', '03%', '02%', 'windowsize', '48%', '92%'],
    'win_right': ['xdotool', 'getactivewindow', 'windowmove', '52%', '02%', 'windowsize', '48%', '92%'],
    'win_max': ['wmctrl', '-r', ':ACTIVE:', '-b', 'add,maximized_vert,maximized_horz'],
    'win_unmax': ['wmctrl', '-r', ':ACTIVE:', '-b', 'remove,maximized_vert,maximized_horz'],
    'win_big': ['xdotool', 'getactivewindow', 'windowmove', '04%', '04%', 'windowsize', '92%', '92%'],
    'win_small': ['xdotool', 'getactivewindow', 'windowmove', '20%', '20%', 'windowsize', '70%', '50%'],
    'scr_cap': ['import', '-window', 'root', '~/Pictures/$(date', '+%Y%m%dT%H%M%S).png'],
    'scr_cap_sel': ['import', '~/Pictures/$(date', '+%Y%m%dT%H%M%S).png'],
    'scr_lock': ['slock'],
    'autolockd_xautolock': ['xautolock\n\t-time', '3', '-locker', '"mxctl.control', 'scr_lock_if"\n\t-killtime', '10', '-killer', '"notify-send', '-u', 'critical', '-t', '10000', '--', "'Killing", 'system', '...\'"\n\t-notify', '30', '-notifier', '"notify-send', '-u', 'critical', '-t', '10000', '--', "'Locking", 'system', 'ETA', '30s', '...\'";\n'],
}

Funs = {
    'kb_led_on'     :       mksh(Cmds['kb_led_on'  ]),
    'kb_led_off'    :       mksh(Cmds['kb_led_off' ]),
    'win_left'      :       mksh(Cmds['win_left'   ]),
    'win_right'     :       mksh(Cmds['win_right'  ]),
    'win_max'       :       mksh(Cmds['win_max'    ]),
    'win_unmax'     :       mksh(Cmds['win_unmax'  ]),
    'win_big'       :       mksh(Cmds['win_big'    ]),
    'win_small'     :       mksh(Cmds['win_small'  ]),
    'scr_cap'       :       mksh(Cmds['scr_cap'    ]),
    'scr_cap_sel'   :       mksh(Cmds['scr_cap_sel']),
    'scr_lock'      :       mksh(Cmds['scr_lock'   ]),
    'autolockd_xautolock':  mksh(Cmds['autolockd_xautolock'])
}

