#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 14:41:36 2017

@author
Rohan Tondulkar (CS17MTECH11028), Uddipta Bhattacharjee (CS17MTECH11026), Manisha Dubey (CS17RESCH11003)"""

import re
import constants as config
from nltk.stem.porter import PorterStemmer

class InvertedIndexBuilder( object ):
    
    def __init__( self, directory, step ):
        self.stepsToMethods = { 'Step1': [],
                                'Step2': [ self.removeStopWordsFromIndex 
                                          ],
                                'Step3': [ self.removeStopWordsFromIndex, 
                                           self.applyStemmingOnTokens
                                          ],
                                'Step4': [ self.removeStopWordsFromIndex, 
                                           self.applyStemmingOnTokens,
                                           self.removeLeastFrequentTerms
                                          ],
                               }
        self.directory      = directory
        self.tokenList      = []
        self.termToPosting  = {}
        self.invertedIndex  = {}
        self.step           = step
        
    def removeStopWordsFromIndex( self ):
        """"""
        pass
    
    def applyStemmingOnTokens( self ):
        """"""
        pstem = PorterStemmer()
        for token, docId in self.tokenList:
            self.tokenList.remove((token, docId))
            self.tokenList.append( ( pstem.stem(token), docId ) )
        
    def removeLeastFrequentTerms( self ):
        """"""
        pass
    
    def writeInvertedIndexToFile( self ):
        """"""
        pass

    def getTokensFromDocument( self, docName ):
        """ """
        with open( docName ) as f:
            for line in f:
                if re.findall('CONTENT:.*', line):
                    for word in re.findall(r'\b([a-zA-Z]+)\b', line):
                        print(word)
                    for url in re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line):
                        print(url)
                    for email in re.findall('[^@]+@[^@]+\.[^@]+', line):
                        print(email)
                    for date in re.findall('\d+[-/:]\d+[-/:]\d+', line):
                        print(date)
                
    def getListOfDocumentsFromDirectory( self, dirPath ):
        """"""
        import os
        os.chdir( dirPath )
        docsList = os.listdir()
        self.numDocs = len(docsList)
        return docsList

