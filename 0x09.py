# http://202.207.12.156:9012/context/2e329756827e42330f7897cc9499588e
import requests
import json
import time
import webbrowser
import re

loginInfo='user=test&password=0x2eeb96e90ef7d8c0b0ba220c943c2cb2a9de0148962183ffd8451e6652515c5c39cdd986e69f57d5b4657af535b5d84de709dfbf9d6110de4ca8895773e90d87f5dcb66a03ad3aa653911b23869a0541fed2a7cad215ed960abeaef464e173652f0b7cdff504e3f30c0ef0b167aa5692633bef0a8f822c99e827f49417edfeaa'
deathFlag=0

def joinGame():
    global loginInfo
    response=requests.get('http://202.207.12.156:9012/join_game?data_type=json&'+loginInfo)
    gameIdJson=json.loads(response.text)
    gameId=gameIdJson['game_id']
    print('Have get the ticket:{0}'.format(gameId))
    return gameId

def printBoard(board):
    ans=""
    for i in range(len(board)):
        for j in range(len(board[i])):
            # ans += board[i][j]
            print(board[i][j], end=' ')
        print('')
    return ans

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
        ans+=board[x-moveList[i]][y-moveList[i]]
    return ans

def getStrScore(String): # 匹配两次??
    global deathFlag
    score=0
    if re.search(r'CMMMM', String) or re.search(r'MCMMM', String) or re.search(r'MMCMM', String)\
        or re.search(r'MMMCM', String) or re.search(r'MMMMC', String):
            score+=20000
    if re.search(r'OOOCO', String) or re.search(r'OOCOO', String) or re.search(r'OCOOO', String)\
        or re.search(r'COOOO', String) or re.search(r'OOOOC', String):
            score+=20000 # 必防, 坑点
    if re.search(r'\.OOCO', String) or re.search(r'OOCO\.', String) or re.search(r'\.OCOO', String)\
        or re.search(r'OCOO\.', String):
            score+=20000 # 防, 坑点

    if re.search(r'COOO\.', String) or re.search(r'\.OOOC', String) or re.search(r'\.OOCO\.', String)\
        or re.search(r'\.OCOO\.', String):
            score+=6000 # 防眠三

    if re.search(r'\.CMMM\.', String) or re.search(r'\.MCMM\.', String) or re.search(r'\.MMCM\.', String)\
        or re.search(r'\.MMMC\.', String): # 棋形在先手后手的情况下就有所不同, 先手主攻, 后手主防
            score+=5000

    if re.search(r'OCMMM\.', String) or re.search(r'OMCMM\.', String) or re.search(r'OMMCM\.', String)\
        or re.search(r'OMMMC\.', String) or re.search(r'\.CMMMO', String) or re.search(r'\.MCMMO', String)\
            or re.search(r'\.MMCMO', String) or re.search(r'\.MMMCO', String):
                score+=2000

    if re.search(r'\.MMC\.', String) or re.search(r'\.MCM\.', String) or re.search(r'\.CMM\.', String):
        score+=400

    if re.search(r'\.OOC', String) or re.search(r'COO\.', String):
            if deathFlag == 1:
                score+=9000 # 防止出现两个活三
                deathFlag = 0
            score+=400
            deathFlag = 1

    if  re.search(r'MOOOC', String)\
        or re.search(r'COOOM', String):
            score+=400

    if re.search(r'\.MMCO', String) or re.search(r'\.MCMO', String) or re.search(r'\.CMMO', String) \
        or re.search(r'OMMC\.', String) or re.search(r'OMCM.', String) or re.search(r'OCMM\.', String)\
            or re.search(r'MOOC', String) or re.search(r'COOM', String):
                score+=200

    if re.search(r'\.MC\.', String) or re.search(r'\.CM\.', String):
        score+=50

    if re.search(r'\.OC\.', String) or re.search(r'\.CO\.', String):
        score+=50

    score+=20

    return score

def playThatPlace(x,y):
    global loginInfo
    x, y=str(x), str(y)
    playBase='http://202.207.12.156:9012/play_game/'+str(gameId) + '?' + loginInfo +'&coord='
    response=requests.get(playBase + x + y)
    print('['+ response.text + '] push position in: '+x+y)
    return response

