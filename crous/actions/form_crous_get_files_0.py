#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

import actions.actions as ac

class Form0(FormAction):
    """
    Example of a custom form action
    """

    def name(self) -> Text:
        """
        Unique identifier of the form
        """
        return "form_crous_get_files_0"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """
        A list of required slots that the form has to fill
        """
        return ['guarantor_name']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """
        A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked
        """
        return {"guarantor_name": [self.from_text()], }

    

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        """
        Call the action script
        """
        print("Form " + self.name() + " have finish !")
        return []
