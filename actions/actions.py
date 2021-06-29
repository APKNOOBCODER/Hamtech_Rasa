# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import json

# from yaml.events import NodeEvent
import hazm
Norm = hazm.Normalizer()
from typing import Any, Counter, Text, Dict, List
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionAnswerGreet(Action):

    def name(self) -> Text:
        return "action_answer_greet"

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
## mavared masraf
# checked II
class ActionAnswerDrugUsage(Action):

    def name(self) -> Text:
        return "action_answer_drug_usage"

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
        try:
            intentsList = tracker.latest_message["intent_ranking"]
        except KeyError:
            intentsList = None
        # print(intentsList)
        # end
        drug_name = next(tracker.get_latest_entity_values("drug_name"), None)
        ans = "اطلاعاتی موجود نیست. این اتفاق احتمالا به خاطر اشتباه تایپی در نوشتار دارو به زبان فارسی رخ داده. لطفا نحوه نوشتار آن را به دقت از روی جعبه دارو به دست آورید."
        if drug_name == None:
            dispatcher.utter_message(text=ans)
            return []
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())
        drug_name = Norm.normalize(drug_name)
        print("drug_name: " + drug_name)
        
        find_drug_name = False
        for name in data:
            if name == drug_name or drug_name in name:
                find_drug_name = True
                Usage = data[name]["Mechanisms"][0]["Usage"]
                Usage = Norm.normalize(Usage)
                checkans = Usage.replace(" ", "")
                checkans = checkans.replace("\r","")
                checkans = checkans.replace("\n","")

                ans = "موارد مصرف داروی " + drug_name + ": " + Usage
                
                if checkans != "":
                    break
        print("ans: " + ans)
        ans = ans[:4096]
        if not find_drug_name:
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
 
        elif checkans == "":
            ans = "موارد مصرف داروی " + drug_name + " یافت نشد"
        
        dispatcher.utter_message(text=ans)
        # dispatcher.utter_message(text=ans2)
        entities: list = [drug_name]
        ## log
        newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                    "entities": entities, "ans": ans}}
        try:
            with open(dir_path +  "/Log.json","r") as f:
                logdic: dict = json.loads(f.read())
                logdic.update(newlogdic)
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(logdic, f, indent=4, ensure_ascii=False)
        except:
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(newlogdic, f, indent=4, ensure_ascii=False)
        ## end log
        return [SlotSet("drug_name", drug_name)]

# checked II
class ActionAnswerAskDrugUsageComp(Action):

    def name(self) -> Text:
        return "action_answer_drug_usage_comp"

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
        # dispatcher.utter_message(text=ans2)
        try:
            intentsList = tracker.latest_message["intent_ranking"]
        except KeyError:
            intentsList = None
        ans = "متوجه نشدم، لطفا دوباره تلاش کنید"
        entities = None
        if confidence < 0.6:
            ## log
            newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                        "entities": entities, "ans": ans}}
            try:
                with open(dir_path +  "/Log.json","r") as f:
                    logdic: dict = json.loads(f.read())
                    logdic.update(newlogdic)
                with open(dir_path +  "/Log.json","w") as f:
                    json.dump(logdic, f, indent=4, ensure_ascii=False)
            except:
                with open(dir_path +  "/Log.json","w") as f:
                    json.dump(newlogdic, f, indent=4, ensure_ascii=False)
            ## end log
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        # print(intentsList)
        # end
        try:
            drug_name = tracker.slots["drug_name"]
        except:
            drug_name = None
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())
        if drug_name == None:
            ## log
            newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                        "entities": entities, "ans": ans}}
            try:
                with open(dir_path +  "/Log.json","r") as f:
                    logdic: dict = json.loads(f.read())
                    logdic.update(newlogdic)
                with open(dir_path +  "/Log.json","w") as f:
                    json.dump(logdic, f, indent=4, ensure_ascii=False)
            except:
                with open(dir_path +  "/Log.json","w") as f:
                    json.dump(newlogdic, f, indent=4, ensure_ascii=False)
            ## end log
            dispatcher.utter_message(text="متوجه نشدم، لطفا دوباره تلاش کنید")
            return []
        print("drug_name: " + drug_name)
        
        find_drug_name = False
        for name in data:
            if name == drug_name or drug_name in name:
                find_drug_name = True
                Usage = data[name]["Mechanisms"][0]["Usage"]
                Usage = Norm.normalize(Usage)
                checkans = Usage.replace(" ", "")
                checkans = checkans.replace("\r","")
                checkans = checkans.replace("\n","")

                ans = "موارد مصرف داروی " + drug_name + ": " + Usage
                
                if checkans != "":
                    break
        print("ans: " + ans)
        ans = ans[:4096]
        if not find_drug_name:
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
 
        elif checkans == "":
            ans = "موارد مصرف داروی " + drug_name + " یافت نشد"
        

        dispatcher.utter_message(text=ans)
        
        ## log
        newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                    "entities": entities, "ans": ans}}
        try:
            with open(dir_path +  "/Log.json","r") as f:
                logdic: dict = json.loads(f.read())
                logdic.update(newlogdic)
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(logdic, f, indent=4, ensure_ascii=False)
        except:
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(newlogdic, f, indent=4, ensure_ascii=False)
        ## end log
        return [SlotSet("drug_name", drug_name)]
