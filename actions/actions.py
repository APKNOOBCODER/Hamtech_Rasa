# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import json
import hazm
Norm = hazm.Normalizer()
from typing import Any, Text, Dict, List
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionAnswerGreat(Action):

    def name(self) -> Text:
        return "action_answer_great"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        dispatcher.utter_message(text="درود، من یک ربات برای پاسخ به سوالات دارویی شما هستم. چه کمکی ازم بر می آید؟  \
                                       \nمیتوان این سوالات را در زمینه های زیر بپرسید: \
                                       \n1- موارد مصرف دارو (به علاوه بیماری ها و علائم) \
                                       \n2- تداخل دارویی \
                                       \n3- طریقه مصرف دارو ها \
                                       \n4- نکات و هشدار های مربوط به مصرف دارو ها \
                                       \n5- ناسازگاری های دارویی با بیماری ها \
                                       \n6- قیمت دارو ها \
                                       \n7- نام دارو ها و مشابه آن ها در بازار")
        return []



class ActionAnswerDrugUsage1(Action):

    def name(self) -> Text:
        return "action_answer_drug_usage_1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        ### another way:
        # ent = tracker.latest_message["entities"]
        # I want to cook noodles.
        # output: 
        # ("entity", 
        # [{u"extractor": u"ner_crf", 
        # u"confidence": 0.787280111194543,
        # u"end": 19, 
        # u"value": u"noodles", 
        # u"entity":
        # u"Dish",
        # u"start": 13
        # }])
        # findout that intent is correct
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # end
        drug_name = next(tracker.get_latest_entity_values("drug_name"), None)
        ans = "اطلاعاتی موجود نیست. این اتفاق احتمالا به خاطر اشتباه تایپی در نوشتار دارو به زبان فارسی رخ داده. لطفا نحوه نوشتار آن را به دقت از روی جعبه دارو به دست آورید."
        if drug_name == None:
            dispatcher.utter_message(text=ans)
            return []
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())
        print("drug_name: " + drug_name)
        
        for name in data:
            if (name == drug_name) or (drug_name in name):
                ans = "موارد مصرف داروی " + drug_name + data[name]["Mechanisms"][0]["Usage"]
                ans = Norm.normalize(ans)
                checkans = ans.replace("\r","")
                checkans = checkans.replace("\n","")
                checkans = checkans.replace("موارد مصرف داروی ","")
                checkans = checkans.replace(drug_name,"")
                checkans = checkans.replace(" ", "")
                if checkans != "":
                    break
        print("ans: " + ans)
        ans = ans[:4096]
        checkans = ans.replace("\r","")
        checkans = checkans.replace("\n","")
        checkans = checkans.replace(" ", "")
        if checkans == "":
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        
        dispatcher.utter_message(text=ans)
        # dispatcher.utter_message(text=ans2)

        return [SlotSet("drug_name", drug_name)]

"""
class ActionAnswerDrugUsage1Comp2(Action):

    def name(self) -> Text:
        return "action_answer_drug_usage_1_comp_2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # end

        drug_name = tracker.slots["drug_name"]
        symptom = next(tracker.get_latest_entity_values("symptom"), None)
        ans = "اطلاعاتی یافت نشد. لطفا به نوشتار فارسی دارو و علائم گفته شده در سوال خود دقت فرمایید."
        if drug_name == None or symptom == None:
            dispatcher.utter_message(text=ans)
            return []
        
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())
        print("drug_name: " + drug_name)
        print("symptom: " + symptom)
        for name in data:
            if name == drug_name:
                usage = data[name]["Mechanisms"][0]["Usage"]
                if symptom in usage:
                    ans = "بلی، " + drug_name + " برای موارد زیر استفاده می شود: " + "\n" + usage
                    break
                else:
                    ans = "خیر، " + drug_name + " برای موارد زیر استفاده می شود: " + "\n" + usage
        print("ans: " + ans)
        ans = ans[:4096]
        checkans = ans.replace("\r","")
        checkans = checkans.replace("\n","")
        checkans = checkans.replace(" ", "")
        if checkans == "":
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        dispatcher.utter_message(text=ans)

        return [SlotSet("drug_name", drug_name), SlotSet("symptom", symptom)]

class ActionAnswerDrugUsage1Comp3(Action):

    def name(self) -> Text:
        return "action_answer_drug_usage_1_comp_3"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # end
        drug_name = tracker.slots["drug_name"]
        ans = "اطلاعاتی یافت نشد. لطفا به نوشتار فارسی دارو و بیماری گفته شده در سوال خود دقت فرمایید."

        illness = next(tracker.get_latest_entity_values("illness"), None)
        if drug_name == None or illness == None:
            dispatcher.utter_message(text=""+ ans)
            return []

        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())
        print("drug_name: " + drug_name)
        print("illness: " + illness)
        for name in data:
            if name == drug_name:
                usage = data[name]["Mechanisms"][0]["Usage"]
                if illness in usage:
                    ans = "بلی، " + drug_name + "برای موارد زیر استفاده می شود: " + "\n" + usage
                    break
                else:
                    ans = "خیر، " + drug_name + "برای موارد زیر استفاده می شود: " + "\n" + usage

        print("ans: " + ans)
        ans = ans[:4096]
        checkans = ans.replace("\r","")
        checkans = checkans.replace("\n","")
        checkans = checkans.replace(" ", "")
        if checkans == "" or ans == "اطلاعاتی یافت نشد. لطفا به نوشتار فارسی دارو و بیماری گفته شده در سوال خود دقت فرمایید.":
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        dispatcher.utter_message(text=ans)

        return [SlotSet("drug_name", drug_name), SlotSet("illness", illness)]"""


class ActionAnswerDrugUsage2(Action):

    def name(self) -> Text:
        return "action_answer_drug_usage_2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # end
        drug_name = next(tracker.get_latest_entity_values("drug_name"), None)
        symptom = next(tracker.get_latest_entity_values("symptom"), None)
        ans = "اطلاعاتی یافت نشد. لطفا به نوشتار فارسی دارو و علائم گفته شده در سوال خود دقت فرمایید."
        if drug_name == None:
            print("slot")
            drug_name = tracker.slots["drug_name"]
        if symptom == None or drug_name == None:
            print("None")
            dispatcher.utter_message(text=ans)
            return []
        
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())
        print("drug_name: " + drug_name)
        print("symptom: " + symptom)
        for name in data:
            if name == drug_name:
                usage = data[name]["Mechanisms"][0]["Usage"]
                usage = Norm.normalize(usage)
                if symptom in usage:
                    ans = drug_name + "برای رفع" + symptom + "مناسب است، به علاوه برای موارد زیر استفاده می شود: " + "\n" + usage
                    break
                else:
                    ans = drug_name + "، " + symptom + "را از بین نمیبرد! اما برای موارد زیر استفاده می شود: " + "\n" + usage
        print("ans: " + ans)
        ans = ans[:4096]
        checkans = ans.replace("\r","")
        checkans = checkans.replace("\n","")
        checkans = checkans.replace(" ", "")
        if checkans == "":
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        dispatcher.utter_message(text=ans)

        return [SlotSet("drug_name", drug_name), SlotSet("symptom", symptom)]

class ActionAnswerDrugUsage3(Action):

    def name(self) -> Text:
        return "action_answer_drug_usage_3"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # end
        drug_name = next(tracker.get_latest_entity_values("drug_name"), None)
        ans = "اطلاعاتی یافت نشد. لطفا به نوشتار فارسی دارو و بیماری گفته شده در سوال خود دقت فرمایید."

        illness = next(tracker.get_latest_entity_values("illness"), None)
        if drug_name == None:
            print("slot")
            drug_name = tracker.slots["drug_name"]
            print(drug_name)
        if drug_name == None or illness == None:
            print("None")
            print(illness)
            dispatcher.utter_message(text=""+ ans)
            return []

        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())
        print("drug_name: " + drug_name)
        print("illness: " + illness)
        for name in data:
            if name == drug_name:
                usage = data[name]["Mechanisms"][0]["Usage"]
                usage = Norm.normalize(usage)
                if illness in usage:
                    ans = drug_name + "برای رفع" + illness + "مناسب است، به علاوه برای موارد زیر استفاده می شود: " + "\n" + usage
                    break
                else:
                    ans = drug_name + "، " + illness + "را از بین نمیبرد! اما برای موارد زیر استفاده می شود: " + "\n" + usage

        print("ans: " + ans)
        ans = ans[:4096]
        checkans = ans.replace("\r","")
        checkans = checkans.replace("\n","")
        checkans = checkans.replace(" ", "")
        if checkans == "":
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        dispatcher.utter_message(text=ans)

        return [SlotSet("drug_name", drug_name), SlotSet("illness", illness)]


