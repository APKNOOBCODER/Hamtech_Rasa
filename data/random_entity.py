import random
import os
import json
import yaml

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path + "/nlu.yml", "r", encoding='utf-8') as f:
    nluyml:dict = yaml.full_load(f)
    drugL:str = nluyml["nlu"][21]["examples"]
    symptomL:str = nluyml["nlu"][22]["examples"]
    illnessL:str = nluyml["nlu"][23]["examples"]
    drugList:list = drugL[2:-1].split("\n- ")
    symptomList:list = symptomL[2:-1].split("\n- ")
    illnessList:list = illnessL[2:-1].split("\n- ")
    # print(drugList)
"""

for name in data:
    drug_names.append(name)
"""
n = int(input("how many drugs needed?!"))
for x in range(n):
    dindex1 = random.randrange(0,len(drugList))
    dindex2 = random.randrange(0,len(drugList))
    sindex = random.randrange(0,len(symptomList))
    iindex = random.randrange(0,len(illnessList))
    # "    - ["+ drug_names[index1] +"](drug_name) و ["+ drug_names[index2] +"](drug_name) مثل همن؟"
    # [" + drugList[dindex1] + "](drug_name)
    # print(symptomList[sindex])
    print("    - چه دارو هایی رو نباید با [" + drugList[dindex1] + "](drug_name) بخورم؟")
