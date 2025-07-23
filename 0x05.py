# http://202.207.12.156:9012/context/eb63fffd85c01a0a5d8f3cadea18cf56
import requests
import re

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


if __name__=='__main__':
    base='http://202.207.12.156:9012/step_05?user=0191121339&password='
    sslNum=str2num('Wge7sPRKu5sQvR7')

    encrySSL=encryNum(sslNum)
    targetRegex = requests.get(base+str(hex(int(str(encrySSL))))).text
    regex = '"message": "(.*?)"'
    data = re.findall(regex,str(targetRegex))[0]
    dataNum = int(data, 16)
    temp=encryNum(dataNum) # then we will split it to 256 scale

    print(data)

    ans=[]

    while temp != 0:
        ans.append(chr(temp%256))
        temp //= 256 # floor, math.floor is wrong... use gex() to verify

    for i in range(len(ans)):
        print(ans[-i], end='')
