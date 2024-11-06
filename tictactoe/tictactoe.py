"""
Tic Tac Toe Player
"""

import math
import copy
X = "X"
O = "O"
EMPTY = None
b=[[X,EMPTY,O],[EMPTY,X,O],[X,EMPTY,EMPTY]]
b1=[[X,EMPTY,O],[EMPTY,X,O],[EMPTY,EMPTY,X]]
b2=[[X,X,X],[O,EMPTY,O],[EMPTY,EMPTY,EMPTY]]
b3=[[O,EMPTY,X],[O,X,EMPTY],[O,EMPTY,X]]
b4=[[X,EMPTY,O],[EMPTY,O,X],[O,EMPTY,X]]
b5=[[X,O,X],[O,O,X],[X,X,O]]

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    nX=0
    nO=0
    for row in board:
        for pole in row:
            if pole==X:
                nX=nX+1
            elif pole==O:
                nO=nO+1
    if nX==nO:
        return X
    else:
        return O
    
   


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    res=set()
    for row,i in zip(board,range(len(board))):
        if EMPTY in row:
            j=[index for index,cell in enumerate(row) if cell==EMPTY]
            cells=[(i,j1) for j1 in j]   
            res.update(cells)
    return res
    

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Incorrect action to current board.")
    sign=player(board)
    b=copy.deepcopy(board)
    b[action[0]][action[1]]=sign
    return b
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    res=None
    boardC=list(zip(*board))
    diag1=[]
    diag2=[]
    for row,col,i in zip(board,boardC,range(3)):
        diag1.append(row[i])
        diag2.append(row[-i-1])
        if all(cell==X for cell in row) or all(cell==X for cell in col):
            res=X
        if all(cell==O for cell in row) or all(cell==O for cell in col):
            res=O
    if all(cell==X for cell in diag1):
        res=X
    if all(cell==X for cell in diag2):
        res=X
    if all(cell==O for cell in diag1):
        res=O
    if all(cell==O for cell in diag2):
        res=O
    return res

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or not (any(cell==EMPTY for row in board for cell in row) and winner(board) is None):
        return True
    return False
    
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board)==True:
        if winner(board)==X:
            return 1
        elif winner(board)==O:
            return -1
        else:
            return 0
        
    



def maxi(board):
    
    if terminal(board):
        return utility(board),None
    
    val=float('-inf')
    baction=None
    for action in actions(board):
        #print(action,v1,"max")
        v,act=mini(result(board,action))
        if v>val:
            val=v
            baction=action
            if val==1:
                return val,baction
    return val,baction

def mini(board):
    #print("Funkcja")
    if terminal(board):
        #print("finish")
        return utility(board),None
    val=float('inf')
    baction=None
    for action in actions(board):
        #print(action,v1)
        v,act=maxi(result(board,action))
        if v<val:
            val=v
            baction=action
            if val==-1:
                return val,baction
    return val,baction

    

    
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    play=player(board)
    
    if play==X:
        m=maxi(board)[1]
    elif play==O:    
        m=mini(board)[1]
    return m

x=mini(b)
'''

def get_values(dic):
    suma = {}    
    for key, value in dic.items():
        if isinstance(value, dict):
            suma[key] = sum(v for v in get_nested_ints(value))
        elif isinstance(value, int):
            suma[key] = value

    return suma

def get_nested_ints(d):
    """Funkcja pomocnicza do wyciągania wszystkich liczb int z zagnieżdżonych słowników."""
    for v in d.values():
        if isinstance(v, dict):
            yield from get_nested_ints(v)
        elif isinstance(v, int):
            yield v
'''
