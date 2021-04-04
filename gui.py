import tkinter as tk


class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.__setValues(-1, [], -1, [])

    def __setValues(self, numStates, transitions, start, accept):
        self.numStates = numStates
        self.fTransitions = transitions
        self.start = start
        self.accept = accept
        # default values, updated later
        self.dimensions = [600, 600]
        self.regions = []
        self.transitions = []
        # tkinter widgets, defined as instance fields for scope reasons
        self.canvas = tk.Canvas(self)

    def __findDimensions(self):
        width = self.numStates*50 + (self.numStates-1)*50 + 100  # 50px/state, 50px/gap, 50px padding on both ends
        height = self.numStates*25 + 150 # 25px/state (for drawing transitions), 50px for the horizontal line of states, 50 px padding on top/bottom
        self.dimensions[0] = width
        self.dimensions[1] = height

    def __defineRegions(self):
        if self.regions != []:
            return
        self.regions.append(50)
        prev = self.regions[0]
        for i in range(self.numStates-1):
            prev += 100
            self.regions.append(prev)

    # for each transition represented as a string, convert into a list of [curr, next] lists
    def __unpackTransitions(self):
        for fTrans in self.fTransitions:
            withoutParens = fTrans.replace('(', '').replace(')', '')
            tokens = withoutParens.split(':')
            self.transitions.append([int(tokens[0]), int(tokens[1]), tokens[2]])

    def __drawStates(self):
        y = 50
        i = 0
        for x in self.regions:
            self.canvas.create_oval(x, y, x+50, y+50)
            self.canvas.create_text(x+25, y+25, text=str(i))
            i += 1

    def build(self, fsa):
        self.__setValues(fsa.numStates, fsa.transitions, fsa.start, fsa.accept)
        self.__findDimensions()
        self.__defineRegions()
        self.__unpackTransitions()

        self.canvas.config(width=self.dimensions[0], height=self.dimensions[1])
        self.__drawStates()

    def display(self):
        self.geometry(f'{self.dimensions[0]}x{self.dimensions[1]}+100+100')

        self.canvas.pack()
        self.mainloop()