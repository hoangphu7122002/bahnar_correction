#return true: if vi, else: bahnar
import json
import re
import secrets
import string
from scan_bahnar import *

punc = string.punctuation

fi = open("preprocess_vi\\dict_one_vi.json", encoding='utf-8')
one_dict = json.load(fi)

fi = open("preprocess_vi\\dict_second_vi.json", encoding='utf-8')
second_dict = json.load(fi)

fi = open("preprocess_bahnar\\dict_one_bahnar.json", encoding='utf-8')
bahnar_one_dict = json.load(fi)

fi = open("preprocess_bahnar\\dict_second_bahnar.json", encoding='utf-8')
bahnar_second_dict = json.load(fi)

def similarity_word(tok1,tok2):
    count = 0
    for i in range(min(len(tok1),len(tok2))):
        if tok1[i] == tok2[i]:
            count += 1
    if min(len(tok1),len(tok2)) == 0:
        return 0
    return count / (1.0 * min(len(tok1),len(tok2)))

def check_replace(token):
    flag = False
    for ele in range(0,10):
        if str(ele) in token:
            flag = True
            break
    for ele in punc:
        if ele == '-' or ele == ',' or ele == '.' or '\'': #error in tokenize
            continue
        if ele in token:
            flag = True
            break
    return flag

def check_sentence(line):
    token = line.split(' ')
    count_vi = 0
    for tok in token:
        if tok in one_dict.keys():
            count_vi += 1
    if count_vi >= 0.8 * len(token):
        return True
    return False

def check_phase_single(tok,one_dict=one_dict):
    if tok in one_dict.keys():
        return True
    return False

def check_phase_couple(tok,second_dict=second_dict):
    if tok in second_dict.keys():
        return True
    return False

def find_match_pre(tok1,tok2,second_dict = second_dict):
    candidate = []
    for ele in second_dict.keys():
        ele = ele.split(' ')
        if ele[0] == tok1:
            candidate.append(ele[1])
    
    max_point = 0.0
    max_ele = []
    for i in range(len(candidate)):
        if similarity_word(tok2,candidate[i]) > max_point:
            max_ele = [candidate[i]]
            max_point = similarity_word(tok2,candidate[i])
        elif similarity_word(tok2,candidate[i]) == max_point:
            max_ele.append(candidate[i])
    return max_ele
    
def find_single_word(tok1,one_dict = one_dict):
    max_point = 0.0
    max_ele = []
    for ele in one_dict.keys():
        if similarity_word(tok1,ele) > max_point:    
            max_ele = [ele]
            max_point = similarity_word(tok1,ele)
        elif similarity_word(tok1,ele) == max_point:
            max_ele.append(ele)
    max_ele += [tok1]
    return secrets.choice(max_ele)
    
def find_match_pos(tok1,tok2,second_dict=second_dict):
    candidate = []
    for ele in second_dict.keys():
        ele = ele.split(' ')
        if ele[1] == tok2:
            candidate.append(ele[0])
    
    max_point = 0.0
    max_ele = []
    for i in range(len(candidate)):
        if similarity_word(tok1,candidate[i]) > max_point:
            max_ele = [candidate[i]]
            max_point = similarity_word(tok1,candidate[i])
        elif similarity_word(tok1,candidate[i]) == max_point:
            max_ele.append(candidate[i])
    return max_ele
        
def find_fix_ele(lst1,lst2,tok=''):
    candidate = set()
    for ele1 in lst1:
        for ele2 in lst2:
            if ele1 == ele2:
                candidate.add(ele1)
    candidate = list(candidate)
    if len(candidate) == 0:
        if tok != '': 
            if check_replace(tok):
                return secrets.choice(lst1 + lst2)
            return tok
    return secrets.choice(candidate)
    
#dau cau
def process_vi(line):
    sen = ''
    token = line.split(' ')
    if len(token) == 0:
        return sen

    if len(token) == 1:
        i = 0
        if (token[i] in punc) or (token[i] in one_dict.keys()) or (set(list(token[i])).intersection(set(punc)) != []) or (token[i] in bahnar_one_dict.keys()):
            sen = sen + token[i] + ' ' #dung chinh ta
        else:
            sen = sen + token[i] + '#E ' #giu nguyen
        return sen[:-1]
    for i in range(len(token)):
        if i == 0:
            whole_sen = token[i] + ' ' + token[i + 1]
            if check_phase_single(token[i]) and check_phase_couple(whole_sen):
                sen = sen + token[i] + ' ' #dung chinh ta
            elif check_phase_single(token[i]):
                pos = find_match_pos(token[i],token[i + 1])
                if len(pos) == 0:
                    sen = sen + token[i] + '#E ' #giu nguyen
                else:
                    if check_replace(token[i]):
                        sen = sen + secrets.choice(pos) + ' '
                    else:
                        sen = sen + token[i] + ' '
            else:
                if (token[i] in punc)  or (set(list(token[i])).intersection(set(punc)) != []) or (token[i] in bahnar_one_dict.keys()):
                    sen = sen + token[i] + ' ' #giu nguyen
                else:
                    if check_replace(token[i]):
                        sen = sen + find_single_word(token[i]) + ' '
                    else:
                        sen = sen + token[i] + ' ' 
        if i >= 1 and i < len(token) - 1:
            # print(token[i-1],token[i + 1])
            whole_sen_1 = token[i] + ' ' + token[i + 1]
            whole_sen_2 = token[i - 1] + ' ' + token[i] 
            if check_phase_single(token[i]) and (check_phase_couple(whole_sen_1) or check_phase_couple(whole_sen_2)):
                sen = sen + token[i] + ' ' #dung chinh ta
            elif check_phase_single(token[i]):
                pos = find_match_pos(token[i],token[i + 1])
                pre = find_match_pre(token[i-1],token[i])
                if len(pos) + len(pre) == 0 :
                    sen = sen + token[i] + '#E ' #giu nguyen
                else:
                    sen = sen + find_fix_ele(pos,pre,token[i]) + ' '
            else:
                if (token[i] in punc)  or (set(list(token[i])).intersection(set(punc)) != []) or (token[i] in bahnar_one_dict.keys()):
                    sen = sen + token[i] + ' ' #giu nguyen
                else:
                    if check_replace(token[i]):
                        sen = sen + find_single_word(token[i]) + ' ' #giu nguyen
                    else:
                        sen = sen + token[i] + ' ' #giu nguyen
        if i == len(token) - 1:
            whole_sen = token[i - 1] + ' ' + token[i]
            if check_phase_single(token[i]) and check_phase_couple(whole_sen):
                sen = sen + token[i] + ' ' #dung chinh ta
            elif check_phase_single(token[i]):
                pre = find_match_pre(token[i - 1],token[i])
                if len(pre) == 0:
                    sen = sen + token[i] + '#E ' #giu nguyen
                else:
                    if check_replace(token[i]):
                        sen = sen + secrets.choice(pre) + ' '
                    else:
                        sen = sen + token[i] + ' '
            else:
                if (token[i] in punc)  or (set(list(token[i])).intersection(set(punc)) != []) or (token[i] in bahnar_one_dict.keys()):
                    sen = sen + token[i] + ' ' #giu nguyen
                else:
                    if check_replace(token[i]):
                        sen = sen + find_single_word(token[i]) + ' ' #giu nguyen    
                    else:
                        sen = sen + token[i] + ' '
    sen = sen[:-1]
    return sen 
    
    
