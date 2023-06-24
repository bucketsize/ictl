import os
import io
import subprocess
import logging

logger = logging.getLogger()

def brightness(delta):
    logger.info("brightness", delta)
    bf = os.listdir("/sys/class/backlight")
    if bf:
        bf = bf[0]
        max = int(io.open(f"/sys/class/backlight/{bf}/max_brightness", "r").read())
        cur = int(io.open(f"/sys/class/backlight/{bf}/brightness", "r").read())
        tar = int(cur + delta * max / 100)
        if tar > max:
            tar = max
        if tar < 0:
            tar = cur
        logger.info("brightness", delta, bf, cur, tar, max)
        with io.open(f"/sys/class/backlight/{bf}/brightness", "w") as h:
            h.write(str(tar))

def brightness_up():
    brightness(Cfg.lux_step)

def brightness_down():
    brightness(-Cfg.lux_step)

