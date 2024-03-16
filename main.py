# loss function - ?
# typo check!!
# divided into training/working model

# use 2 model: kNN and liner network --> result = medium ans 2 model
# kNN: - len kNN - hyper-parametric

import pymorphy2
import math
import numpy as np
import re

import datetime
# pip install pyenchant
import enchant  # при импроте пишем именно enchant (не pyenchant)
import difflib
morph = pymorphy2.MorphAnalyzer()


def input_one_block(file):  # a function that reads 1 job opening or resume and turns it into a dictionary
    # accepts a list of input data as input
    split_dataset_dictionary = {}
    for line in file:
        str_line = re.split(r'[,( ).\n]', line.lower())  # split to token
        for word in str_line:
            token = morph.parse(word)[0].normal_form  # basic word form
            if (len(token) != 0) and (token != '\n'):
                # add in dict
                if token in split_dataset_dictionary:
                    split_dataset_dictionary[token] += 1
                else:
                    split_dataset_dictionary[token] = 1
    return split_dataset_dictionary

'''
mass_dictionary = np.array([])  # 1 vac - 1 dictionary. Key = word; Sum = count word in vac
dictionary = {}  # list of all words and count it
answer_name = np.array([])  # vacancy name
temp_dict = {}
dictionary_count = {}  # key = word; sum = count of documents with this word
'''


def input_bloc_vac(file):
    def_mass_dictionary = np.array([])  # 1 vac - 1 dictionary. Key = word; Sum = count word in vac
    def_dictionary = {}  # list of all words and count it
    def_answer_name = np.array([])  # vacancy name
    def_temp_dict = {}
    def_dictionary_count = {}  # key = word; sum = count of documents with this word

    f = file.readlines()
    last_line = f[-1]
    for line in f:
        if line is last_line:
            def_mass_dictionary = np.append(def_mass_dictionary, def_temp_dict)  # add vacancy in mass_dictionary[i]
            def_temp_dict = {}  # reset the dictionary

        elif line != '-------------------\n':
            if len(def_temp_dict) == 0:
                def_answer_name = np.append(def_answer_name, line)  # add name
            str_line = re.split(r'[,( ).\n]', line.lower())  # split to token
            for word in str_line:
                token = morph.parse(word)[0].normal_form  # basic word form
                if (len(token) != 0) and (token != '\n'):
                    if token in def_temp_dict:
                        def_temp_dict[token] += 1
                        def_dictionary[token] += 1
                    elif token in def_dictionary:
                        def_dictionary[token] += 1
                    else:
                        def_temp_dict[token] = 1
                        def_dictionary[token] = 1

            for word in def_temp_dict:
                if word in def_dictionary_count:
                    def_dictionary_count[word] += 1
                else:
                    def_dictionary_count[word] = 1

        elif line == '-------------------\n':
            def_mass_dictionary = np.append(def_mass_dictionary, def_temp_dict)  # add vacancy in mass_dictionary[i]
            def_temp_dict = {}  # reset the dictionary
    # the index in def_mass_dictionary and def_answer_name are related,
    # so def_mass_dictionary[1] == def_answer_name[1]
    return def_dictionary, def_mass_dictionary, def_dictionary_count, def_answer_name


def choosing_important_words(mass_dict, most_impotent_d):
    for i in range(len(mass_dict)):
        most_impotent_word = ''
        most_impotent_value = 0
        for word in mass_dictionary[i]:
            if mass_dict[i][word] > most_impotent_value:
                most_impotent_value = mass_dict[i][word]
                most_impotent_word = word
        if most_impotent_word in most_impotent_d:
            most_impotent_d[most_impotent_word] += most_impotent_value
        else:
            most_impotent_d[most_impotent_word] = most_impotent_value

    return most_impotent_d


