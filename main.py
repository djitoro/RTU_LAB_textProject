# the system must be built on a recurrent or feed-forward network

# the simplest option for solving the problem:
# present a set of skills as a vector
# (the vector will be the same length as the total number of individual skills)
# ,then we compare the resulting vector and determine the general compliance index,
# and if it is needed at a threshold level, then we output none

# for this method we need data preprocessing, highlighting significant words
# (at the first level you can write your own list of suitable terms and compare with it)

# is it possible to use a decision tree?
# collect a graph of skills and pass each candidate through it
# (but how to identify those who are completely unsuitable?)
#
# the option of trees is not suitable,
# as the candidate may have a partial match of skills

# loss function - ?

# design stages:
# 1. Definition of the loss function
# 2. data set
# 3. building model

# data set tokenization

# to day plan:
# 1. input data, split to token and sort this list


# split vacancy to "_________"

# The program takes as input a solid array of declarations and gives it some weight
# (important words will have a large weight, unimportant words will have about zero weight)
#
# The disadvantage may be that it costs too much resources

# When the vacancies are divided into weighted words,
# then subtract the vacancy vector from the resume vector
# - with a high level of correspondence, produce an answer


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
# math.log(numeric_expression,base_value)

# write input model
print('input path resume file:')
input_file = input()
# C:\Users\dimai\PycharmProjects\RTULAB_project\rezyume.txt
input_data = list(open(input_file, encoding="utf-8"))  # problem!!! i m delite first line, because this code creat
# void input_data_vac_tok[0]


data = list(open('vakansii.txt', encoding="utf-8"))  # add an algorithm to remove extra char
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
print(input_data_tok[0])
input_dictionary = {
}
# count in input data set
for i in range(len(input_data_tok)):
    for line in input_data_tok[i]:
        word = line
        if word in input_dictionary:
            input_dictionary[word] += 1
        else:
            input_dictionary[word] = 1
print(input_dictionary)

dictionary = {
}
# count in full data set
for i in range(len(data_vac_tok)):
    for line in data_vac_tok[i]:
        word = line
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
print(dictionary)

mass_dictionary = []  # 1 vac - 1 dictionary. Key = word; Sum = count word in vac
for i in range(len(data_vac_tok)):
    local_dictionary = {}
    for line in data_vac_tok[i]:
        word = line
        if word in local_dictionary:
            local_dictionary[word] += 1
        else:
            local_dictionary[word] = 1
    mass_dictionary.append(local_dictionary)

print(mass_dictionary[0])
print(mass_dictionary[1])
# we can calculate the meaning of a word on the go