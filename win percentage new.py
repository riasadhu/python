# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 12:40:47 2019

@author: Dell
"""
import pandas as pd
import os
os.chdir("D:\\Ria\\from Dell Old laptop - Ria - 20Jan2019\\totality\\ANACONDA OUTPUT")
# FIND MATCH WIN PERCENTAGE OF ALL USERS 
trans18to26=pd.read_csv("file:///D:/Ria/from Dell Old laptop - Ria - 20Jan2019/totality/Fraud Detection/transcations/trans15feb.csv")


#filter INR Matches
Transmatchinr=trans18to26[(trans18to26['transactions.category']=='MATCH')&(trans18to26['transactions.currency']=='INR')]
Transmatchinr['onlydate']=Transmatchinr['date'].str.split(' ').str[0]
#debit transactions
allinrdebittransactions=Transmatchinr[Transmatchinr['transactions.type']=='DR']
#credit transactions
allinrcredittransactions=Transmatchinr[Transmatchinr['transactions.type']=='CR']
#user wise debit transactions of all games
debitsbyuser=allinrdebittransactions.groupby(['transactions.userId','transactions.gameId'])[['transactions.type']].count()
#user wise credit transactions of all games
creditsbyuser=allinrcredittransactions.groupby(['transactions.userId','transactions.gameId'])[['transactions.type']].count()
debitsbyuser=debitsbyuser.reset_index()
creditsbyuser=creditsbyuser.reset_index()
#merge on the basis of column columns userId,gameId
debitsandcredits=pd.merge(debitsbyuser,creditsbyuser,on=['transactions.userId','transactions.gameId'])
#rename the columns
debitsandcredits.columns=['transactions.userId','gameId','debits','wins']
#calculate win percentage no of wins/no of matches played
debitsandcredits['winperc']=debitsandcredits['wins']/debitsandcredits['debits']
#if incase wins>no of matches played then wins=no of debits
debitsandcredits.loc[debitsandcredits[debitsandcredits['winperc']>1].index,'wins']=debitsandcredits.loc[debitsandcredits[debitsandcredits['winperc']>1].index,'debits']
#take those where matches played by users are greater than or equal to 4
debitsandcredits=debitsandcredits[(debitsandcredits['debits']>=4)]
#extract the maximum win percentage for all games played
gameidwithmaxwinperc=debitsandcredits.groupby(['transactions.userId'])['winperc'].max()
gameidwithmaxwinperc=gameidwithmaxwinperc.reset_index()
#we will get the gameId corresponding maximum win percentage
winpercentage=pd.merge(debitsandcredits,gameidwithmaxwinperc,on=['transactions.userId','winperc'])
#needed those users who have played more than 4 and also their win percentage should be greater than 55%
required=winpercentage[(winpercentage['debits']>=4)&(winpercentage['winperc']>=0.55)]


# LMS WIN PERCENTAGE
#filter LMS Matches
Transmatchlms=trans18to26[(trans18to26['transactions.category']=='LMS')&(trans18to26['transactions.currency']=='INR')]
Transmatchlms['onlydate']=Transmatchlms['date'].str.split(' ').str[0]
#debit transactions
allinrdebittransactions=Transmatchlms[Transmatchlms['transactions.type']=='DR']
#credit transactions
allinrcredittransactions=Transmatchlms[Transmatchlms['transactions.type']=='CR']
#user wise debit transactions of all games
credits=allinrcredittransactions.groupby(['transactions.userId','transactions.gameId'])[['transactions.type']].count()
#user wise credit transactions of all games
debits=allinrdebittransactions.groupby(['transactions.userId','transactions.gameId'])[['transactions.type']].count()
credits=credits.reset_index()
debits=debits.reset_index()
lmsdebitsandcredits=pd.merge(debits,credits,on=['transactions.userId','transactions.gameId'])
#merge on the basis of column columns userId,gameId
lmsdebitsandcredits.columns=['transactions.userId', 'transactions.gameId', 'debits','credits']
#calculate win percentage no of wins/no of matches played
lmsdebitsandcredits['win%']=lmsdebitsandcredits['credits']/lmsdebitsandcredits['debits']
#if incase wins>no of matches played then wins=no of debits
lmsdebitsandcredits.loc[lmsdebitsandcredits[lmsdebitsandcredits['win%']>1].index,'credits']=lmsdebitsandcredits.loc[lmsdebitsandcredits[lmsdebitsandcredits['win%']>1].index,'debits']
#take those where matches played by users are greater than or equal to 4
lmsdebitsandcredits=lmsdebitsandcredits[(lmsdebitsandcredits['debits']>=4)]
#extract the maximum win percentage for all games played
gameidwithmaxwinperclms=lmsdebitsandcredits.groupby(['transactions.userId'])['win%'].max()
#we will get the gameId corresponding maximum win percentage
gameidwithmaxwinperclms=gameidwithmaxwinperclms.reset_index()
#we will get the gameId corresponding maximum win percentage
winpercentagelms=pd.merge(lmsdebitsandcredits,gameidwithmaxwinperclms,on=['transactions.userId','win%'])
#needed those users who have played more than 4 and also their win percentage should be greater than 55%
requiredlms=winpercentagelms[(winpercentagelms['debits']>=4)&(winpercentagelms['win%']>=0.55)]
requiredlms.columns=required.columns
#concatenate the users having win% >55% in Inr matches and the users having win% >55% in lms matches
checklist=pd.concat([required,requiredlms],ignore_index=False)
#extract maximum win percentage from both INR AND LMS matches
gameidwithmaxwinpercchecklist=checklist.groupby(['transactions.userId'])['winperc'].max()
gameidwithmaxwinpercchecklist=gameidwithmaxwinpercchecklist.reset_index()
#we will get the gameId corresponding maximum win percentage
winpercentage1=pd.merge(checklist,gameidwithmaxwinpercchecklist,on=['transactions.userId','winperc'])
#Extract incase the user has same maximum win percentage in more than one game
t=winpercentage1.groupby(['transactions.userId'])[['transactions.userId']].count()
count2=t[t['transactions.userId']>=2]
#Having the data of user with same maximum win percentage in more than one game 
users_2=winpercentage1[(winpercentage1['transactions.userId'].isin(count2.index))]
#Game Ids wise no of users having win percentage more than 55% and matches played more than 4
top10gameids=winpercentage1['gameId'].value_counts()
# Create a Pandas Excel writer using XlsxWriter as the engine.
from datetime import *
date=str(datetime.date(datetime.today()))
date="successrate"+date
writer = pd.ExcelWriter(date+'.xlsx', engine='xlsxwriter')

# Write each dataframe to a different worksheet.
users_2.to_excel(writer, sheet_name='2gameidswithsamewin%')
winpercentage1.to_excel(writer, sheet_name='successrate')
top10gameids.to_excel(writer, sheet_name='gameidscountwithusers')
writer.save()