class ActionAnswerDrugUsage4(Action):

    def name(self) -> Text:
        return "action_answer_drug_usage_4"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # end
        symptom = next(tracker.get_latest_entity_values("symptom"), None)
        ans = "دارویی برای چنین علائمی یافت نشد. لطفا به نحوه نوشتار علائم گفته شده در سوالتان دقت کنید."
        
        if symptom == None:
            print("None")
            dispatcher.utter_message(text=ans)
            return []
        print("symptom: " + symptom)
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())
        for name in data:
            usage = data[name]["Mechanisms"][0]["Usage"]
            usage = Norm.normalize(usage)
            if symptom in usage:
                if ans == "دارویی برای چنین علائمی یافت نشد. لطفا به نحوه نوشتار علائم گفته شده در سوالتان دقت کنید.":
                    ans = "دارو های زیر برای رفع علامت شما مصرف میشود: \n"
                else:
                    ans += " ,"
                    ans += name
        
        print("ans: " + ans)
        ans = ans[:4096]
        checkans = ans.replace("\r","")
        checkans = checkans.replace("\n","")
        checkans = checkans.replace(" ", "")
        if checkans == "" or ans == "دارویی برای چنین علائمی یافت نشد. لطفا به نحوه نوشتار علائم گفته شده در سوالتان دقت کنید.":
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        # ans = ans.replace("\r","")
        # if ans == "":
            # ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        dispatcher.utter_message(text=ans)

        return [SlotSet("symptom", symptom)]

class ActionAnswerDrugUsage5(Action):

    def name(self) -> Text:
        return "action_answer_drug_usage_5"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # end
        illness = next(tracker.get_latest_entity_values("illness"), None)
        ans = "دارویی برای چنین بیماری ای یافت نشد. لطفا به نحوه نوشتار بیماری گفته شده در سوالتان دقت کنید."
        if illness == None:
            dispatcher.utter_message(text=ans)
            return []
        # drug_name = tracker.get_latest_entity_values(entity_type="drug_name")
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())
        print("illness: " + illness)
        for name in data:
            usage = data[name]["Mechanisms"][0]["Usage"]
            usage = Norm.normalize(usage)
            if illness in usage:
                if ans == "دارویی برای چنین بیماری ای یافت نشد. لطفا به نحوه نوشتار بیماری گفته شده در سوالتان دقت کنید.":
                    ans = "دارو های زیر برای رفع بیماری شما مصرف میشود: \n"
                else:
                    ans += " ,"
                    ans += name

        print("ans: " + ans)
        ans = ans[:4096]
        checkans = ans.replace("\r","")
        checkans = checkans.replace("\n","")
        checkans = checkans.replace(" ", "")
        if checkans == "" or ans == "دارویی برای چنین بیماری ای یافت نشد. لطفا به نحوه نوشتار بیماری گفته شده در سوالتان دقت کنید.":
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        # ans = ans.replace("\r","")
        # if ans == "":
            # ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        dispatcher.utter_message(text=ans)

        return [SlotSet("illness", illness)]

## tadakhol
class ActionDrugInterferences1(Action):

    def name(self) -> Text:
        return "action_answer_drug_interferences_1"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # end
        drug_name = next(tracker.get_latest_entity_values("drug_name"), None)
        ans = "تداخل دارویی برای داروی %s یافت نشد" % drug_name

        if drug_name == None:
            dispatcher.utter_message(text=ans)
            return []
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())

        for name in data:
            if name == drug_name or drug_name in name:
                ans = "تداخل های زیر برای داروی " + drug_name + " یافت شد: \n" + data[name]["Cautions"][0]["Drug_Interferences"]
                ans = Norm.normalize(ans)
                checkans = ans.replace("تداخل های زیر برای داروی ","")
                checkans = checkans.replace(" یافت شد: \n","")
                checkans = checkans.replace(drug_name, "")
                checkans = checkans.replace("\r","")
                checkans = checkans.replace("\n","")
                checkans = checkans.replace(" ", "")
                if checkans != "":
                    break
       
        print("ans: " + ans)
        ans = ans[:4096]
        checkans = ans.replace("\r","")
        checkans = checkans.replace("\n","")
        checkans = checkans.replace(" ", "")
        if checkans == "":
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        # ans = ans.replace("\r","")
        # if ans == "":
            # ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        dispatcher.utter_message(text=ans)
        
        return [SlotSet("drug_name", drug_name)]

