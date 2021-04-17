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
        # tracker.latest_massage.entity[]
        
        ### another way:
        # ent = tracker.latest_message['entities']
        # I want to cook noodles.
        # output: 
        ('entity', 
        [{u'extractor': u'ner_crf', 
        u'confidence': 0.787280111194543,
        u'end': 19, 
        u'value': u'noodles', 
        u'entity':
        u'Dish',
        u'start': 13
        }])
        # findout that intent is correct
        confidence = tracker.latest_massage['intent']['confidence']
        if confidence < 0.3:
            dispatcher.utter_message(text='متوجه نشدم، لطفا دوباره تلاش کنید')
            break
        # end
        drug_name = next(tracker.get_latest_entity_values('drug_name'), None)
        # drug_name = tracker.get_latest_entity_values(entity_type="drug_name")
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        print(drug_name)
        # print(drug_name[0])
        usage = 'اطلاعاتی موجود نیست. این اتفاق احتمالا به خاطر اشتباه تایپی در نوشتار دارو به زبان فارسی رخ داده. لطفا نحوه نوشتار آن را به دقت از روی جعبه دارو به دست آورید.'
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
        # findout that intent is correct
        confidence = tracker.latest_massage['intent']['confidence']
        if confidence < 0.3:
            dispatcher.utter_message(text='متوجه نشدم، لطفا دوباره تلاش کنید')
            break
        # end
        ans = 'اطلاعاتی یافت نشد. لطفا به نوشتار فارسی دارو و علائم گفته شده در سوال خود دقت فرمایید.'
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
        # findout that intent is correct
        confidence = tracker.latest_massage['intent']['confidence']
        if confidence < 0.3:
            dispatcher.utter_message(text='متوجه نشدم، لطفا دوباره تلاش کنید')
            break
        # end
        ans = 'اطلاعاتی یافت نشد. لطفا به نوشتار فارسی دارو و بیماری گفته شده در سوال خود دقت فرمایید.'
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
        # findout that intent is correct
        confidence = tracker.latest_massage['intent']['confidence']
        if confidence < 0.3:
            dispatcher.utter_message(text='متوجه نشدم، لطفا دوباره تلاش کنید')
            break
        # end
        symptom = next(tracker.get_latest_entity_values('symptom'), None)
        # drug_name = tracker.get_latest_entity_values(entity_type="drug_name")
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        # print(drug_name[0])
        ans = 'دارویی برای چنین علائمی یافت نشد. لطفا به نحوه نوشتار علائم گفته شده در سوالتان دقت کنید.'
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
        # findout that intent is correct
        confidence = tracker.latest_massage['intent']['confidence']
        if confidence < 0.3:
            dispatcher.utter_message(text='متوجه نشدم، لطفا دوباره تلاش کنید')
            break
        # end
        illness = next(tracker.get_latest_entity_values('illness'), None)
        # drug_name = tracker.get_latest_entity_values(entity_type="drug_name")
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        # print(drug_name[0])
        ans = 'دارویی برای چنین بیماری ای یافت نشد. لطفا به نحوه نوشتار بیماری گفته شده در سوالتان دقت کنید.'
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
class ActionDrugInterferences1(Action):

    def name(self) -> Text:
        return "action_answer_drug_interferences_1"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        confidence = tracker.latest_massage['intent']['confidence']
        if confidence < 0.3:
            dispatcher.utter_message(text='متوجه نشدم، لطفا دوباره تلاش کنید')
            break
        # end
        drug_name = next(tracker.get_latest_entity_values('drug_name'), None)
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        ans = 'تداخل دارویی برای داروی %s یافت نشد' % drug_name

        for name in data:
            if name == drug_name or drug_name in name:
                ans = data[name]['Cautions']['Drug_Interferences']
        dispatcher.utter_message(text=ans)

