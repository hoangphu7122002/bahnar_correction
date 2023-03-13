from scan_bahnar import *
import json

fi = open("preprocess_bahnar\\dict_one_bahnar.json", encoding='utf-8')
bahnar_one_dict = json.load(fi)

print(bahnar_one_dict)
