import requests
import json
import time
import webbrowser
import re

loginInfo=''
deathFlag=0

def str2num(String):
    String=String[::-1]
    Temp=1
    ans=0
    for i in range(len(String)):
        ans += ord(String[i]) * Temp
        Temp *= 256
    return ans

def multimod(a,k,n):
    ans=1
    while(k!=0):
        if k%2==1:
            ans=ans*a%n
        a=a*a%n
        k=k//2
    return ans

def encryNum(int):
    return multimod(int, 65537, 135261828916791946705313569652794581721330948863485438876915508683244111694485850733278569559191167660149469895899348939039437830613284874764820878002628686548956779897196112828969255650312573935871059275664474562666268163936821302832645284397530568872432109324825205567091066297960733513602409443790146687029)

def initSys(usr, initStr):
    global loginInfo
    loginInfo = 'user='+ usr + '&password=' + initStr
    return

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
            print(board[j][i], end=' ') # refer server result
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

def getStrScore(String):
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

    #config
    usr = '0191121339'
    password='Wge7sPRKu5sQvR7'

    #init
    encrySSL=encryNum(str2num(password))
    encrySSL=str(hex(int(str(encrySSL))))
    initSys(usr,encrySSL)

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

    while nowOpponent == 'None': # is instead ==???
        print('Founding Opponent....')
        time.sleep(5)
        nowStatus=requests.get(cheakBase)
        nowOpponent=json.loads(nowStatus.text)['opponent']
    print('Have found opponent:'+nowOpponent)

    step=0
    playing = 1
    while playing==1:

        if step ==1000: # control step of chess -> to test
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