## end

# mavared masraf ba alaem
# checked II
class ActionAnswerDrugUsageForSymptom(Action):

    def name(self) -> Text:
        return "action_answer_drug_usage_for_symptom"

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
        ans = "اطلاعاتی یافت نشد. لطفا به نوشتار فارسی دارو و علائم گفته شده در سوال خود دقت فرمایید."
        drug_name = next(tracker.get_latest_entity_values("drug_name"), None)
        
        if symptom == None or drug_name == None:
            dispatcher.utter_message(text=ans)
            return []
        
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())
        print("drug_name: " + drug_name)
        print("symptom: " + symptom)
        find_drug_name = False
        for name in data:
            if name == drug_name or drug_name in name:
                find_drug_name = True
                usage = data[name]["Mechanisms"][0]["Usage"]
                usage = Norm.normalize(usage)
                checkans = usage.replace("\r","")
                checkans = checkans.replace("\n","")
                checkans = checkans.replace(" ", "")
                if symptom in usage:
                    ans = drug_name + " برای رفع " + symptom + " مناسب است، به علاوه برای موارد زیر استفاده می شود: " + "\n" + usage
                    break
                else:
                    ans = drug_name + "، " + symptom + " را از بین نمیبرد! اما برای موارد زیر استفاده می شود: " + "\n" + usage
        print("ans: " + ans)
        ans = ans[:4096]
        
        if not find_drug_name:
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        dispatcher.utter_message(text=ans)
        entities: list = [drug_name, symptom]
        try:
            intentsList = tracker.latest_message["intent_ranking"]
        except KeyError:
            intentsList = None
        ## log
        newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                    "entities": entities, "ans": ans}}
        try:
            with open(dir_path +  "/Log.json","r") as f:
                logdic: dict = json.loads(f.read())
                logdic.update(newlogdic)
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(logdic, f, indent=4, ensure_ascii=False)
        except:
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(newlogdic, f, indent=4, ensure_ascii=False)
        ## end log

        return [SlotSet("drug_name", drug_name), SlotSet("symptom", symptom)]

# chacked II
class ActionAnswerDrugUsageForSymptomComp(Action):

    def name(self) -> Text:
        return "action_answer_drug_usage_for_symptom_comp"

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
        ans = "اطلاعاتی یافت نشد. لطفا به نوشتار فارسی دارو و علائم گفته شده در سوال خود دقت فرمایید."
        drug_name = tracker.slots["drug_name"]
        if symptom == None or drug_name == None:
            print("None")
            dispatcher.utter_message(text=ans)
            return []
        
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())
        print("drug_name: " + drug_name)
        print("symptom: " + symptom)
        find_drug_name = False
        for name in data:
            if name == drug_name or drug_name in name:
                find_drug_name = True
                usage = data[name]["Mechanisms"][0]["Usage"]
                usage = Norm.normalize(usage)
                checkans = usage.replace("\r","")
                checkans = checkans.replace("\n","")
                checkans = checkans.replace(" ", "")
                if symptom in usage:
                    ans = drug_name + " برای رفع " + symptom + " مناسب است، به علاوه برای موارد زیر استفاده می شود: " + "\n" + usage
                    break
                else:
                    ans = drug_name + "، " + symptom + " را از بین نمیبرد! اما برای موارد زیر استفاده می شود: " + "\n" + usage
        print("ans: " + ans)
        ans = ans[:4096]
        
        if not find_drug_name:
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        dispatcher.utter_message(text=ans)
        entities: list = [drug_name, symptom]
        try:
            intentsList = tracker.latest_message["intent_ranking"]
        except KeyError:
            intentsList = None
        ## log
        newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                    "entities": entities, "ans": ans}}
        try:
            with open(dir_path +  "/Log.json","r") as f:
                logdic: dict = json.loads(f.read())
                logdic.update(newlogdic)
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(logdic, f, indent=4, ensure_ascii=False)
        except:
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(newlogdic, f, indent=4, ensure_ascii=False)
        ## end log

        return [SlotSet("drug_name", drug_name), SlotSet("symptom", symptom)]
