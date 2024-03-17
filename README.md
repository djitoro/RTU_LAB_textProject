# Selection of vacancies
___
## Main idaes: 
### 1.TF-IDF
  Sentence A: the car is driven on the road
  
  Sentence B: the truck is driven on the highway
  
  ![tf-idf](https://github.com/djitoro/RTU_LAB_textProject/blob/main/pictures/tf-idf-4.png)
      
      we consider the “weight” of a word in the subtext
 
  I used this particular model because on relatively small data sets it is more efficient in terms of memory and processor load (compared to transformers)
### 2.kNN
  The most suitable vacancy will be determined using the nearest neighbors method. Since the number of significant words in the resume text is quite small, this method will allow you to determine answers much faster than linear and nonlinear classifiers

   ![kNN](https://github.com/djitoro/RTU_LAB_textProject/blob/main/pictures/kNN.png)

      a resume is a point in space N, 
      and the desired vacancy is the one closest to this point
### 3.list of spam-word
  To optimize the work, I used a list of “not important” words.
  
  Algorithm: 
  
  1.you make the first sentence of the answer: 
  ```python
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
  ```

2. if the answer is correct, then we move on to point 1
   ```python
            possible_answer = choosing_correct_answer(input_one_vacancy_dictionary, count_mass_dictionary, answer_name, most_impotent_dict)
            training_flag = False
            last_len_imposible_dict = 0
            # you can go backwards and determine the minimum number of words for an accurate definition
            while last_len_imposible_dict != len(most_impotent_dict):
                if possible_answer != right_answer[iterations]:
                    most_impotent_dict = choosing_important_words(mass_dictionary, most_impotent_dict)
                    possible_answer = choosing_correct_answer(input_one_vacancy_dictionary, count_mass_dictionary,
                                                              answer_name, most_impotent_dict)
                else:
                    training_flag = True
                    break
   ```
4. if not, then we add elements with the maximum weight value to the list of important words and calculate the answer again
   ```python
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

        del mass_dict[i][most_impotent_word]  # remove written words from the list
        
    return most_impotent_d
   ```
5. if we took into account absolutely all the words, but still did not get the correct answer, then the program suggests repeating the training on a larger data set
   ```python
   if not training_flag:
         print('the data set is insufficient for training')
   ```
6. we transfer the dictionary of weights to work
   ```python
    else:
         use_most_impotent_dict = most_impotent_dict  # we transfer the dictionary of important words to work
   ```
___ 
## Data: 
### data preparation:
test 
### System architecture:
test
### System accuracy
test


As a result, we get a vector for each vacancy and a vector for the resume
___

**test**
*test2*

:wink:
