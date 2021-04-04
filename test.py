import sys
import fsa

#improves readability / leaves room for redefinition
def succ(msg):
    print(f'[SUCCESS]    ({msg})')
    
def fail(msg):
    print(f'[FAIURE]    ({msg})')

#main function
if __name__ == '__main__':
    print('Tests begin:')

    # constructor
    print(' \nConstructor Tests:')
    fsm = fsa.FSA()

    if fsm.numStates == 0:
        succ('numStates')
    else:
        fail('numStates')

    if fsm.alphabet == []:
        succ('alphabet')
    else:
        fail('alphabet')

    if fsm.transitions == []:
        succ('transitions')
    else:
        fail('transitions')

    if fsm.start == -1:
        succ('start')
    else:
        fail('start')

    if fsm.accept == []:
        succ('accept')
    else:
        fail('accept')

    # factory method: load
    print(' \nLoad Function')
    fsm.load(2, ['a'], ['(0:1:a)','(1:0:a)'], 0, [0])
    
    loadSuccess = fsm.numStates == 2
    if (loadSuccess == False):
        fail('numStates')
    loadSuccess = fsm.alphabet[0] == 'a'
    if (loadSuccess == False):
        fail('alphabet')
    loadSuccess = fsm.transitions[0] == '(0:1:a)' and fsm.transitions[1] == '(1:0:a)'
    if (loadSuccess == False):
        fail('transitions')
    loadSuccess = fsm.start == 0
    if (loadSuccess == False):
        fail('start')
    loadSuccess = fsm.accept[0] == 0
    if (loadSuccess == False):
        fail('accept')

    if (loadSuccess):
        succ('load function')

    # method: isLegal
    print(' \nisLegal Function')
    if fsm.isLegal('aaaa'):
        succ('aaaa is legal')
    else:
        fail('aaaa is not legal')
    
    if fsm.isLegal('aaa'):
        fail('aaa is legal')
    else:
        succ('aaa is not legal')

    fsm2 = fsa.FSA()
    fsm2.load(2,['a','b'],['(0:0:b)','(0:1:a)','(1:1:a)','(1:0:b)'],0,[0]) # fsm that accepts words that start and end with 'b'

    if fsm2.isLegal('bab'):
        succ('bab is legal')
    else:
        fail('bab is not legal')
    
    if fsm2.isLegal('babaaaaab'):
        succ('babaaaaab is legal')
    else:
        fail('babaaaaab is not legal')
    
    if fsm2.isLegal('baaba'):
        fail('baaba is legal')
    else:
        succ('baaba is not legal')

