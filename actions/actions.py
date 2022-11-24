from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from bs4 import BeautifulSoup
import requests
import time 

def get_price_coin(coin):
    url="https://www.google.com/search?q="+coin+"+price&hl=en"
    HTML= requests.get(url)
    soup=BeautifulSoup(HTML.text,"html.parser")
    text=soup.find('div', attrs={'class':'BNeawe iBp4i AP7Wnd'}).find('div', attrs={'class':'BNeawe iBp4i AP7Wnd'}).text
    return text
def get_price_stock(stock):
    url="https://www.google.com/finance/quote/"+stock
    HTML= requests.get(url)
    soup=BeautifulSoup(HTML.text,"html.parser")
    count=0
    return soup.find_all('div', attrs={'class':'YMlKec'})[10].text   


class ActionGiveCoinPrice(Action):

    def name(self) -> Text:
        return "action_give_coin_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_coin = next(tracker.get_latest_entity_values("coin"), None)
        
        if not current_coin:
            msg = "the tunisian dinar is stable. you can give me another currency and see how much is it worth in TND"
            dispatcher.utter_message(text=msg)
            return []
        
       
                
        msg = f"One {current_coin} is now worth {get_price_coin(current_coin)} ."
        dispatcher.utter_message(text=msg)
        
        return []


class ActionGiveStockPrice(Action):

    def name(self) -> Text:
        return "action_give_stock_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_stock = next(tracker.get_latest_entity_values("stock"), None)
        
        if not current_stock:
            msg = "i can t seem to recognize the stock you are asking about. would you please rephrase"
            dispatcher.utter_message(text=msg)
            return []
        
       
                
        msg = f"The {current_stock} stock price is now  {get_price_stock(current_stock)} ."
        dispatcher.utter_message(text=msg)
        
        return []
