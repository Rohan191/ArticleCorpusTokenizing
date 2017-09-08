#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 16:12:50 2017

@author
Rohan Tondulkar (CS17MTECH11028), Uddipta Bhattacharjee (CS17MTECH11026), Manisha Dubey (CS17RESCH11003)
"""

#This file has code required for Section 3.2 and 3.3

import os
import constants as config
import csv
import ast
import matplotlib.pyplot as plt
import numpy as np

POSTING_GAPS_FILE = 'PostingGapsIndex.csv'


def generateFreqGraph( invertedIndex ):
    """Section 3.2) TO generate frequency based plot"""
    print('Printing plot for Step 3 frequencies')
    print('----------------------------------------------------------------')
    tempList = sorted( invertedIndex, key=lambda element: element[1], reverse = True )
    freqDict = {}
    count = 1
    for term, freq in tempList:
        freqDict[count] = freq
        count+=1
        
    #Plot the frequency based graph
    plt.figure()
    plt.xlabel('$\log_{10}(i)$ for $i^{th}$ most frequent term')
    plt.ylabel('$\log_{10}(y_i)$ for freq of $i^{th}$ term')
    plt.title('$\log_{10} y_i$ vs $\log_{10}i$')
    plt.plot(np.log10(list(freqDict.keys())), np.log10(list(freqDict.values())), '-o')
    
def generatePostingGapGraph( invertedIndex ):
    """Section 3.3) To generate the posting list gap based histogram """
    print('Printing plot for Step 3 posting gaps')
    print('----------------------------------------------------------------')
    postingGaps = []
    for key, postingList in invertedIndex.items():
        postingList = sorted( postingList ) 
        gapsList = []
        for id in range( len(postingList)-1 ):
            gap = int(postingList[id+1]) - int(postingList[id])
            gapsList.append( gap )
            postingGaps.append( gap )
        invertedIndex[key] = gapsList
        
    #Write the inverted index with gaps to a file
    print('Writing Inverted index with gaps to file {0}'.format( POSTING_GAPS_FILE ))
    os.chdir( config.CORPUS_DIRECTORY )
    with open( POSTING_GAPS_FILE, 'w') as f:
        writer = csv.writer( f, delimiter=',')
        for termTuple, gapsList in invertedIndex.items():
            writer.writerow( [ termTuple[0], gapsList ] )
    
    #Plot the histogram for posting list gaps
    plt.figure()
    plt.xlabel('Gaps in posting list')
    plt.ylabel('Count')
    plt.title('Posting Gaps histogram')
    plt.hist( postingGaps, bins = 100 )
    
def generateStatisticsForStep3():
    """TTo generate stats based on step 3 asked in Section 3 of assignment"""
    os.chdir( config.CORPUS_DIRECTORY )
    invertedIndex = {}
    with open('Step3.csv') as f:
        fileList = csv.reader( f )
        for entry in fileList:
            postingList = list(ast.literal_eval(entry[2]))
            invertedIndex[(entry[0], int(entry[1]))]= [ int(x) for x in postingList]
    generateFreqGraph( invertedIndex )
    generatePostingGapGraph( invertedIndex )