# http://202.207.12.156:9012/context/f64710b4861e6ff10678036548bf7afa
import requests
import re
import json

def modular_pow(a,k,n):
    # 1. c = (c*b) % m
    # mod to every result is not well in too many k(loop)
    # use the dichotomy by `k//=2`
    if n==1:
        return 0
    ans=1
    while(k!=0):
        if k%2==1: # make sure following // is correct
            ans=ans*a%n
        a=a*a%n
        k//=2
    return ans

if __name__=='__main__':
    _ansList=[]
    base="http://202.207.12.156:9012/step_04?ans="
    respond=requests.get('http://202.207.12.156:9012/step_04')
    data = (json.loads(respond.text))['questions']
    data = data[1:len(data)-1]

    dataList = re.findall('\[(\d+), (\d+), (\d+)\]',data)

    temp=""
    for i in range(len(dataList)):
        temp += str(modular_pow(int(dataList[i][0]), int(dataList[i][1]), int(dataList[i][2])))
        temp +=','
    temp=temp[0:len(temp)-1]
    requestUrl=base+temp

    respond=requests.get(requestUrl)
    print(respond.text)