import random
import os
import json
dir_path = os.path.dirname(os.path.realpath(__file__))

f = open(dir_path + "/../actions/data.json", "r", encoding='utf-8')
data:dict = json.loads(f.read())

drug_names = []

for name in data:
    drug_names.append(name)

n = int(input("how many drugs needed?!"))
for x in range(n):
    index1 = random.randrange(0,len(drug_names))
    index2 = random.randrange(0,len(drug_names))
    # "    - ["+ drug_names[index1] +"](drug_name) و ["+ drug_names[index2] +"](drug_name) مثل همن؟"
    print("    - آیا ["+ drug_names[index1] +"](drug_name) برای ["+ drug_names[index2] +"](drug_name) بده؟")

