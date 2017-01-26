import pytest

from get_window_and_resize import (
    get_active_window,
    get_screens,
    frame_to_bounds,
    which_screen_contains_window,
    screenlist_to_desktop,
    coordinate_screens,
)

@pytest.fixture
def screen_zero_above():
    return [[0.0, 0.0, 1440.0, 900.0], [0.0, -1200.0, 1920.0, 0.0]]

@pytest.fixture
def screen_zero_below():
    return [[0.0, 0.0, 1440.0, 900.0], [0.0, 900.0, 1920.0, 2100.0]]

@pytest.fixture
def screen_zero_right():
    return [[0.0, 0.0, 1440.0, 900.0], [-1920.0, -300.0, 0.0, 900.0]]

@pytest.fixture
def screen_zero_left():
    return [[0.0, 0.0, 1440.0, 900.0], [1440.0, -300.0, 3360.0, 900.0]]

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
    dbounds = screenlist_to_desktop(screen_zero_above())
    assert dbounds == [0, 0.0, 1920.0, 2100.0]

def test_coordinate_screens():
    csl = coordinate_screens(screen_zero_above())
    assert csl == [[0.0, 0.0, 1440.0, 900.0], [0.0, 900.0, 1920.0, 2100.0]], \
        'screens not coordinated when zeroscreen is above'
    csl = coordinate_screens(screen_zero_below())
    assert csl == [[0.0, 0.0, 1440.0, 900.0], [0.0, -1200.0, 1920.0, 0.0]], \
        'screens not coordinated when zeroscreen is below'
    csl = coordinate_screens(screen_zero_right())
    assert csl == [[0.0, 0.0, 1440.0, 900.0], [-1920.0, 0.0, 0.0, 1200.0]], \
        'screens not coordinated when zeroscreen is right'
    csl = coordinate_screens(screen_zero_left())
    assert csl == [[0.0, 0.0, 1440.0, 900.0], [1440.0, 0.0, 3360.0, 900.0]], \
        'screens not coordinated when zeroscreen is left'

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
    assert type(fbounds).__name__ == 'list', 'frame bounds are nout a list'
    assert len(fbounds) == 4, 'frame bounds not four values'
    assert fbounds[0] < fbounds[2], 'left is greater than right'
    assert fbounds[1] < fbounds[3], 'top is greater than bottom'

def test_which_screen_contains_window():
    s0_win = (412, 23, 1013, 551)
    print('Test with zero screen below')
    s0_below = coordinate_screens(screen_zero_below())
    s1_win = (461, -639, 1062, -111)
    sid = which_screen_contains_window(s0_below, s0_win)
    assert sid == 0, 'window should be on screen 0'
    sid = which_screen_contains_window(s0_below, s1_win)
    assert sid == 1, 'window should be on screen 1'
    print('Test with zero screen above')
    s0_above = screen_zero_above()
    s1_win = (423, -618, 1024, -90)
    sid = which_screen_contains_window(s0_above, s0_win)
    assert sid == 0, 'window should be on screen 0'
    sid = which_screen_contains_window(s0_above, s1_win)
    assert sid == 1, 'window should be on screen 1'
    print('Test with zero screen right')
    s0_right = screen_zero_right()
    s1_win = (-1554, 481, -953, 1094)
    sid = which_screen_contains_window(s0_right, s0_win)
    assert sid == 0, 'window should be on screen 0'
    sid = which_screen_contains_window(s0_right, s1_win)
    assert sid == 1, 'window should be on screen 1'
    print('Test with zero screen left')
    s0_left = screen_zero_left()
    s1_win = (1734, 207, 2335, 820)
    sid = which_screen_contains_window(s0_left, s0_win)
    assert sid == 0, 'window should be on screen 0'
    sid = which_screen_contains_window(s0_left, s1_win)
    assert sid == 1, 'window should be on screen 1'