class ActionDrugInterferences2(Action):

    def name(self) -> Text:
        return "action_answer_drug_interferences_2"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # end
        drug_names = []
        try:
            # print("try")
            for dn in tracker.latest_message["entities"]:
                print(dn["value"])
                drug_names.append(dn["value"])
        except:
            # print("except")
            dispatcher.utter_message(text="لطفا در نوشتار دارو توجه فرمایید.")
            return []
        if len(drug_names)==1:
            try:
                drug_name_2 = drug_names[0]
                drug_name_1 = tracker.slots["drug_name"]
            except:
                dispatcher.utter_message(text="لطفا در نوشتار دارو توجه فرمایید.")
                return []
        ans = "تداخل دارویی برای دارو های موجود در پرسش یافت نشد"

        # if drug_name_1 == None:
            # dispatcher.utter_message(text="%s"%ans)
            # return []
        with open(dir_path + "/" +"data.json","r", encoding="utf-8") as f:
            data: dict = json.loads(f.read())
        for drug_name_1 in drug_names:
            for drug_name_2 in drug_names:
                for name in data:
                    if name == drug_name_1 or drug_name_1 in name:
                        Drug_Interferences = data[name]["Cautions"][0]["Drug_Interferences"]
                        Drug_Interferences = Norm.normalize(Drug_Interferences)
                        if drug_name_2 in Drug_Interferences:
                            ans = "دارو ها با هم تداخل دارند: \n %s" % Drug_Interferences
                            print("found")
                            break
                
                        # elif drug_name_2 in Drug_Interferences:
                            # ans += "\n %s" % Drug_Interferences
                            # print("found again!")
        
        print("ans: " + ans)
        ans = ans[:4096]
        checkans = ans.replace("\r","")
        checkans = checkans.replace("\n","")
        checkans = checkans.replace(" ", "")
        if checkans == "":
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        # ans = ans.replace("\r","")

        # if ans == "":
            # ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        dispatcher.utter_message(text=ans)
        return []

## avarez
class SideEffects1(Action):

    def name(self) -> Text:
        return "action_answer_side_effects_1"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # end
        drug_name = next(tracker.get_latest_entity_values("drug_name"), None)
        ans = "عوارض جانبی برای داروی %s یافت نشد" % drug_name

        if drug_name == None:
            dispatcher.utter_message(text="%s"%ans)
            return []

        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())

        for name in data:
            if name == drug_name or drug_name in name:
                ans = "عوارض جانبی زیر برای داروی " + drug_name + " یافت شد: \n" + data[name]["Cautions"][0]["Side_Effects"]
                ans = Norm.normalize(ans)
                checkans = ans.replace("عوارض جانبی زیر برای داروی ","")
                checkans = checkans.replace(" یافت شد: \n","")
                checkans = checkans.replace(drug_name, "")
                checkans = checkans.replace("\r","")
                checkans = checkans.replace("\n","")
                checkans = checkans.replace(" ", "")
                if checkans != "":
                    break
        
        print("ans: " + ans)
        ans = ans[:4096]
        checkans = ans.replace("\r","")
        checkans = checkans.replace("\n","")
        checkans = checkans.replace(" ", "")
        if checkans == "":
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        # ans = ans.replace("\r","")

        # if ans == "":
            # ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        dispatcher.utter_message(text=ans)
        return [SlotSet("drug_name", drug_name)]

