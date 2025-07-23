# http://202.207.12.156:9012/context/c03152f5db8918b9905d449686685f77
import requests
import json

def firstPrint(board, x, y):
    ans = ''
    moveList = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
    for i in range(len(moveList)):
        if x+moveList[i] > 14:
            continue
        if x+moveList[i] < 0:
            continue
        ans+=board[x+moveList[i]][y]
    return ans
def secondPrint(board, x, y):
    ans = ''
    moveList = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
    for i in range(len(moveList)):
        if x+moveList[i] > 14:
            continue
        if x+moveList[i] < 0:
            continue
        if y-moveList[i] > 14:
            continue
        if y-moveList[i] < 0:
            continue
        ans+=board[x+moveList[i]][y-moveList[i]]
    return ans
def thirdPrint(board, x, y):
    ans = ''
    moveList = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
    for i in range(len(moveList)):
        if y+moveList[i] > 14:
            continue
        if y+moveList[i] < 0:
            continue
        ans+=board[x][y+moveList[i]]
    return ans
def fourthPrint(board, x, y):
    ans = ''
    moveList = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
    for i in range(len(moveList)):
        if x-moveList[i] > 14:
            continue
        if x-moveList[i] < 0:
            continue
        if y-moveList[i] > 14:
            continue
        if y-moveList[i] < 0:
            continue
        # if x==1 and y==13:
            # print(x-moveList[i], end=' ')
            # print(y-moveList[i])
        ans+=board[x-moveList[i]][y-moveList[i]]
    return ans
    # indexX, indexY=x, y
    # if y < 4:
        # indexX = 4-x
    # if y > 11:
        # indexY = 8-(y-11)

if __name__=='__main__':
    whiteLocations=[]
    blackLocations=[]

    url='http://202.207.12.156:9012/step_07'
    base="http://202.207.12.156:9012/step_07?ans="

    respond=requests.get(url)
    data = json.loads(respond.text)
    dataBoard = data['board']
    jsonData = data['coord']

    for i in range(len(dataBoard)//2):
        xLocation = i*2
        yLocation = i*2+1
        if i%2 == 0:
            blackLocations.append((ord(dataBoard[xLocation])-ord('a'), ord(dataBoard[yLocation])-ord('a')))
        else:
            whiteLocations.append((ord(dataBoard[xLocation])-ord('a'), ord(dataBoard[yLocation])-ord('a')))

    board = [['.' for i in range(15)] for j in range(15)] 
    for i in range(len(blackLocations)):
        board[blackLocations[i][0]] [blackLocations[i][1]]='x'
        board[whiteLocations[i][0]] [whiteLocations[i][1]]='o'

    _ans=''
    for i in range(len(jsonData)):
        x = ord(jsonData[i][0])-ord('a')
        y = ord(jsonData[i][1])-ord('a')

        if _ans != '':
            _ans+=','
        _ans+=firstPrint(board, x, y)
        
        if _ans != '':
            _ans+=','
        _ans+=secondPrint(board, x, y)

        if _ans != '':
            _ans+=','
        _ans+=thirdPrint(board, x, y)

        if _ans != '':
            _ans+=','
        _ans+=fourthPrint(board, x, y)

    print(_ans)

    respond=requests.get('http://202.207.12.156:9012/step_07?ans='+_ans)
    print(respond.text)
