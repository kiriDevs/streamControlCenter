class View:

    def __init__(self, title, on_load=None):
        self.title = f"Stream Control Panel - {title}"  # Title to be displayed as window title when the view is active
        self.struct = []  # Empty widget hierarchy
        self.on_load = on_load

    def addLine(self, row=None, *elements):
        self.struct.append(row)

    def draw(self, xpad=10, ypad=10):
        for row in self.struct:
            for element in row:
                element.grid(row=self.struct.index(row), column=row.index(element), padx=xpad, pady=ypad)

    def destroy(self):
        for row in self.struct:
            for element in row:
                element.grid_forget()
