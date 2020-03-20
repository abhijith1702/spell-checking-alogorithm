

import sys
import json
import operator
from typing import List, Any

import tables
from correction import correction

# list for correction class objects
correction_list = []

#function for creating dictionaries
def create_dict(table_name):
    my_key = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z']
    my_dict = {}
    for item in table_name:
        values = item[1:]
        new_l = dict(zip(my_key, values))
        my_dict[item[0]] = new_l
    return my_dict

#function for adding letter in bewteen the word
def insert_At(word, i, j):
    return word[:i] + chr(j) + word[i:]

# function for list of  possible correction word by adding
# alphabet to input_word
def insertion(input_word, complete_dict, total_count, delete_table_dict):
    ins_prune_list, ins_word_list = [], []
    error_letter, error_type = "-", "D"
    for i in range(len(input_word) + 1):
        for j in range(ord('a'), ord('z') + 1, 1):
            add_word = insert_At(input_word, i, j)
            ins_word_list.extend([add_word])
            if add_word in complete_dict["words"]:
                ins_prune_list.extend([add_word])
                candidate_correction, correct_letter, error_position =\
                    add_word, add_word[i], i
                x = add_word[i - 1]
                w = add_word[i - 1] + add_word[i]
                x_given_word = (delete_table_dict[x][add_word[i]]
                        / complete_dict["bigrams"][w])
                x_given_w = x + "|" + w
                #Kernighan’s approach to find the probability of
                # each possible correction
                prob_word = (complete_dict["words"][add_word] ) \
                            / (total_count )
                final_val = round(((10 ** 9) * x_given_word * prob_word), 6)
                correction_list.append(
                    correction(candidate_correction, correct_letter,
                    error_letter,x_given_w, x_given_word, prob_word,
                               final_val,error_type,error_position))
    return correction_list, ins_word_list, ins_prune_list

#function for deleting each letter from word
def get_del_char(word, i):
    return word[:i] + word[i+1:]

# function for  list of possible correction by
# deleting letter from input_word
def deletion(input_word, complete_dict, total_count, add_table_dict):
    del_prune_list, del_word_list = [], []
    correct_letter, error_type = "-", "I"
    for i in range(len(input_word)):
        del_word = get_del_char(input_word, i)
        del_word_list.extend([del_word])
        if del_word in complete_dict["words"]:
            del_prune_list.extend([del_word])
            candidate_correction, error_position, error_letter =\
                del_word, i, input_word[i]
            x = input_word[(i - 1):(i - 1) + 2]
            w = input_word[i - 1]
            x_given_word = ((add_table_dict[input_word[i - 1]]
            [input_word[i]]) / (complete_dict["unigrams"][w]))
            x_given_w = x + "|" + w
            #Kernighan’s approach to find the probability of
            # each possible correction
            prob_word =(complete_dict["words"][del_word]) / (total_count )
            final_val = round(((10 ** 9) * x_given_word * prob_word), 6)
            correction_list.append(
                correction(candidate_correction, correct_letter,
                error_letter, x_given_w, x_given_word, prob_word,
                           final_val,error_type,error_position))
    return correction_list, del_word_list, del_prune_list

#function for susbstiting each characte by another in word
def get_sub_word(word, i, j):
    return word[:i] + chr(j) + word[i+1:]

# create list of word by substituting each character by other alphabet
def substitution(input_word, complete_dict, total_count, sub_table_dict):
    sub_prune_list, sub_word_list = [], []
    error_type = "S"
    for i in range(len(input_word)):
        for j in range(ord('a'), ord('z') + 1, 1):
            if input_word[i] != chr(j):
                sub_word = get_sub_word(input_word, i, j)
                sub_word_list.extend([sub_word])
                if sub_word in complete_dict["words"]:
                    sub_prune_list.extend([sub_word])
                    candidate_correction = sub_word
                    correct_letter, error_letter, error_position =\
                        sub_word[i], input_word[i], i
                    x = error_letter
                    w = correct_letter
                    x_given_w = x + "|" + w
                    #Kernighan’s approach to find the probability
                    # of each possible correction
                    x_given_word =(sub_table_dict[error_letter]
                    [correct_letter] / complete_dict["unigrams"][correct_letter])
                    prob_word =(complete_dict["words"][sub_word]) / (total_count)
                    final_val = round(((10 ** 9) * x_given_word * prob_word), 6)
                    correction_list.append(
                    correction(candidate_correction, correct_letter,
                    error_letter,x_given_w, x_given_word, prob_word,
                               final_val,error_type,error_position))
    return correction_list, sub_word_list, sub_prune_list

#function for swapping two consecutive character in between the word
def get_trans_word(word, i):
    return word[:i] + word[i + 1] + word[i] + word[i + 2:]

 # function for list of word by swapping two consecutive character in a word
def transposition(input_word, complete_dict, total_count, transpose_table_dict):
    trans_prune_list, trans_word_list = [], []
    error_type = "T"
    for i in range(len(input_word) - 1):
        rev_word = get_trans_word(input_word, i)
        trans_word_list.extend([rev_word])
        if rev_word in complete_dict["words"]:
            trans_prune_list.extend([rev_word])
            candidate_correction = rev_word
            correct_letter, error_letter, error_position =\
                rev_word[i] + rev_word[i + 1],rev_word[i + 1] + rev_word[i], i
            x_given_w = error_letter + "|" + correct_letter
            #Kernighan’s approach to find the probability
            # of each possible correction
            x_given_word =(transpose_table_dict[rev_word[i]][rev_word[i + 1]]
                           /complete_dict["bigrams"][error_letter])
            prob_word = (complete_dict["words"][rev_word]) / (total_count)
            final_val = round(((10 ** 9) * x_given_word * prob_word), 6)
            correction_list.append(
                correction(candidate_correction, correct_letter, error_letter,
                           x_given_w, x_given_word, prob_word,
                           final_val,error_type,error_position))
    return correction_list, trans_word_list, trans_prune_list

