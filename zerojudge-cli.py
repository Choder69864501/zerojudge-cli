#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import colorTable as cT
import getpass
import webbrowser
headers={}
headers['User-Agent']="Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
loginurl='https://zerojudge.tw/Login'
logouturl='https://zerojudge.tw/Logout'
Userurl='https://zerojudge.tw/UserStatistic'
resurl='https://zerojudge.tw/Submissions'
qurl='https://zerojudge.tw/ShowProblem?problemid='
user={'token':''}
purl='https://zerojudge.tw/Solution.api?action=SubmitCode&'
session=requests.session()
def Login():
    account=input('account: ')
    pswd=getpass.getpass('password: ')
    user['account']=account
    user['passwd']=pswd
    session.post(loginurl,user,headers=headers)
    if dashBoard(1, 0)==1:
        return 1
    return 0
def submitCode():
    data={}
    problem=input('Problem: ')
    lang=input('language(Default is CPP): ')
    if lang=='':
        lang='CPP'
    data['language']=lang
    filename=input('Code file name without extension: ')
    codes=[]
    try:
        data['code']=open(filename+'.'+lang.lower(),"r").read()
    except (OSError,IOError) as e:
        print(cT.bcolors.BOLD+cT.bcolors.FAIL+'File not found !'+cT.bcolors.ENDC)
    data['problemid']=problem
    data['contestid']=0
    session.post(purl,data=data,headers=headers)
def Help():
    print('Type d or dashboard to see the dashboard')
    print('Type \'d [1, 20]\' to show specific numbers of submissions(default:5). ex: d 10') 
    print('Type s or submit to submit code')
    print('Type h for help')
    print('Type sp or showproblem to show the specific problem')
    print('Type quit or exit to logout and quit')
def cmpString(first, second):
    if first == second:
        return 1
    if len(second) >= 15:
        cnt = 0
        for i in first:
            if cnt == 14:
                return 1
            if i != second[cnt]:
                return 0;
            cnt += 1
def dashBoard(flag, times):
    soup=BeautifulSoup(session.get(resurl,headers=headers).text,"lxml")
    if len(soup.find_all('tr',attrs={'solutionid':True}))==0:
        return 1
    if flag:
        return 0
    cnt=0
    for i in soup.find_all('tr',attrs={'solutionid':True}):
        if cnt == times:
            break
        if cnt >= 9:
            out = 16
        else:
            out = 17
        print(cT.bcolors.BOLD+cT.bcolors.FAIL+'-'*out+cT.bcolors.CYAN+str(cnt + 1)+cT.bcolors.BOLD+cT.bcolors.FAIL+'-'*16+cT.bcolors.ENDC)
        solveId=i.find('td',id='solutionid').text
        userId=[]
        userId.append(i.find('a',attrs={'title':True}).text)
        userId.append(i.find('span',attrs={'title':True}).text.rstrip())
        pr=[]
        p=i.find_all('a',attrs={'title':True})[1]
        pr.append(p.get('href').split('=')[1])
        pr.append(p.text)
        resp=[]
        resp.append(i.find('span',id='judgement',attrs={'data-solutionid':solveId}).text)
        resp.append(i.find_all('span',id='summary')[1].text)
        #if userId[0]==user['account']:
        if cmpString(userId[0], user['account']):
            print(cT.bcolors.UNDERLINE+cT.bcolors.OKGREEN, end='')
            print(solveId,userId[0],userId[1])
            print(pr[0],pr[1],cT.bcolors.ENDC, end='')
        else:
            print(solveId,userId[0], userId[1])
            print(pr[0],pr[1], end='')
        print(cT.bcolors.BOLD)
        str1=''.join(list(filter(str.isalnum,resp[0])))
        if str1=='AC':
            print(cT.bcolors.OKGREEN+str1, end='')
        elif str1=='TLE':
            print(cT.bcolors.OKBLUE+str1, end='')
        elif str1=='WA':
            print(cT.bcolors.FAIL+str1, end='')
        else:
            print(cT.bcolors.WARNING+str1, end='')
        print(cT.bcolors.ENDC,resp[1])
        print()
        cnt += 1
    return 0
def showProblem(prob):
    response=requests.get(qurl+prob)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('Error: '+str(e))
        print(cT.bcolors.BOLD+cT.bcolors.FAIL+'wrong problem number'+cT.bcolors.ENDC)
        return 1
    webbrowser.open_new_tab(qurl+prob)
    return 0

while Login()==1:
    print(cT.bcolors.BOLD+cT.bcolors.FAIL+'Login failed ,try again'+cT.bcolors.ENDC)

while True:
    while 1:
        c=input(cT.bcolors.OKBLUE+cT.bcolors.BOLD+'>> '+cT.bcolors.ENDC)
        if c:
            break
    if c=='h':
        Help()
    elif c=='submit' or c=='s':
        submitCode()
    elif c=='dashboard' or c[0]=='d':
        tmp = 0
        cnt = 5
        x = c.split(' ')
        for i in x:
            tmp += 1
            if tmp == 2:
                cnt = i
            elif tmp > 2:
                break
        if tmp > 2 or (x[0] != 'dashboard' and x[0] != 'd'):
            print('Unknown conform_login , type h for help')
        else:
            dashBoard(None, int(cnt))
    elif c=='showproblem' or c=='sp':
        showProblem(input('Problem: '))
    elif c=='quit' or c=='exit' or c=='q': 
        break 
    else:
        print('Unknown conform_login , type h for help')
        continue
session.get(logouturl,headers=headers)