## khatar
class ActionAnswerDrugCaution1(Action):

    def name(self) -> Text:
        return "action_answer_drug_caution_1"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # end
        drug_name = next(tracker.get_latest_entity_values("drug_name"), None)
        ans = "خطری برای داروی %s یافت نشد" % drug_name

        if drug_name == None:
            dispatcher.utter_message(text="%s"%ans)
            return []
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())

        for name in data:
            if name == drug_name or drug_name in name:
                ans = "هشدار ها: \n " + \
                      data[name]["Cautions"][0]["Warnings"] + "\n" + \
                      "عوارض جانبی: \n" + \
                      data[name]["Cautions"][0]["Side_Effects"] + "\n" + \
                      "تداخلات دارویی: \n" + \
                      data[name]["Cautions"][0]["Drug_Interferences"] + "\n" + \
                      "نکات پیشنهادی: \n" + \
                      data[name]["Cautions"][0]["Recommended_Tips"] + "\n"
                ans = Norm.normalize(ans)
                checkans = ans.replace("\r","")
                checkans = checkans.replace("\n","")
                checkans = checkans.replace("هشدار ها: ", "")
                checkans = checkans.replace("عوارض جانبی: ", "")
                checkans = checkans.replace("تداخلات دارویی: ", "")
                checkans = checkans.replace("نکات پیشنهادی: ", "")
                checkans = checkans.replace(" ", "")
                if checkans != "":
                    break

        print("ans: " + ans)
        ans = ans[:4096]
        checkans = ans.replace("\r","")
        checkans = checkans.replace("\n","")
        checkans = checkans.replace(" ", "")
        if checkans == "":
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        # ans = ans.replace("\r","")
        # if ans == "":
            # ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        
        dispatcher.utter_message(text=ans)
        return [SlotSet("drug_name", drug_name)]

## hoshdar
class ActionAnswerWarning1(Action):

    def name(self) -> Text:
        return "action_answer_warning_1"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # end
        drug_name = next(tracker.get_latest_entity_values("drug_name"), None)
        ans = "هیچ هشداری برای داروی %s یافت نشد" % drug_name
        if drug_name == None:
            dispatcher.utter_message(text="%s"%ans)
            return []
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())

        for name in data:
            if name == drug_name or drug_name in name:
                ans = "هشدار های زیر برای داروی " + drug_name + " یافت شد: \n" + data[name]["Cautions"][0]["Warnings"]
                ans = Norm.normalize(ans)
                checkans = ans.replace("هشدار های زیر برای داروی ","")
                checkans = checkans.replace(" یافت شد: \n","")
                checkans = checkans.replace(drug_name, "")
                checkans = checkans.replace("\r","")
                checkans = checkans.replace("\n","")
                checkans = checkans.replace(" ", "")
                if checkans != "":
                    break

        print("ans: " + ans)
        ans = ans[:4096]
        checkans = ans.replace("\r","")
        checkans = checkans.replace("\n","")
        checkans = checkans.replace(" ", "")
        if checkans == "":
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        # ans = ans.replace("\r","")
        # if ans == "":
            # ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        
        dispatcher.utter_message(text=ans)
        return [SlotSet("drug_name", drug_name)]

class ActionAnswerWarning2(Action):

    def name(self) -> Text:
        return "action_answer_warning_2"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # end
        drug_name = next(tracker.get_latest_entity_values("drug_name"), None)
        ans = "هیچ هشداری برای داروی مورد نظر در تداخل با بیماری یافت نشد"
        illness = next(tracker.get_latest_entity_values("illness"), None)
        if drug_name == None or illness == None:
            dispatcher.utter_message(text=ans)
            return []
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())

        for name in data:
            if name == drug_name or drug_name in name:
                warning  = data[name]["Cautions"][0]["Warnings"]
                ans = Norm.normalize(ans)
                if illness in warning:
                    ans = " داروی مورد نظر با بیماری موجود در پرسش در تداخل است: \n %s" % warning

                    checkans = ans.replace("\r","")
                    checkans = checkans.replace(" داروی مورد نظر با بیماری موجود در پرسش در تداخل است: \n ","")
                    checkans = checkans.replace(warning,"")
                    checkans = checkans.replace("\n","")
                    checkans = checkans.replace(" ", "")
                    if checkans != "":
                        break
        
        print("ans: " + ans)
        ans = ans[:4096]
        checkans = ans.replace("\r","")
        checkans = checkans.replace("\n","")
        checkans = checkans.replace(" ", "")
        if checkans == "":
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        # ans = ans.replace("\r","")
        # if ans == "":
            # ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        
        dispatcher.utter_message(text=ans)
        return [SlotSet("drug_name", drug_name)]

