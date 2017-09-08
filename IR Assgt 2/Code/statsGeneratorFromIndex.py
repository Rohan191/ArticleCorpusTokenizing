#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 18:58:47 2017

@author
Rohan Tondulkar (CS17MTECH11028), Uddipta Bhattacharjee (CS17MTECH11026), Manisha Dubey (CS17RESCH11003)
"""

#This file has code required for Section 2

import os
import constants as config
import csv
import ast

def generateStatsForMaximumKFrequencies( invertedIndex, k):
    """Section 2.1) To get statistics for Most K frequent terms"""
    print('Printing stats for most frequent {0} words'.format(k))
    print('----------------------------------------------------------------')
    tempList = sorted( invertedIndex, key=lambda element: element[1], reverse = True )
    count=0
    for token, freq in tempList:
        #print('Token:{0} Freq:{1}'.format(token, freq))
        count+=1
        print('For K = {0}'.format(count))
        postingList = sorted(invertedIndex[(token, freq)]) 
        print('Postings list size:{0}'.format(len(postingList)))
        sum = 0
        for id in range( len(postingList)-1 ):
            sum = sum + int(postingList[id+1]) - int(postingList[id])
        #print('Total gap: {0}'.format(sum))
        print('Average Gap Size in the Postings List: {0}'.format( sum/(len(postingList)-1)))
        print('-----------------------------')
        if count == k:
            break
    print('----------------------------------------------------------------')
        
def generateStatsForMinimumKFrequencies( invertedIndex, k):
    """Section 2.3) To get statistics for Least K frequent terms"""
    print('Printing stats for least frequent {0} words'.format(k))
    print('----------------------------------------------------------------')
    tempList = sorted( invertedIndex, key=lambda element: element[1] )
    count=0
    for token, freq in tempList:
        #print('Token:{0} Freq:{1}'.format(token, freq))
        count+=1
        print('For K = {0}'.format(count))
        postingList = sorted(invertedIndex[(token, freq)]) 
        print('Postings list size:{0}'.format(len(postingList)))
        sum = 0
        for id in range( len(postingList)-1 ):
            sum = sum + int(postingList[id+1]) - int(postingList[id])
        #print('Total gap: {0}'.format(sum))
        print('Average Gap Size in the Postings List: {0}'.format( sum/(len(postingList)-1)))
        print('-----------------------------')
        if count == k:
            break
    print('----------------------------------------------------------------')
        
def generateStatsForMedianKFrequencies( invertedIndex, k):
    """Section 2.2) To get statistics for Median K frequent terms"""
    print('Printing stats for Median frequent {0} words'.format(k))
    print('----------------------------------------------------------------')
    tempList = sorted( invertedIndex, key=lambda element: element[1] )
    middle = len(tempList)/2
    rangel = int(middle - k/2)
    ranger = int(middle + k/2)
    for i in range( rangel, ranger ):
        token, freq = tempList[i]
        print('For K = {0}'.format(i))
        postingList = sorted(invertedIndex[(token, freq)]) 
        print('Postings list size:{0}'.format(len(postingList)))
        sum = 0
        for id in range( len(postingList)-1 ):
            sum = sum + int(postingList[id+1]) - int(postingList[id])
        print('Average Gap Size in the Postings List: {0}'.format( sum/(len(postingList)-1)))
        print('-----------------------------')
    print('----------------------------------------------------------------')
           
def generateIndexStatistics():
    """ Section 2 - To get statistics after step 4 for various K"""
    os.chdir( config.CORPUS_DIRECTORY )
    invertedIndex = {}
    with open('Step4.csv') as f:
        fileList = csv.reader( f )
        for entry in fileList:
            postingList = list(ast.literal_eval(entry[2]))
            invertedIndex[(entry[0], int(entry[1]))]= [ int(x) for x in postingList]

    generateStatsForMaximumKFrequencies( invertedIndex, config.K )
    generateStatsForMinimumKFrequencies( invertedIndex, config.K )
    generateStatsForMedianKFrequencies( invertedIndex, config.K )