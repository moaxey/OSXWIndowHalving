import pytest

from get_window_and_resize import (
    get_active_window,
    get_screens,
    get_windows_screen,
    frame_to_bounds,
    which_screen_contains_window,
    screenlist_to_desktop,
    coordinate_screens,
)

def test_get_active_window():
    win = get_active_window()
    assert type(win).__name__ == 'Reference', 'windows not an applescript ref'
    bounds = win.bounds()
    assert type(bounds).__name__ == 'tuple', 'window bounds are not a tuple'
    assert len(bounds) == 4, 'length of window bounds tuple is not 4'
    print('bounds', bounds)

def test_get_screens():
    screens = get_screens()
    assert len(screens) > 0, 'no screens found'
    if len(screens) > 1:
        assert type(screens).__name__ == '__NSArrayI', 'screens not an NSArrayI'
    elif len(screens) == 1:
        assert type(screens).__name__ == '__NSSingleObjectArrayI', 'screen not an __NSSingleObjectArrayI'
    screen = screens[0]
    assert type(screen).__name__ == 'NSScreen', 'first screen in not NSScreen'
    frame = screen.frame()
    assert type(frame).__name__ == 'NSRect', 'frame() does not return NSRect'

def test_desktop_bounds():
    s0_above = [[0.0, 0.0, 1440.0, 900.0], [0.0, -1200.0, 1920.0, 0.0]]
    dbounds = screenlist_to_desktop(s0_above)
    assert dbounds == [0, 0.0, 1920.0, 2100.0]

def test_coordinate_screens():
    s0_above = [[0.0, 0.0, 1440.0, 900.0], [0.0, -1200.0, 1920.0, 0.0]]
    csl = coordinate_screens(s0_above)
    assert csl == [[0.0, 0.0, 1440.0, 900.0], [0.0, 900.0, 1920.0, 2100.0]], \
        'screens not coordinated when zeroscreen is above'
    s0_below = [[0.0, 0.0, 1440.0, 900.0], [0.0, 900.0, 1920.0, 2100.0]]
    csl = coordinate_screens(s0_below)
    assert csl == [[0.0, 900, 1440.0, 2100.0], [0.0, 0.0, 1920.0, 1200.0]], \
        'screens not coordinated when zeroscreen is below'
""" 
zeroscreen     screens()                                           window bounds screen 2
above [[0.0, 0.0, 1440.0, 900.0], [0.0, -1200.0, 1920.0, 0.0]]     (523, 1499, 1116, 2038)
below [[0.0, 0.0, 1440.0, 900.0], [0.0, 900.0, 1920.0, 2100.0]]    (523, -601, 1116, -62)
right [[0.0, 0.0, 1440.0, 900.0], [-1920.0, -300.0, 0.0, 900.0]])  (-1397, 599, -804, 1138)
left  [[0.0, 0.0, 1440.0, 900.0], [1440.0, -300.0, 3360.0, 900.0]] (1963, 599, 2556, 1138)

"""
    
def test_frame_to_bounds():
    screens = get_screens()
    fbounds = frame_to_bounds(screens[0].frame())
    assert type(fbounds).__name__ == 'tuple', 'frame bounds are nout a tuple'
    assert len(fbounds) == 4, 'frame bounds not four values'
    assert fbounds[0] < fbounds[2], 'left is greater than right'
    assert fbounds[1] < fbounds[3], 'top is greater than bottom'

def test_get_windows_screen():
    boundlist = (577, -562, 1170, -23), (0, 0, 100, 100)
    for bounds in boundlist:
        screen = get_windows_screen(bounds)
        assert type(screen).__name__ == 'NSScreen', 'screen in not NSScreen'
        frame = screen.frame()
        assert type(frame).__name__ == 'NSRect', 'frame() does not return NSRect'
        print('frame', frame)

def test_which_screen_contains__window():
    s0_above = [[0.0, 0.0, 1440.0, 900.0], [0.0, -1200.0, 1920.0, 0.0]]
    s0_win = (0, 23, 100, 100)
    s1_win = (523, 1499, 1116, 2038)
    sid = which_screen_contains_window(s0_above, s0_win)
    assert sid == 0, 'window should be on screen 0'
    sid = which_screen_contains_window(s0_above, s1_win)
    assert sid == 1, 'window should be on screen 1'
