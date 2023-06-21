#!/usr/bin/env python

import control_app as Ctl

def test_findapps():
   apps = Ctl.find()

def test_parsedesktopfile():
   app = Ctl.parsedesktopfile(nil, "tests/res/URxvtc.desktop")

def test_tmenu_run():
   app = Ctl.tmenu_run()

