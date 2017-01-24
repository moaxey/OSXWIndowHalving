#!/usr/bin/env python

from AppKit import NSScreen
import appscript
import sys

"""
Resize the window to the left or right half of the screen its on

"""


def doit(direction=-1, resize=1):
    try:
        sev = appscript.app(u'System Events')
        thapp = sev.application_processes[
            appscript.its.frontmost == True
            ].application_processes[1].name.get()
        thwin = appscript.app(thapp).windows[1].get()
        bounds = thwin.bounds()
        winsize = bounds[2] - bounds[0], bounds[3] - bounds[1]
        winpos = bounds[0], bounds[1]
        centerx = winpos[0] + winsize[1] / 2.0
        screens = [(s.frame().origin.x,
                    s.frame().origin.y,
                    s.frame().origin.x + s.frame().size.width,
                    s.frame().origin.y + s.frame().size.height,
                    )
                   for s in NSScreen.screens()]
        for s in NSScreen.screens():
            if s.frame().origin.x < centerx < \
                    s.frame().origin.x + s.frame().size.width:
                if resize==1:
                    dw = s.frame().size.width / 2.0
                else:
                    dw = winsize[0]
                dh = s.frame().size.height
                if direction < 0:
                    # thwin.position.set([s.frame().origin.x, 0])
                    ox, oy = s.frame().origin.x, s.frame().origin.y
                elif direction > 0:
                    # thwin.position.set([s.frame().origin.x + dw, 0])
                    ox, oy = s.frame().origin.x + \
                             (s.frame().size.width - dw), \
                             s.frame().origin.y
                else:
                    dw = s.frame().size.width
                    ox, oy = s.frame().origin.x, s.frame().origin.y
                #thwin.size.set([dw, dh])
                thwin.bounds.set([
                        ox,
                        oy,
                        ox + dw,
                        oy + dh
                        ])
                break
    except Exception as e:
        with open('/tmp/wrs.log', 'w') as log:
            log.write(str(e))
            
if __name__ == '__main__':
    doit(
        *[int(n) for n in sys.argv[1:]]
    )
