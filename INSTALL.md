Installation
============

Limitations
-----------

An increasing number of OSX applications no longer support AppleScript, which
this app uses to find the current app and communicate with its windows.

-   LibreOffice does not respond

-   There are certainly others.

You will get an error dialog when they fail. A log file at /tmp/wrs.log will
capture more detail about errors.

The resizing script
-------------------

### Easy method:

-   Download the pre-built app (get_window_and_resize)

-   Put it in your Applications folder

### Manual methods

-   Run the tests. You'll need pytest, pyappscript and pyobj in your default
    python.

-   Test it works on your terminal window. Run this to move it to the left side
    of the screen

>   \$ python get_window_and_resize.py -1 -1

#### Building and installing the App bundle

-   Build the app

>   \$ python setup.py py2app

-   Move the created app bundle from the ‘dist' folder to the Applications
    folder

### System integration

Double-click the workflows (in the workflows folder) and choose to install them.

The 'Services' menu item in any application menu should then contain entries
matching the workflow names and selecting them should affect Finder and Terminal
windows.

Set unique and memorable keyboard shortcuts for the services from

>   System Preferences \> Keyboard Shortcuts

Applications get the keyboard input first, so their shortcuts receive priority.
