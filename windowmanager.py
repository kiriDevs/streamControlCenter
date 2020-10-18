from tkinter import Tk as newWindow

mainWin = newWindow()
views = {}
current_view = None


def registerView(view, name):
    views[name] = view


def switchView(to_view_name):
    # Removing current view from window, if applicable
    global current_view
    if current_view is not None:
        current_view.destroy()

    try:
        to_view = views[to_view_name]  # Getting the view with the desired name from the registered views
    except KeyError:
        mainWin.destroy()
        raise KeyError

    if to_view.on_load:
        to_view.on_load()  # If an on_load Method is defined, run it before drawing the view

    to_view.draw()  # Drawing the new view to the window

    if to_view_name == "error":
        import errorview
        if errorview.titleAppendix is not None:
            mainWin.title(f"Stream Control Panel - Critical Error: {errorview.titleAppendix}")
        else:
            mainWin.title("Stream Control Panel - Critical Error")
    else:
        mainWin.title(to_view.title)  # Changing window title to match the new view

    current_view = to_view  # Re-Setting current_view

    mainWin.mainloop()

def close():
    mainWin.destroy()
