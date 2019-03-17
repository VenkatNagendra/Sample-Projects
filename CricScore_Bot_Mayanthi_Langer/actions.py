from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

class ActionMatch(Action):
    def name(self):
        return 'action_match'
    
    def run(self, dispatcher, tracker, domain):
        from pycricbuzz import Cricbuzz
        c = Cricbuzz()
        mats = tracker.get_slot("matches")
        response = ""
        for match in c.matches():
            response = response + str(match['srs']) + "\n"
        response = response + "Select the Match"
        dispatcher.utter_message(response)
        return [SlotSet('matches',mats)]

class ActionScore(Action):
    def name(self):
        return 'action_score'
    
    def run(self, dispatcher, tracker, domain):
        from pycricbuzz import Cricbuzz
        c = Cricbuzz()
        scr = tracker.get_slot('match_between')
        response = ""
        for match in c.matches():
            response = response + str(match['status']) + "\n"
        response = response + "Select the Match"
        dispatcher.utter_message(response)
        return [SlotSet('match_between',scr)]