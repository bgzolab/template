
str = input('input:')
li2 = []
point = []
max_x = 0
max_y = 0
max_p = 0

for i in range(15):
    point.append([])
    for j in range(15):
        point[i].append(0)

for i in range(15):
    li2.append([])
    for j in range(15):
        li2[i].append('.')

count = 2
count2 = 2
for h in range(0,len(str),2):
    if count % 2 == 0:
        li2[ord(str[h])-97][ord(str[h+1])-97] = 'x'
        count2 += 1
    else:
        li2[ord(str[h])-97][ord(str[h+1])-97] = 'o'
        count2 += 1
    count = count + 1
for k in range(15):
    for l in range(15):
         if l == 14:
              print(li2[k][l])
         else:
              print(li2[k][l], end='')

for i in range(15):
    for j in range(15):
        if li2[i][j] == '.':
            li2[i][j] = 'c'
            if count2 % 2 == 0:#该下黑棋
                if 0<=i<15 and j+4<15 and j+1>=0 and li2[i][j+1] == 'x' and li2[i][j+2] == 'x' and li2[i][j+3] == 'x' and li2[i][j+4] == 'x':
                    point[i][j] += 10000
                elif 0<=i<15 and j+3<15 and j-1>=0 and li2[i][j-1] == 'x' and li2[i][j+1] == 'x' and li2[i][j+2] == 'x' and li2[i][j+3] == 'x':
                    point[i][j] += 10000
                elif 0<=i<15 and j+2<15 and j-2>=0 and li2[i][j-2] == 'x' and li2[i][j-1] == 'x' and li2[i][j+1] == 'x' and li2[i][j+2] == 'x':
                    point[i][j] += 10000
                elif 0<=i<15 and j+1<15 and j-3>=0 and li2[i][j-3] == 'x' and li2[i][j-2] == 'x' and li2[i][j-1] == 'x' and li2[i][j+1] == 'x':
                    point[i][j] += 10000
                elif 0<=i<15 and j-1<15 and j-4>=0 and li2[i][j-4] == 'x' and li2[i][j-3] == 'x' and li2[i][j-2] == 'x' and li2[i][j-1] == 'x':
                    point[i][j] += 10000
                    #横向
                if 0<=i+1 and i+4<15 and 0<=j+1 and j+4<15 and li2[i+1][j+1] == 'x' and li2[i+2][j+2] == 'x' and li2[i+3][j+3] == 'x' and li2[i+4][j+4] == 'x':
                    point[i][j] += 10000
                elif 0<=i-1 and i+3<15 and 0<=j-1 and j+3<15 and li2[i-1][j-1] == 'x' and li2[i+1][j+1] == 'x' and li2[i+2][j+2] == 'x' and li2[i+3][j+3] == 'x':
                    point[i][j] += 10000
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i-2][j-2] == 'x' and li2[i-1][j-1] == 'x' and li2[i+1][j+1] == 'x' and li2[i+2][j+2] == 'x':
                    point[i][j] += 10000
                elif 0<=i-3 and i+1<15 and 0<=j-3 and j+1<15 and li2[i-3][j-3] == 'x' and li2[i-2][j-2] == 'x' and li2[i-1][j-1] == 'x' and li2[i+1][j+1] == 'x':
                    point[i][j] += 10000
                elif 0<=i-4 and i-1<15 and 0<=j-4 and j-1<15 and li2[i-4][j-4] == 'x' and li2[i-3][j-3] == 'x' and li2[i-2][j-2] == 'x' and li2[i-1][j-1] == 'x':
                    point[i][j] += 10000
                    #左上-》右下
                if 0<=j<15 and i+4<15 and i+1>=0 and li2[i+1][j] == 'x' and li2[i+2][j] == 'x' and li2[i+3][j] == 'x' and li2[i+4][j] == 'x':
                    point[i][j] += 10000
                elif 0<=j<15 and i+3<15 and i-1>=0 and li2[i-1][j] == 'x' and li2[i+1][j] == 'x' and li2[i+2][j] == 'x' and li2[i+3][j] == 'x':
                    point[i][j] += 10000
                elif 0<=j<15 and i+2<15 and i-2>=0 and li2[i-2][j] == 'x' and li2[i-1][j] == 'x' and li2[i+1][j] == 'x' and li2[i+2][j] == 'x':
                    point[i][j] += 10000
                elif 0<=j<15 and i+1<15 and i-3>=0 and li2[i-3][j] == 'x' and li2[i-2][j] == 'x' and li2[i-1][j] == 'x' and li2[i+1][j] == 'x':
                    point[i][j] += 10000
                elif 0<=j<15 and i-1<15 and i-4>=0 and li2[i-4][j] == 'x' and li2[i-3][j] == 'x' and li2[i-2][j] == 'x' and li2[i-1][j] == 'x':
                    point[i][j] += 10000
                    #纵向
                if 0<=i+1 and i+4<15 and 0<=j-4 and j-1<15 and li2[i+1][j-1] == 'x' and li2[i+2][j-2] == 'x' and li2[i+3][j-3] == 'x' and li2[i+4][j-4] == 'x':
                    point[i][j] += 10000
                elif 0<=i-1 and i+3<15 and 0<=j-3 and j+1<15 and li2[i-1][j+1] == 'x' and li2[i+1][j-1] == 'x' and li2[i+2][j-2] == 'x' and li2[i+3][j-3] == 'x':
                    point[i][j] += 10000
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i-2][j+2] == 'x' and li2[i-1][j+1] == 'x' and li2[i+1][j-1] == 'x' and li2[i+2][j-2] == 'x':
                    point[i][j] += 10000
                elif 0<=i-3 and i+1<15 and 0<=j-1 and j+3<15 and li2[i-3][j+3] == 'x' and li2[i-2][j+2] == 'x' and li2[i-1][j+1] == 'x' and li2[i+1][j-1] == 'x':
                    point[i][j] += 10000
                elif i-4>=0 and i-1<15 and j+4<15 and j+1>0 and li2[i-4][j+4] == 'x' and li2[i-3][j+3] == 'x' and li2[i-2][j+2] == 'x' and li2[i-1][j+1] == 'x':
                    point[i][j] += 10000
                    #右上-》左下
                    #致胜棋形
                if 0<=i<15 and j+4<15 and j+1>=0 and li2[i][j+1] == 'o' and li2[i][j+2] == 'o' and li2[i][j+3] == 'o' and li2[i][j+4] == 'o':
                    point[i][j] += 6000
                elif 0<=i<15 and j+3<15 and j-1>=0 and li2[i][j-1] == 'o' and li2[i][j+1] == 'o' and li2[i][j+2] == 'o' and li2[i][j+3] == 'o':
                    point[i][j] += 6000
                elif 0<=i<15 and j+2<15 and j-2>=0 and li2[i][j-2] == 'o' and li2[i][j-1] == 'o' and li2[i][j+1] == 'o' and li2[i][j+2] == 'o':
                    point[i][j] += 6000
                elif 0<=i<15 and j+1<15 and j-3>=0 and li2[i][j-3] == 'o' and li2[i][j-2] == 'o' and li2[i][j-1] == 'o' and li2[i][j+1] == 'o':
                    point[i][j] += 6000
                elif 0<=i<15 and j-1<15 and j-4>=0 and li2[i][j-4] == 'o' and li2[i][j-3] == 'o' and li2[i][j-2] == 'o' and li2[i][j-1] == 'o':
                    point[i][j] += 6000
                    #横向
                if 0<=i+1 and i+4<15 and 0<=j+1 and j+4<15 and li2[i+1][j+1] == 'o' and li2[i+2][j+2] == 'o' and li2[i+3][j+3] == 'o' and li2[i+4][j+4] == 'o':
                    point[i][j] += 6000
                elif 0<=i-1 and i+3<15 and 0<=j-1 and j+3<15 and li2[i-1][j-1] == 'o' and li2[i+1][j+1] == 'o' and li2[i+2][j+2] == 'o' and li2[i+3][j+3] == 'o':
                    point[i][j] += 6000
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i-2][j-2] == 'o' and li2[i-1][j-1] == 'o' and li2[i+1][j+1] == 'o' and li2[i+2][j+2] == 'o':
                    point[i][j] += 6000
                elif 0<=i-3 and i+1<15 and 0<=j-3 and j+1<15 and li2[i-3][j-3] == 'o' and li2[i-2][j-2] == 'o' and li2[i-1][j-1] == 'o' and li2[i+1][j+1] == 'o':
                    point[i][j] += 6000
                elif 0<=i-4 and i-1<15 and 0<=j-4 and j-1<15 and li2[i-4][j-4] == 'o' and li2[i-3][j-3] == 'o' and li2[i-2][j-2] == 'o' and li2[i-1][j-1] == 'o':
                    point[i][j] += 6000
                    #左上-》右下
                if 0<=j<15 and i+4<15 and i+1>=0 and li2[i+1][j] == 'o' and li2[i+2][j] == 'o' and li2[i+3][j] == 'o' and li2[i+4][j] == 'o':
                    point[i][j] += 6000
                elif 0<=j<15 and i+3<15 and i-1>=0 and li2[i-1][j] == 'o' and li2[i+1][j] == 'o' and li2[i+2][j] == 'o' and li2[i+3][j] == 'o':
                    point[i][j] += 6000
                elif 0<=j<15 and i+2<15 and i-2>=0 and li2[i-2][j] == 'o' and li2[i-1][j] == 'o' and li2[i+1][j] == 'o' and li2[i+2][j] == 'o':
                    point[i][j] += 6000
                elif 0<=j<15 and i+1<15 and i-3>=0 and li2[i-3][j] == 'o' and li2[i-2][j] == 'o' and li2[i-1][j] == 'o' and li2[i+1][j] == 'o':
                    point[i][j] += 6000
                elif 0<=j<15 and i-1<15 and i-4>=0 and li2[i-4][j] == 'o' and li2[i-3][j] == 'o' and li2[i-2][j] == 'o' and li2[i-1][j] == 'o':
                    point[i][j] += 6000
                    #纵向
                if 0<=i+1 and i+4<15 and 0<=j-4 and j-1<15 and li2[i+1][j-1] == 'o' and li2[i+2][j-2] == 'o' and li2[i+3][j-3] == 'o' and li2[i+4][j-4] == 'o':
                    point[i][j] += 6000
                elif 0<=i-1 and i+3<15 and 0<=j-3 and j+1<15 and li2[i-1][j+1] == 'o' and li2[i+1][j-1] == 'o' and li2[i+2][j-2] == 'o' and li2[i+3][j-3] == 'o':
                    point[i][j] += 6000
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i-2][j+2] == 'o' and li2[i-1][j+1] == 'o' and li2[i+1][j-1] == 'o' and li2[i+2][j-2] == 'o':
                    point[i][j] += 6000
                elif 0<=i-3 and i+1<15 and 0<=j-1 and j+3<15 and li2[i-3][j+3] == 'o' and li2[i-2][j+2] == 'o' and li2[i-1][j+1] == 'o' and li2[i+1][j-1] == 'o':
                    point[i][j] += 6000
                elif 0<=i-4 and i-1<15 and 0<=j+1 and j+4<15 and li2[i-4][j+4] == 'o' and li2[i-3][j+3] == 'o' and li2[i-2][j+2] == 'o' and li2[i-1][j+1] == 'o':
                    point[i][j] += 6000
                    #右上-》左下
                    #必须防守棋形
                if 0<=i<15 and j+4<15 and j-1>=0 and li2[i][j-1] == '.' and li2[i][j+1]=='x' and li2[i][j+2]=='x' and li2[i][j+3]=='x' and li2[i][j+4]=='.':
                    point[i][j] += 5000
                elif 0<=i<15 and j+3<15 and j-2>=0 and li2[i][j-2] == '.' and li2[i][j-1]=='x' and li2[i][j+1]=='x' and li2[i][j+2]=='x' and li2[i][j+3]=='.':
                    point[i][j] += 5000
                elif 0<=i<15 and j+2<15 and j-3>=0 and li2[i][j-3] == '.' and li2[i][j-2]=='x' and li2[i][j-1]=='x' and li2[i][j+1]=='x' and li2[i][j+2]=='.':
                    point[i][j] += 5000
                elif 0<=i<15 and j+1<15 and j-4>=0 and li2[i][j-4] == '.' and li2[i][j-3]=='x' and li2[i][j-2]=='x' and li2[i][j-1]=='x' and li2[i][j+1]=='.':
                    point[i][j] += 5000
                    #横向
                if 0<=i-1 and i+4<15 and 0<=j-1 and j+4<15 and li2[i-1][j-1] == '.' and li2[i+1][j+1]=='x' and li2[i+2][j+2]=='x' and li2[i+3][j+3]=='x' and li2[i+4][j+4]=='.':
                    point[i][j] += 5000
                elif 0<=i-2 and i+3<15 and 0<=j-2 and j+3<15 and li2[i-2][j-2] == '.' and li2[i-1][j-1]=='x' and li2[i+1][j+1]=='x' and li2[i+2][j+2]=='x' and li2[i+3][j+3]=='.':
                    point[i][j] += 5000
                elif 0<=i-3 and i+2<15 and 0<=j-3 and j+2<15 and li2[i-3][j-3] == '.' and li2[i-2][j-2]=='x' and li2[i-1][j-1]=='x' and li2[i+1][j+1]=='x' and li2[i+2][j+2]=='.':
                    point[i][j] += 5000
                elif 0<=i-4 and i+1<15 and 0<=j-4 and j+1<15 and li2[i-4][j-4] == '.' and li2[i-3][j-3]=='x' and li2[i-2][j-2]=='x' and li2[i-1][j-1]=='x' and li2[i+1][j+1]=='.':
                    point[i][j] += 5000
                    #左上-》右下
                if 0<=j<15 and i+4<15 and i-1>=0 and li2[i-1][j] == '.' and li2[i+1][j]=='x' and li2[i+2][j]=='x' and li2[i+3][j]=='x' and li2[i+4][j]=='.':
                    point[i][j] += 5000
                elif 0<=j<15 and i+3<15 and i-2>=0 and li2[i-2][j] == '.' and li2[i-1][j]=='x' and li2[i+1][j]=='x' and li2[i+2][j]=='x' and li2[i+3][j]=='.':
                    point[i][j] += 5000
                elif 0<=j<15 and i+2<15 and i-3>=0 and li2[i-3][j] == '.' and li2[i-2][j]=='x' and li2[i-1][j]=='x' and li2[i+1][j]=='x' and li2[i+2][j]=='.':
                    point[i][j] += 5000
                elif 0<=j<15 and i+1<15 and i-4>=0 and li2[i-4][j] == '.' and li2[i-3][j]=='x' and li2[i-2][j]=='x' and li2[i-1][j]=='x' and li2[i+1][j]=='.':
                    point[i][j] += 5000
                    #纵向
                if 0<=i-4 and i+1<15 and 0<=j-1 and j+4<15 and li2[i+1][j-1] == '.' and li2[i-1][j+1]=='x' and li2[i-2][j+2]=='x' and li2[i-3][j+3]=='x' and li2[i-4][j+4]=='.':
                    point[i][j] += 5000
                elif 0<=i-3 and i+2<15 and 0<=j-2 and j+3<15 and li2[i+2][j-2] == '.' and li2[i+1][j-1]=='x' and li2[i-1][j+1]=='x' and li2[i-2][j+2]=='x' and li2[i-3][j+3]=='.':
                    point[i][j] += 5000
                elif 0<=i-2 and i+3<15 and 0<=j-3 and j+2<15 and li2[i+3][j-3] == '.' and li2[i+2][j-2]=='x' and li2[i+1][j-1]=='x' and li2[i-1][j+1]=='x' and li2[i-2][j+2]=='.':
                    point[i][j] += 5000
                elif 0<=i-1 and i+4<15 and 0<=j-4 and j+1<15 and li2[i+4][j-4] == '.' and li2[i+3][j-3]=='x' and li2[i+2][j-2]=='x' and li2[i+1][j-1]=='x' and li2[i-1][j+1]=='.':
                    point[i][j] += 5000
                    #右上-》左下
                    #两步致胜
                if 0<=i<15 and j+4<15 and j-1>=0 and li2[i][j+4] == '.' and li2[i][j+3]=='o' and li2[i][j+2]=='o' and li2[i][j+1]=='o':
                    point[i][j] += 2500
                elif 0<=i<15 and j+3<15 and j-2>=0 and li2[i][j-2] == '.' and li2[i][j-1]=='o' and li2[i][j+1]=='o' and li2[i][j+2]=='o' and li2[i][j+3]=='.':
                    point[i][j] += 2500
                elif 0<=i<15 and j+2<15 and j-3>=0 and li2[i][j-3] == '.' and li2[i][j-2]=='o' and li2[i][j-1]=='o' and li2[i][j+1]=='o' and li2[i][j+2]=='.':
                    point[i][j] += 2500
                elif 0<=i<15 and j+1<15 and j-4>=0 and li2[i][j-4] == '.' and li2[i][j-3]=='o' and li2[i][j-2]=='o' and li2[i][j-1]=='o':
                    point[i][j] += 2500
                    #横向
                if 0<=i-1 and i+4<15 and 0<=j-1 and j+4<15 and li2[i+4][j+4] == '.' and li2[i+2][j+2]=='o' and li2[i+3][j+3]=='o' and li2[i+1][j+1]=='o':
                    point[i][j] += 2500
                elif 0<=i-2 and i+3<15 and 0<=j-2 and j+3<15 and li2[i-2][j-2] == '.' and li2[i-1][j-1]=='o' and li2[i+1][j+1]=='o' and li2[i+2][j+2]=='o' and li2[i+3][j+3]=='.':
                    point[i][j] += 2500
                elif 0<=i-3 and i+2<15 and 0<=j-3 and j+2<15 and li2[i-3][j-3] == '.' and li2[i-2][j-2]=='o' and li2[i-1][j-1]=='o' and li2[i+1][j+1]=='o' and li2[i+2][j+2]=='.':
                    point[i][j] += 2500
                elif 0<=i-4 and i+1<15 and 0<=j-4 and j+1<15 and li2[i-4][j-4] == '.' and li2[i-3][j-3]=='o' and li2[i-2][j-2]=='o' and li2[i-1][j-1]=='o':
                    point[i][j] += 2500
                    #左上-》右下
                if 0<=j<15 and i+4<15 and i-1>=0 and li2[i+4][j] == '.' and li2[i+1][j]=='o' and li2[i+2][j]=='o' and li2[i+3][j]=='o':
                    point[i][j] += 2500
                elif 0<=j<15 and i+3<15 and i-2>=0 and li2[i-2][j] == '.' and li2[i-1][j]=='o' and li2[i+1][j]=='o' and li2[i+2][j]=='o' and li2[i+3][j]=='.':
                    point[i][j] += 2500
                elif 0<=j<15 and i+2<15 and i-3>=0 and li2[i-3][j] == '.' and li2[i-2][j]=='o' and li2[i-1][j]=='o' and li2[i+1][j]=='o' and li2[i+2][j]=='.':
                    point[i][j] += 2500
                elif 0<=j<15 and i+1<15 and i-4>=0 and li2[i-4][j] == '.' and li2[i-3][j]=='o' and li2[i-2][j]=='o' and li2[i-1][j]=='o':
                    point[i][j] += 2500
                    #纵向
                if 0<=i-4 and i+1<15 and 0<=j-1 and j+4<15 and li2[i-4][j+4] == '.' and li2[i-1][j+1]=='o' and li2[i-2][j+2]=='o' and li2[i-3][j+3]=='o':
                    point[i][j] += 2500
                elif 0<=i-3 and i+2<15 and 0<=j-2 and j+3<15 and li2[i+2][j-2] == '.' and li2[i+1][j-1]=='o' and li2[i-1][j+1]=='o' and li2[i-2][j+2]=='o' and li2[i-3][j+3]=='.':
                    point[i][j] += 2500
                elif 0<=i-2 and i+3<15 and 0<=j-3 and j+2<15 and li2[i+3][j-3] == '.' and li2[i+2][j-2]=='o' and li2[i+1][j-1]=='o' and li2[i-1][j+1]=='o' and li2[i-2][j+2]=='.':
                    point[i][j] += 2500
                elif 0<=i-1 and i+4<15 and 0<=j-4 and j+1<15 and li2[i+4][j-4] == '.' and li2[i+3][j-3]=='o' and li2[i+2][j-2]=='o' and li2[i+1][j-1]=='o':
                    point[i][j] += 2500
                    #右上-》左下
                    #两部防守
                if 0<=i<15 and j+4<15 and j-1>=0 and li2[i][j-1] == 'o' and li2[i][j+1]=='x' and li2[i][j+2]=='x' and li2[i][j+3]=='x' and li2[i][j+4]=='.':
                    point[i][j] += 2000
                elif 0<=i<15 and j+3<15 and j-2>=0 and li2[i][j-2] == 'o' and li2[i][j-1]=='x' and li2[i][j+1]=='x' and li2[i][j+2]=='x' and li2[i][j+3]=='.':
                    point[i][j] += 2000
                elif 0<=i<15 and j+2<15 and j-3>=0 and li2[i][j-3] == 'o' and li2[i][j-2]=='x' and li2[i][j-1]=='x' and li2[i][j+1]=='x' and li2[i][j+2]=='.':
                    point[i][j] += 2000
                elif 0<=i<15 and j+1<15 and j-4>=0 and li2[i][j-4] == 'o' and li2[i][j-3]=='x' and li2[i][j-2]=='x' and li2[i][j-1]=='x' and li2[i][j+1]=='.':
                    point[i][j] += 2000
                elif 0<=i<15 and j+4<15 and j-1>=0 and li2[i][j - 1] == '.' and li2[i][j + 1] == 'x' and li2[i][j + 2] == 'x' and li2[i][j + 3] == 'x' and li2[i][j + 4] == 'o':
                    point[i][j] += 2000
                elif 0<=i<15 and j+3<15 and j-2>=0 and li2[i][j - 2] == '.' and li2[i][j - 1] == 'x' and li2[i][j + 1] == 'x' and li2[i][j + 2] == 'x' and li2[i][j + 3] == 'o':
                    point[i][j] += 2000
                elif 0<=i<15 and j+2<15 and j-3>=0 and li2[i][j - 3] == '.' and li2[i][j - 2] == 'x' and li2[i][j - 1] == 'x' and li2[i][j + 1] == 'x' and li2[i][j + 2] == 'o':
                    point[i][j] += 2000
                elif 0<=i<15 and j+1<15 and j-4>=0 and li2[i][j - 4] == '.' and li2[i][j - 3] == 'x' and li2[i][j - 2] == 'x' and li2[i][j - 1] == 'x' and li2[i][j + 1] == 'o':
                    point[i][j] += 2000
                    #横向
                if 0<=i-1 and i+4<15 and 0<=j-1 and j+4<15 and li2[i-1][j-1] == 'o' and li2[i+1][j+1]=='x' and li2[i+2][j+2]=='x' and li2[i+3][j+3]=='x' and li2[i+4][j+4]=='.':
                    point[i][j] += 2000
                elif 0<=i-2 and i+3<15 and 0<=j-2 and j+3<15 and li2[i-2][j-2] == 'o' and li2[i-1][j-1]=='x' and li2[i+1][j+1]=='x' and li2[i+2][j+2]=='x' and li2[i+3][j+3]=='.':
                    point[i][j] += 2000
                elif 0<=i-3 and i+2<15 and 0<=j-3 and j+2<15 and li2[i-3][j-3] == 'o' and li2[i-2][j-2]=='x' and li2[i-1][j-1]=='x' and li2[i+1][j+1]=='x' and li2[i+2][j+2]=='.':
                    point[i][j] += 2000
                elif 0<=i-4 and i+1<15 and 0<=j-4 and j+1<15 and li2[i-4][j-4] == 'o' and li2[i-3][j-3]=='x' and li2[i-2][j-2]=='x' and li2[i-1][j-1]=='x' and li2[i+1][j+1]=='.':
                    point[i][j] += 2000
                elif 0<=i-1 and i+4<15 and 0<=j-1 and j+4<15 and li2[i - 1][j - 1] == '.' and li2[i + 1][j + 1] == 'x' and li2[i + 2][j + 2] == 'x' and li2[i + 3][j + 3] == 'x' and li2[i + 4][j + 4] == 'o':
                    point[i][j] += 2000
                elif 0<=i-2 and i+3<15 and 0<=j-2 and j+3<15 and li2[i - 2][j - 2] == '.' and li2[i - 1][j - 1] == 'x' and li2[i + 1][j + 1] == 'x' and li2[i + 2][j + 2] == 'x' and li2[i + 3][j + 3] == 'o':
                    point[i][j] += 2000
                elif 0<=i-3 and i+2<15 and 0<=j-3 and j+2<15 and li2[i - 3][j - 3] == '.' and li2[i - 2][j - 2] == 'x' and li2[i - 1][j - 1] == 'x' and li2[i + 1][j + 1] == 'x' and li2[i + 2][j + 2] == 'o':
                    point[i][j] += 2000
                elif 0<=i-4 and i+1<15 and 0<=j-4 and j+1<15 and li2[i - 4][j - 4] == '.' and li2[i - 3][j - 3] == 'x' and li2[i - 2][j - 2] == 'x' and li2[i - 1][j - 1] == 'x' and li2[i + 1][j + 1] == 'o':
                    point[i][j] += 2000
                    #左上-》右下
                if 0<=j<15 and i+4<15 and i-1>=0 and li2[i-1][j] == 'o' and li2[i+1][j]=='x' and li2[i+2][j]=='x' and li2[i+3][j]=='x' and li2[i+4][j]=='.':
                    point[i][j] += 2000
                elif 0<=j<15 and i+3<15 and i-2>=0 and li2[i-2][j] == 'o' and li2[i-1][j]=='x' and li2[i+1][j]=='x' and li2[i+2][j]=='x' and li2[i+3][j]=='.':
                    point[i][j] += 2000
                elif 0<=j<15 and i+2<15 and i-3>=0 and li2[i-3][j] == 'o' and li2[i-2][j]=='x' and li2[i-1][j]=='x' and li2[i+1][j]=='x' and li2[i+2][j]=='.':
                    point[i][j] += 2000
                elif 0<=j<15 and i+1<15 and i-4>=0 and li2[i-4][j] == 'o' and li2[i-3][j]=='x' and li2[i-2][j]=='x' and li2[i-1][j]=='x' and li2[i+1][j]=='.':
                    point[i][j] += 2000
                elif 0<=j<15 and i+4<15 and i-1>=0 and li2[i - 1][j] == '.' and li2[i + 1][j] == 'x' and li2[i + 2][j] == 'x' and li2[i + 3][j] == 'x' and li2[i + 4][j] == 'o':
                    point[i][j] += 2000
                elif 0<=j<15 and i+3<15 and i-2>=0 and li2[i - 2][j] == '.' and li2[i - 1][j] == 'x' and li2[i + 1][j] == 'x' and li2[i + 2][j] == 'x' and li2[i + 3][j] == 'o':
                    point[i][j] += 2000
                elif 0<=j<15 and i+2<15 and i-3>=0 and li2[i - 3][j] == '.' and li2[i - 2][j] == 'x' and li2[i - 1][j] == 'x' and li2[i + 1][j] == 'x' and li2[i + 2][j] == 'o':
                    point[i][j] += 2000
                elif 0<=j<15 and i+1<15 and i-4>=0 and li2[i - 4][j] == '.' and li2[i - 3][j] == 'x' and li2[i - 2][j] == 'x' and li2[i - 1][j] == 'x' and li2[i + 1][j] == 'o':
                    point[i][j] += 2000
                    #纵向
                if 0<=i-4 and i+1<15 and 0<=j-1 and j+4<15 and li2[i+1][j-1] == 'o' and li2[i-1][j+1]=='x' and li2[i-2][j+2]=='x' and li2[i-3][j+3]=='x' and li2[i-4][j+4]=='.':
                    point[i][j] += 2000
                elif 0<=i-3 and i+2<15 and 0<=j-2 and j+3<15 and li2[i+2][j-2] == 'o' and li2[i+1][j-1]=='x' and li2[i-1][j+1]=='x' and li2[i-2][j+2]=='x' and li2[i-3][j+3]=='.':
                    point[i][j] += 2000
                elif 0<=i-2 and i+3<15 and 0<=j-3 and j+2<15 and li2[i+3][j-3] == 'o' and li2[i+2][j-2]=='x' and li2[i+1][j-1]=='x' and li2[i-1][j+1]=='x' and li2[i-2][j+2]=='.':
                    point[i][j] += 2000
                elif 0<=i-1 and i+4<15 and 0<=j-4 and j+1<15 and li2[i+4][j-4] == 'o' and li2[i+3][j-3]=='x' and li2[i+2][j-2]=='x' and li2[i+1][j-1]=='x' and li2[i-1][j+1]=='.':
                    point[i][j] += 2000
                elif 0<=i-4 and i+1<15 and 0<=j-1 and j+4<15 and li2[i + 1][j - 1] == '.' and li2[i - 1][j + 1] == 'x' and li2[i - 2][j + 2] == 'x' and li2[i - 3][j + 3] == 'x' and li2[i - 4][j + 4] == 'o':
                    point[i][j] += 2000
                elif 0<=i-3 and i+2<15 and 0<=j-2 and j+3<15 and li2[i + 2][j - 2] == '.' and li2[i + 1][j - 1] == 'x' and li2[i - 1][j + 1] == 'x' and li2[i - 2][j + 2] == 'x' and li2[i - 3][j + 3] == 'o':
                    point[i][j] += 2000
                elif 0<=i-2 and i+3<15 and 0<=j-3 and j+2<15 and li2[i + 3][j - 3] == '.' and li2[i + 2][j - 2] == 'x' and li2[i + 1][j - 1] == 'x' and li2[i - 1][j + 1] == 'x' and li2[i - 2][j + 2] == 'o':
                    point[i][j] += 2000
                elif 0<=i-1 and i+4<15 and 0<=j-4 and j+1<15 and li2[i + 4][j - 4] == '.' and li2[i + 3][j - 3] == 'x' and li2[i + 2][j - 2] == 'x' and li2[i + 1][j - 1] == 'x' and li2[i - 1][j + 1] == 'o':
                    point[i][j] += 2000
                    #右上-》左下
                    #进攻棋形
                if 0<=i<15 and j+1<15 and j-3>=0 and li2[i][j-3] == '.' and li2[i][j-2] == 'x' and li2[i][j-1] == 'x' and li2[i][j+1] == '.':
                    point[i][j] += 400
                elif 0<=i<15 and j+2<15 and j-2>=0 and li2[i][j-2] == '.' and li2[i][j-1] == 'x' and li2[i][j+1] == 'x' and li2[i][j+2] == '.':
                    point[i][j] += 400
                elif 0<=i<15 and j+3<15 and j-1>=0 and li2[i][j-1] == '.' and li2[i][j+1] == 'x' and li2[i][j+2] == 'x' and li2[i][j+3] == '.':
                    point[i][j] += 400
                    #横向
                if 0<=i-3 and i+1<15 and 0<=j-3 and j+1<15 and li2[i-3][j-3] == '.' and li2[i-2][j-2] == 'x' and li2[i-1][j-1] == 'x' and li2[i+1][j+1] == '.':
                    point[i][j] += 400
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i-2][j-2] == '.' and li2[i-1][j-1] == 'x' and li2[i+1][j+1] == 'x' and li2[i+2][j+2] == '.':
                    point[i][j] += 400
                elif 0<=i-1 and i+3<15 and 0<=j-1 and j+3<15 and li2[i-1][j-1] == '.' and li2[i+1][j+1] == 'x' and li2[i+2][j+2] == 'x' and li2[i+3][j+3] == '.':
                    point[i][j] += 400
                    #左上-》右下
                if 0<=j<15 and i+1<15 and i-3>=0 and li2[i - 3][j] == '.' and li2[i - 2][j] == 'x' and li2[i - 1][j] == 'x' and li2[i + 1][j] == '.':
                    point[i][j] += 400
                elif 0<=j<15 and i+2<15 and i-2>=0 and li2[i - 2][j] == '.' and li2[i - 1][j] == 'x' and li2[i + 1][j] == 'x' and li2[i + 2][j] == '.':
                    point[i][j] += 400
                elif 0<=j<15 and i+3<15 and i-1>=0 and li2[i - 1][j] == '.' and li2[i + 1][j] == 'x' and li2[i + 2][j] == 'x' and li2[i + 3][j] == '.':
                    point[i][j] += 400
                    #纵向
                if 0<=i-1 and i+3<15 and 0<=j-3 and j+1<15 and li2[i+3][j - 3] == '.' and li2[i+2][j - 2] == 'x' and li2[i+1][j - 1] == 'x' and li2[i-1][j + 1] == '.':
                    point[i][j] += 400
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i+2][j - 2] == '.' and li2[i+1][j - 1] == 'x' and li2[i-1][j + 1] == 'x' and li2[i-2][j + 2] == '.':
                    point[i][j] += 400
                elif 0<=i-3 and i+1<15 and 0<=j-1 and j+3<15 and li2[i+1][j - 1] == '.' and li2[i-1][j + 1] == 'x' and li2[i-2][j + 2] == 'x' and li2[i-3][j + 3] == '.':
                    point[i][j] += 400
                    #右上-》左下
                    #两部进攻棋形
                if 0<=i<15 and j-1<15 and j-3>=0 and li2[i][j-3] == '.' and li2[i][j-2] == 'o' and li2[i][j-1] == 'o':
                    point[i][j] += 400
                elif 0<=i<15 and j+3<15 and j+1>=0 and li2[i][j+3] == '.' and li2[i][j+2] == 'o' and li2[i][j+1] == 'o':
                    point[i][j] += 400
                elif 0<=i<15 and j-1<15 and j-4>=0 and li2[i][j-4] == 'x' and li2[i][j-3] == 'o' and li2[i][j-2] == 'o' and li2[i][j-1] == 'o':
                    point[i][j] += 400
                elif 0<=i<15 and j+4<15 and j+1>=0 and li2[i][j+1] == 'o' and li2[i][j+2] == 'o' and li2[i][j+3] == 'o' and li2[i][j+4] == 'x':
                    point[i][j] += 400
                    #横向
                if 0<=i-3 and i-1<15 and 0<=j-3 and j-1<15 and li2[i-3][j-3] == '.' and li2[i-2][j-2] == 'o' and li2[i-1][j-1] == 'o':
                    point[i][j] += 400
                elif 0<=i+1 and i+3<15 and 0<=j+1 and j+3<15 and li2[i+3][j+3] == '.' and li2[i+2][j+2] == 'o' and li2[i+1][j+1] == 'o':
                    point[i][j] += 400
                elif 0<=i-4 and i-1<15 and 0<=j-4 and j-1<15 and li2[i-4][j-4] == 'x' and li2[i-3][j-3] == 'o' and li2[i-2][j-2] == 'o' and li2[i-1][j-1] == 'o':
                    point[i][j] += 400
                elif 0<=i+1 and i+4<15 and 0<=j+1 and j+4<15 and li2[i+1][j+1] == 'o' and li2[i+2][j+2] == 'o' and li2[i+3][j+3] == 'o' and li2[i+4][j+4] == 'x':
                    point[i][j] += 400
                    #左上-》右下
                if 0<=j<15 and i-1<15 and i-3>=0 and li2[i-3][j] == '.' and li2[i-2][j] == 'o' and li2[i-1][j] == 'o':
                    point[i][j] += 400
                elif 0<=j<15 and i+3<15 and i+1>=0 and li2[i+3][j] == '.' and li2[i+2][j] == 'o' and li2[i+1][j] == 'o':
                    point[i][j] += 400
                elif 0<=j<15 and i-1<15 and i-4>=0 and li2[i-4][j] == 'x' and li2[i-3][j] == 'o' and li2[i-2][j] == 'o' and li2[i-1][j] == 'o':
                    point[i][j] += 400
                elif 0<=j<15 and i+4<15 and i+1>=0 and li2[i+1][j] == 'o' and li2[i+2][j] == 'o' and li2[i+3][j] == 'o' and li2[i+4][j] == 'x':
                    point[i][j] += 400
                    #纵向
                if 0<=i+1 and i+3<15 and 0<=j-3 and j-1<15 and li2[i+3][j-3] == '.' and li2[i+2][j-2] == 'o' and li2[i+1][j-1] == 'o':
                    point[i][j] += 400
                elif 0<=i-3 and i-1<15 and 0<=j+1 and j+3<15 and li2[i-3][j+3] == '.' and li2[i-2][j+2] == 'o' and li2[i-1][j+1] == 'o':
                    point[i][j] += 400
                elif 0<=i+1 and i+4<15 and 0<=j-4 and j-1<15 and li2[i+4][j-4] == 'x' and li2[i+3][j-3] == 'o' and li2[i+2][j-2] == 'o' and li2[i+1][j-1] == 'o':
                    point[i][j] += 400
                elif 0<=i-4 and i-1<15 and 0<=j+1 and j+4<15 and li2[i-1][j+1] == 'o' and li2[i-2][j+2] == 'o' and li2[i-3][j+3] == 'o' and li2[i-4][j+4] == 'x':
                    point[i][j] += 400
                    #右上-》左下
                    #预防棋形
                if 0<=i<15 and j+1<15 and j-3>=0 and li2[i][j-3] == '.' and li2[i][j-2] == 'x' and li2[i][j-1] == 'x' and li2[i][j+1] == 'o':
                    point[i][j] += 200
                elif 0<=i<15 and j+2<15 and j-2>=0 and li2[i][j-2] == '.' and li2[i][j-1] == 'x' and li2[i][j+1] == 'x' and li2[i][j+2] == 'o':
                    point[i][j] += 200
                elif 0<=i<15 and j+3<15 and j-1>=0 and li2[i][j-1] == '.' and li2[i][j+1] == 'x' and li2[i][j+2] == 'x' and li2[i][j+3] == 'o':
                    point[i][j] += 200
                elif 0<=i<15 and j+1<15 and j-3>=0 and li2[i][j-3] == 'o' and li2[i][j-2] == 'x' and li2[i][j-1] == 'x' and li2[i][j+1] == '.':
                    point[i][j] += 200
                elif 0<=i<15 and j+2<15 and j-2>=0 and li2[i][j-2] == 'o' and li2[i][j-1] == 'x' and li2[i][j+1] == 'x' and li2[i][j+2] == '.':
                    point[i][j] += 200
                elif 0<=i<15 and j+3<15 and j-1>=0 and li2[i][j-1] == 'o' and li2[i][j+1] == 'x' and li2[i][j+2] == 'x' and li2[i][j+3] == '.':
                    point[i][j] += 200
                elif 0<=i<15 and j-1<15 and j-3>=0 and li2[i][j-3] == 'x' and li2[i][j-2] == 'o' and li2[i][j-1] == 'o':
                    point[i][j] += 200
                elif 0<=i<15 and j+3<15 and j+1>=0 and li2[i][j+3] == 'x' and li2[i][j+2] == 'o' and li2[i][j+1] == 'o':
                    point[i][j] += 200
                    #横向
                if 0<=i-3 and i+1<15 and 0<=j-3 and j+1<15 and li2[i-3][j-3] == '.' and li2[i-2][j-2] == 'x' and li2[i-1][j-1] == 'x' and li2[i+1][j+1] == 'o':
                    point[i][j] += 200
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i-2][j-2] == '.' and li2[i-1][j-1] == 'x' and li2[i+1][j+1] == 'x' and li2[i+2][j+2] == 'o':
                    point[i][j] += 200
                elif 0<=i-1 and i+3<15 and 0<=j-1 and j+3<15 and li2[i-1][j-1] == '.' and li2[i+1][j+1] == 'x' and li2[i+2][j+2] == 'x' and li2[i+3][j+3] == 'o':
                    point[i][j] += 200
                elif 0<=i-3 and i+1<15 and 0<=j-3 and j+1<15 and li2[i-3][j-3] == 'o' and li2[i-2][j-2] == 'x' and li2[i-1][j-1] == 'x' and li2[i+1][j+1] == '.':
                    point[i][j] += 200
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i-2][j-2] == 'o' and li2[i-1][j-1] == 'x' and li2[i+1][j+1] == 'x' and li2[i+2][j+2] == '.':
                    point[i][j] += 200
                elif 0<=i-1 and i+3<15 and 0<=j-1 and j+3<15 and li2[i-1][j-1] == 'o' and li2[i+1][j+1] == 'x' and li2[i+2][j+2] == 'x' and li2[i+3][j+3] == '.':
                    point[i][j] += 200
                elif 0<=i-3 and i-1<15 and 0<=j-3 and j-1<15 and li2[i-3][j-3] == 'x' and li2[i-2][j-2] == 'o' and li2[i-1][j-1] == 'o':
                    point[i][j] += 200
                elif 0<=i+1 and i+3<15 and 0<=j+1 and j+3<15 and li2[i+3][j+3] == 'x' and li2[i+2][j+2] == 'o' and li2[i+1][j+1] == 'o':
                    point[i][j] += 200
                    #左上-》右下
                if 0<=j<15 and i+1<15 and i-3>=0 and li2[i-3][j] == '.' and li2[i-2][j] == 'x' and li2[i-1][j] == 'x' and li2[i+1][j] == 'o':
                    point[i][j] += 200
                elif 0<=j<15 and i+2<15 and i-2>=0 and li2[i-2][j] == '.' and li2[i-1][j] == 'x' and li2[i+1][j] == 'x' and li2[i+2][j] == 'o':
                    point[i][j] += 200
                elif 0<=j<15 and i+3<15 and i-1>=0 and li2[i-1][j] == '.' and li2[i+1][j] == 'x' and li2[i+2][j] == 'x' and li2[i+3][j] == 'o':
                    point[i][j] += 200
                elif 0<=j<15 and i+1<15 and i-3>=0 and li2[i-3][j] == 'o' and li2[i-2][j] == 'x' and li2[i-1][j] == 'x' and li2[i+1][j] == '.':
                    point[i][j] += 200
                elif 0<=j<15 and i+2<15 and i-2>=0 and li2[i-2][j] == 'o' and li2[i-1][j] == 'x' and li2[i+1][j] == 'x' and li2[i+2][j] == '.':
                    point[i][j] += 200
                elif 0<=j<15 and i+3<15 and i-1>=0 and li2[i-1][j] == 'o' and li2[i+1][j] == 'x' and li2[i+2][j] == 'x' and li2[i+3][j] == '.':
                    point[i][j] += 200
                elif 0<=j<15 and i-1<15 and i-3>=0 and li2[i-3][j] == 'x' and li2[i-2][j] == 'o' and li2[i-1][j] == 'o':
                    point[i][j] += 200
                elif 0<=j<15 and i+3<15 and i+1>=0 and li2[i+3][j] == 'x' and li2[i+2][j] == 'o' and li2[i+1][j] == 'o':
                    point[i][j] += 200
                    #纵向
                if 0<=i-1 and i+3<15 and 0<=j-3 and j+1<15 and li2[i+3][j-3] == '.' and li2[i+2][j-2] == 'x' and li2[i+1][j-1] == 'x' and li2[i-1][j+1] == 'o':
                    point[i][j] += 200
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i+2][j-2] == '.' and li2[i+1][j-1] == 'x' and li2[i-1][j+1] == 'x' and li2[i-2][j+2] == 'o':
                    point[i][j] += 200
                elif 0<=i-3 and i+1<15 and 0<=j-1 and j+3<15 and li2[i+1][j-1] == '.' and li2[i-1][j+1] == 'x' and li2[i-2][j+2] == 'x' and li2[i-3][j+3] == 'o':
                    point[i][j] += 200
                elif 0<=i-1 and i+3<15 and 0<=j-3 and j+1<15 and li2[i+3][j-3] == 'o' and li2[i+2][j-2] == 'x' and li2[i+1][j-1] == 'x' and li2[i-1][j+1] == '.':
                    point[i][j] += 200
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i+2][j-2] == 'o' and li2[i+1][j-1] == 'x' and li2[i-1][j+1] == 'x' and li2[i-2][j+2] == '.':
                    point[i][j] += 200
                elif 0<=i-3 and i+1<15 and 0<=j-1 and j+3<15 and li2[i+1][j-1] == 'o' and li2[i-1][j+1] == 'x' and li2[i-2][j+2] == 'x' and li2[i-3][j+3] == '.':
                    point[i][j] += 200
                elif 0<=i+1 and i+3<15 and 0<=j-3 and j-1<15 and li2[i+3][j-3] == 'x' and li2[i+2][j-2] == 'o' and li2[i+1][j-1] == 'o':
                    point[i][j] += 200
                elif 0<=i-3 and i-1<15 and 0<=j+1 and j+3<15 and li2[i-3][j+3] == 'x' and li2[i-2][j+2] == 'o' and li2[i-1][j+1] == 'o':
                    point[i][j] += 200
                    #右上—》左下
                    #无效进攻防守
                if 0<=i<15 and j+1<15 and j-2>=0 and li2[i][j-2] == '.' and li2[i][j-1] == 'x' and li2[i][j+1] == '.':
                    point[i][j] += 50
                elif 0<=i<15 and j+2<15 and j-1>=0 and li2[i][j-1] == '.' and li2[i][j+1] == 'x' and li2[i][j+2] == '.':
                    point[i][j] += 50
                    #横向
                if 0<=i-2 and i+1<15 and 0<=j-2 and j+1<15 and li2[i-2][j-2] == '.' and li2[i-1][j-1] == 'x' and li2[i+1][j+1] == '.':
                    point[i][j] += 50
                elif 0<=i-1 and i+2<15 and 0<=j-1 and j+2<15 and li2[i-1][j-1] == '.' and li2[i+1][j+1] == 'x' and li2[i+2][j+2] == '.':
                    point[i][j] += 50
                    #左上-》右下
                if 0<=j<15 and i+1<15 and i-2>=0 and li2[i-2][j] == '.' and li2[i-1][j] == 'x' and li2[i+1][j] == '.':
                    point[i][j] += 50
                elif 0<=j<15 and i+2<15 and i-1>=0 and li2[i-1][j] == '.' and li2[i+1][j] == 'x' and li2[i+2][j] == '.':
                    point[i][j] += 50
                    #纵向
                if 0<=i-2 and i+1<15 and 0<=j-1 and j+2<15 and li2[i-2][j+2] == '.' and li2[i-1][j+1] == 'x' and li2[i+1][j-1] == '.':
                    point[i][j] += 50
                elif 0<=i-1 and i+2<15 and 0<=j-2 and j+1<15 and li2[i-1][j+1] == '.' and li2[i+1][j-1] == 'x' and li2[i+2][j-2] == '.':
                    point[i][j] += 50
                    #右上左下
                    #布局棋形
            else:#该下白棋
                if 0<=i<15 and j+4<15 and j+1>=0 and li2[i][j+1] == 'o' and li2[i][j+2] == 'o' and li2[i][j+3] == 'o' and li2[i][j+4] == 'o':
                    point[i][j] += 10000
                elif 0<=i<15 and j+3<15 and j-1>=0 and li2[i][j-1] == 'o' and li2[i][j+1] == 'o' and li2[i][j+2] == 'o' and li2[i][j+3] == 'o':
                    point[i][j] += 10000
                elif 0<=i<15 and j+2<15 and j-2>=0 and li2[i][j-2] == 'o' and li2[i][j-1] == 'o' and li2[i][j+1] == 'o' and li2[i][j+2] == 'o':
                    point[i][j] += 10000
                elif 0<=i<15 and j+1<15 and j-3>=0 and li2[i][j-3] == 'o' and li2[i][j-2] == 'o' and li2[i][j-1] == 'o' and li2[i][j+1] == 'o':
                    point[i][j] += 10000
                elif 0<=i<15 and j-1<15 and j-4>=0 and li2[i][j-4] == 'o' and li2[i][j-3] == 'o' and li2[i][j-2] == 'o' and li2[i][j-1] == 'o':
                    point[i][j] += 10000
                    #横向
                if 0<=i+1 and i+4<15 and 0<=j+1 and j+4<15 and li2[i+1][j+1] == 'o' and li2[i+2][j+2] == 'o' and li2[i+3][j+3] == 'o' and li2[i+4][j+4] == 'o':
                    point[i][j] += 10000
                elif 0<=i-1 and i+3<15 and 0<=j-1 and j+3<15 and li2[i-1][j-1] == 'o' and li2[i+1][j+1] == 'o' and li2[i+2][j+2] == 'o' and li2[i+3][j+3] == 'o':
                    point[i][j] += 10000
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i-2][j-2] == 'o' and li2[i-1][j-1] == 'o' and li2[i+1][j+1] == 'o' and li2[i+2][j+2] == 'o':
                    point[i][j] += 10000
                elif 0<=i-3 and i+1<15 and 0<=j-3 and j+1<15 and li2[i-3][j-3] == 'o' and li2[i-2][j-2] == 'o' and li2[i-1][j-1] == 'o' and li2[i+1][j+1] == 'o':
                    point[i][j] += 10000
                elif 0<=i-4 and i-1<15 and 0<=j-4 and j-1<15 and li2[i-4][j-4] == 'o' and li2[i-3][j-3] == 'o' and li2[i-2][j-2] == 'o' and li2[i-1][j-1] == 'o':
                    point[i][j] += 10000
                    #左上-》右下
                if 0<=j<15 and i+4<15 and i+1>=0 and li2[i+1][j] == 'o' and li2[i+2][j] == 'o' and li2[i+3][j] == 'o' and li2[i+4][j] == 'o':
                    point[i][j] += 10000
                elif 0<=j<15 and i+3<15 and i-1>=0 and li2[i-1][j] == 'o' and li2[i+1][j] == 'o' and li2[i+2][j] == 'o' and li2[i+3][j] == 'o':
                    point[i][j] += 10000
                elif 0<=j<15 and i+2<15 and i-2>=0 and li2[i-2][j] == 'o' and li2[i-1][j] == 'o' and li2[i+1][j] == 'o' and li2[i+2][j] == 'o':
                    point[i][j] += 10000
                elif 0<=j<15 and i+1<15 and i-3>=0 and li2[i-3][j] == 'o' and li2[i-2][j] == 'o' and li2[i-1][j] == 'o' and li2[i+1][j] == 'o':
                    point[i][j] += 10000
                elif 0<=j<15 and i-1<15 and i-4>=0 and li2[i-4][j] == 'o' and li2[i-3][j] == 'o' and li2[i-2][j] == 'o' and li2[i-1][j] == 'o':
                    point[i][j] += 10000
                    #纵向
                if 0<=i+1 and i+4<15 and 0<=j-4 and j-1<15 and li2[i+1][j-1] == 'o' and li2[i+2][j-2] == 'o' and li2[i+3][j-3] == 'o' and li2[i+4][j-4] == 'o':
                    point[i][j] += 10000
                elif 0<=i-1 and i+3<15 and 0<=j-3 and j+1<15 and li2[i-1][j+1] == 'o' and li2[i+1][j-1] == 'o' and li2[i+2][j-2] == 'o' and li2[i+3][j-3] == 'o':
                    point[i][j] += 10000
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i-2][j+2] == 'o' and li2[i-1][j+1] == 'o' and li2[i+1][j-1] == 'o' and li2[i+2][j-2] == 'o':
                    point[i][j] += 10000
                elif 0<=i-3 and i+1<15 and 0<=j-1 and j+3<15 and li2[i-3][j+3] == 'o' and li2[i-2][j+2] == 'o' and li2[i-1][j+1] == 'o' and li2[i+1][j-1] == 'o':
                    point[i][j] += 10000
                elif i-4>=0 and i-1<15 and j+4<15 and j+1>0 and li2[i-4][j+4] == 'o' and li2[i-3][j+3] == 'o' and li2[i-2][j+2] == 'o' and li2[i-1][j+1] == 'o':
                    point[i][j] += 10000
                    #右上-》左下
                    #致胜棋形
                if 0<=i<15 and j+4<15 and j+1>=0 and li2[i][j+1] == 'x' and li2[i][j+2] == 'x' and li2[i][j+3] == 'x' and li2[i][j+4] == 'x':
                    point[i][j] += 6000
                elif 0<=i<15 and j+3<15 and j-1>=0 and li2[i][j-1] == 'x' and li2[i][j+1] == 'x' and li2[i][j+2] == 'x' and li2[i][j+3] == 'x':
                    point[i][j] += 6000
                elif 0<=i<15 and j+2<15 and j-2>=0 and li2[i][j-2] == 'x' and li2[i][j-1] == 'x' and li2[i][j+1] == 'x' and li2[i][j+2] == 'x':
                    point[i][j] += 6000
                elif 0<=i<15 and j+1<15 and j-3>=0 and li2[i][j-3] == 'x' and li2[i][j-2] == 'x' and li2[i][j-1] == 'x' and li2[i][j+1] == 'x':
                    point[i][j] += 6000
                elif 0<=i<15 and j-1<15 and j-4>=0 and li2[i][j-4] == 'x' and li2[i][j-3] == 'x' and li2[i][j-2] == 'x' and li2[i][j-1] == 'x':
                    point[i][j] += 6000
                    #横向
                if 0<=i+1 and i+4<15 and 0<=j+1 and j+4<15 and li2[i+1][j+1] == 'x' and li2[i+2][j+2] == 'x' and li2[i+3][j+3] == 'x' and li2[i+4][j+4] == 'x':
                    point[i][j] += 6000
                elif 0<=i-1 and i+3<15 and 0<=j-1 and j+3<15 and li2[i-1][j-1] == 'x' and li2[i+1][j+1] == 'x' and li2[i+2][j+2] == 'x' and li2[i+3][j+3] == 'x':
                    point[i][j] += 6000
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i-2][j-2] == 'x' and li2[i-1][j-1] == 'x' and li2[i+1][j+1] == 'x' and li2[i+2][j+2] == 'x':
                    point[i][j] += 6000
                elif 0<=i-3 and i+1<15 and 0<=j-3 and j+1<15 and li2[i-3][j-3] == 'x' and li2[i-2][j-2] == 'x' and li2[i-1][j-1] == 'x' and li2[i+1][j+1] == 'x':
                    point[i][j] += 6000
                elif 0<=i-4 and i-1<15 and 0<=j-4 and j-1<15 and li2[i-4][j-4] == 'x' and li2[i-3][j-3] == 'x' and li2[i-2][j-2] == 'x' and li2[i-1][j-1] == 'x':
                    point[i][j] += 6000
                    #左上-》右下
                if 0<=j<15 and i+4<15 and i+1>=0 and li2[i+1][j] == 'x' and li2[i+2][j] == 'x' and li2[i+3][j] == 'x' and li2[i+4][j] == 'x':
                    point[i][j] += 6000
                elif 0<=j<15 and i+3<15 and i-1>=0 and li2[i-1][j] == 'x' and li2[i+1][j] == 'x' and li2[i+2][j] == 'x' and li2[i+3][j] == 'x':
                    point[i][j] += 6000
                elif 0<=j<15 and i+2<15 and i-2>=0 and li2[i-2][j] == 'x' and li2[i-1][j] == 'x' and li2[i+1][j] == 'x' and li2[i+2][j] == 'x':
                    point[i][j] += 6000
                elif 0<=j<15 and i+1<15 and i-3>=0 and li2[i-3][j] == 'x' and li2[i-2][j] == 'x' and li2[i-1][j] == 'x' and li2[i+1][j] == 'x':
                    point[i][j] += 6000
                elif 0<=j<15 and i-1<15 and i-4>=0 and li2[i-4][j] == 'x' and li2[i-3][j] == 'x' and li2[i-2][j] == 'x' and li2[i-1][j] == 'x':
                    point[i][j] += 6000
                    #纵向
                if 0<=i+1 and i+4<15 and 0<=j-4 and j-1<15 and li2[i+1][j-1] == 'x' and li2[i+2][j-2] == 'x' and li2[i+3][j-3] == 'x' and li2[i+4][j-4] == 'x':
                    point[i][j] += 6000
                elif 0<=i-1 and i+3<15 and 0<=j-3 and j+1<15 and li2[i-1][j+1] == 'x' and li2[i+1][j-1] == 'x' and li2[i+2][j-2] == 'x' and li2[i+3][j-3] == 'x':
                    point[i][j] += 6000
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i-2][j+2] == 'x' and li2[i-1][j+1] == 'x' and li2[i+1][j-1] == 'x' and li2[i+2][j-2] == 'x':
                    point[i][j] += 6000
                elif 0<=i-3 and i+1<15 and 0<=j-1 and j+3<15 and li2[i-3][j+3] == 'x' and li2[i-2][j+2] == 'x' and li2[i-1][j+1] == 'x' and li2[i+1][j-1] == 'x':
                    point[i][j] += 6000
                elif 0<=i-4 and i-1<15 and 0<=j+1 and j+4<15 and li2[i-4][j+4] == 'x' and li2[i-3][j+3] == 'x' and li2[i-2][j+2] == 'x' and li2[i-1][j+1] == 'x':
                    point[i][j] += 6000
                    #右上-》左下
                    #必须防守棋形
                if 0<=i<15 and j+4<15 and j-1>=0 and li2[i][j-1] == '.' and li2[i][j+1]=='o' and li2[i][j+2]=='o' and li2[i][j+3]=='o' and li2[i][j+4]=='.':
                    point[i][j] += 5000
                elif 0<=i<15 and j+3<15 and j-2>=0 and li2[i][j-2] == '.' and li2[i][j-1]=='o' and li2[i][j+1]=='o' and li2[i][j+2]=='o' and li2[i][j+3]=='.':
                    point[i][j] += 5000
                elif 0<=i<15 and j+2<15 and j-3>=0 and li2[i][j-3] == '.' and li2[i][j-2]=='o' and li2[i][j-1]=='o' and li2[i][j+1]=='o' and li2[i][j+2]=='.':
                    point[i][j] += 5000
                elif 0<=i<15 and j+1<15 and j-4>=0 and li2[i][j-4] == '.' and li2[i][j-3]=='o' and li2[i][j-2]=='o' and li2[i][j-1]=='o' and li2[i][j+1]=='.':
                    point[i][j] += 5000
                    #横向
                if 0<=i-1 and i+4<15 and 0<=j-1 and j+4<15 and li2[i-1][j-1] == '.' and li2[i+1][j+1]=='o' and li2[i+2][j+2]=='o' and li2[i+3][j+3]=='o' and li2[i+4][j+4]=='.':
                    point[i][j] += 5000
                elif 0<=i-2 and i+3<15 and 0<=j-2 and j+3<15 and li2[i-2][j-2] == '.' and li2[i-1][j-1]=='o' and li2[i+1][j+1]=='o' and li2[i+2][j+2]=='o' and li2[i+3][j+3]=='.':
                    point[i][j] += 5000
                elif 0<=i-3 and i+2<15 and 0<=j-3 and j+2<15 and li2[i-3][j-3] == '.' and li2[i-2][j-2]=='o' and li2[i-1][j-1]=='o' and li2[i+1][j+1]=='o' and li2[i+2][j+2]=='.':
                    point[i][j] += 5000
                elif 0<=i-4 and i+1<15 and 0<=j-4 and j+1<15 and li2[i-4][j-4] == '.' and li2[i-3][j-3]=='o' and li2[i-2][j-2]=='o' and li2[i-1][j-1]=='o' and li2[i+1][j+1]=='.':
                    point[i][j] += 5000
                    #左上-》右下
                if 0<=j<15 and i+4<15 and i-1>=0 and li2[i-1][j] == '.' and li2[i+1][j]=='o' and li2[i+2][j]=='o' and li2[i+3][j]=='o' and li2[i+4][j]=='.':
                    point[i][j] += 5000
                elif 0<=j<15 and i+3<15 and i-2>=0 and li2[i-2][j] == '.' and li2[i-1][j]=='o' and li2[i+1][j]=='o' and li2[i+2][j]=='o' and li2[i+3][j]=='.':
                    point[i][j] += 5000
                elif 0<=j<15 and i+2<15 and i-3>=0 and li2[i-3][j] == '.' and li2[i-2][j]=='o' and li2[i-1][j]=='o' and li2[i+1][j]=='o' and li2[i+2][j]=='.':
                    point[i][j] += 5000
                elif 0<=j<15 and i+1<15 and i-4>=0 and li2[i-4][j] == '.' and li2[i-3][j]=='o' and li2[i-2][j]=='o' and li2[i-1][j]=='o' and li2[i+1][j]=='.':
                    point[i][j] += 5000
                    #纵向
                if 0<=i-4 and i+1<15 and 0<=j-1 and j+4<15 and li2[i+1][j-1] == '.' and li2[i-1][j+1]=='o' and li2[i-2][j+2]=='o' and li2[i-3][j+3]=='o' and li2[i-4][j+4]=='.':
                    point[i][j] += 5000
                elif 0<=i-3 and i+2<15 and 0<=j-2 and j+3<15 and li2[i+2][j-2] == '.' and li2[i+1][j-1]=='o' and li2[i-1][j+1]=='o' and li2[i-2][j+2]=='o' and li2[i-3][j+3]=='.':
                    point[i][j] += 5000
                elif 0<=i-2 and i+3<15 and 0<=j-3 and j+2<15 and li2[i+3][j-3] == '.' and li2[i+2][j-2]=='o' and li2[i+1][j-1]=='o' and li2[i-1][j+1]=='o' and li2[i-2][j+2]=='.':
                    point[i][j] += 5000
                elif 0<=i-1 and i+4<15 and 0<=j-4 and j+1<15 and li2[i+4][j-4] == '.' and li2[i+3][j-3]=='o' and li2[i+2][j-2]=='o' and li2[i+1][j-1]=='o' and li2[i-1][j+1]=='.':
                    point[i][j] += 5000
                    #右上-》左下
                    #两步致胜
                if 0<=i<15 and j+4<15 and j-1>=0 and li2[i][j+1]=='x' and li2[i][j+2]=='x' and li2[i][j+3]=='x' and li2[i][j+4]=='.':
                    point[i][j] += 2500
                elif 0<=i<15 and j+3<15 and j-2>=0 and li2[i][j-2] == '.' and li2[i][j-1]=='x' and li2[i][j+1]=='x' and li2[i][j+2]=='x' and li2[i][j+3]=='.':
                    point[i][j] += 2500
                elif 0<=i<15 and j+2<15 and j-3>=0 and li2[i][j-3] == '.' and li2[i][j-2]=='x' and li2[i][j-1]=='x' and li2[i][j+1]=='x' and li2[i][j+2]=='.':
                    point[i][j] += 2500
                elif 0<=i<15 and j+1<15 and j-4>=0 and li2[i][j-4] == '.' and li2[i][j-3]=='x' and li2[i][j-2]=='x' and li2[i][j-1]=='x':
                    point[i][j] += 2500
                    #横向
                if 0<=i-1 and i+4<15 and 0<=j-1 and j+4<15 and li2[i+1][j+1]=='x' and li2[i+2][j+2]=='x' and li2[i+3][j+3]=='x' and li2[i+4][j+4]=='.':
                    point[i][j] += 2500
                elif 0<=i-2 and i+3<15 and 0<=j-2 and j+3<15 and li2[i-2][j-2] == '.' and li2[i-1][j-1]=='x' and li2[i+1][j+1]=='x' and li2[i+2][j+2]=='x' and li2[i+3][j+3]=='.':
                    point[i][j] += 2500
                elif 0<=i-3 and i+2<15 and 0<=j-3 and j+2<15 and li2[i-3][j-3] == '.' and li2[i-2][j-2]=='x' and li2[i-1][j-1]=='x' and li2[i+1][j+1]=='x' and li2[i+2][j+2]=='.':
                    point[i][j] += 2500
                elif 0<=i-4 and i+1<15 and 0<=j-4 and j+1<15 and li2[i-4][j-4] == '.' and li2[i-3][j-3]=='x' and li2[i-2][j-2]=='x' and li2[i-1][j-1]=='x':
                    point[i][j] += 2500
                    #左上-》右下
                if 0<=j<15 and i+4<15 and i-1>=0 and li2[i+1][j]=='x' and li2[i+2][j]=='x' and li2[i+3][j]=='x' and li2[i+4][j]=='.':
                    point[i][j] += 2500
                elif 0<=j<15 and i+3<15 and i-2>=0 and li2[i-2][j] == '.' and li2[i-1][j]=='x' and li2[i+1][j]=='x' and li2[i+2][j]=='x' and li2[i+3][j]=='.':
                    point[i][j] += 2500
                elif 0<=j<15 and i+2<15 and i-3>=0 and li2[i-3][j] == '.' and li2[i-2][j]=='x' and li2[i-1][j]=='x' and li2[i+1][j]=='x' and li2[i+2][j]=='.':
                    point[i][j] += 2500
                elif 0<=j<15 and i+1<15 and i-4>=0 and li2[i-4][j] == '.' and li2[i-3][j]=='x' and li2[i-2][j]=='x' and li2[i-1][j]=='x':
                    point[i][j] += 2500
                    #纵向
                if 0<=i-4 and i+1<15 and 0<=j-1 and j+4<15 and li2[i-1][j+1]=='x' and li2[i-2][j+2]=='x' and li2[i-3][j+3]=='x' and li2[i-4][j+4]=='.':
                    point[i][j] += 2500
                elif 0<=i-3 and i+2<15 and 0<=j-2 and j+3<15 and li2[i+2][j-2] == '.' and li2[i+1][j-1]=='x' and li2[i-1][j+1]=='x' and li2[i-2][j+2]=='x' and li2[i-3][j+3]=='.':
                    point[i][j] += 2500
                elif 0<=i-2 and i+3<15 and 0<=j-3 and j+2<15 and li2[i+3][j-3] == '.' and li2[i+2][j-2]=='x' and li2[i+1][j-1]=='x' and li2[i-1][j+1]=='x' and li2[i-2][j+2]=='.':
                    point[i][j] += 2500
                elif 0<=i-1 and i+4<15 and 0<=j-4 and j+1<15 and li2[i+4][j-4] == '.' and li2[i+3][j-3]=='x' and li2[i+2][j-2]=='x' and li2[i+1][j-1]=='x':
                    point[i][j] += 2500
                    #右上-》左下
                    #两部防守
                if 0<=i<15 and j+4<15 and j-1>=0 and li2[i][j-1] == 'x' and li2[i][j+1]=='o' and li2[i][j+2]=='o' and li2[i][j+3]=='o' and li2[i][j+4]=='.':
                    point[i][j] += 2000
                elif 0<=i<15 and j+3<15 and j-2>=0 and li2[i][j-2] == 'x' and li2[i][j-1]=='o' and li2[i][j+1]=='o' and li2[i][j+2]=='o' and li2[i][j+3]=='.':
                    point[i][j] += 2000
                elif 0<=i<15 and j+2<15 and j-3>=0 and li2[i][j-3] == 'x' and li2[i][j-2]=='o' and li2[i][j-1]=='o' and li2[i][j+1]=='o' and li2[i][j+2]=='.':
                    point[i][j] += 2000
                elif 0<=i<15 and j+1<15 and j-4>=0 and li2[i][j-4] == 'x' and li2[i][j-3]=='o' and li2[i][j-2]=='o' and li2[i][j-1]=='o' and li2[i][j+1]=='.':
                    point[i][j] += 2000
                elif 0<=i<15 and j+4<15 and j-1>=0 and li2[i][j - 1] == '.' and li2[i][j + 1] == 'o' and li2[i][j + 2] == 'o' and li2[i][j + 3] == 'o' and li2[i][j + 4] == 'x':
                    point[i][j] += 2000
                elif 0<=i<15 and j+3<15 and j-2>=0 and li2[i][j - 2] == '.' and li2[i][j - 1] == 'o' and li2[i][j + 1] == 'o' and li2[i][j + 2] == 'o' and li2[i][j + 3] == 'x':
                    point[i][j] += 2000
                elif 0<=i<15 and j+2<15 and j-3>=0 and li2[i][j - 3] == '.' and li2[i][j - 2] == 'o' and li2[i][j - 1] == 'o' and li2[i][j + 1] == 'o' and li2[i][j + 2] == 'x':
                    point[i][j] += 2000
                elif 0<=i<15 and j+1<15 and j-4>=0 and li2[i][j - 4] == '.' and li2[i][j - 3] == 'o' and li2[i][j - 2] == 'o' and li2[i][j - 1] == 'o' and li2[i][j + 1] == 'x':
                    point[i][j] += 2000
                    #横向
                if 0<=i-1 and i+4<15 and 0<=j-1 and j+4<15 and li2[i-1][j-1] == 'x' and li2[i+1][j+1]=='o' and li2[i+2][j+2]=='o' and li2[i+3][j+3]=='o' and li2[i+4][j+4]=='.':
                    point[i][j] += 2000
                elif 0<=i-2 and i+3<15 and 0<=j-2 and j+3<15 and li2[i-2][j-2] == 'x' and li2[i-1][j-1]=='o' and li2[i+1][j+1]=='o' and li2[i+2][j+2]=='o' and li2[i+3][j+3]=='.':
                    point[i][j] += 2000
                elif 0<=i-3 and i+2<15 and 0<=j-3 and j+2<15 and li2[i-3][j-3] == 'x' and li2[i-2][j-2]=='o' and li2[i-1][j-1]=='o' and li2[i+1][j+1]=='o' and li2[i+2][j+2]=='.':
                    point[i][j] += 2000
                elif 0<=i-4 and i+1<15 and 0<=j-4 and j+1<15 and li2[i-4][j-4] == 'x' and li2[i-3][j-3]=='o' and li2[i-2][j-2]=='o' and li2[i-1][j-1]=='o' and li2[i+1][j+1]=='.':
                    point[i][j] += 2000
                elif 0<=i-1 and i+4<15 and 0<=j-1 and j+4<15 and li2[i - 1][j - 1] == '.' and li2[i + 1][j + 1] == 'o' and li2[i + 2][j + 2] == 'o' and li2[i + 3][j + 3] == 'o' and li2[i + 4][j + 4] == 'x':
                    point[i][j] += 2000
                elif 0<=i-2 and i+3<15 and 0<=j-2 and j+3<15 and li2[i - 2][j - 2] == '.' and li2[i - 1][j - 1] == 'o' and li2[i + 1][j + 1] == 'o' and li2[i + 2][j + 2] == 'o' and li2[i + 3][j + 3] == 'x':
                    point[i][j] += 2000
                elif 0<=i-3 and i+2<15 and 0<=j-3 and j+2<15 and li2[i - 3][j - 3] == '.' and li2[i - 2][j - 2] == 'o' and li2[i - 1][j - 1] == 'o' and li2[i + 1][j + 1] == 'o' and li2[i + 2][j + 2] == 'x':
                    point[i][j] += 2000
                elif 0<=i-4 and i+1<15 and 0<=j-4 and j+1<15 and li2[i - 4][j - 4] == '.' and li2[i - 3][j - 3] == 'o' and li2[i - 2][j - 2] == 'o' and li2[i - 1][j - 1] == 'o' and li2[i + 1][j + 1] == 'x':
                    point[i][j] += 2000
                    #左上-》右下
                if 0<=j<15 and i+4<15 and i-1>=0 and li2[i-1][j] == 'x' and li2[i+1][j]=='o' and li2[i+2][j]=='o' and li2[i+3][j]=='o' and li2[i+4][j]=='.':
                    point[i][j] += 2000
                elif 0<=j<15 and i+3<15 and i-2>=0 and li2[i-2][j] == 'x' and li2[i-1][j]=='o' and li2[i+1][j]=='o' and li2[i+2][j]=='o' and li2[i+3][j]=='.':
                    point[i][j] += 2000
                elif 0<=j<15 and i+2<15 and i-3>=0 and li2[i-3][j] == 'x' and li2[i-2][j]=='o' and li2[i-1][j]=='o' and li2[i+1][j]=='o' and li2[i+2][j]=='.':
                    point[i][j] += 2000
                elif 0<=j<15 and i+1<15 and i-4>=0 and li2[i-4][j] == 'x' and li2[i-3][j]=='o' and li2[i-2][j]=='o' and li2[i-1][j]=='o' and li2[i+1][j]=='.':
                    point[i][j] += 2000
                elif 0<=j<15 and i+4<15 and i-1>=0 and li2[i - 1][j] == '.' and li2[i + 1][j] == 'o' and li2[i + 2][j] == 'o' and li2[i + 3][j] == 'o' and li2[i + 4][j] == 'x':
                    point[i][j] += 2000
                elif 0<=j<15 and i+3<15 and i-2>=0 and li2[i - 2][j] == '.' and li2[i - 1][j] == 'o' and li2[i + 1][j] == 'o' and li2[i + 2][j] == 'o' and li2[i + 3][j] == 'x':
                    point[i][j] += 2000
                elif 0<=j<15 and i+2<15 and i-3>=0 and li2[i - 3][j] == '.' and li2[i - 2][j] == 'o' and li2[i - 1][j] == 'o' and li2[i + 1][j] == 'o' and li2[i + 2][j] == 'x':
                    point[i][j] += 2000
                elif 0<=j<15 and i+1<15 and i-4>=0 and li2[i - 4][j] == '.' and li2[i - 3][j] == 'o' and li2[i - 2][j] == 'o' and li2[i - 1][j] == 'o' and li2[i + 1][j] == 'x':
                    point[i][j] += 2000
                    #纵向
                if 0<=i-4 and i+1<15 and 0<=j-1 and j+4<15 and li2[i+1][j-1] == 'x' and li2[i-1][j+1]=='o' and li2[i-2][j+2]=='o' and li2[i-3][j+3]=='o' and li2[i-4][j+4]=='.':
                    point[i][j] += 2000
                elif 0<=i-3 and i+2<15 and 0<=j-2 and j+3<15 and li2[i+2][j-2] == 'x' and li2[i+1][j-1]=='o' and li2[i-1][j+1]=='o' and li2[i-2][j+2]=='o' and li2[i-3][j+3]=='.':
                    point[i][j] += 2000
                elif 0<=i-2 and i+3<15 and 0<=j-3 and j+2<15 and li2[i+3][j-3] == 'x' and li2[i+2][j-2]=='o' and li2[i+1][j-1]=='o' and li2[i-1][j+1]=='o' and li2[i-2][j+2]=='.':
                    point[i][j] += 2000
                elif 0<=i-1 and i+4<15 and 0<=j-4 and j+1<15 and li2[i+4][j-4] == 'x' and li2[i+3][j-3]=='o' and li2[i+2][j-2]=='o' and li2[i+1][j-1]=='o' and li2[i-1][j+1]=='.':
                    point[i][j] += 2000
                elif 0<=i-4 and i+1<15 and 0<=j-1 and j+4<15 and li2[i + 1][j - 1] == '.' and li2[i - 1][j + 1] == 'o' and li2[i - 2][j + 2] == 'o' and li2[i - 3][j + 3] == 'o' and li2[i - 4][j + 4] == 'x':
                    point[i][j] += 2000
                elif 0<=i-3 and i+2<15 and 0<=j-2 and j+3<15 and li2[i + 2][j - 2] == '.' and li2[i + 1][j - 1] == 'o' and li2[i - 1][j + 1] == 'o' and li2[i - 2][j + 2] == 'o' and li2[i - 3][j + 3] == 'x':
                    point[i][j] += 2000
                elif 0<=i-2 and i+3<15 and 0<=j-3 and j+2<15 and li2[i + 3][j - 3] == '.' and li2[i + 2][j - 2] == 'o' and li2[i + 1][j - 1] == 'o' and li2[i - 1][j + 1] == 'o' and li2[i - 2][j + 2] == 'x':
                    point[i][j] += 2000
                elif 0<=i-1 and i+4<15 and 0<=j-4 and j+1<15 and li2[i + 4][j - 4] == '.' and li2[i + 3][j - 3] == 'o' and li2[i + 2][j - 2] == 'o' and li2[i + 1][j - 1] == 'o' and li2[i - 1][j + 1] == 'x':
                    point[i][j] += 2000
                    #右上-》左下
                    #进攻棋形
                if 0<=i<15 and j+1<15 and j-3>=0 and li2[i][j-3] == '.' and li2[i][j-2] == 'o' and li2[i][j-1] == 'o' and li2[i][j+1] == '.':
                    point[i][j] += 400
                elif 0<=i<15 and j+2<15 and j-2>=0 and li2[i][j-2] == '.' and li2[i][j-1] == 'o' and li2[i][j+1] == 'o' and li2[i][j+2] == '.':
                    point[i][j] += 400
                elif 0<=i<15 and j+3<15 and j-1>=0 and li2[i][j-1] == '.' and li2[i][j+1] == 'o' and li2[i][j+2] == 'o' and li2[i][j+3] == '.':
                    point[i][j] += 400
                    #横向
                if 0<=i-3 and i+1<15 and 0<=j-3 and j+1<15 and li2[i-3][j-3] == '.' and li2[i-2][j-2] == 'o' and li2[i-1][j-1] == 'o' and li2[i+1][j+1] == '.':
                    point[i][j] += 400
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i-2][j-2] == '.' and li2[i-1][j-1] == 'o' and li2[i+1][j+1] == 'o' and li2[i+2][j+2] == '.':
                    point[i][j] += 400
                elif 0<=i-1 and i+3<15 and 0<=j-1 and j+3<15 and li2[i-1][j-1] == '.' and li2[i+1][j+1] == 'o' and li2[i+2][j+2] == 'o' and li2[i+3][j+3] == '.':
                    point[i][j] += 400
                    #左上-》右下
                if 0<=j<15 and i+1<15 and i-3>=0 and li2[i - 3][j] == '.' and li2[i - 2][j] == 'o' and li2[i - 1][j] == 'o' and li2[i + 1][j] == '.':
                    point[i][j] += 400
                elif 0<=j<15 and i+2<15 and i-2>=0 and li2[i - 2][j] == '.' and li2[i - 1][j] == 'o' and li2[i + 1][j] == 'o' and li2[i + 2][j] == '.':
                    point[i][j] += 400
                elif 0<=j<15 and i+3<15 and i-1>=0 and li2[i - 1][j] == '.' and li2[i + 1][j] == 'o' and li2[i + 2][j] == 'o' and li2[i + 3][j] == '.':
                    point[i][j] += 400
                    #纵向
                if 0<=i-1 and i+3<15 and 0<=j-3 and j+1<15 and li2[i+3][j - 3] == '.' and li2[i+2][j - 2] == 'o' and li2[i+1][j - 1] == 'o' and li2[i-1][j + 1] == '.':
                    point[i][j] += 400
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i+2][j - 2] == '.' and li2[i+1][j - 1] == 'o' and li2[i-1][j + 1] == 'o' and li2[i-2][j + 2] == '.':
                    point[i][j] += 400
                elif 0<=i-3 and i+1<15 and 0<=j-1 and j+3<15 and li2[i+1][j - 1] == '.' and li2[i-1][j + 1] == 'o' and li2[i-2][j + 2] == 'o' and li2[i-3][j + 3] == '.':
                    point[i][j] += 400
                    #右上-》左下
                    #两部进攻棋形
                if 0<=i<15 and j-1<15 and j-3>=0 and li2[i][j-3] == '.' and li2[i][j-2] == 'x' and li2[i][j-1] == 'x':
                    point[i][j] += 400
                elif 0<=i<15 and j+3<15 and j+1>=0 and li2[i][j+3] == '.' and li2[i][j+2] == 'x' and li2[i][j+1] == 'x':
                    point[i][j] += 400
                elif 0<=i<15 and j-1<15 and j-4>=0 and li2[i][j-4] == 'o' and li2[i][j-3] == 'x' and li2[i][j-2] == 'x' and li2[i][j-1] == 'x':
                    point[i][j] += 400
                elif 0<=i<15 and j+4<15 and j+1>=0 and li2[i][j+1] == 'x' and li2[i][j+2] == 'x' and li2[i][j+3] == 'x' and li2[i][j+4] == 'o':
                    point[i][j] += 400
                    #横向
                if 0<=i-3 and i-1<15 and 0<=j-3 and j-1<15 and li2[i-3][j-3] == '.' and li2[i-2][j-2] == 'x' and li2[i-1][j-1] == 'x':
                    point[i][j] += 400
                elif 0<=i+1 and i+3<15 and 0<=j+1 and j+3<15 and li2[i+3][j+3] == '.' and li2[i+2][j+2] == 'x' and li2[i+1][j+1] == 'x':
                    point[i][j] += 400
                elif 0<=i-4 and i-1<15 and 0<=j-4 and j-1<15 and li2[i-4][j-4] == 'o' and li2[i-3][j-3] == 'x' and li2[i-2][j-2] == 'x' and li2[i-1][j-1] == 'x':
                    point[i][j] += 400
                elif 0<=i+1 and i+4<15 and 0<=j+1 and j+4<15 and li2[i+1][j+1] == 'x' and li2[i+2][j+2] == 'x' and li2[i+3][j+3] == 'x' and li2[i+4][j+4] == 'o':
                    point[i][j] += 400
                    #左上-》右下
                if 0<=j<15 and i-1<15 and i-3>=0 and li2[i-3][j] == '.' and li2[i-2][j] == 'x' and li2[i-1][j] == 'x':
                    point[i][j] += 400
                elif 0<=j<15 and i+3<15 and i+1>=0 and li2[i+3][j] == '.' and li2[i+2][j] == 'x' and li2[i+1][j] == 'x':
                    point[i][j] += 400
                elif 0<=j<15 and i-1<15 and i-4>=0 and li2[i-4][j] == 'o' and li2[i-3][j] == 'x' and li2[i-2][j] == 'x' and li2[i-1][j] == 'x':
                    point[i][j] += 400
                elif 0<=j<15 and i+4<15 and i+1>=0 and li2[i+1][j] == 'x' and li2[i+2][j] == 'x' and li2[i+3][j] == 'x' and li2[i+4][j] == 'o':
                    point[i][j] += 400
                    #纵向
                if 0<=i+1 and i+3<15 and 0<=j-3 and j-1<15 and li2[i+3][j-3] == '.' and li2[i+2][j-2] == 'x' and li2[i+1][j-1] == 'x':
                    point[i][j] += 400
                elif 0<=i-3 and i-1<15 and 0<=j+1 and j+3<15 and li2[i-3][j+3] == '.' and li2[i-2][j+2] == 'x' and li2[i-1][j+1] == 'x':
                    point[i][j] += 400
                elif 0<=i+1 and i+4<15 and 0<=j-4 and j-1<15 and li2[i+4][j-4] == 'o' and li2[i+3][j-3] == 'x' and li2[i+2][j-2] == 'x' and li2[i+1][j-1] == 'x':
                    point[i][j] += 400
                elif 0<=i-4 and i-1<15 and 0<=j+1 and j+4<15 and li2[i-1][j+1] == 'x' and li2[i-2][j+2] == 'x' and li2[i-3][j+3] == 'x' and li2[i-4][j+4] == 'o':
                    point[i][j] += 400
                    #右上-》左下
                    #预防棋形
                if 0<=i<15 and j+1<15 and j-3>=0 and li2[i][j-3] == '.' and li2[i][j-2] == 'o' and li2[i][j-1] == 'o' and li2[i][j+1] == 'x':
                    point[i][j] += 200
                elif 0<=i<15 and j+2<15 and j-2>=0 and li2[i][j-2] == '.' and li2[i][j-1] == 'o' and li2[i][j+1] == 'o' and li2[i][j+2] == 'x':
                    point[i][j] += 200
                elif 0<=i<15 and j+3<15 and j-1>=0 and li2[i][j-1] == '.' and li2[i][j+1] == 'o' and li2[i][j+2] == 'o' and li2[i][j+3] == 'x':
                    point[i][j] += 200
                elif 0<=i<15 and j+1<15 and j-3>=0 and li2[i][j-3] == 'x' and li2[i][j-2] == 'o' and li2[i][j-1] == 'o' and li2[i][j+1] == '.':
                    point[i][j] += 200
                elif 0<=i<15 and j+2<15 and j-2>=0 and li2[i][j-2] == 'x' and li2[i][j-1] == 'o' and li2[i][j+1] == 'o' and li2[i][j+2] == '.':
                    point[i][j] += 200
                elif 0<=i<15 and j+3<15 and j-1>=0 and li2[i][j-1] == 'x' and li2[i][j+1] == 'o' and li2[i][j+2] == 'o' and li2[i][j+3] == '.':
                    point[i][j] += 200
                elif 0<=i<15 and j-1<15 and j-3>=0 and li2[i][j-3] == 'o' and li2[i][j-2] == 'x' and li2[i][j-1] == 'x':
                    point[i][j] += 200
                elif 0<=i<15 and j+3<15 and j+1>=0 and li2[i][j+3] == 'o' and li2[i][j+2] == 'x' and li2[i][j+1] == 'x':
                    point[i][j] += 200
                    #横向
                if 0<=i-3 and i+1<15 and 0<=j-3 and j+1<15 and li2[i-3][j-3] == '.' and li2[i-2][j-2] == 'o' and li2[i-1][j-1] == 'o' and li2[i+1][j+1] == 'x':
                    point[i][j] += 200
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i-2][j-2] == '.' and li2[i-1][j-1] == 'o' and li2[i+1][j+1] == 'o' and li2[i+2][j+2] == 'x':
                    point[i][j] += 200
                elif 0<=i-1 and i+3<15 and 0<=j-1 and j+3<15 and li2[i-1][j-1] == '.' and li2[i+1][j+1] == 'o' and li2[i+2][j+2] == 'o' and li2[i+3][j+3] == 'x':
                    point[i][j] += 200
                elif 0<=i-3 and i+1<15 and 0<=j-3 and j+1<15 and li2[i-3][j-3] == 'x' and li2[i-2][j-2] == 'o' and li2[i-1][j-1] == 'o' and li2[i+1][j+1] == '.':
                    point[i][j] += 200
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i-2][j-2] == 'x' and li2[i-1][j-1] == 'o' and li2[i+1][j+1] == 'o' and li2[i+2][j+2] == '.':
                    point[i][j] += 200
                elif 0<=i-1 and i+3<15 and 0<=j-1 and j+3<15 and li2[i-1][j-1] == 'x' and li2[i+1][j+1] == 'o' and li2[i+2][j+2] == 'o' and li2[i+3][j+3] == '.':
                    point[i][j] += 200
                elif 0<=i-3 and i-1<15 and 0<=j-3 and j-1<15 and li2[i-3][j-3] == 'o' and li2[i-2][j-2] == 'x' and li2[i-1][j-1] == 'x':
                    point[i][j] += 200
                elif 0<=i+1 and i+3<15 and 0<=j+1 and j+3<15 and li2[i+3][j+3] == 'o' and li2[i+2][j+2] == 'x' and li2[i+1][j+1] == 'x':
                    point[i][j] += 200
                    #左上-》右下
                if 0<=j<15 and i+1<15 and i-3>=0 and li2[i-3][j] == '.' and li2[i-2][j] == 'o' and li2[i-1][j] == 'o' and li2[i+1][j] == 'x':
                    point[i][j] += 200
                elif 0<=j<15 and i+2<15 and i-2>=0 and li2[i-2][j] == '.' and li2[i-1][j] == 'o' and li2[i+1][j] == 'o' and li2[i+2][j] == 'x':
                    point[i][j] += 200
                elif 0<=j<15 and i+3<15 and i-1>=0 and li2[i-1][j] == '.' and li2[i+1][j] == 'o' and li2[i+2][j] == 'o' and li2[i+3][j] == 'x':
                    point[i][j] += 200
                elif 0<=j<15 and i+1<15 and i-3>=0 and li2[i-3][j] == 'x' and li2[i-2][j] == 'o' and li2[i-1][j] == 'o' and li2[i+1][j] == '.':
                    point[i][j] += 200
                elif 0<=j<15 and i+2<15 and i-2>=0 and li2[i-2][j] == 'x' and li2[i-1][j] == 'o' and li2[i+1][j] == 'o' and li2[i+2][j] == '.':
                    point[i][j] += 200
                elif 0<=j<15 and i+3<15 and i-1>=0 and li2[i-1][j] == 'x' and li2[i+1][j] == 'o' and li2[i+2][j] == 'o' and li2[i+3][j] == '.':
                    point[i][j] += 200
                elif 0<=j<15 and i-1<15 and i-3>=0 and li2[i-3][j] == 'o' and li2[i-2][j] == 'x' and li2[i-1][j] == 'x':
                    point[i][j] += 200
                elif 0<=j<15 and i+3<15 and i+1>=0 and li2[i+3][j] == 'o' and li2[i+2][j] == 'x' and li2[i+1][j] == 'x':
                    point[i][j] += 200
                    #纵向
                if 0<=i-1 and i+3<15 and 0<=j-3 and j+1<15 and li2[i+3][j-3] == '.' and li2[i+2][j-2] == 'o' and li2[i+1][j-1] == 'o' and li2[i-1][j+1] == 'x':
                    point[i][j] += 200
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i+2][j-2] == '.' and li2[i+1][j-1] == 'o' and li2[i-1][j+1] == 'o' and li2[i-2][j+2] == 'x':
                    point[i][j] += 200
                elif 0<=i-3 and i+1<15 and 0<=j-1 and j+3<15 and li2[i+1][j-1] == '.' and li2[i-1][j+1] == 'o' and li2[i-2][j+2] == 'o' and li2[i-3][j+3] == 'x':
                    point[i][j] += 200
                elif 0<=i-1 and i+3<15 and 0<=j-3 and j+1<15 and li2[i+3][j-3] == 'x' and li2[i+2][j-2] == 'o' and li2[i+1][j-1] == 'o' and li2[i-1][j+1] == '.':
                    point[i][j] += 200
                elif 0<=i-2 and i+2<15 and 0<=j-2 and j+2<15 and li2[i+2][j-2] == 'x' and li2[i+1][j-1] == 'o' and li2[i-1][j+1] == 'o' and li2[i-2][j+2] == '.':
                    point[i][j] += 200
                elif 0<=i-3 and i+1<15 and 0<=j-1 and j+3<15 and li2[i+1][j-1] == 'x' and li2[i-1][j+1] == 'o' and li2[i-2][j+2] == 'o' and li2[i-3][j+3] == '.':
                    point[i][j] += 200
                elif 0<=i+1 and i+3<15 and 0<=j-3 and j-1<15 and li2[i+3][j-3] == 'o' and li2[i+2][j-2] == 'x' and li2[i+1][j-1] == 'x':
                    point[i][j] += 200
                elif 0<=i-3 and i-1<15 and 0<=j+1 and j+3<15 and li2[i-3][j+3] == 'o' and li2[i-2][j+2] == 'x' and li2[i-1][j+1] == 'x':
                    point[i][j] += 200
                    #右上—》左下
                    #无效进攻防守
                if 0<=i<15 and j+1<15 and j-2>=0 and li2[i][j-2] == '.' and li2[i][j-1] == 'o' and li2[i][j+1] == '.':
                    point[i][j] += 50
                elif 0<=i<15 and j+2<15 and j-1>=0 and li2[i][j-1] == '.' and li2[i][j+1] == 'o' and li2[i][j+2] == '.':
                    point[i][j] += 50
                    #横向
                if 0<=i-2 and i+1<15 and 0<=j-2 and j+1<15 and li2[i-2][j-2] == '.' and li2[i-1][j-1] == 'o' and li2[i+1][j+1] == '.':
                    point[i][j] += 50
                elif 0<=i-1 and i+2<15 and 0<=j-1 and j+2<15 and li2[i-1][j-1] == '.' and li2[i+1][j+1] == 'o' and li2[i+2][j+2] == '.':
                    point[i][j] += 50
                    #左上-》右下
                if 0<=j<15 and i+1<15 and i-2>=0 and li2[i-2][j] == '.' and li2[i-1][j] == 'o' and li2[i+1][j] == '.':
                    point[i][j] += 50
                elif 0<=j<15 and i+2<15 and i-1>=0 and li2[i-1][j] == '.' and li2[i+1][j] == 'o' and li2[i+2][j] == '.':
                    point[i][j] += 50
                    #纵向
                if 0<=i-2 and i+1<15 and 0<=j-1 and j+2<15 and li2[i-2][j+2] == '.' and li2[i-1][j+1] == 'o' and li2[i+1][j-1] == '.':
                    point[i][j] += 50
                elif 0<=i-1 and i+2<15 and 0<=j-2 and j+1<15 and li2[i-1][j+1] == '.' and li2[i+1][j-1] == 'o' and li2[i+2][j-2] == '.':
                    point[i][j] += 50
                    #右上左下
                    #布局棋形
            point[i][j] += 20
            if point[i][j] > max_p:
                max_p = point[i][j]
                max_x = i
                max_y = j
            li2[i][j]='.'
print(count2%2)
print(max_p)
print(chr(max_x+97))
print(chr(max_y+97))
for i in range(15):
    for j in range(15):
        print(point[i][j],end='')
        print(' ',end='')
    print('\n')


