import traceback

from os import system as syscall

import windowmanager as winman



def quit(code):
    syscall("rm -rfd __pycache__")
    exit(code)


# noinspection PyBroadException
try:
    # Importing views
    import channelcheckview
    import titlechangeview

    # Importing Main View
    import mainview
except Exception:
    trace = traceback.format_exc()
    print("Exception occured in runtime:")
    print("")
    print(trace)
    quit(1)

winman.switchView("mainmenu")

quit(0)