#function checking for a valid input
def is_valid_word(word):
    return not any(char.isdigit() for char in word)

#function for a valid input
def miss_spelled_words():
    # create a dictionary from list of table
    temp_dict = {}
    delete_table_dict = create_dict(tables.del_table)
    add_table_dict = create_dict(tables.add_table)
    sub_table_dict = create_dict(tables.sub_table)
    transpose_table_dict = create_dict(tables.transpose_table)
    read_json = open("json-data.json", 'r')  # unjson the json file
    complete_dict = json.load(read_json)
    total_count = sum(complete_dict["words"].values())
    read_json.close()
    for i in range(1, len(sys.argv)):  # perform processing for each
        # of the passed mis-spelled word
        if (not is_valid_word(sys.argv[i])):
            print("\n", sys.argv[i], " is not valid word")
            continue
        correction_list, ins_word_list, ins_prune_list = \
            insertion(sys.argv[i], complete_dict, total_count,
                      delete_table_dict)
        correction_list, del_word_list, del_prune_list = \
            deletion(sys.argv[i], complete_dict, total_count,
                     add_table_dict)
        correction_list, sub_word_list, sub_prune_list = \
            substitution(sys.argv[i], complete_dict, total_count,
                         sub_table_dict)
        correction_list, trans_word_list, trans_prune_list =\
            transposition(sys.argv[i], complete_dict,
                          total_count,transpose_table_dict)
        #printing number of unique words, words
        print(" ")
        print("Number of unique words =   {:>10} "
              .format(len(complete_dict["words"].values())))
        print("Number of words        =   {:10} "
              .format(sum(complete_dict["words"].values())))
        print(" ")
        print("Current word being corrected is: ", sys.argv[i])
        print(" ")
        #printing number of possible corrections and pruning list
        print("No. of possible corrections using insertion is {:>1}"
              .format(len(del_word_list)))
        print("After pruning the list contains {:>1}"
              .format(len(del_prune_list)))
        print(" ")
        print("No. of possible corrections using deletion is {:>1}"
              .format(len(ins_word_list)))
        print("After pruning the list contains {:>1}"
              .format(len(ins_prune_list)))
        print(" ")
        print("No. of possible corrections using substitution is {:>1}"
              .format(len(sub_word_list)))
        print("After pruning the list contains {:>1}"
              .format(len(sub_prune_list)))
        print(" ")
        print("No. of possible corrections using transposition is {:>1}"
              .format(len(trans_word_list)))
        print("After pruning the list contains {:>1}"
              .format(len(trans_prune_list)))
        print(" ")
        #printing table
        print("{:<18} {:<10} {:<10}{:<8}  {:<9}  {:<9}  {:<13} "
        .format("Candidate", "Err", "Err", "Cor", "Err", "x|w", "P(x|w)"), end="")
        print("{:<13} {:<12} ".format("P(word)", "10^9 * (P(x|w) P(w)"))
        print("{:<19}{:<11}{:<10}{:<10}{:<10}"
        .format("Corr", "Typ", "Pos", "Let", "Let"), end="")
        print(" {:<12}{:<12}".format("       ", "           "))
        print(" ")
        #sorting the correction_list
        correction_update = sorted(correction_list,
            key=operator.attrgetter('final_val'), reverse=True)
        #printing the fields required for the table
        for j in range(len(correction_update)):
            #adding the probability of duplicate entries
            if correction_update[j].candidate_correction not in temp_dict:
                temp_dict[correction_update[j].candidate_correction] =\
                    correction_update[j].final_val
            else:
                temp_dict[correction_update[j].candidate_correction] =\
                    temp_dict[correction_update[j].candidate_correction] \
                                        + correction_update[j].final_val
            sort_temp = sorted(temp_dict.items(),
                               key=operator.itemgetter(1), reverse=True)
            print("{:<19}".format(correction_update[j]
                         .candidate_correction), end="")
            print("{:<11}".format(correction_update[j].error_type), end="")
            print("{:<10}".format(correction_update[j].error_position), end="")
            print("{:<10}{:<11}".format(correction_update[j].correct_letter,
                         correction_update[j].error_letter), end="")
            print("{:<11}{:<.10f}{:<2}"
                  .format(correction_update[j].x_given_w,
                          correction_update[j].x_given_word, " "), end="")
            print("{:<5.10f} {}"
                  .format(correction_update[j].prob_word, " "), end="")
            print("{:^.6f}         {}"
                  .format(correction_update[j].final_val, " "))
        print(" ")
        print("EXTRA CREDIT")
        print(" ")
        print("{:<20}{:>10}".format("Candidate", "10^9 * (P(x|w) P(w)"))
        print(" ")
        temp_dict.clear()
        for a, b in sort_temp:
            print("{:10}{:>18.6f}".format(a, b))

        correction_list.clear()

if len(sys.argv) < 2:
    # exiting if none provided
    print("Expected at least one Mispelled word as an argument.")
    sys.exit()
else:
    miss_spelled_words()