def resetFlag0():
    global deathFlag
    deathFlag=0
    return

if __name__=='__main__':

    gameId = joinGame()

    browserBase='http://202.207.12.156:9012/game/'+str(gameId)
    webbrowser.open(browserBase)

    cheakBase='http://202.207.12.156:9012/check_game/'+str(gameId)
    nowStatus=requests.get(cheakBase)
    nowData=json.loads(nowStatus.text)

    if nowData['creator'] == 'test':
        nowOpponent = nowData['opponent'] # 对手
        nowStone = nowData['creator_stone']
    else:
        nowOpponent = nowData['creator']
        nowStone = nowData['current_stone']
    if nowStone == 'o': # 白
        nextBlackOrWhite = 1
    if nowStone == 'x': # 黑
        nextBlackOrWhite = 0 
    # odd is block(1), next(mine) is white(0).
    # even is white(0), next(mine) is black(1).

    while nowOpponent == 'None': # can not use is instead ==???
        print('Founding Opponent....')
        time.sleep(5)
        nowStatus=requests.get(cheakBase)
        nowOpponent=json.loads(nowStatus.text)['opponent']
    print('Have found opponent:'+nowOpponent)


    step=0
    playing = 1
    while playing==1:

        if step ==1000:
            break

        whiteLocations=[]
        blackLocations=[]
        time.sleep(5)

        nowStatus=requests.get(cheakBase)
        nowJson=json.loads(nowStatus.text)
        print(nowJson)

        if nowJson['winner'] != 'None':
            print('ohhhhhhhh!!! WINNER is {0}'.format(nowJson['winner']))
            playing=0
            break

        if nowJson['current_turn'] != 'test':
            print('waiting opponent playing...')
        else:
            step+=1
            if nowStone=='x' and nowJson['step']=='0':
                playThatPlace('h','h')
                continue
            if nowStone=='o' and nowJson['step']=='1':
                playThatPlace('g', 'h')
                continue

            nowBoard = nowJson['board']

            for i in range(len(nowBoard)//2): # 偶数次循环
                xLocation = i*2
                yLocation = i*2+1
                if i%2 == 0:
                    blackLocations.append((ord(nowBoard[xLocation])-ord('a'), \
                        ord(nowBoard[yLocation])-ord('a')))
                else:
                    whiteLocations.append((ord(nowBoard[xLocation])-ord('a'), \
                        ord(nowBoard[yLocation])-ord('a')))

            board = [['.' for i in range(15)] for j in range(15)]
            firstInit='O'
            secondInit='M'
            if nowStone == 'x':
                firstInit='M'
                secondInit='O'
            for i in range(len(blackLocations)):
                board[blackLocations[i][0]] [blackLocations[i][1]] = firstInit
            for i in range(len(whiteLocations)):
                board[whiteLocations[i][0]] [whiteLocations[i][1]] = secondInit

            maxX, maxY, maxScore=0,0,0
            boardScore = [[0 for i in range(15)] for j in range(15)]
            for i in range(len(board)):
                for j in range(len(board[i])):
                    resetFlag0()# 死亡旗帜重置
                    if board[i][j] != '.':
                        continue
                    board[i][j]='C'
                    tempSco=0
                    tempStr=firstPrint(board, i, j)
                    tempSco+=getStrScore(tempStr)

                    tempStr=secondPrint(board, i, j)
                    tempSco+=getStrScore(tempStr)

                    tempStr=thirdPrint(board, i, j)
                    tempSco+=getStrScore(tempStr)
                    
                    tempStr=fourthPrint(board, i, j)
                    tempSco+=getStrScore(tempStr)

                    boardScore[i][j]=tempSco
                    if tempSco>maxScore:
                        maxScore=tempSco
                        maxX=i
                        maxY=j
                    board[i][j]='.'

            playThatPlace(chr(maxX+ord('a')), chr(maxY+ord('a')))

            board[maxX][maxY]='M'
            printBoard(board)