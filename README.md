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
  def choosing_correct_answer(input_one_vacancy_dictionary, mass_dictionary, answer_name, most_impotent_dict, min_value):
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
    if max_ans_value < min_value:
        return 'None\n'
    else:
        return answer_name[ans_index]
```

2. if the answer is correct, then we move on to point 1
   
3. if not, then we add elements with the maximum weight value to the list of important words and calculate the answer again
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
   if training_flag < (len(answer_name)/2):
      print('the data set is insufficient for training')
      # training requires a large number of resumes      
   ```
6. we transfer the dictionary of weights to work
   ```python
   else:
      use_min_ans_value = min_ans_value
      use_most_impotent_dict = most_impotent_dict
    # we transfer the dictionary of important words to work
   ```
___ 
## Data: 
### data preparation:
We vacancies and resumes for dictionaries from individual words, we reduce words to lower case and to the basic form

But I abandoned the typo check in favor of greater code efficiency and the not entirely correct operation of this module 
P.S. it is in the last 2 commits

### data requirements:
Corresponds to the technical requirements The data should be expanded taking into account the specified style

___
## Ideas for improvement: 
### Model: 
provided unlimited computing resources, it is possible to create an ensemble of models - kNN and a classical transformer

However, for this it will also be necessary to significantly increase the training data set.
### Interface: 
Add a window for interaction and the ability to drag and drop files

As well as the ability to upload a single file for the full cycle of work
___

:wink:
