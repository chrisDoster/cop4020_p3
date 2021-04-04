import re

class FSA:

    def __init__(self):
        self.__setValues(0, [], [], -1, [])
    
    # public method to set instance fields
    def load(self, numStates, alphabet, transitions, start, accept):
        self.__setValues(numStates, alphabet, transitions, start, accept)

    def fromFile(self, fileName):
        f = open(fileName, 'r')
        line = f.readline()

        params = line.split(';')
        numStates = int(params[0])
        alph = params[1].split(',')
        transitions = params[2].split(',')
        startState = int(params[3])
        acceptStates = params[4].split(',')
        for i in range(len(acceptStates)):
            acceptStates[i] = int(acceptStates[i])

        self.__setValues(numStates, alph, transitions, startState, acceptStates)
        

    # private helper
    def __setValues(self, numStates, alphabet, transitions, start, accept):
        self.numStates = numStates      #int
        self.alphabet = alphabet        #char arr
        self.transitions = []           #str arr
        for transition in transitions:  
            self.addTransition(transition)
        self.start = start              #int
        self.accept = accept            #int arr

        self.__finalState = -1
        
    # adds transition to transition array
    def addTransition(self, trans):
        self.transitions.append(trans)

    # determines if str is legal
    def isLegal(self, str):
        state = self.start
        for symbol in str:
            state = self.__stateChange(state, symbol)
            if state == -1:
                return False
        
        if state in self.accept:
            return True
        else:
            return False

    def __stateChange(self, state, sym):
        for t in self.transitions:
            # remove parentheses, split string into list of 3 items [inState, outState, symbol]
            withoutParens = re.sub('[()]','',t)
            tList = withoutParens.split(':')
            if int(tList[0]) == state and tList[2] == sym:
                self.__finalState = int(tList[1])
                return int(tList[1])
        return -1

    def status(self):
        status = f'INFO: \n# states: {self.numStates} \nlegal alph: {self.alphabet} \ntransitions: {self.transitions} '
        status += f'\nstart: {self.start} \naccept: {self.accept}'
        return status
        

