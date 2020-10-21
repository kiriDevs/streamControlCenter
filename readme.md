# streamControlCenter
A simple Control Center for your stream on Twitch, written in Python using the TwitchAPI, requests and tkinter!

## Installation
At first, make sure you meet all the requirements in terms of dependencies. You can install all of them via `pip install [package name]` (or `pip3 ...` if you are using multiple pip installations).
#### Dependencies
- `tkinter`
- `requests`
- `tqdm`

Download the files in this repository and make sure to keep them all in a single directory. You can rename the directory, obviously, but make sure they all share the same path.

## Usage
`python __main__.py` (or `python3 __main__.py for` for multiple python installations) should be enough for startup. After a very short time and a loading bar in the terminal showing how the initialization of the different views is coming along, you will see the GUI pop up. From there, everything should be self-explanatory.

#### Note on runtime errors:
Some common and expected errors will be announced by a special view in the GUI telling you an error occured and what to do about it.
<br>
These errors are:
* auth.yml is not properly filled

While this list is likely to be extended in the future, all other errors will have the exception stack trace printed in the console. Feel free to open an issue here on Github if you need further assistance of have found your error is a problem with the source code.
