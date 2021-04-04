import sys
import fsa
import gui


def handleInput(fsm, input):
    f = open(input, 'r')
    s = f.read()

    if fsm.isLegal(s):
        print(f'{s} is legal!')
    else:
        print(f'{s} not legal...')


if __name__ == "__main__":
    # main logic
    if len(sys.argv) < 3:
        print('ERROR: too few command-line args')
    else:
        fsaFile = sys.argv[1]
        inputFile = sys.argv[2]

        fsm = fsa.FSA()
        fsm.fromFile(fsaFile)

        handleInput(fsm, inputFile)
        gui = gui.GUI()
        gui.build(fsm)
        gui.display()