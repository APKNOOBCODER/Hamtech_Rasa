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
    index = random.randrange(0,len(drug_names))
    print("    - چقدره قیمت [" + drug_names[index] + "](drug_name)؟")

