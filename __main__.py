import traceback
from tqdm import tqdm
from os import system as syscall

import windowmanager as winman


def quit(code):
    syscall("rm -rfd __pycache__")
    exit(code)


viewImports = [
    "import channelcheckview",  # Creating channelcheckview
    "import titlechangeview",  # Creating titlechangeview
    "import mainview"  # finally, creating the mainview
]

print("Creating views...")
# noinspection PyBroadException
try:
    # Creating a loading bar for the view imports
    for i in tqdm(range(len(viewImports))):
        exec(viewImports[i])

except Exception:
    trace = traceback.format_exc()
    print("Exception occured in runtime:")
    print("")
    print(trace)
    quit(1)

winman.switchView("mainmenu")

quit(0)
