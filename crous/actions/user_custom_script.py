#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import random

from rasa_sdk import Tracker
import os

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
JSON_DB_PATH = "../session.json"


def is_user_eligible(dispatcher, tracker: Tracker, domain):
    """
    car change custom script
    :param dispatcher: (CollectingDispatcher) The dispatcher which is used to send messages back to the user.
        Use dipatcher.utter_message() or any other rasa_sdk.executor.CollectingDispatcher method.
    :param tracker: (Tracker) The state tracker for the current user. You can access slot values using tracker.
        get_slot(slot_name), the most recent user message is tracker.
        latest_message.text and any other rasa_sdk.Tracker property.
    :param domain: (Dict[Text, Any]) – the bot’s domain
    :return: (List[Dict[Text, Any]]) All the action that the bot need to do
    """
    km = random.randint(30, 500)  # TODO API
    if int(tracker.slots["annual_income"]) > 25_000:
        dispatcher.utter_message(f"Sorry {tracker.slots['user_name']}, you are NOT eligible to the CROUS since "
                                 f"your income ({tracker.slots['annual_income']}€) is too high")

    elif km < 45:
        dispatcher.utter_message(f"Sorry {tracker.slots['user_name']}, you are NOT eligible to the CROUS since "
                                 f"the distance between your home and university is too low ({km}km calculated by our API)")
    else:
        dispatcher.utter_message(f"Congrats {tracker.slots['user_name']}, you ARE eligible to the CROUS !")
        dispatcher.utter_message(f"To apply to a crous accommodation, please give me your RIB")
        dispatcher.utter_template("quest_rib_redirection", tracker)


def get_user_guarantor(dispatcher, tracker: Tracker, domain):
    dispatcher.utter_template("quest_crous_don", tracker)
