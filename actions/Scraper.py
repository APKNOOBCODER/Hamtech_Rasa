# import json
# import requests as rq
# from bs4 import BeautifulSoup as BS
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

import winsound


# with open(dir_path + "/" +"new_data.json","r", encoding='utf-8') as f:
#     data: dict = json.loads(f.read())

# start = 101
# data_count = 2000

# for t in range(start, data_count + 1):
#     print(t)
#     # site url
#     URL = "http://irc.fda.gov.ir/nfi/Detail/%s" % t
#     # site response
#     res = rq.get(URL)
#     # get body
#     Body = BS(res.content, 'html.parser').find('body')

#     # Mechanisms:
#     try:
#         mmd = Body.find('div', {'class': 'i-circle warning'})
#         mmd.find('div')
#     except AttributeError:
#         Names = []
#         NamesGrid = Body.find_all('td', {'class': 'TxtSearchGrid'})
#         # print(len(Names))
#         for x in range(len(NamesGrid)):
#             Name = NamesGrid[x].text
#             if(x % 2 == 0 and Name not in Names):
#                 Names.append(Name)
#         for x in Names:
#             data[x].update({'Sames': Names})
    
# with open(dir_path + "/" +"new_data.json","w", encoding='utf-8') as f:
#     json.dump(data, f, indent=4, ensure_ascii=False)

# frequency = 2500  # Set Frequency To 2500 Hertz
# duration = 1000  # Set Duration To 1000 ms == 1 second
# winsound.Beep(frequency, duration)

# # data_old = json.loads(f.read())
# # data_load.update(data)
# # f.close()
# # f = open("new_data.json", "w", encoding='utf-8')
# # json.dump(data, f, indent=4, ensure_ascii=False)
# # f.close()

import json
import time
import requests as rq
from bs4 import BeautifulSoup as BS

Drugs_Data = {}

start = 1
data_count = 35011
m = 0

for t in range(start, data_count + 1):
    if(m > 20):
        t += 1
    print(t)
    if(t % 1000 == 0):
        time.sleep(20)
    # site url
    URL = "http://irc.fda.gov.ir/nfi/Detail/%s" % t
    try:
        # site response
        res = rq.get(URL)
        # get body
        Body = BS(res.content, 'html.parser').find('body')
        # get header
        Head = BS(res.content, 'html.parser').find('head')

        try:
            mmd = Body.find('div', {'class': 'i-circle warning'})
            mmd.find('div')
        except AttributeError:
            Sames = []
            NamesGrid = Body.find_all('td', {'class': 'TxtSearchGrid'})
            for x in range(len(NamesGrid)):
                Name = NamesGrid[x].text
                if(x % 2 == 0 and Name not in Sames):
                    Sames.append(Name)
            # Name = Body.find_all('span',{'class': 'txtAlignLTR'})[0].text
            Mechanism = Body.find('div', {'class':
                                        'col-lg-12 col-md-12 col-sm-12 col-xs-12 searchRowDetail2'})
            # Price
            try:
                Price = Body.find_all('span', {'class': 'txtAlignLTRFa priceTxt'})[0].text
                Price = Price.replace('\r', '')
                Price = Price.replace('\n', '')
                Price = Price.replace(' ', '')
            except:
                Price = "0"

            Usage = Mechanism.find_all('span', {'class': "txtSearch1"})[0].text
            mechanism = Mechanism.find_all('span', {'class': "txtSearch1"})[1].text
            Pharmaceutic = Mechanism.find_all('span', {'class': "txtSearch1"})[2].text

            Mechanisms = {'Usage': Usage, 'Mechanism': mechanism, 'Pharmaceutic': Pharmaceutic}

            # Cautions:
            Caution = Body.find('div', {'class':
                                        'col-lg-12 col-md-12 col-sm-12 col-xs-12 searchRowDetail3'})

            Warnings = Caution.find_all('span', {'class': "txtSearch1"})[0].text
            Side_Effects = Caution.find_all('span', {'class': "txtSearch1"})[1].text
            Drug_Interferences = Caution.find_all('span', {'class': "txtSearch1"})[2].text
            Recommended_Tips = Caution.find_all('span', {'class': "txtSearch1"})[3].text

            Cautions = {'Warnings': Warnings, 'Side_Effects': Side_Effects, 'Drug_Interferences': Drug_Interferences,
                        'Recommended_Tips': Recommended_Tips}
            
            Title = Head.find('title').text
            # Mechanisms
            try:
                oldM: list = Drugs_Data[Title]['Mechanisms']
                if Mechanisms not in oldM:
                    oldM.append(Mechanisms)
            except:
                try:
                    Drugs_Data[Title].update({'Mechanisms':[Mechanisms]})
                except:
                    Drugs_Data.update({Title: {'Mechanisms': [Mechanisms]}})
            # Cautions
            try:
                oldC: list = Drugs_Data[Title]['Cautions']
                if Cautions not in oldCM:
                    oldC.append(Cautions)
            except:
                try:
                    Drugs_Data[Title].update({'Cautions':[Cautions]})
                except:
                    Drugs_Data.update({Title: {'Cautions': [Cautions]}})
            # Sames
            try:
                oldS: list = Drugs_Data[Title]['Sames']
                for same in Sames:
                    if same not in oldS:
                        oldS.append(same)
            except:
                try:
                    Drugs_Data[Title].update({'Sames':Sames})
                except:
                    Drugs_Data.update({Title: {'Sames': Sames}})
            # Price
            try:
                oldP: list = Drugs_Data[Title]['Price']
                if Price not in oldP:
                    oldP.append(Price)
            except:
                try:
                    Drugs_Data[Title].update({'Price':[Price]})
                except:
                    Drugs_Data.update({Title: {'Price': [Price]}})
            

            # Drugs_Data.update({Title: {'Mechanisms': Mechanisms, 'Cautions': Cautions, 'Sames': Names}})
            # print(Usage)
            # print(mechanism)
            # print(pharmacokintig)
            # print(Warnings)
            # print(Side_Effects)
            # print(Drug_Interferences)
            # print(Recommended_Tips)
            # print(Drugs_Data)
            m = 0
            f = open("new_data_copy.json", "r", encoding='utf-8')
            data = json.loads(f.read())
            data.update(Drugs_Data)
            f.close()
            f = open("new_data_copy.json", "w", encoding='utf-8')
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.close()
    except:
        m += 1
        t -= 1
# data = {}

