# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import json
from typing import Any, Text, Dict, List
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

 
class ActionAnswerDrugUsage1(Action):

    def name(self) -> Text:
        return "action_answer_drug_usage_1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        drug_name = next(tracker.get_latest_entity_values('drug_name'), None)
        # drug_name = tracker.get_latest_entity_values(entity_type="drug_name")
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        print(drug_name)
        # print(drug_name[0])
        usage = 'اطلاعاتی موجود نیست'
        for name in data:
            if (name == drug_name) or (drug_name in name):
                usage = data[name]['Mechanisms']['Usage']
        
        dispatcher.utter_message(text="%s"%usage)

        return []

class ActionAnswerDrugUsage2(Action):

    def name(self) -> Text:
        return "action_answer_drug_usage_2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ans = 'اطلاعاتی یافت نشد'
        drug_name = next(tracker.get_latest_entity_values('drug_name'), None)
        symptom = next(tracker.get_latest_entity_values('symptom'), None)
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        # print(drug_name)
        for name in data:
            if name == drug_name:
                usage = data[name]['Mechanisms']['Usage']
                if symptom in usage:
                    ans = 'بلی، ' + drug_name + 'برای موارد زیر استفاده می شود: ' + "\n" + usage
                else:
                    ans = 'خیر، ' + drug_name + 'برای موارد زیر استفاده می شود: ' + "\n" + usage

        
        dispatcher.utter_message(text="%s"%ans)

        return []

class ActionAnswerDrugUsage3(Action):

    def name(self) -> Text:
        return "action_answer_drug_usage_3"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ans = 'اطلاعاتی یافت نشد'
        drug_name = next(tracker.get_latest_entity_values('drug_name'), None)
        illness = next(tracker.get_latest_entity_values('illness'), None)
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        # print(drug_name)
        for name in data:
            if name == drug_name:
                usage = data[name]['Mechanisms']['Usage']
                if illness in usage:
                    ans = 'بلی، ' + drug_name + 'برای موارد زیر استفاده می شود: ' + "\n" + usage
                else:
                    ans = 'خیر، ' + drug_name + 'برای موارد زیر استفاده می شود: ' + "\n" + usage

        
        dispatcher.utter_message(text="%s"%ans)

        return []

class ActionAnswerDrugUsage4(Action):

    def name(self) -> Text:
        return "action_answer_drug_usage_4"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        symptom = next(tracker.get_latest_entity_values('symptom'), None)
        # drug_name = tracker.get_latest_entity_values(entity_type="drug_name")
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        # print(drug_name[0])
        ans = 'دارویی برای چنین علائمی یافت نشد'
        for name in data:
            usage = data[name]['Mechanisms']['Usage']
            if symptom in usage:
                if ans == 'دارویی برای چنین علائمی یافت نشد':
                    ans = ""
                else:
                    ans += " ,"
                ans += name
        
        dispatcher.utter_message(text="%s"%ans)

        return []

class ActionAnswerDrugUsage5(Action):

    def name(self) -> Text:
        return "action_answer_drug_usage_5"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        illness = next(tracker.get_latest_entity_values('illness'), None)
        # drug_name = tracker.get_latest_entity_values(entity_type="drug_name")
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        # print(drug_name[0])
        ans = 'دارویی برای چنین بیماری ای یافت نشد'
        for name in data:
            usage = data[name]['Mechanisms']['Usage']
            if illness in usage:
                if ans == 'دارویی برای چنین بیماری ای یافت نشد':
                    ans = ""
                else:
                    ans += " ,"
                ans += name
        
        dispatcher.utter_message(text="%s"%ans)

        return []

## tadakhol
class ActionAnswerDrugCaution1(Action):

    def name(self) -> Text:
        return "action_answer_drug_caution_1"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        drug_name = next(tracker.get_latest_entity_values('drug_name'), None)
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        ans = 'تداخل دارویی برای داروی %s یافت نشد' % drug_name

        for name in data:
            if name == drug_name or drug_name in name:
                ans = data[name]['Cautions']['Drug_Interferences']
        dispatcher.utter_message(text=ans)

## avarez
class ActionAnswerDrugCaution2(Action):

    def name(self) -> Text:
        return "action_answer_drug_caution_2"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        drug_name = next(tracker.get_latest_entity_values('drug_name'), None)
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        ans = 'عوارض جانبی برای داروی %s یافت نشد' % drug_name

        for name in data:
            if name == drug_name or drug_name in name:
                ans = data[name]['Cautions']['Side_Effects']
        dispatcher.utter_message(text=ans)

## khatar
class ActionAnswerDrugCaution3(Action):

    def name(self) -> Text:
        return "action_answer_drug_caution_3"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        drug_name = next(tracker.get_latest_entity_values('drug_name'), None)
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        ans = 'خطری برای داروی %s یافت نشد' % drug_name

        for name in data:
            if name == drug_name or drug_name in name:
                ans = "هشدار ها: \n " + \
                      data[name]['Cautions']['Warnings'] + "\n" + \
                      "عوارض جانبی: \n" + \
                      data[name]['Cautions']['Side_Effects'] + "\n" + \
                      "تداخلات دارویی: \n" + \
                      data[name]['Cautions']['Drug_Interferences'] + "\n" + \
                      "نکات پیشنهادی: \n" + \
                      data[name]['Cautions']['Recommended_Tips'] + "\n"

        dispatcher.utter_message(text=ans)

## hoshdar
class ActionAnswerDrugCaution4(Action):

    def name(self) -> Text:
        return "action_answer_drug_caution_4"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        drug_name = next(tracker.get_latest_entity_values('drug_name'), None)
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        ans = 'هیچ هشداری برای داروی %s یافت نشد' % drug_name

        for name in data:
            if name == drug_name or drug_name in name:
                ans = data[name]['Cautions']['Warnings']
        dispatcher.utter_message(text=ans)

## nokte
class ActionAnswerDrugCaution5(Action):

    def name(self) -> Text:
        return "action_answer_drug_caution_5"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        drug_name = next(tracker.get_latest_entity_values('drug_name'), None)
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        ans = 'عوارض جانبی برای داروی %s یافت نشد' % drug_name

        for name in data:
            if name == drug_name or drug_name in name:
                ans = data[name]['Cautions']['Recommended_Tips']
        dispatcher.utter_message(text=ans)