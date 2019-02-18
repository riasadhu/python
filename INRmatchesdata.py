# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 17:32:21 2019

@author: Dell
"""
A=pd.read_csv("file:///D:/Ria/from Dell Old laptop - Ria - 20Jan2019/totality/Fraud Detection/transcations/trans6feb.csv")
B=pd.read_csv("file:///D:/Ria/from Dell Old laptop - Ria - 20Jan2019/totality/Fraud Detection/transcations/trans5feb.csv")
C=pd.read_csv("file:///D:/Ria/from Dell Old laptop - Ria - 20Jan2019/totality/Fraud Detection/transcations/trans4feb.csv")
D=pd.read_csv("file:///D:/Ria/from Dell Old laptop - Ria - 20Jan2019/totality/Fraud Detection/transcations/trans1feb.csv")
E=pd.read_csv("file:///D:/Ria/from Dell Old laptop - Ria - 20Jan2019/totality/Fraud Detection/transcations/trans2_3feb.csv")
F=pd.read_csv("file:///D:/Ria/from Dell Old laptop - Ria - 20Jan2019/totality/Fraud Detection/transcations/trans8feb.csv")
G=pd.read_csv("file:///D:/Ria/from Dell Old laptop - Ria - 20Jan2019/totality/Fraud Detection/transcations/trans7feb.csv")
H=pd.read_csv("file:///D:/Ria/from Dell Old laptop - Ria - 20Jan2019/totality/Fraud Detection/transcations/trans9_10feb.csv")
I=pd.read_csv("file:///D:/Ria/from Dell Old laptop - Ria - 20Jan2019/totality/Fraud Detection/transcations/trans11feb.csv")
J=pd.read_csv("file:///D:/Ria/from Dell Old laptop - Ria - 20Jan2019/totality/Fraud Detection/transcations/trans12feb.csv")
K=pd.read_csv("file:///D:/Ria/from Dell Old laptop - Ria - 20Jan2019/totality/Fraud Detection/transcations/trans13feb.csv")
L=pd.read_csv("file:///D:/Ria/from Dell Old laptop - Ria - 20Jan2019/totality/Fraud Detection/transcations/trans15feb.csv")
M=pd.read_csv("file:///D:/Ria/from Dell Old laptop - Ria - 20Jan2019/totality/Fraud Detection/transcations/trans16_17feb.csv")
trans11to2nddec1=pd.concat([L,M])
trans11to2nddec1['onlydate']=trans11to2nddec1['date'].str.split(' ').str[0]

trans11to2nddec1['onlydate']=trans11to2nddec1['date'].str.split(' ').str[0]
trans11to2nddec1['onlydate']=trans11to2nddec1['onlydate'].str.replace('/','-')
trans11to2nddec1['onlydate']=trans11to2nddec1['onlydate'].replace(['03-02-2019','03-05-2019','03-06-2019','03-07-2019','03-08-2019','03-09-2019','03-10-2019','03-11-2019','03-12-2019'],['02-02-2019','02-05-2019','02-06-2019','02-07-2019','02-08-2019','02-09-2019','02-10-2019','02-11-2019','02-12-2019'])
trans11to2nddec1['onlydate']=pd.to_datetime(trans11to2nddec1['onlydate'],format='%m-%d-%Y')
#find no of SIGNUPS
Signups=trans11to2nddec1[trans11to2nddec1['transactions.category']=='SIGNUP']
signupsdatewise=Signups.groupby('onlydate')['transactions.userId'].nunique()
# filter INRMATCH
matchinr=trans11to2nddec1[(trans11to2nddec1['transactions.currency']=='INR')&(trans11to2nddec1['transactions.category']=='MATCH')]
matchinrdebittransactions=matchinr[matchinr['transactions.type']=='DR']
#find no of UNIQUEUSERS playing INR matches
matchinrtotaluniqueusers=matchinrdebittransactions['transactions.userId'].nunique()
#NO OF MATCHES PLAYED GROUPED BY GAMEID,DATE
noofmatches1v1uniquematchids1=matchinrdebittransactions.groupby(['transactions.gameId','onlydate'])[['transactions.orderId']].nunique()
#NO OF MATCHES PLAYED GROUPED BY GAMEID
noofmatches1v1uniquematchids=matchinrdebittransactions.groupby(['transactions.gameId'])[['transactions.orderId']].nunique()
noofmatches1v1uniquematchids['% of Matches played']=(noofmatches1v1uniquematchids['transactions.orderId']/matchinrdebittransactions[['transactions.orderId']].nunique().iloc[0])*100
noofmatches1v1uniquematchids=noofmatches1v1uniquematchids.sort_values(by='transactions.orderId',ascending=False)
noofmatches1v1uniquematchids.columns=['INR Matches played','% of Matches played']
#No of debit transactions grouped by gameId,userId
matchesplayedbyuserspergameId=matchinrdebittransactions.groupby(['transactions.gameId','transactions.userId'])[['transactions.type']].count()
matchesplayedbyuserspergameId=matchesplayedbyuserspergameId.reset_index()
#five point summary of matches played by users for each gameId
matchesplayedbyuserspergameId=matchesplayedbyuserspergameId.groupby(['transactions.gameId'])[['transactions.type']].describe()
# Float values to integer values
matchesplayedbyuserspergameId=matchesplayedbyuserspergameId.round()
#Drop multi level columns
matchesplayedbyuserspergameId.columns=matchesplayedbyuserspergameId.columns.droplevel()
#Dropping some columns 
matchesplayedbyuserspergameId.drop(columns=['count','25%','50%','75%'],inplace=True)
#Renaming columns
matchesplayedbyuserspergameId.columns=['Average no of matches played by users','variablity in no of matches played by users','minimum no of matches played','maximum no of matches played']
#Extraction of top 10+ users for each gameId
userswhosedebittransactionsgreaterthan10=matchinrdebittransactions.groupby(['transactions.userId','transactions.gameId'])[['transactions.type']].count()
userswhosedebittransactionsgreaterthan10=userswhosedebittransactionsgreaterthan10[userswhosedebittransactionsgreaterthan10['transactions.type']>=10]
userswhosedebittransactionsgreaterthan10=userswhosedebittransactionsgreaterthan10.reset_index()
Total10_users=userswhosedebittransactionsgreaterthan10['transactions.gameId'].value_counts()
Total10_users=pd.DataFrame(Total10_users)
Total10_users.columns=['Total 10+ users']
#Unique users for each gameId
uniqueusersingameIds=matchinrdebittransactions.groupby('transactions.gameId')[['transactions.userId']].nunique()
uniqueusersingameIds.columns=['unique users']
# users who played once,played twice,played 3-5,played>5
users_gameid_debittransactions=matchinrdebittransactions.groupby(['transactions.userId','transactions.gameId'])[['transactions.orderId']].count()
users_gameid_debittransactions=users_gameid_debittransactions.reset_index()

playedonce=[]
playedtwice=[]
playedtwoto5=[]
playedmorethan5=[]
import numpy as np
for i in np.array([1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,18,19,20,22,23,27,28]):
    
    
    playedonce.append(users_gameid_debittransactions[(users_gameid_debittransactions['transactions.gameId']==i)&(users_gameid_debittransactions['transactions.orderId']==1)]['transactions.userId'].nunique())
    playedtwice.append(users_gameid_debittransactions[(users_gameid_debittransactions['transactions.gameId']==i)&(users_gameid_debittransactions['transactions.orderId']==2)]['transactions.userId'].nunique())
    playedtwoto5.append(users_gameid_debittransactions[(users_gameid_debittransactions['transactions.gameId']==i)&(users_gameid_debittransactions['transactions.orderId']>2)&(users_gameid_debittransactions['transactions.orderId']<=5)]['transactions.userId'].nunique())
    playedmorethan5.append(users_gameid_debittransactions[(users_gameid_debittransactions['transactions.gameId']==i)&(users_gameid_debittransactions['transactions.orderId']>5)]['transactions.userId'].nunique())
k=pd.DataFrame({'gameId':np.array([1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,18,19,20,22,23,27,28]),'usersplayedonce':playedonce,'usersplayedtwice':playedtwice,'usersplayedthriceto5':playedtwoto5,'usersplayedmorethan5':playedmorethan5})
#Matches played grouped by Amount,GameId
matchinrdebittransactions1=matchinrdebittransactions.groupby(['transactions.gameId','transactions.amount'])[['transactions.orderId']].nunique()
matchinrdebittransactions1.columns=['INR Matches played']
#Unique users grouped by Amount,GameId
userinrdebittransactions=matchinrdebittransactions.groupby(['transactions.gameId','transactions.amount'])[['transactions.userId']].nunique()
userinrdebittransactions.columns=['unique users']
uniqueusers=pd.DataFrame([{'uniqueusers':matchinrtotaluniqueusers}])

#Export to excel
file="D://Ria//from Dell Old laptop - Ria - 20Jan2019//totality//Fraud Detection//transcations//12_13FEB"
date=[]
dateorder=[]
dateorder1=[]
dateorder2=[]
for filename in os.listdir(file):
   date.append(filename.split('.')[0][5:])
dateorder=[date[:4] for date in date]
dateorder1=[date.split('fe')[0] for date in dateorder]
dateorder2=[date.split('_')[0] for date in dateorder1]
dateorder2=[int(date) for date in dateorder2]
dateorder2.sort()
from datetime import datetime
month=datetime.now().strftime('%B')
date1='{}_{}_{}'.format(dateorder2[0],dateorder2[-1],month)
date1="15to17feb"
writer = pd.ExcelWriter('INRMatches{}.xlsx'.format(date1),engine='xlsxwriter')  
#filter LMS matches
matchlms=trans11to2nddec1[(trans11to2nddec1['transactions.currency']=='INR')&(trans11to2nddec1['transactions.category']=='LMS')]
matchinrdebittransactionslms=matchlms[matchlms['transactions.type']=='DR']
# No of lms matches
lms=matchinrdebittransactionslms.groupby('transactions.gameId')[['transactions.orderId']].nunique()
lms['LMS Matches played']=(lms['transactions.orderId']/3).round()
lms=lms.sort_values(by='transactions.orderId',ascending=False)
lmsuniqueusers=matchinrdebittransactionslms.groupby('transactions.gameId')[['transactions.userId']].nunique()
lmsuniqueusers.columns=['unique users']
#no of lms matches grouped by GameId,Amount
lmsamountwise=matchinrdebittransactionslms.groupby(['transactions.gameId','transactions.amount'])[['transactions.orderId']].nunique()
lmsamountwise['LMS Matches played']=(lmsamountwise['transactions.orderId']/3).round()
uniqueusers.to_excel(writer,sheet_name='INR 1V1',startrow=0,startcol=0)
signupsdatewise.to_excel(writer,sheet_name='INR 1V1',startrow=3,startcol=0)
noofmatches1v1uniquematchids1.to_excel(writer,sheet_name='datewise_matches_gameIdwise',startrow=0, startcol=0) 
noofmatches1v1uniquematchids.to_excel(writer,sheet_name='INR 1V1',startrow=12, startcol=0) 
Total10_users.to_excel(writer,sheet_name='INR 1V1',startrow=36,startcol=0) 
matchesplayedbyuserspergameId.to_excel(writer,sheet_name='INR 1V1',startrow=59,startcol=0)
uniqueusersingameIds.to_excel(writer,sheet_name='INR 1V1',startrow=84,startcol=0) 
k.to_excel(writer,startrow=110, sheet_name='INR 1V1',startcol=0,index=False) 
matchinrdebittransactions1.to_excel(writer,startrow=134, startcol=0,sheet_name='INR 1V1')
matchinrdebittransactions1=matchinrdebittransactions1.reset_index()
noofmatches1v1uniquematchids['transactions.gameId']=noofmatches1v1uniquematchids.index
merge1=pd.merge(matchinrdebittransactions1,noofmatches1v1uniquematchids,on='transactions.gameId')
merge1.drop(columns='% of Matches played',inplace=True)
required=merge1[merge1['transactions.amount']>=3]
required.columns=['transactions.gameId', 'transactions.amount','Matchesplayed', 'Total Matches played']
required['% of Matches played of 3 and above fees']=required['Matchesplayed']/required['Total Matches played']
required1=required.groupby('transactions.gameId')[['% of Matches played of 3 and above fees']].sum()
r=required1.sort_values(by='% of Matches played of 3 and above fees',ascending=False) 
r.to_excel(writer,sheet_name='INR 1V1', startrow=270,startcol=0) 
userinrdebittransactions.to_excel(writer,startrow=295 ,sheet_name='INR 1V1', startcol=0)
lms.to_excel(writer,startrow=0 ,sheet_name='LMS', startcol=0)
lmsuniqueusers.to_excel(writer,startrow=25 ,sheet_name='LMS', startcol=0)
lmsamountwise.to_excel(writer,startrow=50 ,sheet_name='LMS', startcol=0)
writer.save()

