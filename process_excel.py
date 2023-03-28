from util import *
import time
import pandas as pd
import os

name = 'Bok Set phat rung 246-483.xlsx'


def process_text(name):
    print(name)
    df = pd.read_excel(name)
    df.columns = [col.upper() for col in df.columns]
    print(df.head())
    lines_bahnar = []
    lines_vi = []
    for i,col in enumerate(df.columns):
        if i == len(df.columns) - 2:
            lines_bahnar = df[col].to_list()
        if i == len(df.columns) - 1:
            lines_vi = df[col].to_list()
    
    lines = []
    print(lines_bahnar)
    print(lines_vi)
    for text in lines_bahnar:
        try:
            for original, replace in radioContentMap.items():
                text = text.replace(original, replace)
            for original, replace in contentSpecialMap.items():
                text = text.replace(original, replace)
            for original, replace in contentMap.items():
                text = text.replace(original, replace)
            lines.append(process_bahnar(text))
        except:
            lines.append(text)
    
    dict_util = {'Tiếng BANA' : lines,
            'Tiếng VIỆT' : lines_vi}
    df = pd.DataFrame.from_dict(dict_util)
    return df

# process_text('doc_csv\GIA LAI\Kinh Thánh Ba Na - Số hóa\Kinh thanh Ba Na_1-83.xlsx').head()
path =r'doc_csv/'
for root, directories, file in os.walk(path):
    for file in file:
        try:
            if file.split('.')[-1] != 'xlsx': continue
            print("================================")
            print(os.path.join(root,file))
            df = process_text(os.path.join(root,file))
            correct_path = os.path.join(root).replace('doc_csv','correct')
            if correct_path[-1] != '/': correct_path += '/'
            if not os.path.exists(correct_path): os.makedirs(correct_path)
            print(correct_path + file)
            df.to_excel(correct_path + file, index=False)
            print("================================")
        except:
            print('Error ' + os.path.join(root,file))
            continue
		    