# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 10:10:43 2017

@author: manisha
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 00:58:21 2017

@author: manisha
"""
import constant as config
from os import listdir
from os import path
from nltk.tokenize import word_tokenize
import InvertedIndex as index
import Statistics as statistics
import linecache
from nltk.tokenize import regexp_tokenize
from nltk.stem import PorterStemmer
from string import punctuation

regex_str = ['[\w\.-]+@[\w\.-]+', 'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', 
             '[0-9]{2}/[0-9]{2}/[0-9]{4}', '[0-9]{2}-[0-9]{2}-[0-9]{4}', '^(([0-1]?[0-9])|([2][0-3])):([0-5]?[0-9])(:([0-5]?[0-9]))?$'
              '(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})', '[0-9]{2}/[0-9]{2}/[0-9]{2}', '[0-9]{2}-[0-9]{2}-[0-9]{2}']


class Corpus:
    def ___init__( self ):
         self.fileNames = []
         
# List the file names of corpus         
    def enumerateFiles( self, path ):
        self.fileNames = [f for f in listdir( path )]
        self.parseCorpus( self.fileNames )
        
        
    def parseCorpus( self, list_of_files ):
        for each_file in list_of_files:
            tokens = self.indexBuildingStep1(each_file) 
            filtered_tokens = self.indexBuildingStep2(each_file, tokens)
            stemmed_tokens = self.indexBuildingStep3(each_file, filtered_tokens)
                
        self.indexBuildingStep4()    
        index.printIndex(idx1.index_dict, 1) 
        index.printIndex(idx2.index_dict, 2) 
        index.printIndex(idx3.index_dict, 3) 
        index.printIndex(idx4.index_dict, 4) 
        
# Parse documents for Step 1 considering date, email ID and link as single token        
    def indexBuildingStep1( self, file ):
        regex = []
        file_content = parseFile(file)
        content_without_regex = file_content
        regex = self.regularExpressions(file_content)
        # save all regular ex[pressions and remove them from original content]      
        if regex is not []:
            for each in regex:
                content_without_regex = file_content.replace(each, "")
        # reove punctuation        
        content_without_regex = removePunctuation(content_without_regex) 
        tokens = self.tokenize(content_without_regex)
        tokens = tokens + regex
        idx1.createIndex(tokens, file)
        return tokens    
        
# Parse documents for Step 2 for stopword removal and apply length constraint    
    def indexBuildingStep2( self, file, tokens ):
        length_constrained_tokens = filterTokens(tokens)
        filtered_tokens = stripStopwords(length_constrained_tokens)
        idx2.createIndex(filtered_tokens, file)
        return filtered_tokens
    
# Step 3 - Apply porter stemmer
    def indexBuildingStep3( self, file, tokens ):
        stemmer = PorterStemmer()
        stemmed_tokens = [stemmer.stem(t) for t in tokens]
        tokens_stemming.append(len(tokens))
        terms_stemming.append(len(set(stemmed_tokens)))
        idx3.createIndex(stemmed_tokens, file)
        return stemmed_tokens
    
# Step 4 - Remove terms with frequency less than 1% of corpus
    def indexBuildingStep4( self ):
        temp_dict = index.copyDict(idx3.index_dict)
        idx4.index_dict = index.copyDict(idx3.index_dict)
        for key in temp_dict:
            values = temp_dict.get(key)
            if len(values) < config.MIN_POSTING_SIZE:
                idx4.index_dict.pop(key)
                
# Perform tokenization        
    def tokenize(self, file_content):
        simple_tokenized = word_tokenize(file_content)
        return simple_tokenized
    
# Find date, email ID, link using regular expressions   
    def regularExpressions( self, file_content ):
        tokens_with_regex = []
        final_list_regex = []
        for each in regex_str:
            tokens_with_regex.append(regexp_tokenize(file_content, pattern = each))
        for sublist in tokens_with_regex:
            for item in sublist:
                final_list_regex.append(item)
        return final_list_regex
    
 # Remove tokens of size less than length 2   
def filterTokens( tokens ):
    final_tokens = [t for t in tokens if len(t) > config.MIN_TOKEN_SIZE ]
    return final_tokens
                                
 # Retrieve content from each file   
def parseFile( file_name ):
    file_path = path.join(config.FILE_PATH, file_name)
    content_line = linecache.getline(file_path, 6)
    content = content_line.split("CONTENT:b")[1]
    content = foldCase(content)
    return content

# Convert to lower case
def foldCase( text ):
    return text.lower()

# Remove punctuation
def removePunctuation( text ):
    final_text = ''.join(c for c in text if c not in punctuation)
    return final_text

# Remove stopwords
def stripStopwords( tokens ):
    stopwords = []
    file = open(config.STOPWORDS_FILE_PATH, "r")
    data = file.readlines()
    for line in data:
        stopwords.append(line.strip('\n'))
    [x for x in stopwords if x]    
    filtered_tokens = [w for w in tokens if not w in stopwords]
    return filtered_tokens
    
    

tokens_stemming = []
terms_stemming = []
idx1 = index.InvertedIndex()
idx2 = index.InvertedIndex()    
idx3 = index.InvertedIndex()
idx4 = index.InvertedIndex() 
invertedIndex1 = Corpus()
stats = statistics.Statistics()
invertedIndex1.enumerateFiles(config.CORPUS_PATH)
stats.findStatistics()


