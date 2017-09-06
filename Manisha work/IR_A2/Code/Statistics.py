# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 12:56:19 2017

@author: manisha
"""


import Parse as parse
import constant as config
from math import log
import matplotlib.pyplot as plt
import numpy
import InvertedIndex as index
import sys

class Statistics:
    
    def __init__( self ):
        self.no_of_terms = 0

    def findStatistics( self ):
        k = 1
        list_of_objects = [ parse.idx1, parse.idx2,parse.idx3, parse.idx4  ]
        for each_object in list_of_objects:
            print("SECTION 1 STATISTICS FOR INDEX AT STEP " + str(k))
            self.statisticsSection1(each_object)
            k = k + 1
        print("\n\n\n")   
        self.statisticsSection2(parse.idx4.index_dict)
        print("\n\n\n") 
        self.statisticsSection3()
    
# Calculate statistics for section 1 to find number of terms and maximum, minimum and average posting size at each step
    def statisticsSection1( self, index ):
        min_length = config.CORPUS_SIZE + 1
        max_length = 0
        total_length = 0
        
#        Number of terms
        self.no_of_terms = len(index.index_dict.keys())
           
#        Maximum number of postings
        for key in index.index_dict.keys():
            value = index.index_dict.get(key)
            posting_length = len(value)
            total_length = total_length + posting_length
            if posting_length > max_length:
                max_length = posting_length
            if posting_length < min_length:
                min_length = posting_length
        maximum_posting_length = max_length
        minimum_posting_length = min_length
        avg_length = total_length/config.CORPUS_SIZE
        
        print(" \t Number of terms is " + str(self.no_of_terms))
        print(" \t Maximum posting length is " + str(maximum_posting_length))
        print(" \t Minimum posting length is " + str(minimum_posting_length))
        print(" \t Average posting length is " + str(avg_length))
        print("\n\n")  
        
# Calculate statistics for section 2
    def statisticsSection2( self, index ):
        print(" STATISTICS FOR SECTION 2 ")
        gapped_dict = dict()
        sorted_items = self.sortDictionary(index)
        top_K_frequent = dict(sorted_items[1 : config.K + 1])
        last_K_frequent = dict(sorted_items[-20:])
        median_K_frequent = dict(sorted_items[int((self.no_of_terms - config.K)/2) : int((self.no_of_terms + config.K)/2)])
        
        
        
        list_of_dict = [last_K_frequent, top_K_frequent, median_K_frequent]
        string_of_dict = [" LAST K FREQUENT ", " TOP K FREQUENT ", " MEDIAN K FREQUENT "]
        for each_dict in list_of_dict:
            print("  Statistics for " + string_of_dict[list_of_dict.index(each_dict)])
            gapped_dict = self.findAverageGap(each_dict)
            for key in gapped_dict.keys():
                    print("\t \t Key is " + str(key))
                    values = gapped_dict.get(key)
                    average = sum(values)/len(values)
                    print("\t \t Posting size " + str(len(values) + 1))
                    print("\t \t Average size " + str(average) + "\n")
                    
# Statistics for section 3
    def statisticsSection3( self ):
        print(" STATISTICS FOR SECTION 3 ")
        # Part A
        temp_dict = dict()
        gapped_dict = dict()
        logged_tokens_stemming = [log(y,10) for y in parse.tokens_stemming]
        logged_terms_stemming = [log(y,10) for y in parse.terms_stemming]
       
        plt.plot(logged_tokens_stemming, logged_terms_stemming, 'ro')
        plt.xlabel("log of tokens")
        plt.ylabel("log of terms")
        plt.show()
        plt.savefig("graph_section3_partA.png")
        
        # PART B
        temp_dict = dict(self.sortDictionary(parse.idx3.index_dict))
        x = list(range(1, len(temp_dict.keys()) + 1))
        y = []
        for key in temp_dict.keys():
            length_of_values = len(temp_dict.get(key))
            y.append(length_of_values)
        logged_x = list(log(each,10) for each in x)
        logged_y = list(log(each,10) for each in y)
        plt.plot(logged_x, logged_y, 'ro')
        plt.xlabel("log i")
        plt.ylabel("log y")
        plt.show()
        plt.savefig("graph_section3_partB.png")
        
        # PART C
        gapped_dict = self.findAverageGap(parse.idx3.index_dict)
        index.printIndex(gapped_dict,5)    
        
       
        
    def plotGraph(self, list1, list2):
       return plt.plot(list1, list2, 'ro')
        
   
    def sortDictionary(self, index):
        sorted_items = sorted(index.items(), key = lambda item : len(item[1]), reverse = True)
        return sorted_items
   
    # Find dictionary with postings as gap
    def findAverageGap(self, gapped_index):
        dictionary_of_gaps = dict()
        for key in gapped_index.keys():
            list_of_gaps = []
            values = gapped_index.get(key)
            stripped_values = [int(s.strip('.txt')) for s in values]
            stripped_values.sort()
            list_of_gaps = list(numpy.diff(stripped_values))
            dictionary_of_gaps[key] = list_of_gaps
            
        
#        X = len(dictionary_of_gaps.keys())
#        plt.bar(range(X), dictionary_of_gaps.values(), stacked = True)
        return dictionary_of_gaps
            
sys.stdout = open("FinalReport.log", "a") 

                
            
            
        
        
        
        
