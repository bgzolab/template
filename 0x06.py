# http://202.207.12.156:9012/context/3ff280105813f582c7c38dabedd901bc
import requests
import json

def printBoard(board):
    ans=""
    for i in range(len(board)):
        for j in range(len(board[i])):
            ans += board[i][j]
    return ans

if __name__=='__main__':
    whiteLocations=[]
    blackLocations=[]

    base="http://202.207.12.156:9012/step_06?ans="
    respond=requests.get('http://202.207.12.156:9012/step_06')
    data = (json.loads(respond.text))['questions']
    # data = 'ggffhggfhffgiefhfeheidehdidhghegcidfgiefcfeeeied'

    for i in range(len(data)//2):
        xLocation = i*2
        yLocation = i*2+1
        if i%2 == 0:
            blackLocations.append((ord(data[xLocation])-ord('a'), ord(data[yLocation])-ord('a')))
        else:
            whiteLocations.append((ord(data[xLocation])-ord('a'), ord(data[yLocation])-ord('a')))

    board = [['.' for i in range(15)] for j in range(15)] 

    temp=''
    for i in range(len(blackLocations)):
        print(temp)
        if temp != '': 
            temp +=','
        board[blackLocations[i][0]] [blackLocations[i][1]]='x'
        temp += printBoard(board)

        if temp != '':
            temp +=',' 
        board[whiteLocations[i][0]] [whiteLocations[i][1]]='o'
        temp += printBoard(board)

    respond=requests.get(base+temp)
    print(respond.text)