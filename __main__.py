import traceback

import windowmanager as winman

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
    exit(1)

winman.switchView("mainmenu")

exit(0)
