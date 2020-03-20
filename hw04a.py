

import re
import sys
from collections import defaultdict
import operator
import time
import json
if(len(sys.argv) > 1):
    filename = sys.argv[1]
else:
    filename = "ap88.txt"
try:
    in_file = open(filename,'r')
except IOError:
    print('cannot open',filename)
    exit()
#initializing unigram,bigram and word dictionaries
word_dict= defaultdict(int)
unigram = defaultdict(int)
bigram = defaultdict(int)
start_time=time.perf_counter()
start_cpu_time=time.process_time()
count = 0

#removing AP tag and data clean up
for line in in_file:
    #removing AP tag ,replacing every char by space which is not an ascii value
    #converting to lower case
    new_line= re.sub('(AP[0-9]+\-[0-9]+)|([^a-zA-Z])'," ", line).lower()
    word_list = new_line.split()#using split to break
    for words in word_list:
        word_dict[words] += 1
        token = "<" + words +">"
        for i in token:
            if i in unigram:
                unigram[i] = unigram[i]+1
            else:
                unigram[i] = 1
        bigram_list = [token[i] + token[i+1] for i in range(len(token) - 1)]
        for val in bigram_list:
            bigram[val] += 1
in_file.close()
end_time= time.perf_counter()
end_cpu_time=time.process_time()
#printing no of unigrams,bugrams,words and distinct words
print("Number of unigrams:{:>5}"
      .format(len(unigram)))
print("Number of bigrams:{:6}"
      .format(len(bigram)))
print(" ")
print("Number Of Words:  {:>18}  "
      .format(sum(word_dict.values())))
print("Number Of Distinct Words: {:10}    "
      .format(len(word_dict), end="\n"))
print(" ")

#sorting word_dict
sorted_word_dict = sorted(word_dict.items(),
key=operator.itemgetter(1), reverse = True)

#printing the list of top 10 frequency words
print("Top 10 words:", end="\n")
for i in range(len(sorted_word_dict)):
    if count == 10:
        break
    else:
        print("{:<10s} {:>15d}"
              .format(sorted_word_dict[i][0] , sorted_word_dict[i][1]))
        count += 1
print(" ")
print("start time   {0:>17.4f}, cpu time {0:>18.4f}"
      .format(start_time,start_cpu_time))
print("end time   {0:>19.4f}, cpu time {0:>18.4f}"
      .format(end_time,end_cpu_time ))
print("total elapsed time   {:>9.4f}, cpu time {:>18.4f}"
      .format(end_time-start_time,end_cpu_time - start_cpu_time))
print(" ")
sorted_unigram=  sorted(unigram.keys())
x = {"unigrams":unigram,"bigrams":bigram,"words":word_dict}
my_file=open("json-data.json","w") #unjson the json file
json.dump(x, my_file)
my_file.close()