# kNN:
# use matrix multiplication (via dot function in np) - ?
def choosing_correct_answer(input_one_vacancy_dictionary, mass_dictionary, answer_name, most_impotent_dict):
    ans_index = 0
    max_ans_value = 0

    for i in range(len(mass_dictionary)):
        temp_ans_value = 0
        for word in input_one_vacancy_dictionary:
            if (word in most_impotent_dict) and (word in mass_dictionary[i]):
                temp_ans_value += (mass_dictionary[i][word] * most_impotent_dict[word])
        if temp_ans_value > max_ans_value:
            ans_index = i
            max_ans_value = temp_ans_value

    return answer_name[ans_index]


print('Exit - -1')
print('To train the model press - 0')
print('To operate the model press - 1')
ans_q = int(input())  # variable for writing commands
use_most_impotent_dict = {}
while True:
    if ans_q == 0:
        '''
        exceptions_set = set()  # insignificant words (spam)
        dictionary_for_come_back = {}
        # we take a large set of data
        # (job texts from the Internet) so that our model learns to identify important and unimportant words
        # you need a corpus of random abstracts to learn how to separate common words from special ones
        '''
        #  The model is trained by weighting words.
        #  General-purpose words receive low weight,
        #  or even end up in the exclusion list
        #  (this allows for increased efficiency during the work of the main part),
        #  words that relate to special terms and highlight the specialist receive more weight

        #  Data requirements:
        # 1. uniform distribution of vacancies across areas
        # 2. A large number of non-IT vacancies (so that the model evaluates general words below)

        print('enter the path to the file with the training sample:')
        input_file = input()  # C:\Users\dimai\PycharmProjects\RTULAB_project\myData.txt
        # myData - a collection of vacancy texts from the Internet
        # But this set include only IT-vac
        with open(file=input_file, encoding="utf-8") as file:
            training_dataset_dictionary = input_one_block(file)  # dictionary with all training data

        # we take the sequence of correct answers from the annotated data set
        right_answer = np.array([])  # create file right answers:
        print('enter the path to the file with the correct answers:')
        input_file = input()  # C:\Users\dimai\PycharmProjects\RTULAB_project\primery_rezyume.txt
        with open(file=input_file, encoding="utf-8") as file:
            past_line = ''
            for line in file:
                if past_line == 'Вакансия:\n':
                    right_answer = np.append(right_answer, line)
                past_line = line
        print(right_answer)

        print('enter the path to the file with a complete list of vacancies to select:')
        input_file = input()  # C:\Users\dimai\PycharmProjects\RTULAB_project\vakansii.txt
        with open(file=input_file, encoding="utf-8") as file:
            dictionary, mass_dictionary, dictionary_count, answer_name = input_bloc_vac(file)
        print(dictionary)

        hyperpar = 0  # threshold for words to enter the spam list == max value
        for word in training_dataset_dictionary:
            if word in dictionary:
                dictionary[word] += training_dataset_dictionary[word]
            else:
                dictionary[word] = training_dataset_dictionary[word]
        print(dictionary)

        # tf idf:
        index_ans = 0
        value_ans = 0
        for i in np.arange(len(mass_dictionary)):
            # temp_value_ans = 0
            for word in mass_dictionary[i]:
                if dictionary_count[word] == 1:
                    mass_dictionary[i][word] = (mass_dictionary[i][word] / dictionary[word]) * \
                                               len(mass_dictionary)
                else:
                    mass_dictionary[i][word] = (mass_dictionary[i][word] / dictionary[word]) * \
                                               math.log(len(mass_dictionary), dictionary_count[word])
                '''
                # kNN: (not an effective option)
                temp_value_ans += mass_dictionary[i][word]
            if temp_value_ans > value_ans:  # add minimum threshold
                value_ans = temp_value_ans
                index_ans = i
                '''
        # go from the reverse:
        # from one to more important words, adding the rest to add from the spam list
        print()
        print(mass_dictionary[0])
        for iterations in range(len(right_answer)):
            print('enter the path to the file with one resume:')
            print('ATTENTION: the resume must be from the file that was entered above')
            input_file = input()  # C:\Users\dimai\PycharmProjects\RTULAB_project\rezyume.txt
            with open(file=input_file, encoding="utf-8") as file:
                input_one_vacancy_dictionary = input_one_block(file)
            print(input_one_vacancy_dictionary)

            # None class vacancies:
            # after training on classified data,
            # we will receive a list of important and unimportant words,
            # if a word receives a total amount less than the minimum,
            # then its class will be None
            most_impotent_dict = {}
            most_impotent_dict = choosing_important_words(mass_dictionary, most_impotent_dict)
            # list of sufficient words to define a class
            print('most_impotent_dict')
            print(most_impotent_dict)
            # we take one most significant word from each vacancy
            print('ans1:')
            # first hypothetical answer:
            possible_answer = choosing_correct_answer(input_one_vacancy_dictionary, mass_dictionary, answer_name, most_impotent_dict)
            training_flag = False
            last_len_imposible_dict = 0
            # you can go backwards and determine the minimum number of words for an accurate definition
            while last_len_imposible_dict != len(most_impotent_dict):
                if possible_answer != right_answer[iterations]:
                    most_impotent_dict = choosing_important_words(mass_dictionary, most_impotent_dict)
                    possible_answer = choosing_correct_answer(input_one_vacancy_dictionary, mass_dictionary,
                                                              answer_name, most_impotent_dict)
                else:
                    training_flag = True
                    break
                    # stop stady and come back

            if not training_flag:
                print('the data set is insufficient for training')
                # training requires a large number of resumes
            else:
                use_most_impotent_dict = most_impotent_dict
        print('Exit - -1')
        print('to repeat training press - 0')
        print('To operate the model press - 1')
        ans_q = int(input())
    if ans_q == 1:
        mass_str_vac = np.array([])
        temp_str = ''
        print('enter the path to the file with a complete list of vacancies:')
        input_file = input()  # C:\Users\dimai\PycharmProjects\RTULAB_project\vakansii.txt
        with open(file=input_file, encoding="utf-8") as file:
            dictionary, mass_dictionary, dictionary_count, answer_name = input_bloc_vac(file)

        print('enter the path to the resume file:')
        input_file = input()  # C:\Users\dimai\PycharmProjects\RTULAB_project\rezyume.txt
        with open(file=input_file, encoding="utf-8") as file:
            input_one_vacancy_dictionary = input_one_block(file)
        print(input_one_vacancy_dictionary)

        possible_answer = choosing_correct_answer(input_one_vacancy_dictionary, mass_dictionary, answer_name,
                                                  use_most_impotent_dict)
        print(possible_answer)

    if ans_q == -1:
        break

start = datetime.datetime.now()

# nested dictionaries - ?

exceptions_set = set()  # insignificant words (spam)
# on the first pass, the algorithm will collect stop words into a file,
# and then read them from it - this will significantly speed up the work on subsequent runs
with open(file='exceptions_set.txt', encoding="utf-8") as file:
    for line in file:
        split_line = line.split()
        exceptions_set.update(split_line)

# write in file: add spam word
# use mode = 'a'
with open(file='exceptions_set.txt', mode='w', encoding="utf-8") as file:
    file.writelines([word + ' ' for word in exceptions_set])

# add split into bath and add modul parallel computing
# create data set on one companies

finish = datetime.datetime.now()
print('Время работы: ' + str(finish - start))

woi = "игра"
sim = dict()

dictionary = enchant.Dict("ru_Ru")
suggestions = set(dictionary.suggest(woi))
s = 0
for word in suggestions:
    measure = difflib.SequenceMatcher(None, woi, word).ratio()
    sim[measure] = word
    s += 1
print(s)
print(sim)
print("Correct word is:", sim[max(sim.keys())])

print(dictionary.check("река"))


