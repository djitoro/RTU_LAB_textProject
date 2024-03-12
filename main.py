# loss function - ?

# idea for optimaiz: replase list to numpy

# add an algorithm to remove extra char

# variable in with open = global variable!!!

# idea: we can normal vector skils -
# you can take the 64 most important words

# math.log(numeric_expression,base_value)
# use idf:

# use 2 model: kNN and liner network --> result = medium ans 2 model
# kNN: - len kNN - hyper-parametric

import pymorphy2
import math
import numpy as np
import re

# nested dictionaries - ?

exceptions_set = set()  # insignificant words (spam)
# on the first pass, the algorithm will collect stop words into a file,
# and then read them from it - this will significantly speed up the work on subsequent runs
with open(file='exceptions_set.txt', encoding="utf-8") as file:
    for line in file:
        split_line = line.split()
        exceptions_set.update(split_line)

print('input path resume file:')
input_file = input()
# C:\Users\dimai\PycharmProjects\RTULAB_project\rezyume.txt
morph = pymorphy2.MorphAnalyzer()
input_dictionary = {}  # Key = word; Sum = count word in vac
with open(file=input_file, encoding="utf-8") as file:
    for line in file:
        str_line = re.split(r'[,( ).\n]', line.lower())  # split to token
        # print(str_line)
        for word in str_line:
            token = morph.parse(word)[0].normal_form  # basic word form
            if (len(token) != 0) and (not(token in exceptions_set)) and (token != '\n'):
                # add in dict
                if token in input_dictionary:
                    input_dictionary[token] += 1
                else:
                    input_dictionary[token] = 1

mass_dictionary = np.array([])  # 1 vac - 1 dictionary. Key = word; Sum = count word in vac
dictionary = {}  # list of all words and count it
answer_name = np.array([])  # vacancy name
temp_dict = {}
dictionary_count = {}  # key = word; sum = count of documents with this word
# i m need: mass_weight_dictionary -> dict + mass_dict + weight_dict
with open(file='myDataSet.txt', encoding="utf-8") as file:
    for line in file:
        if line == '-------------------\n':
            mass_dictionary = np.append(mass_dictionary, temp_dict)  # add vacancy in mass_dictionary[i]
            temp_dict = {}  # reset the dictionary
        else:
            if len(temp_dict) == 0:
                answer_name = np.append(answer_name, line)  # add name
            str_line = re.split(r'[,( ).\n]', line.lower())  # split to token
            for word in str_line:
                token = morph.parse(word)[0].normal_form  # basic word form
                if (len(token) != 0) and (not(token in exceptions_set)) and (token != '\n'):
                    if token in temp_dict:
                        temp_dict[token] += 1
                        dictionary[token] += 1
                    elif token in dictionary:
                        dictionary[token] += 1
                    else:
                        temp_dict[token] = 1
                        dictionary[token] = 1

            for word in temp_dict:
                if word in dictionary_count:
                    dictionary_count[word] += 1
                else:
                    dictionary_count[word] = 1

# ....
# tf idf:
index_ans = 0
value_ans = 0
for i in np.arange(len(mass_dictionary)):
    temp_value_ans = 0
    for word in mass_dictionary[i]:
        if dictionary_count[word] == 1:
            mass_dictionary[i][word] = (mass_dictionary[i][word] / dictionary[word]) * \
                                       len(mass_dictionary)
        else:
            mass_dictionary[i][word] = (mass_dictionary[i][word] / dictionary[word]) * \
                                        math.log(len(mass_dictionary), dictionary_count[word])
        # add in spam-bloc
        if mass_dictionary[i][word] < 0.1:  # edit params and my dataset:
            exceptions_set.add(word)
        # kNN: (not an effective option)
        temp_value_ans += mass_dictionary[i][word]
    if temp_value_ans > value_ans:
        value_ans = temp_value_ans
        index_ans = i
print(answer_name[index_ans])

# write in file: add spam word
# use mode = 'a'
with open(file='exceptions_set.txt', mode='w', encoding="utf-8") as file:
    file.writelines([word + ' ' for word in exceptions_set])

# add split into bath and add modul parallel computing
# create data set on one companies


