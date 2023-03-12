#ref lib: https://github.com/thuy-le-ep/Vietnamese-data

import glob
import json

data_path = "lib_vi/"
data_files = glob.glob(data_path + '*.txt')
print(data_files)

data_files = reversed(data_files)

one_vi = set()
second_vi = set()
upper_vi = set()

for d_file in data_files:
    with open(d_file,'r',encoding='utf-8') as f:
        words = f.readlines()
    for word in words:
        word_lst = word.split(' ')
        if len(word_lst) == 0:
            continue
        if len(word_lst) == 1:
            one_vi.add(word[0])
        elif len(word_lst) == 2:
            second_vi.add(word)
            one_vi.add(word_lst[0])
            one_vi.add(word_lst[1])
        elif len(word_lst) >= 3:
            upper_vi.add(word)
            for w in word_lst:
                one_vi.add(w)
            for i in range(1,len(word_lst)):
                second_vi.add(word_lst[i - 1] + ' ' + word_lst[i])
    
one_vi = list(one_vi)
second_vi = list(second_vi)
upper_vi = list(upper_vi)

dict_one_vi = {ele:0 for ele in one_vi}
dict_second_vi = {ele:0 for ele in second_vi}
dict_upper_vi = {ele:0 for ele in upper_vi}
with open('preprocess_vi\\dict_one_vi.json', 'w') as fp:
    json.dump(dict_one_vi, fp)
with open('preprocess_vi\\dict_second_vi.json', 'w') as fp:
    json.dump(dict_second_vi, fp)
with open('preprocess_vi\\dict_upper_vi.json', 'w') as fp:
    json.dump(dict_upper_vi, fp)