# checked II
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
        drug_name = Norm.normalize(drug_name)
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())
        print("drug_name: " + drug_name)
        print("illness: " + illness)
        find_drug_name = False
        for name in data:
            if name == drug_name or drug_name in name:
                find_drug_name = True
                usage = data[name]["Mechanisms"][0]["Usage"]
                usage = Norm.normalize(usage)
                checkans = usage.replace("\r","")
                checkans = checkans.replace("\n","")
                checkans = checkans.replace(" ", "")
                if illness in usage:
                    ans = drug_name + "برای رفع" + illness + " مناسب است، به علاوه برای موارد زیر استفاده می شود: " + "\n" + usage
                    break
                else:
                    ans = drug_name + "، " + illness + " را از بین نمیبرد! اما برای موارد زیر استفاده می شود: " + "\n" + usage

        print("ans: " + ans)
        ans = ans[:4096]
        
        if not find_drug_name:
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        dispatcher.utter_message(text=ans)
        entities: list = [drug_name, illness]
        try:
            intentsList = tracker.latest_message["intent_ranking"]
        except KeyError:
            intentsList = None
        ## log
        newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                    "entities": entities, "ans": ans}}
        try:
            with open(dir_path +  "/Log.json","r") as f:
                logdic: dict = json.loads(f.read())
                logdic.update(newlogdic)
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(logdic, f, indent=4, ensure_ascii=False)
        except:
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(newlogdic, f, indent=4, ensure_ascii=False)
        ## end log

        return [SlotSet("drug_name", drug_name), SlotSet("illness", illness)]

# checked II
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
        count = 0 
        find_drug_name = False
        for name in data:
            usage = data[name]["Mechanisms"][0]["Usage"]
            usage = Norm.normalize(usage)
            checkans = usage.replace("\r","")
            checkans = checkans.replace("\n","")
            checkans = checkans.replace(" ", "")
            if count > 10:
                    break
            if symptom in usage:
                find_drug_name = True
                if count == 0:
                    ans = "دارو های زیر برای رفع علامت شما مصرف میشود: \n"
                else:
                    ans += (str(count) + "- ")
                    ans += (name + "\n")
                count += 1
                
        
        print("ans: " + ans)
        ans = ans[:4096]
        if not find_drug_name:
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        if checkans == "":
            ans = "دارویی برای رفع علامت شما موجود نیست"
        # ans = ans.replace("\r","")
        # if ans == "":
            # ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        dispatcher.utter_message(text=ans)
        entities: list = [symptom]
        try:
            intentsList = tracker.latest_message["intent_ranking"]
        except KeyError:
            intentsList = None
        ## log
        newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                    "entities": entities, "ans": ans}}
        try:
            with open(dir_path +  "/Log.json","r") as f:
                logdic: dict = json.loads(f.read())
                logdic.update(newlogdic)
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(logdic, f, indent=4, ensure_ascii=False)
        except:
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(newlogdic, f, indent=4, ensure_ascii=False)
        ## end log

        return [SlotSet("symptom", symptom)]

# checked II
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
        count = 0
        find_drug_name = False
        for name in data:
            usage = data[name]["Mechanisms"][0]["Usage"]
            usage = Norm.normalize(usage)
            checkans = usage.replace("\r","")
            checkans = checkans.replace("\n","")
            checkans = checkans.replace(" ", "")
            if count > 10:
                break
            if illness in usage:
                find_drug_name = True
                if count == 0:
                    ans = "دارو های زیر برای رفع بیماری شما مصرف میشود: \n"
                else:
                    ans += (str(count) + "- ")
                    ans += (name + "\n")
                count += 1

        print("ans: " + ans)
        ans = ans[:4096]
        if not find_drug_name:
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        if checkans == "":
            ans = "دارویی برای رفع بیماری شما یافت نشد"
        dispatcher.utter_message(text=ans)
        entities: list = [illness]
        try:
            intentsList = tracker.latest_message["intent_ranking"]
        except KeyError:
            intentsList = None
        ## log
        newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                    "entities": entities, "ans": ans}}
        try:
            with open(dir_path +  "/Log.json","r") as f:
                logdic: dict = json.loads(f.read())
                logdic.update(newlogdic)
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(logdic, f, indent=4, ensure_ascii=False)
        except:
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(newlogdic, f, indent=4, ensure_ascii=False)
        ## end log

        return [SlotSet("illness", illness)]
## end

## tadakhol
# checked II
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
        drug_name = None
        for dn in tracker.latest_message["entities"]:
                DN = Norm.normalize(dn["value"])
                if (DN != "") and (DN != " ") and (DN != "\n") and (DN != "\r"):
                    print("dn: " + DN)
                    if drug_name == None:
                        drug_name = DN
                    elif len(drug_name) < len(DN):
                        drug_name = DN
        ans = "لطفا به نحوه نوشتار خود دقت کنید"
        if drug_name == None:
            dispatcher.utter_message(text=ans)
            return []
        ans = "تداخل دارویی برای داروی %s یافت نشد" % drug_name
        
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())

        find_drug_name = False
        for name in data:
            if name == drug_name or drug_name in name:
                find_drug_name = True
                Drug_Interferences = data[name]["Cautions"][0]["Drug_Interferences"]
                Drug_Interferences = Norm.normalize(Drug_Interferences)
                checkans = Drug_Interferences.replace("\r","")
                checkans = checkans.replace("\n","")
                checkans = checkans.replace(" ", "")
                ans = "تداخل های زیر برای داروی " + drug_name + " یافت شد: \n" + Drug_Interferences

                if checkans != "":
                    break
       
        print("ans: " + ans)
        ans = ans[:4096]
        if not find_drug_name:
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        elif checkans == "":
            ans = "تداخل دارویی خاصی برای " + drug_name + " وجود ندارد"
        
        dispatcher.utter_message(text=ans)
        entities = [drug_name]
        try:
            intentsList = tracker.latest_message["intent_ranking"]
        except KeyError:
            intentsList = None
        ## log
        newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                    "entities": entities, "ans": ans}}
        try:
            with open(dir_path +  "/Log.json","r") as f:
                logdic: dict = json.loads(f.read())
                logdic.update(newlogdic)
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(logdic, f, indent=4, ensure_ascii=False)
        except:
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(newlogdic, f, indent=4, ensure_ascii=False)
        ## end log
        
        return [SlotSet("drug_name", drug_name)]

# checked II
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
                DN = Norm.normalize(dn["value"])
                if (DN not in drug_names) and (DN != "") and (DN != " ") and (DN != "\n") and (DN != "\r"):
                    print("dn: " + DN)
                    drug_names.append(DN)
        except:
            # print("except")
            dispatcher.utter_message(text="لطفا در نوشتار دارو توجه فرمایید.")
            return []
        if len(drug_names) == 0:
            dispatcher.utter_message(text="لطفا در نوشتار دارو توجه فرمایید.")
            return []
        elif len(drug_names)==1:
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
        dispatcher.utter_message(text=ans)
        entities: list = [drug_names]
        try:
            intentsList = tracker.latest_message["intent_ranking"]
        except KeyError:
            intentsList = None
        ## log
        newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                    "entities": entities, "ans": ans}}
        try:
            with open(dir_path +  "/Log.json","r") as f:
                logdic: dict = json.loads(f.read())
                logdic.update(newlogdic)
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(logdic, f, indent=4, ensure_ascii=False)
        except:
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(newlogdic, f, indent=4, ensure_ascii=False)
        ## end log


        return []
## end

## avarez
# checked II
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
        drug_name = None
        for dn in tracker.latest_message["entities"]:
                DN = Norm.normalize(dn["value"])
                if (DN != "") and (DN != " ") and (DN != "\n") and (DN != "\r"):
                    print("dn: " + DN)
                    if drug_name == None:
                        drug_name = DN
                    elif len(drug_name) < len(DN):
                        drug_name = DN
        ans = "لطفا به نحوه نوشتار داور دقت فرمایید"
        if drug_name == None:
            dispatcher.utter_message(text="%s"%ans)
            return []
        ans = "عوارض جانبی برای داروی %s یافت نشد" % drug_name
        print(drug_name)
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())
        
        find_drug_name = False
        for name in data:
            if name == drug_name or drug_name in name:
                find_drug_name = True
                Caution = data[name]["Cautions"][0]["Side_Effects"]
                checkans = Caution.replace("\r","")
                checkans = checkans.replace("\n","")
                checkans = checkans.replace(" ", "")
                ans = "عوارض جانبی زیر برای داروی " + drug_name + " یافت شد: \n" + Caution
                ans = Norm.normalize(ans)
                if checkans != "":
                    # print("ans1: " + ans)
                    break
        
        print("ans: " + ans)
        ans = ans[:4096]
        if not find_drug_name:
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        elif checkans == "":
            ans = "هیچ عارضه جانبی برای " + drug_name + " وجود ندارد."

        dispatcher.utter_message(text=ans)
        entities: list = [drug_name]
        print(tracker.latest_message)
        try:
            intentsList = tracker.latest_message["intent_ranking"]
        except KeyError:
            intentsList = None
        ## log
        newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                    "entities": entities, "ans": ans}}
        try:
            with open(dir_path +  "/Log.json","r") as f:
                logdic: dict = json.loads(f.read())
                logdic.update(newlogdic)
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(logdic, f, indent=4, ensure_ascii=False)
        except:
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(newlogdic, f, indent=4, ensure_ascii=False)
        ## end log

        return [SlotSet("drug_name", drug_name)]
## end

## khatar
# checked II
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
        drug_name = None
        for dn in tracker.latest_message["entities"]:
                DN = Norm.normalize(dn["value"])
                if (DN != "") and (DN != " ") and (DN != "\n") and (DN != "\r"):
                    print("dn: " + DN)
                    if drug_name == None:
                        drug_name = DN
                    elif len(drug_name) < len(DN):
                        drug_name = DN
        ans = "لطفا به نحوه نوشتار نام دارو توجه فرمایید"
        if drug_name == None:
            dispatcher.utter_message(text="%s"%ans)
            return []
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())
        ans = "خطری برای داروی %s یافت نشد" % drug_name

        find_drug_name = False
        for name in data:
            if name == drug_name or drug_name in name:
                find_drug_name = True
                ### Warnigns
                Warnings = data[name]["Cautions"][0]["Warnings"]
                Warnings = Norm.normalize(Warnings)
                Wcheckans = Warnings.replace("\r","")
                Wcheckans = Wcheckans.replace("\n","")
                ### end
                ### Side_Effects
                Side = data[name]["Cautions"][0]["Side_Effects"]
                Side = Norm.normalize(Side)
                Scheckans = Side.replace("\r","")
                Scheckans = Scheckans.replace("\n","")
                ### end
                ### Drug_Interferences
                Drug_Interferences = data[name]["Cautions"][0]["Drug_Interferences"]
                Drug_Interferences = Norm.normalize(Drug_Interferences)
                Dcheckans = Drug_Interferences.replace("\r","")
                Dcheckans = Dcheckans.replace("\n","")
                ### end
                ### Recommended_Tips
                Recom = data[name]["Cautions"][0]["Recommended_Tips"]
                Recom = Norm.normalize(Recom)
                Rcheckans = Recom.replace("\r","")
                Rcheckans = Rcheckans.replace("\n","")
                ### end
                ans = "هشدار ها: \n " + \
                      Warnings + "\n" + \
                      "عوارض جانبی: \n" + \
                      Side + "\n" + \
                      "تداخلات دارویی: \n" + \
                      Drug_Interferences + "\n" + \
                      "نکات پیشنهادی: \n" + \
                      Recom + "\n"

                if Wcheckans != "" or Scheckans != "" or Dcheckans != "" or Rcheckans != "":
                    break

        print("ans: " + ans)
        ans = ans[:4096]
        if not find_drug_name:
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        elif Wcheckans == "" and Scheckans == "" or Dcheckans == "" or Rcheckans == "":
            ans = "خطری برای داروی %s یافت نشد" % drug_name
        dispatcher.utter_message(text=ans)
        entities = [drug_name]
        try:
            intentsList = tracker.latest_message["intent_ranking"]
        except KeyError:
            intentsList = None
        ## log
        newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                    "entities": entities, "ans": ans}}
        try:
            with open(dir_path +  "/Log.json","r") as f:
                logdic: dict = json.loads(f.read())
                logdic.update(newlogdic)
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(logdic, f, indent=4, ensure_ascii=False)
        except:
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(newlogdic, f, indent=4, ensure_ascii=False)
        ## end log

        return [SlotSet("drug_name", drug_name)]
## end

## hoshdar
# checked II
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
        drug_name = None
        illness = next(tracker.get_latest_entity_values("illness"), None)
        for dn in tracker.latest_message["entities"]:
                DN = Norm.normalize(dn["value"])
                if (DN != "") and (DN != " ") and (DN != "\n") and (DN != "\r") and (DN != illness):
                    print("dn: " + DN)
                    if drug_name == None:
                        drug_name = DN
                    elif len(drug_name) < len(DN):
                        drug_name = DN
        ans = "در نحوه نوشتار دارو دقت فرمایید"
        if drug_name == None:
            dispatcher.utter_message(text="%s"%ans)
            return []
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())
        ans = "هیچ هشداری برای داروی %s یافت نشد" % drug_name

        find_drug_name = False
        for name in data:
            if name == drug_name or drug_name in name:
                find_drug_name = True
                Warnings = data[name]["Cautions"][0]["Warnings"]
                Warnings = Norm.normalize(Warnings)
                checkans = Warnings.replace("\r","")
                checkans = checkans.replace("\n","")
                checkans = checkans.replace(" ", "")
                ans = "هشدار های زیر برای داروی " + drug_name + " یافت شد: \n" + Warnings
                if checkans != "":
                    break

        print("ans: " + ans)
        ans = ans[:4096]
        if not find_drug_name:
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        elif checkans == "":
            ans = "هشدار خاصی برای داروی " + drug_name + " وجود ندارد"
        
        # ans = ans.replace("\r","")
        # if ans == "":
            # ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        
        dispatcher.utter_message(text=ans)
        entities: list = [drug_name]
        try:
            intentsList = tracker.latest_message["intent_ranking"]
        except KeyError:
            intentsList = None
        ## log
        newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                    "entities": entities, "ans": ans}}
        try:
            with open(dir_path +  "/Log.json","r") as f:
                logdic: dict = json.loads(f.read())
                logdic.update(newlogdic)
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(logdic, f, indent=4, ensure_ascii=False)
        except:
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(newlogdic, f, indent=4, ensure_ascii=False)
        ## end log

        return [SlotSet("drug_name", drug_name)]

# checked II
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
        drug_name = None
        illness = next(tracker.get_latest_entity_values("illness"), None)
        for dn in tracker.latest_message["entities"]:
                DN = Norm.normalize(dn["value"])
                if (DN != "") and (DN != " ") and (DN != "\n") and (DN != "\r") and (DN != illness):
                    print("dn: " + DN)
                    if drug_name == None:
                        drug_name = DN
                    elif len(drug_name) < len(DN):
                        drug_name = DN
        ans = "لطفا به نحوه نوشتار نام دارو و بیماری توجه فرمایید"
        
        if drug_name == None or illness == None:
            dispatcher.utter_message(text=ans)
            return []
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())
        ans = "هیچ هشداری برای داروی مورد نظر در تداخل با بیماری یافت نشد"
        find_drug_name = False
        for name in data:
            if name == drug_name or drug_name in name:
                find_drug_name = True
                Warnings  = data[name]["Cautions"][0]["Warnings"]
                Warnings = Norm.normalize(Warnings)
                checkans = Warnings.replace("\r","")
                checkans = checkans.replace("\n","")
                checkans = checkans.replace(" ", "")
                if illness in Warnings:
                    ans = " داروی مورد نظر با بیماری موجود در پرسش در تداخل است: \n %s" % Warnings
                    if checkans != "":
                        break
        
        print("ans: " + ans)
        ans = ans[:4096]
        if  not find_drug_name:
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        elif checkans == "":
            ans = "هیچ هشداری برای داروی مورد نظر در تداخل با بیماری یافت نشد"
        
        dispatcher.utter_message(text=ans)
        entities = [drug_name, illness]
        try:
            intentsList = tracker.latest_message["intent_ranking"]
        except KeyError:
            intentsList = None
        ## log
        newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                    "entities": entities, "ans": ans}}
        try:
            with open(dir_path +  "/Log.json","r") as f:
                logdic: dict = json.loads(f.read())
                logdic.update(newlogdic)
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(logdic, f, indent=4, ensure_ascii=False)
        except:
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(newlogdic, f, indent=4, ensure_ascii=False)
        ## end log

        return [SlotSet("drug_name", drug_name)]
## end

## nokte
# checked II
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
        drug_name = None
        for dn in tracker.latest_message["entities"]:
                DN = Norm.normalize(dn["value"])
                if (DN != "") and (DN != " ") and (DN != "\n") and (DN != "\r"):
                    print("dn: " + DN)
                    if drug_name == None:
                        drug_name = DN
                    elif len(drug_name) < len(DN):
                        drug_name = DN
        ans = "لطفا به نوشتار دارو توجه فرمایید"
        if drug_name == None:
            dispatcher.utter_message(text="%s"%ans)
            return []
        with open(dir_path + "/" +"data.json","r") as f:
            data: dict = json.loads(f.read())
        find_drug_name = False
        for name in data:
            if name == drug_name or drug_name in name:
                find_drug_name = True
                Recomm = data[name]["Cautions"][0]["Recommended_Tips"]
                Recomm = Norm.normalize(Recomm)
                checkans = Recomm.replace("\r","")
                checkans = checkans.replace("\n","")
                checkans = checkans.replace(" ", "")
                ans = "نحوه مصرف در متن زیر برای داروی " + drug_name + " یافت شد: \n" + Recomm
                
                if checkans != "":
                    break
        if not find_drug_name:
            ans = "با عرض پوزش، در اطلاعات دیتابیس من اطلاعات مربوط به سوال شما موجود نیست"
        elif checkans == "":
            ans = "اطلاعاتی درباره نحوه مصرف " + drug_name + " وجود ندارد"
        print("ans: " + ans)
        ans = ans[:4096]
        checkans = ans.replace("\r","")
        checkans = checkans.replace("\n","")
        checkans = checkans.replace(" ", "")
        
        dispatcher.utter_message(text=ans)
        entities: list = [drug_name]
        try:
            intentsList = tracker.latest_message["intent_ranking"]
        except KeyError:
            intentsList = None
        ## log
        newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                    "entities": entities, "ans": ans}}
        try:
            with open(dir_path +  "/Log.json","r") as f:
                logdic: dict = json.loads(f.read())
                logdic.update(newlogdic)
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(logdic, f, indent=4, ensure_ascii=False)
        except:
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(newlogdic, f, indent=4, ensure_ascii=False)
        ## end log

        return [SlotSet("drug_name", drug_name)]
## end

## gheimat
# checked II
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
        drug_name = None
        for dn in tracker.latest_message["entities"]:
                DN = Norm.normalize(dn["value"])
                if (DN != "") and (DN != " ") and (DN != "\n") and (DN != "\r"):
                    print("dn: " + DN)
                    if drug_name == None:
                        drug_name = DN
                    elif len(drug_name) < len(DN):
                        drug_name = DN
        # drug_name = next(tracker.get_latest_entity_values("drug_name"), None)
        with open(dir_path + "/" +"data.json", "r", encoding='utf-8') as f:
            data: dict = json.loads(f.read())

        if drug_name == None:
            print("slot")
            drug_name = tracker.slots["drug_name"]
        if drug_name == None:
            dispatcher.utter_message(text="لطفا در نحوه نوشتار دارو توجه فرمایید.")
        find_drug_name = False
        ans = "قیمت یافت نشد"
        for name in data:
            if name == drug_name or drug_name in name:
                find_drug_name = True
                try:
                    Prices = data[name]["Price"]
                    while "0" in Prices:
                        Prices.remove("0")
                    if len(Prices) == 0:
                        continue
                    Prices = list(map(int,Prices))
                    ans = str(min(data[name]["Price"]))
                    break
                except:
                    ans = "قیمت یافت نشد"
        if not find_drug_name:
            ans = "اطلاعاتی در دیتابیس من برای این سوال موجود نیست"
        print("ans: " + ans)
        ans = "اطلاعاتی در دیتابیس من برای این سوال موجود نیست"
        dispatcher.utter_message(text=ans)
        entities: list = [drug_name]
        try:
            intentsList = tracker.latest_message["intent_ranking"]  
        except:
            intentsList = None

        ## log
        newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                    "entities": entities, "ans": ans}}
        try:
            with open(dir_path +  "/Log.json","r") as f:
                logdic: dict = json.loads(f.read())
                logdic.update(newlogdic)
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(logdic, f, indent=4, ensure_ascii=False)
        except:
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(newlogdic, f, indent=4, ensure_ascii=False)
        ## end log

        return [SlotSet("drug_name", drug_name)]
## end

