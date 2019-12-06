#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from rasa_sdk import Tracker
import os

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
JSON_DB_PATH = os.path.join(FOLDER_ABSOLUTE_PATH, "..", "..", "session.json")


def save_user(dispatcher, tracker: Tracker, domain):
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
    full_json = {}
    try:
        with open(JSON_DB_PATH, 'r', encoding='utf-8') as f:
            full_json = json.load(f)
    except FileNotFoundError:
        pass
    user_info = {}
    user_info["user_name"] = tracker.slots["user_name"]
    user_info["user_surname"] = tracker.slots["user_surname"]
    user_info["user_email"] = tracker.slots["user_email"]
    full_json[tracker.sender_id] = user_info

    with open(JSON_DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(full_json, f)

    dispatcher.utter_message("{} votre email {} a été rajouter !".format(tracker.slots["user_name"],
                                                                         tracker.slots["user_email"]))
