#!/usr/bin/env python

from AppKit import NSScreen
import appscript
import sys

"""
Resize the window to the left or right half of the screen its on

"""
def get_active_window():
    sev = appscript.app(u'System Events')
    thapp = sev.application_processes[
        appscript.its.frontmost == True
    ].application_processes[1].name.get()
    return appscript.app(thapp).windows[1].get()

def get_screens():
    return NSScreen.screens()

def frame_to_bounds(frame):
    return (
        frame.origin.x,
        frame.origin.y,
        frame.origin.x + frame.size.width,
        frame.origin.y + frame.size.height,
    )

def get_windows_screen(bounds):
    centre = (
        bounds[0] + (bounds[2] - bounds[0]) / 2,
        bounds[1] + (bounds[3] - bounds[1]) / 2
    )
    print('centre', centre)
    screens = get_screens()
    screenlist = []
    for screen in screens:
        tf = frame_to_bounds(screen.frame())
        #if screenlist[len(screenlist)-1]:
            
        screenlist.append(tf)
        if tf[0] <= centre[0] <= tf[2] and \
           tf[1] <= centre[1] <= tf[3]:
            return screen
    print('sl', screenlist)

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
            # print('zeroscreen is above')
            s[1] = zeroscreen[3]
            s[3] = s[1] + sh
        elif s[1] == zeroscreen[3]:
            # print('zeroscreen is below')
            zeroscreen[1] = s[1]
            zeroscreen[3] = zeroscreen[3] + sh
            s[1] = 0.0
            s[3] = sh
        elif s[0] < 0 and s[3] == zeroscreen[3]:
            print('zeroscreen is right')
        elif s[0] == zeroscreen[2]:
            print('zeroscreen is left')
    screenlist.insert(0, zeroscreen)
    return screenlist

"""

Screen origins are measured from the top left corner of the zero screen in positive down and right.

Window origins are measured from bottom left corner of the zero screen
in positive right and down.

"""    
    
def which_screen_contains_window(screenlist, window_bounds):
    winsize = window_bounds[2] - window_bounds[0], window_bounds[3] - window_bounds[1]
    winpos = window_bounds[0], window_bounds[1]
    centerx = winpos[0] + winsize[0] / 2.0
    centery = winpos[1] + winsize[1] / 2.0
    screencount = 0
    for screen in screenlist:
        if screen[0] < centerx < screen[2] and \
           screen[0] < centery < screen[3]:
            break
        screencount += 1
    return screencount if screencount < len(screenlist) else -1

def doit(direction=-1, resize=1):
    thwin = get_active_window()
    bounds = thwin.bounds()
    """
    winsize = bounds[2] - bounds[0], bounds[3] - bounds[1]
    winpos = bounds[0], bounds[1]
    centerx = winpos[0] + winsize[0] / 2.0
    centery = winpos[1] + winsize[1] / 2.0
    sorigin = winpos #s.frame().origin
    ssize = winsize #s.frame().size
    """
    screens = NSScreen.screens()
    screenlist = [frame_to_bounds(s.frame()) for s in screens]
    screenid = which_screen_contains__window(screenlist, window)
    """     for s in 
        fbounds = 
        print(s, fbounds, NSScreen._isZeroScreen(s), NSScreen._menuBarHeight(s))
        #s.convertRectFromBacking_(

Screens must be aligned with each other.





"""
    print('sss', sorigin, ssize)
    """
    for t in dir(NSScreen):
        print(' ', t)
    if resize==1:
        dw = ssize[1] / 2.0
    else:
        dw = winsize[0]
    dh = ssize[1]
    if direction < 0:
        # thwin.position.set([sorigin.x, 0])
        ox, oy = sorigin[0], sorigin[1]
    elif direction > 0:
        # thwin.position.set([sorigin.x + dw, 0])
        ox, oy = sorigin[0] + \
             (ssize[1] - dw), \
             sorigin[1]
    else:
        dw = ssize[1]
        ox, oy = sorigin[0], sorigin[1]
    #thwin.size.set([dw, dh])
    newbounds = [
        ox,
        oy,
        ox + dw,
        oy + dh
        ]
    print('newb', newbounds)
    thwin.bounds.set(newbounds)
"""
    """
    try:
    except Exception as e:
    with open('/tmp/wrs.log', 'w') as log:
        log.write(str(e))
       """     
if __name__ == '__main__':
    doit(
        *[int(n) for n in sys.argv[1:]]
    )
