# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 00:20:41 2017

@author: manisha
"""


import csv
import copy

class InvertedIndex:
    
    def __init__( self ):
        self.index_dict = dict()
        
              
    def __contains__( self, item ):
        return item in self.index
    
    def createIndex( self, tokens, docID ):
        
        for token in tokens:
                 if token in self.index_dict.keys():
                     list = self.index_dict.get( token )
                     if docID not in list:
                         self.index_dict[token].append( docID )
                 else:
                     self.index_dict[token] = [docID]
                         
                
                
def copyDict( source_dict ):
    dest_dict = dict()
    dest_dict = copy.deepcopy( source_dict )
    return dest_dict
      
# Print contents of dictionary                  
def printIndex( index, turn ):  
    with open("index_step_" + str(turn) + ".csv", 'w', newline='\n') as csvfile:
        writer = csv.writer( csvfile, delimiter = ',' )
        for k,v in index.items():
            writer.writerow([k] + list(v))
                
    
    csvfile.close()
    
    
            
    
