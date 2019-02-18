# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 16:43:17 2019

@author: Dell
"""

a=['word test','word 2 rest ','words','word word']
count=0
for i in a:
    for j in i.split():
        if (j == 'word')|(j == 'test'):
            count+=1
           
    