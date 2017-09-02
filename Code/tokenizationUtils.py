#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 14:41:36 2017

@author
Rohan Tondulkar (CS17MTECH11028), Uddipta Bhattacharjee (CS17MTECH11026), Manisha Dubey (CS17RESCH11003)"""

import os
import re
import constants as config
import csv
from nltk.stem.porter import PorterStemmer

class InvertedIndexBuilder( object ):
    
    def __init__( self, directory, step ):
        self.directory      = directory
        self.step           = step
        self.stepsRuleList  = { 'Step1': [ self.convertTokenListToInvertedIndex,
                                          ],
                                'Step2': [ self.removeStopWordsAndSmallWordsFromIndex,
                                           self.convertTokenListToInvertedIndex,
                                          ],
                                'Step3': [ self.removeStopWordsAndSmallWordsFromIndex, 
                                           self.applyStemmingOnTokens,
                                           self.convertTokenListToInvertedIndex,
                                          ],
                                'Step4': [ self.removeStopWordsAndSmallWordsFromIndex, 
                                           self.applyStemmingOnTokens,
                                           self.convertTokenListToInvertedIndex,
                                           self.removeLeastFrequentTerms,
                                          ],
                               }
        self.tokenList      = set()
        self.termToPosting  = {}
        self.invertedIndex  = {}
        
    def removeStopWordsAndSmallWordsFromIndex( self ):
        """"""
        print('Remove stop words and small words for {0}'.format(self.step))
        os.chdir( self.directory )
        self.stopWords = []
        with open('stopWordsList.csv') as f:
            fileList = csv.reader( f )
            for entry in fileList:
                self.stopWords.append( entry[0] )
  
        self.tokenList = filter(lambda element:element[0] not in self.stopWords and len(element[0])>=2, self.tokenList)
 
    
    def applyStemmingOnTokens( self ):
        """"""
        print('Applying Porter Stemmer on tokens for {0}'.format(self.step))
        pstem          = PorterStemmer()
        tempTokenList  = list(self.tokenList)
        
        self.tokenList = set(map( lambda element: ( pstem.stem(element[0]), element[1] ), tempTokenList ))
        
    def removeLeastFrequentTerms( self ):
        """"""
        print('Removing least frequent terms for {0}'.format(self.step))
        freqThreshold = self.numDocs/100
        removeKeys    = [element for element, posting in self.invertedIndex.items() if element[1] <= freqThreshold]
        for key in removeKeys:
            del self.invertedIndex[key]
    
    def writeInvertedIndexToFile( self ):
        """"""
        print('Writing Inverted index to file for {0}'.format(self.step))
        os.chdir( self.directory )
        with open( self.step+'.csv', 'w') as f:
            writer = csv.writer( f, delimiter=',')
            for termTuple, postingsList in self.invertedIndex.items():
                #print('{0}, {1}=> {2}'.format(termTuple[0], termTuple[1], postingsList))
                writer.writerow( [ termTuple[0], termTuple[1], postingsList ] )

    def generateTokensFromDocument( self, docName ):
        """ """
        if not docName.endswith('.txt'):
            return
        with open( docName ) as f:
            for line in f:
                if line.startswith('CONTENT'):
                    docId = int(docName.split('.')[0])
                    for word in re.findall(r'\b([a-zA-Z]+)\b', line):
                        if not word.startswith('CONTENT'):
                            self.tokenList.add((word, docId))
                    for url in re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line):
                        self.tokenList.add((url, docId))
                    for email in re.findall('[^@]+@[^@]+\.[^@]+', line):
                        if len(email) <30:
                            self.tokenList.add((email, docId))
                    for date in re.findall('\d+[-/:]\d+[-/:]\d+', line):
                        self.tokenList.add((date, docId))
                
    def getListOfDocumentsFromDirectory( self ):
        """"""
        os.chdir( self.directory + '/TextFiles' )
        docsList = os.listdir()
        self.numDocs = len(docsList)
        return docsList
    
    def convertTokenListToInvertedIndex( self ):
        """"""
        print('Building index for step: {0}'.format(self.step))
        for token, docId in self.tokenList:
            postingList = self.termToPosting.get( token, set([]) )
            postingList.add( docId )
            self.termToPosting[ token ] = postingList
                
        for term, postingList in self.termToPosting.items():
            self.invertedIndex[( term, len(postingList) )] = postingList

    def getInvertedIndexStatistics( self ):
        """"""
        os.chdir( self.directory )
        print('Get Index statistics for {0}'.format(self.step))
        print('-----------------------------------------------')
        print('Number of Terms: {0}'.format(len(self.invertedIndex.keys())))
        tempList = sorted(self.invertedIndex, key=lambda element: element[1])
        print('Maximum Length of Postings List:{0}'.format(tempList[len(self.invertedIndex)-1][1]))
        print('Minimum Length of Postings List:{0}'.format(tempList[0][1]))
        sum=0
        for term, freq in self.invertedIndex.keys():
            sum = sum + freq
        print('Average Length of Postings List:{0}'.format(sum/len(self.invertedIndex)))
        print('Size of the file that stores the inverted index: {0} KBs'.format(os.path.getsize(self.step+'.csv')/1024))
        
    def buildInvertedIndex( self ):
        """"""
        print('----------------------------------------------------------------')
        print('Starting process for {0}'.format(self.step))
        print('----------------------------------------------------------------')
        docsList  = self.getListOfDocumentsFromDirectory()
        for doc in docsList:
            self.generateTokensFromDocument( doc )
        stepRules = self.stepsRuleList.get( self.step, [] )
        for rule in stepRules:
            rule()
        self.writeInvertedIndexToFile()
        self.getInvertedIndexStatistics()
        
    
def startIndexCreation():
    """"""
    for step in config.STEPS_LIST:
        indexBuilder = InvertedIndexBuilder( config.CORPUS_DIRECTORY, step )
        indexBuilder.buildInvertedIndex()