class ActionDrugInterferences2(Action):

    def name(self) -> Text:
        return "action_answer_drug_interferences_2"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        confidence = tracker.latest_massage['intent']['confidence']
        if confidence < 0.3:
            dispatcher.utter_message(text='متوجه نشدم، لطفا دوباره تلاش کنید')
            break
        # end
        drug_names = []
        drug_name = next(tracker.get_latest_entity_values('drug_name'), None)
        drug_names.append(drug_name)
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        ans = 'تداخل دارویی برای دارو های موجود در پرسش یافت نشد'
        for drug_name_1 in drug_names:
            for drug_name_2 in drug_names:
                for name in data:
                    if name == drug_name_1 or drug_name_1 in name:
                        Drug_Interferences = data[name]['Cautions']['Drug_Interferences']
                        if drug_name_2 in Drug_Interferences and ans == 'تداخل دارویی برای دارو های موجود در پرسش یافت نشد':
                            ans = 'بلی. دارو ها با هم تداخل دارند: \n %s' % Drug_Interferences
                        elif drug_name_2 in Drug_Interferences:
                            ans += '\n %s' % Drug_Interferences

        dispatcher.utter_message(text=ans)

## avarez
class SideEffects1(Action):

    def name(self) -> Text:
        return "action_answer_side_effects_1"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        confidence = tracker.latest_massage['intent']['confidence']
        if confidence < 0.3:
            dispatcher.utter_message(text='متوجه نشدم، لطفا دوباره تلاش کنید')
            break
        # end
        drug_name = next(tracker.get_latest_entity_values('drug_name'), None)
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        ans = 'عوارض جانبی برای داروی %s یافت نشد' % drug_name

        for name in data:
            if name == drug_name or drug_name in name:
                ans = data[name]['Cautions']['Side_Effects']
        dispatcher.utter_message(text=ans)

## khatar
class ActionAnswerDrugCaution1(Action):

    def name(self) -> Text:
        return "action_answer_drug_caution_1"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        confidence = tracker.latest_massage['intent']['confidence']
        if confidence < 0.3:
            dispatcher.utter_message(text='متوجه نشدم، لطفا دوباره تلاش کنید')
            break
        # end
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
class ActionAnswerWarning1(Action):

    def name(self) -> Text:
        return "action_answer_warning_1"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        confidence = tracker.latest_massage['intent']['confidence']
        if confidence < 0.3:
            dispatcher.utter_message(text='متوجه نشدم، لطفا دوباره تلاش کنید')
            break
        # end
        drug_name = next(tracker.get_latest_entity_values('drug_name'), None)
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        ans = 'هیچ هشداری برای داروی %s یافت نشد' % drug_name

        for name in data:
            if name == drug_name or drug_name in name:
                ans = data[name]['Cautions']['Warnings']
        dispatcher.utter_message(text=ans)

class ActionAnswerWarning2(Action):

    def name(self) -> Text:
        return "action_answer_warning_2"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        confidence = tracker.latest_massage['intent']['confidence']
        if confidence < 0.3:
            dispatcher.utter_message(text='متوجه نشدم، لطفا دوباره تلاش کنید')
            break
        # end
        drug_name = next(tracker.get_latest_entity_values('drug_name'), None)
        illness = next(tracker.get_latest_entity_values('illness'), None)
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        ans = 'هیچ هشداری برای داروی مورد نظر در تداخل با بیماری یافت نشد'

        for name in data:
            if name == drug_name or drug_name in name:
                warning  = data[name]['Cautions']['Warnings']
                if illness in warning:
                    ans = 'بلی، داروی مورد نظر با بیماری موجود در پرسش در تداخل است: \n %s' % warning
        dispatcher.utter_message(text=ans)

## nokte
class ActionAnswerHowToUse1(Action):

    def name(self) -> Text:
        return "action_answer_how_to_use_1"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        confidence = tracker.latest_massage['intent']['confidence']
        if confidence < 0.3:
            dispatcher.utter_message(text='متوجه نشدم، لطفا دوباره تلاش کنید')
            break
        # end
        drug_name = next(tracker.get_latest_entity_values('drug_name'), None)
        with open(dir_path + '/' + 'data.json','r') as f:
            data: dict = json.loads(f.read())
        ans = 'عوارض جانبی برای داروی %s یافت نشد' % drug_name

        for name in data:
            if name == drug_name or drug_name in name:
                ans = data[name]['Cautions']['Recommended_Tips']
        dispatcher.utter_message(text=ans)