def process_bahnar(line):
    sen = ''
    for original, replace in dict_don.items():
        line = line.replace(original, replace)
    token = line.split(' ')
    if len(token) == 0:
        return sen

    if len(token) == 1:
        i = 0
        if (token[i] in punc) or (token[i] in one_dict.keys()) or (set(list(token[i])).intersection(set(punc)) != []):
            sen = sen + token[i] + ' ' #dung chinh ta
        else:
            if check_replace(token[i]):
                sen = sen + find_single_word(token[i]) + ' ' #giu nguyen
            else:
                sen = sen + token[i] + ' ' 
        return sen[:-1]
    for i in range(len(token)):
        if i == 0:
            whole_sen = token[i] + ' ' + token[i + 1]
            if check_phase_single(token[i],bahnar_one_dict) and check_phase_couple(whole_sen,bahnar_second_dict):
                sen = sen + token[i] + ' ' #dung chinh ta
            elif check_phase_single(token[i],bahnar_one_dict):
                pos = find_match_pos(token[i],token[i + 1],bahnar_second_dict)
                if len(pos) == 0:
                    sen = sen + token[i] + '#E ' #giu nguyen
                else:
                    if check_replace(token[i]):
                        sen = sen + secrets.choice(pos) + ' '
                    else:
                        sen = sen + token[i] + ' '
            else:
                if (token[i] in punc)  or (set(list(token[i])).intersection(set(punc)) != []):
                    sen = sen + token[i] + ' ' #giu nguyen
                else:
                    if check_replace(token[i]):
                        sen = sen + find_single_word(token[i]) + ' ' #giu nguyen
                    else:
                        sen = sen + token[i] + ' ' #giu nguyen
        if i >= 1 and i < len(token) - 1:
            whole_sen_1 = token[i] + ' ' + token[i + 1]
            whole_sen_2 = token[i - 1] + ' ' + token[i] 
            # print(token[i-1],token[i + 1])
            if check_phase_single(token[i],bahnar_one_dict) and (check_phase_couple(whole_sen_1,bahnar_second_dict) or check_phase_couple(whole_sen_2,bahnar_second_dict)):
                sen = sen + token[i] + ' ' #dung chinh ta
            elif check_phase_single(token[i],bahnar_one_dict):
                pos = find_match_pos(token[i],token[i + 1],bahnar_second_dict)
                pre = find_match_pre(token[i-1],token[i],bahnar_second_dict)
                if len(pos) + len(pre) == 0 :
                    sen = sen + token[i] + '#E ' #giu nguyen
                else:
                    sen = sen + find_fix_ele(pos,pre,token[i]) + ' '
            else:
                if (token[i] in punc)  or (set(list(token[i])).intersection(set(punc)) != []):
                    sen = sen + token[i] + ' ' #giu nguyen
                else:
                    if check_replace(token[i]):
                        sen = sen + find_single_word(token[i]) + ' ' #giu nguyen
                    else:
                        sen = sen + token[i] + ' '
        if i == len(token) - 1:
            whole_sen = token[i - 1] + ' ' + token[i]
            if check_phase_single(token[i],bahnar_one_dict) and check_phase_couple(whole_sen,bahnar_second_dict):
                sen = sen + token[i] + ' ' #dung chinh ta
            elif check_phase_single(token[i],bahnar_one_dict):
                pre = find_match_pre(token[i - 1],token[i],bahnar_second_dict)
                if len(pre) == 0:
                    sen = sen + token[i] + '#E ' #giu nguyen
                else:
                    if check_replace(token[i]):
                        sen = sen + secrets.choice(pre) + ' '
                    else:
                        sen = sen + token[i] + ' '
            else:
                if (token[i] in punc)  or (set(list(token[i])).intersection(set(punc)) != []):
                    sen = sen + token[i] + ' ' #giu nguyen
                else:
                    if check_replace(token[i]):
                        sen = sen + find_single_word(token[i]) + ' ' #giu nguyen    
                    else:
                        sen = sen + token[i] + ' '
    sen = sen[:-1]
    return sen 