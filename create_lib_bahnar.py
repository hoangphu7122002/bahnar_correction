#ref:
#https://github.com/martinakaduc/bana-tts/blob/master/data/bahnar_lexicon.txt
#https://github.com/buingohoanglong/bahnaric-ocr
#https://github.com/buingohoanglong/vietnamese-bahnaric-nmt-data/blob/master/bana-augmentation/new_output/bird_list_bana.txt
#https://github.com/buingohoanglong/vietnamese-bahnaric-nmt-data/tree/master/bana-augmentation/inputs_old

#phase process: bahnar_lexicon.txt
import json

one_bahnar = set()
with open('lib_bahnar\\bahnar_lexicon.txt','r',encoding='utf-8') as f:
    words = f.readlines()
    for word in words:
        tok = word.split('\t')[0]
        tok = tok.replace('\n','')
        one_bahnar.add(tok)
    
#phase process all other file:
second_bahnar = set()
for d_file in ['lib_bahnar\\bahnar_ba.txt','lib_bahnar\\birlist_bahnar.txt']:
    with open(d_file,'r',encoding='utf-8') as f:
        words = f.readlines()
        for word in words:
            token = word.split(' ')
            for tok in token:
                tok = tok.replace('\n','')
                one_bahnar.add(tok)
            for i in range(1,len(token)):
                second_bahnar.add(token[i - 1].replace('\n','') + ' ' + token[i].replace('\n',''))

one_bahnar = list(one_bahnar)
second_bahnar = list(second_bahnar)

dict_one_bahnar = {ele:0 for ele in one_bahnar}
dict_second_bahnar = {ele:0 for ele in second_bahnar}
    
with open('preprocess_bahnar\\dict_one_bahnar.json', 'w') as fp:
    json.dump(dict_one_bahnar, fp)
with open('preprocess_bahnar\\dict_second_bahnar.json', 'w') as fp:
    json.dump(dict_second_bahnar, fp)