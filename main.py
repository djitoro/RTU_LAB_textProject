# loss function - ?

# idea for optimaiz: replase list to numpy

# add an algorithm to remove extra char

import itertools
import string
import mystring as mystring
import numpy as np
import umap
from nltk.tokenize import WordPunctTokenizer
from matplotlib import pyplot as plt
from IPython.display import clear_output
from nltk.tokenize import sent_tokenize, word_tokenize
import pymorphy2
import math

# write input model
print('input path resume file:')
input_file = input()
# C:\Users\dimai\PycharmProjects\RTULAB_project\rezyume.txt
input_data = list(open(input_file, encoding="utf-8"))  # problem!!! i m delite first line, because this code create
# void input_data_vac_tok[0]
data = list(open('myDataSet.txt', encoding="utf-8"))

tokenizer = WordPunctTokenizer()
# split to token
data_tok = [tokenizer.tokenize(sentence.lower()) for sentence in data]
input_data_tok = [tokenizer.tokenize(sentence.lower()) for sentence in input_data]  # 1 resume

morph = pymorphy2.MorphAnalyzer()
# split to vacancy
data_vac_tok = []
vac_tok = []
for line in data_tok:
    if line == ['-------------------']:
        for i in range(len(vac_tok)):
            vac_tok[i] = morph.parse(vac_tok[i])[0].normal_form  # one form word
        data_vac_tok.append(vac_tok)
        vac_tok = []
    else:
        vac_tok += line

# del data_tok

input_dictionary = {}
dictionary = {}
# count in input data set
for i in range(len(input_data_tok)):
    for line in input_data_tok[i]:
        word = line
        if word in input_dictionary:
            input_dictionary[word] += 1
        else:
            input_dictionary[word] = 1

mass_dictionary = []  # 1 vac - 1 dictionary. Key = word; Sum = count word in vac
# count in full data set
for i in range(len(data_vac_tok)):
    local_dictionary = {}
    for line in data_vac_tok[i]:
        word = line
        if word in dictionary:
            dictionary[word] += 1
        if word in local_dictionary:
            local_dictionary[word] += 1
        else:
            local_dictionary[word] = 1
            dictionary[word] = 1
    mass_dictionary.append(local_dictionary)

# we can calculate the meaning of a word on the go

# create vector input data
# create vector all vac

# idea: we can normal vector skils -
# you can take the 64 most important words

# math.log(numeric_expression,base_value)
# use idf:
weight_dictionary = {}
for dict in dictionary:
    c = 0
    for i in range(len(mass_dictionary)):
        if dict in mass_dictionary[i]:
            c += 1
    if c == 1:
        weight_dictionary[dict] = len(mass_dictionary)  # log(22, 1) = error
    else:
        weight_dictionary[dict] = math.log(len(mass_dictionary), c)


# count weight in 1 vac
# TF * IDF
for i in range(len(mass_dictionary)):
    for dict in mass_dictionary[i]:
        mass_dictionary[i][dict] = (mass_dictionary[i][dict] / dictionary[dict]) * weight_dictionary[dict]

def similarity_vector(): # comparison of two vectors with skill values
    return float

# use 2 model: kNN and liner network ----> result = medium ans 2 model

# kNN:
