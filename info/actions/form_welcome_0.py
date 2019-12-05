#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

from actions import actions as ac


class Form0(FormAction):
    """
    Example of a custom form action
    """

    def name(self) -> Text:
        """
        Unique identifier of the form
        """
        return "form_welcome_0"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """
        A list of required slots that the form has to fill
        """
        return ['user_name', 'user_surname', 'user_email']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """
        A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked
        """
        return {"user_name": [self.from_text()], "user_surname": [self.from_text()], "user_email": [self.from_entity(entity="email"), self.from_text()], }

    
    def validate_user_email(self, value, dispatcher, tracker, domain):
        return ac.default_validator(value, dispatcher, tracker, domain, "email", "user_email")

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        """
        Call the action script
        """
        print("Form " + self.name() + " have finish !")
        return []
