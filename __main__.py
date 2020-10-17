import traceback

import windowmanager as winman

# noinspection PyBroadException
try:
    import channelcheckview
    import mainview
except Exception:
    trace = traceback.format_exc()
    print("Exception occured in runtime:")
    print("")
    print(trace)
    exit(1)

winman.switchView("mainmenu")

exit(0)
