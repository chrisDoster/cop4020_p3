import tkinter as tk
import math


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
        self.drawn = []
        # tkinter widgets, defined as instance fields for scope reasons
        self.canvas = tk.Canvas(self)
        # constants
        self.stateColor = 'SlateGray1'

    def __findDimensions(self):
        width = self.numStates*50 + (self.numStates-1)*50 + 100  # 50px/state, 50px/gap, 50px padding on both ends
        height = self.numStates*(self.numStates-1)*12 + 150 # 12*(numStates-1)px/state (for drawing transitions), 50px for the horizontal line of states, 50 px padding on top/bottom
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

    # sorts transitions in order to reduce the number of crossed lines
    def __sortTransitions(self):
        #fixme
        return

    # for each transition represented as a string, convert into a list of [curr, next] lists
    def __unpackTransitions(self):
        for fTrans in self.fTransitions:
            withoutParens = fTrans.replace('(', '').replace(')', '')
            tokens = withoutParens.split(':')
            self.transitions.append([int(tokens[0]), int(tokens[1]), tokens[2]])
        self.__sortTransitions()

    def __drawStartArrow(self, x, y):
        xDist = 6
        yDist = 9
        self.canvas.create_line(x-12, y+47, x+xDist-4, y+45-yDist)
        tipX = x+xDist-4
        tipY = y+45-yDist
        self.canvas.create_line(tipX-9, tipY, tipX, tipY, tipX, tipY+10)

    def __drawStates(self):
        y = 50
        i = 0
        for x in self.regions:
            self.canvas.create_oval(x, y, x+50, y+50, fill=self.stateColor)
            txt = self.canvas.create_text(x+25, y+25, text=str(i), font='consolas 12')
            self.canvas.tag_raise(txt)
            if i in self.accept:
                self.canvas.create_oval(x+5, y+5, x+45, y+45)
            if i == self.start:
                self.__drawStartArrow(x,y)
            i += 1

    def __alreadyDrawn(self, small, big):
        for t in self.drawn:
            if big == t[0] and small == t[1]:
                return True
            elif small == t[0] and big == t[1]:
                return True
        return False

    def __markDrawn(self, t):
        self.drawn.append(t)

    # draw a single unpacked transition, t, taking a U-shaped route with the height of the U-shape being offset
    def __drawTrans(self, t, offset):
        if offset == 0:
            if t[0] == t[1]: # self transition
                xDist = 25*math.cos(math.pi/4) # x distance to point where circles intersect
                yDist = 25*math.sin(math.pi/4) # y distance to point where circles intersect
                # draw loop from state to itself
                x0 = self.regions[t[0]] + 25 - xDist
                y0 = 25
                loop = self.canvas.create_oval(x0, y0, x0+2*xDist, y0+50)
                # draw arrowhead for self-transition
                x1 = self.regions[t[0]] + 25 - xDist - 8
                y1 = 75 - yDist - 4
                x2 = x1+9
                y2 = y1+3
                x3 = x2+6
                y3 = y2-10
                arrowhead = self.canvas.create_line(x1, y1, x2, y2, x3, y3)
                # move transition to bottom
                self.canvas.tag_lower(loop)
                self.canvas.tag_lower(arrowhead)
                self.canvas.create_text(x0+25-(xDist/2), y0-9, text=t[2], font='consolas 10')
            elif t[0] < t[1]: # transition right
                x0 = self.regions[t[0]] + 50
                y0 = 75
                x1 = x0+50
                y1 = y0
                self.canvas.create_line(x0, y0, x1, y1)
                self.canvas.create_line(x1-7, y1-7, x1, y1, x1-7, y1+7)
                self.canvas.create_text(x0+25, y0-9, text=t[2], font='consolas 10')
            else: # transition left
                x0 = self.regions[t[0]]
                y0 = 75
                x1 = x0-50
                y1 = y0
                self.canvas.create_line(x0, y0, x1, y1)
                self.canvas.create_line(x1+7, y1-7, x1, y1, x1+7, y1+7)
                self.canvas.create_text(x1+25, y0-9, text=[2], font='consolas 10')
        else:
            x0 = self.regions[t[0]]+25
            y0 = 100
            x1 = x0
            y1 = offset
            x2 = self.regions[t[1]]+25
            y2 = y1
            x3 = x2
            y3 = y0
            self.canvas.create_line(x0, y0, x1, y1, x2, y2, x3, y3)
            self.canvas.create_line(x3-7, y3+7, x3, y3, x3+7, y3+7)
            x4 = (x0+x3)/2
            y4 = offset-5
            self.canvas.create_text(x4, y4, text=t[2], font='consolas 10')

             
    def __drawAdjacentTransitions(self):
        for trans in self.transitions:
            bigger = max(trans[0], trans[1])
            smaller = min(trans[0], trans[1])
            if (bigger-smaller) == 1: # if the states in the transition are adjacent
                if self.__alreadyDrawn(smaller, bigger): # if these states are already connected 
                    continue
                self.__drawTrans(trans, 0)
                self.__markDrawn(trans)

    def __drawSelfTransitions(self):
        for trans in self.transitions:
            if trans[0] == trans[1]:
                self.__drawTrans(trans, 0)
                self.__markDrawn(trans)


    def __drawTransitions(self):
        self.__drawAdjacentTransitions()
        self.__drawSelfTransitions()
        numTrans = len(self.transitions)
        yOffset = 112
        for trans in self.transitions:
            if trans in self.drawn:
                continue
            self.__drawTrans(trans, yOffset)
            yOffset += 12

    def build(self, fsa):
        self.__setValues(fsa.numStates, fsa.transitions, fsa.start, fsa.accept)
        self.__findDimensions()
        self.__defineRegions()
        self.__unpackTransitions()

        self.canvas.config(width=self.dimensions[0], height=self.dimensions[1])
        self.__drawStates()
        self.__drawTransitions()

    def display(self):
        self.geometry(f'{self.dimensions[0]}x{self.dimensions[1]}+100+100')

        self.canvas.pack()
        self.mainloop()