## nokte
class ActionAnswerHowToUse1(Action):

    def name(self) -> Text:
        return "action_answer_how_to_use_1"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # end
        drug_name = next(tracker.get_latest_entity_values("drug_name"), None)
        ans = "عوارض جانبی برای داروی %s یافت نشد" % drug_name

        if drug_name == None:
            dispatcher.utter_message(text="%s"%ans)
            return []
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())

        for name in data:
            if name == drug_name or drug_name in name:
                ans = "نحوه مصرف در متن زیر برای داروی " + drug_name + " یافت شد: \n" + data[name]["Cautions"][0]["Recommended_Tips"]
                ans = Norm.normalize(ans)
                checkans = ans.replace("نحوه مصرف در متن زیر برای داروی ","")
                checkans = checkans.replace(" یافت شد: \n","")
                checkans = checkans.replace(drug_name, "")
                checkans = checkans.replace("\r","")
                checkans = checkans.replace("\n","")
                checkans = checkans.replace(" ", "")
                if checkans != "":
                    break
            
        print("ans: " + ans)
        ans = ans[:4096]
        checkans = ans.replace("\r","")
        checkans = checkans.replace("\n","")
        checkans = checkans.replace(" ", "")
        if checkans == "" or ans == "عوارض جانبی برای داروی %s یافت نشد" % drug_name:
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        # ans = ans.replace("\r","")
        # if ans == "":
            # ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        
        dispatcher.utter_message(text=ans)
        return [SlotSet("drug_name", drug_name)]

## gheimat
class ActionAnswerPrice(Action):
    def name(self) -> Text:
        return "action_answer_price"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # end
        drug_name = next(tracker.get_latest_entity_values("drug_name"), None)
        with open(dir_path + "/" +"data.json", "r", encoding='utf-8') as f:
            data: dict = json.loads(f.read())

        for name in data:
            if name == drug_name or drug_name in name:
                try:
                    if "0" in data[name]["Price"]:
                        data[name]["Price"].pop("0")
                    ans = min(data[name]["Price"])
                    break
                except:
                    ans = "قیمت یافت نشد"
        print("ans: " + ans)
        dispatcher.utter_message(text=ans)
        return [SlotSet("drug_name", drug_name)]

## Shebahat
class ActionAnswerSames1(Action):
    def name(self) -> Text:
        return "action_answer_sames_1"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # end
        drug_name = next(tracker.get_latest_entity_values("drug_name"), None)
        with open(dir_path + "/" +"data.json", "r", encoding='utf-8') as f:
            data: dict = json.loads(f.read())

        for name in data:
            if name == drug_name or drug_name in name:
                try:
                    ans = "دارو های مشابه داروی " + drug_name + " این ها است: \n" + data[name]["Sames"][0]
                    for x in data[name]["Sames"][0:]:
                        ans += ", " + x
                    break
                except:
                    ans = "مشابه دارو یافت نشد"
        print("ans: " + ans)
        dispatcher.utter_message(text=ans)
        return [SlotSet("drug_name", drug_name)]

class ActionAnswerSames2(Action):
    def name(self) -> Text:
        return "action_answer_sames_2"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # findout that intent is correct
        Q = tracker.latest_message["text"]
        print("Q: " + Q)
        confidence = tracker.latest_message["intent"]["confidence"]
        print("confidence: " + str(confidence))
        intent = tracker.latest_message["intent"]["name"]
        print("intent: " + intent)
        if confidence < 0.6:
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # end
        drug_names = []
        try:
            # print("try")
            for dn in tracker.latest_message["entities"]:
                print(dn["value"])
                drug_names.append(dn["value"])
        except:
            # print("except")
            dispatcher.utter_message(text="لطفا در نوشتار دارو توجه فرمایید.")
            return []
        if len(drug_names)==1:
            try:
                drug_name_2 = drug_names[0]
                drug_name_1 = tracker.slots["drug_name"]
            except:
                dispatcher.utter_message(text="لطفا در نوشتار دارو توجه فرمایید.")
                return []
        

        with open(dir_path + "/" +"data.json", "r", encoding='utf-8') as f:
            data: dict = json.loads(f.read())

        for drug_name_1 in drug_names:
            for drug_name_2 in drug_names:
                for name in data:
                    if name == drug_name_1 or drug_name_1 in name:
                        try:
                            Sames = data[name]["Sames"]
                            Sames = Norm.normalize(Sames)
                            for x in Sames:
                                if drug_name_2 == x:
                                    ans = "دارو های " + drug_name_1 + " و " + drug_name_2 + "یکسان اند"
                                    break
                                else:
                                    ans = "دارو های " + drug_name_1 + " و " + drug_name_2 + "یکسان نیستند!"
                        except:
                            ans = "مشابه دارو یافت نشد"
        print("ans: " + ans)
        dispatcher.utter_message(text=ans)
        return [SlotSet("drug_name", drug_name_1)]
