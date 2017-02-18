#!/usr/bin/env python

from AppKit import NSScreen
import appscript
import sys
import os

"""
Resize the window to the left or right half of the screen its on

"""
def get_active_window():
    sev = appscript.app(u'System Events')
    thapp = sev.application_processes[
        appscript.its.frontmost == True
    ].application_processes[1].name.get()
    app_translations = {
        'soffice': 'LibreOffice'
    }
    if thapp in app_translations.keys():
        thapp = app_translations[thapp]
    app = appscript.app(thapp)
    if hasattr(app, 'windows'):
        return app.windows[1].get()
    else:
        raise Exception(
            '{} does not reference windows to applescript'.format(
                thapp
            )
        )

def get_screens():
    return NSScreen.screens()

def frame_to_bounds(frame):
    return [
        frame.origin.x,
        frame.origin.y,
        frame.origin.x + frame.size.width,
        frame.origin.y + frame.size.height,
    ]

def screenlist_to_desktop(screenlist):
    if len(screenlist) == 1:
        return screenlist[0]
    desktop_bounds = [0, 0, 0, 0]
    for screen in screenlist:
        if screen[0] < desktop_bounds[0]:
            desktop_bounds[0] = screen[0]
        if screen[1] < desktop_bounds[1]:
            desktop_bounds[1] = screen[1]
        if screen[2] > desktop_bounds[2]:
            desktop_bounds[2] = screen[2]
        if screen[3] > desktop_bounds[3]:
            desktop_bounds[3] = screen[3]
    if desktop_bounds[0] < 0:
        shiftx = abs(desktop_bounds[0])
    else:
        shiftx = 0
    desktop_bounds[0] += shiftx
    desktop_bounds[2] += shiftx
    if desktop_bounds[1] < 0:
        shifty = abs(desktop_bounds[1])
    else:
        shifty = 0
    desktop_bounds[1] += shifty
    desktop_bounds[3] += shifty
    return desktop_bounds
    ### TODO: apply shiftx and shifty values to screen list

def coordinate_screens(screenlist):
    zeroscreen = screenlist.pop(0)
    # compare each screen to zero screen
    # determine if it is above, below, left or right
    # adjust to window oriented coordinates
    for s in screenlist:
        sh = s[3] - s[1]
        sw = s[2] - s[0]
        if s[1] < 0 and s[3] == 0:
            #print('zeroscreen is above')
            s[1] = zeroscreen[3]
            s[3] = s[1] + sh
        elif s[1] == zeroscreen[3]:
            #print('zeroscreen is below')
            s[1] = - sh
            s[3] = 0
        elif s[0] < 0 and s[3] == zeroscreen[3]:
            #print('zeroscreen is right')
            s[3] += abs(s[1])
            s[1] += abs(s[1])
        elif s[0] == zeroscreen[2]:
            #print('zeroscreen is left')
            s[1] += abs(s[1])
    screenlist.insert(0, zeroscreen)
    return screenlist

def which_screen_contains_window(screenlist, window_bounds):
    winsize = window_bounds[2] - window_bounds[0], window_bounds[3] - window_bounds[1]
    winpos = window_bounds[0], window_bounds[1]
    centerx = winpos[0] + winsize[0] / 2.0
    centery = winpos[1] + winsize[1] / 2.0
    screencount = 0
    for screen in screenlist:
        if screen[0] < centerx < screen[2] and \
           screen[1] < centery < screen[3]:
            break
        screencount += 1
    return screencount if screencount < len(screenlist) else -1

def doit(direction=-1, resize=1):
    thwin = get_active_window()
    win_bounds = thwin.bounds()
    screens = NSScreen.screens()
    screenlist = coordinate_screens([frame_to_bounds(s.frame()) for s in screens])
    screenid = which_screen_contains_window(screenlist, win_bounds)
    screen_bounds = screenlist[screenid]
    screen_size = [
        screen_bounds[n+2] - screen_bounds[n] for n in range(len(screen_bounds)) if
        n < len(screen_bounds) - 2
    ]
    window_size = [
        win_bounds[n+2] - win_bounds[n] for n in range(len(win_bounds)) if
        n < len(win_bounds) - 2
    ]
    if resize==1:
        dw = screen_size[0] / 2.0
    else:
        dw = window_size[0]
    dh = screen_size[1]
    if direction < 0:
        ox, oy = screen_bounds[0:2]
    elif direction > 0:
        ox, oy = screen_bounds[0] + (screen_size[0] - dw), screen_bounds[1]
    else:
        dw = screen_size[0]
        ox, oy = screen_bounds[0:2]
    newbounds = [int(n) for n in ox, oy, ox + dw, oy + dh]
    thwin.bounds.set(newbounds)

if __name__ == '__main__':
    if len(sys.argv[1:]) < 2:
        print("""Usage:
python {} [-1,1] [-1,0,1]
1. First argument
  -1: move window to left
  1: move window to right
2. Second argument 
  1: resizes of window to half screen
  0: resizes window to full screen
  -1: does not resize window

""".format(os.path.basename(__file__)))
    try:
        doit(
            *[int(n) for n in sys.argv[1:]]
        )
    except Exception as e:
        with open('/tmp/wrs.log', 'a') as log:
            log.write("{}\n".format(e))
        raise e