## Shebahat
# checked II
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
        # drug_name = next(tracker.get_latest_entity_values("drug_name"), None)
        with open(dir_path + "/" +"data.json", "r", encoding='utf-8') as f:
            data: dict = json.loads(f.read())
        drug_name = None
        for dn in tracker.latest_message["entities"]:
                DN = Norm.normalize(dn["value"])
                if (DN != "") and (DN != " ") and (DN != "\n") and (DN != "\r"):
                    print("dn: " + DN)
                    if drug_name == None:
                        drug_name = DN
                    elif len(drug_name) < len(DN):
                        drug_name = DN
        if drug_name == None:
            print("slot")
            drug_name = tracker.slots["drug_name"]
        if drug_name == None:
            dispatcher.utter_message(text="لطفا در نحوه نوشتار دارو توجه فرمایید.")
        print(drug_name)
        ans = "مشابه دارو در دیتابیس من یافت نشد"
        for name in data:
            if name == drug_name or drug_name in name:
                try:
                    Sames = data[name]["Sames"]
                    NormedSames = []
                    for same in Sames:
                        NormedSames.append(Norm.normalize(same))
                    ans = "دارو های مشابه داروی " + drug_name + " این ها است: \n" + NormedSames[0]
                    for x in data[name]["Sames"][0:]:
                        ans += ", " + x
                    break
                except:
                    ans = "مشابه دارو در دیتابیس من یافت نشد"
        print("ans: " + ans)
        dispatcher.utter_message(text=ans)
        entities: list = [drug_name]
        try:
            intentsList = tracker.latest_message["intent_ranking"]
        except:
            intentsList = None
        ## log
        newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                    "entities": entities, "ans": ans}}
        try:
            with open(dir_path +  "/Log.json","r") as f:
                logdic: dict = json.loads(f.read())
                logdic.update(newlogdic)
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(logdic, f, indent=4, ensure_ascii=False)
        except:
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(newlogdic, f, indent=4, ensure_ascii=False)
        ## end log

        return [SlotSet("drug_name", drug_name)]
# checked II
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
                DN = Norm.normalize(dn["value"])
                if (DN not in drug_names) and (DN != "") and (DN != " ") and (DN != "\n") and (DN != "\r"):
                    print("dn: " + DN)
                    drug_names.append(DN)
        except:
            # print("except")
            dispatcher.utter_message(text="لطفا در نوشتار دارو توجه فرمایید.")
            return []
        if len(drug_names) == 0:
            dispatcher.utter_message(text="لطفا در نوشتار دارو توجه فرمایید.")
            return []
        elif len(drug_names)==1:
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
                if drug_name_1 == drug_name_2:
                    continue
                for name in data:
                    if name == drug_name_1 or drug_name_1 in name:
                        try:
                            Sames = data[name]["Sames"]
                            NormedSames = []
                            for same in Sames:
                                NormedSames.append(Norm.normalize(same))
                            # print(Sames)
                            for x in NormedSames:
                                if drug_name_2 == x or drug_name_2 in x:
                                    ans = "دارو های " + drug_name_1 + " و " + drug_name_2 + " یکسان اند"
                                    print("ans: " + ans)
                                    dispatcher.utter_message(text=ans)
                                    entities: list = drug_names
                                    try:
                                        intentsList = tracker.latest_message["intent_ranking"]
                                    except KeyError:
                                        intentsList = None
                                    ## log
                                    newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                                                "entities": entities, "ans": ans}}
                                    try:
                                        with open(dir_path +  "/Log.json","r") as f:
                                            logdic: dict = json.loads(f.read())
                                            logdic.update(newlogdic)
                                        with open(dir_path +  "/Log.json","w") as f:
                                            json.dump(logdic, f, indent=4, ensure_ascii=False)
                                    except:
                                        with open(dir_path +  "/Log.json","w") as f:
                                            json.dump(newlogdic, f, indent=4, ensure_ascii=False)
                                    ## end log

                                    return [SlotSet("drug_name", drug_name_1)]
                                else:
                                    ans = "دارو های " + drug_name_1 + " و " + drug_name_2 + " یکسان نیستند!"
                        except:
                            ans = "اطلاعاتی برای داروی شما در دیتابیس من یافت نشد"
                        
        print("ans: " + ans)
        dispatcher.utter_message(text=ans)
        entities: list = [drug_names]
        try:
            intentsList = tracker.latest_message["intent_ranking"]
        except KeyError:
            intentsList = None
        ## log
        newlogdic = {Q:{"intent": intent, "intentlist": intentsList, "confidence": confidence, \
                    "entities": entities, "ans": ans}}
        try:
            with open(dir_path +  "/Log.json","r") as f:
                logdic: dict = json.loads(f.read())
                logdic.update(newlogdic)
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(logdic, f, indent=4, ensure_ascii=False)
        except:
            with open(dir_path +  "/Log.json","w") as f:
                json.dump(newlogdic, f, indent=4, ensure_ascii=False)
        ## end log

        return [SlotSet("drug_name", drug_name_1)]
## end
