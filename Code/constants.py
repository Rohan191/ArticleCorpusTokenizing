#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 21:01:49 2017

@author
Rohan Tondulkar (CS17MTECH11028), Uddipta Bhattacharjee (CS17MTECH11026), Manisha Dubey (CS17RESCH11003)"""

#The directory where the folder /TextFiles is made containing corpus
CORPUS_DIRECTORY    = '/Users/rohantondulkar/Projects/Information Retrieval/ArticleCorpusTokenizing'

#Folder for corpus inside CORPUS_DIRECTORY
TEXT_FILES          = '/TextFiles'

#List of steps. Also add the rules for these steps in tokenizationUtils.py (class InvertedIndexBuilder)
STEPS_LIST          = [ 'Step1', 'Step2', 'Step3', 'Step4' ]

#Number for k most, median and least frequent terms plot in section 2
K                   = 20
