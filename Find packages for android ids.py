# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 12:18:18 2019

@author: Dell
"""
import os
import pandas as pd
path='C:\\Users\\riasa\\Downloads\\packages\\packages'
Android_Id_list=[]
date_list=[]
filename_packages=[]
data_error_dict = {}
index = 0
# Iterate file name ends with txt extension
for filename in os.listdir(path):
    if filename.endswith('.txt'):
        try:
            file=pd.read_csv('C:\\Users\\riasa\\Downloads\\packages\\packages\\'+filename,header=None)
            
        except Exception as e:
            #print('Note: filename.csv was empty. Skipping.')
            if str(e) not in data_error_dict:
                data_error_dict[str(e)]=0
            data_error_dict[str(e)] +=1
            continue
        
         
        
        # Extracting Android id From filename and assigning to a list 
        Android_Id_list.append(filename.split("_")[1])
        # Extracting Date From filename and assigning to a list 
        date_list.append(filename.split("_")[2].split('.')[0])
        #reading content of filename and assining to a dataFrame
         # file=pd.read_csv('C:\\Users\\riasa\\Downloads\\packages\\packages\\'+filename,header=None)
        
        #Transposing columns to rows
        file_transpose=file.T
        
        packages=file_transpose.apply(lambda x:x.str.split('|').str[0])
        #creating a new column Android id of the dataFrame packages and assigning Android Id of the filename 
        packages['Android Id']=Android_Id_list[index]
        #creating a new column date and assigning Date of the filename 
        packages['date']=date_list[index]
        # Append DataFrame packages to list
        filename_packages.append(packages)
        index+=1
        
        
   
# Concatenate all the lists appended in the filename_packages and assigning to DataFrame         
packages=pd.concat(filename_packages,axis = 0, ignore_index = True) 
packages=packages.drop(columns=[1,2,3])
# changing columns of the DataFrame (3 columns)
packages.columns=['packages','Android Id','date']
# Groupby DataFrame by Android Id on the data column and count the number of times date has appeared
date_count=packages.groupby(['Android Id'])[['date']].nunique()
date_count=date_count.reindex()
#changing the column name
date_count.columns=['count of dates appearing ']
# Filtering Android ids which appeared more than two times and assigning to numpy array
Androididscountofdatemorethantwo=date_count[date_count['count of dates appearing ']>=2].index
#creating a list
packagesremovingduplicates=[]
for i in range(len(Androididscountofdatemorethantwo)):
    # Taking values from the numpy array one by one
    #Extracting subset of a dataframe which contain the specified Android Id 
    Taking_those_files_having_repeated=packages[packages['Android Id']==Androididscountofdatemorethantwo[i]]
    
    sortbydate=Taking_those_files_having_repeated.sort_values(by='date')
    # Taking recent files by sorting them by date column
    recentfiles=Taking_those_files_having_repeated[Taking_those_files_having_repeated['date']==sortbydate['date'].unique()[-1]]
    #Droping duplicates in packages column and appending to a list
    packagesremovingduplicates.append(recentfiles['packages'].drop_duplicates(keep='first'))
# Concatenate all the lists appended in the packagesremovingduplicates  and assigning to DataFrame
recentfiles_having_Androidids_repeated=pd.concat(packagesremovingduplicates,ignore_index=True)

# Filtering Android ids which appeared one and assigning to numpy array
Androididscountofdateone=date_count[date_count['count of dates appearing ']==1].index
#creating a list
packagesremovingduplicates1=[]


for i in range(len(Androididscountofdateone)):
    # Taking values from the numpy array one by one
    #Extracting subset of a dataframe which contain the specified Android Id 
    recentfiles_havingappearedonce=packages[packages['Android Id']==Androididscountofdateone[i]]
    packagesremovingduplicates1.append(recentfiles_havingappearedonce['packages'].drop_duplicates(keep='first'))
# Concatenate all the lists appended in the packagesremovingduplicates  and assigning to DataFrame
recentfiles_having_Androidids_appeared_once=pd.concat(packagesremovingduplicates1,ignore_index=True)

# All files having the latest file if repeated and also those files appeared once Assigned to a dataFrame packagesusedbyandroidusers
packagesusedbyandroidusers=pd.concat([recentfiles_having_Androidids_repeated,recentfiles_having_Androidids_appeared_once],ignore_index=True)
# Creating a new column packages which has all the packages
packagesusedbyandroidusers.columns=['packages']
# Counting no of times each packages has appeared
countofpackages=packagesusedbyandroidusers.value_counts()
from datetime import datetime

date='Total packages_' + str(datetime.now()).split(' ')[0]+'.xlsx'
#Excel file
writer = pd.ExcelWriter(date,engine='xlsxwriter')
# No of Unique Android ids to be exported to excel file
uniqueandroidusers=pd.DataFrame([{'unique Android ids':len(date_count.index)}])  

uniqueandroidusers.to_excel(writer,startrow=1,startcol=0)
# count of packages to be exported to excel file
countofpackages.to_excel(writer,startrow=4,startcol=0)
writer.save()
print(data_error_dict )
            