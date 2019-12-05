#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Actions file for RASA with all default actions
"""
import io
import json
import logging.handlers
import time

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from utils import *
from .const import *

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/actions_script.log",
                                                 when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(FOLDER_ABSOLUTE_PATH, "..", ACTION_CONFIG_FILE_NAME)) as f:
    ACTION_CONFIG_JSON = json.load(f)

# Import the user custom script
try:
    exec("import actions.{} as us".format(CUSTOM_SCRIPT_FILE_NAME))
except Exception as e:
    PYTHON_LOGGER.error("Error to import the custom file: {}".format(e))


def default_validator(value, dispatcher: CollectingDispatcher, tracker: Tracker, domain, enity_name, slot_name):
    if any(tracker.get_latest_entity_values(enity_name)):
        # entity was picked up, validate slot
        return {slot_name: value}
    else:
        # no entity was picked up, we want to ask again
        return {slot_name: None}


def get_action_json(tracker, action_name, current_intent, nb_call):
    action_json = ACTION_CONFIG_JSON[action_name][current_intent]
    # If his a dic then the intent have a session
    if type(action_json) is dict:
        for session_value in action_json:
            if tracker.slots[SESSION_SLOT_NAME] == session_value:
                return action_json[session_value][nb_call]
    else:
        return ACTION_CONFIG_JSON[action_name][current_intent][nb_call]


class CustomScript(Action):
    """
    Custom user script executor
    """

    def name(self):
        return CUSTOM_SCRIPT

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        """
        Main method to tun the action
        :param dispatcher: (CollectingDispatcher) The dispatcher which is used to send messages back to the user.
            Use dipatcher.utter_message() or any other rasa_sdk.executor.CollectingDispatcher method.
        :param tracker: (Tracker) The state tracker for the current user. You can access slot values using tracker.
            get_slot(slot_name), the most recent user message is tracker.
            latest_message.text and any other rasa_sdk.Tracker property.
        :param domain: (Dict[Text, Any]) – the bot’s domain
        :return: (List[Dict[Text, Any]]) All the action that the bot need to do
        """
        current_intent, nb_call = get_current_intent(tracker, self.name())
        if current_intent is None:
            error_txt = "Error intern: current intent search for {}!".format(self.name())
            PYTHON_LOGGER.error(error_txt)
            dispatcher.utter_message(error_txt)
            return []
        # Now get the json file into the bot data action config
        custom_script_json = get_action_json(tracker, self.name(), current_intent, nb_call)

        # Change all tag with slot values
        custom_script_json = dict_change_format_var_parser(custom_script_json, tracker)

        # Run the user custom script.
        try:
            res = eval("us.{}".format(custom_script_json["function_name"]))(dispatcher, tracker, domain)
        except Exception as e:
            error_txt = "Error in the execution of {}".format(e)
            PYTHON_LOGGER.error(error_txt)
            dispatcher.utter_message(error_txt)
            return []

        if custom_script_json["output_var_name"] is not None:
            return [SlotSet(custom_script_json["output_var_name"], res)]
        return []


class ApiCall(Action):
    """
    API call action
    """

    def name(self):
        return API_CALL

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        """
        Main method to tun the action
        :param dispatcher: (CollectingDispatcher) The dispatcher which is used to send messages back to the user.
            Use dipatcher.utter_message() or any other rasa_sdk.executor.CollectingDispatcher method.
        :param tracker: (Tracker) The state tracker for the current user. You can access slot values using tracker.
            get_slot(slot_name), the most recent user message is tracker.
            latest_message.text and any other rasa_sdk.Tracker property.
        :param domain: (Dict[Text, Any]) – the bot’s domain
        :return: (List[Dict[Text, Any]]) All the action that the bot need to do
        """
        current_intent, nb_call = get_current_intent(tracker, self.name())
        if current_intent is None:
            error_txt = "Error intern: current intent search for {}!".format(self.name())
            PYTHON_LOGGER.error(error_txt)
            dispatcher.utter_message(error_txt)
            return []

        api_call_json = get_action_json(tracker, self.name(), current_intent, nb_call)
        request_params = {}
        method = api_call_json["method"].lower()
        # Get the method
        call_function = requests.get
        if method == "post":
            call_function = requests.post
        elif method == "put":
            call_function = requests.put
        elif method == "delete":
            call_function = requests.delete

        # Change all tag with slot values
        api_call_json = dict_change_format_var_parser(api_call_json, tracker)

        if api_call_json["header"] != "json":
            request_params["headers"] = api_call_json["header"]
            request_params["data"] = api_call_json["body"]
        else:
            request_params["json"] = api_call_json["body"]

        try:
            res = call_function(api_call_json["url"], **request_params)
        except Exception as e:
            PYTHON_LOGGER.error("Error to call the url {}: {}".format(api_call_json["url"], e))
            dispatcher.utter_message("ouch petit problem avec l'apelle du server")
            return []
        # Now get the response content
        try:
            content = res.json()
        except Exception:
            content = res.text
        # Return all get data
        try:
            json_res = {"status_code": res.status_code, "body": content}
            return [SlotSet(api_call_json["output_var_name"], json_res)]
        except Exception as e:
            PYTHON_LOGGER.error("Error to set the slot: {}".format(e))
            return []


class ResetSlot(Action):
    """
    Slot reset tool
    """

    def name(self):
        return SLOT_RESET

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        """
        Main method to tun the action
        :param dispatcher: (CollectingDispatcher) The dispatcher which is used to send messages back to the user.
            Use dipatcher.utter_message() or any other rasa_sdk.executor.CollectingDispatcher method.
        :param tracker: (Tracker) The state tracker for the current user. You can access slot values using tracker.
            get_slot(slot_name), the most recent user message is tracker.
            latest_message.text and any other rasa_sdk.Tracker property.
        :param domain: (Dict[Text, Any]) – the bot’s domain
        :return: (List[Dict[Text, Any]]) All the action that the bot need to do
        """
        current_intent, nb_call = get_current_intent(tracker, self.name())
        if current_intent is None:
            error_txt = "Error intern: current intent search for {}!".format(self.name())
            PYTHON_LOGGER.error(error_txt)
            dispatcher.utter_message(error_txt)
            return []
        # We dont use the method get_action_json because we need to get all the list
        list_slot_reset_json = ACTION_CONFIG_JSON[self.name()][current_intent]
        try:
            # TODO voire si on reset tout les slot dans la liste ou si on reset que le slot choisie
            print("Reset slots: {}".format(list_slot_reset_json))
            return [SlotSet(slot_name, None) for slot_name in list_slot_reset_json]
        except Exception as e:
            PYTHON_LOGGER.error("Error to reset the slot: {}".format(e))
            return []


class SessionLoader(Action):
    """
    Slot reset tool
    """

    def name(self):
        return SESSION_LOADER

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        """
        Main method to tun the action
        :param dispatcher: (CollectingDispatcher) The dispatcher which is used to send messages back to the user.
            Use dipatcher.utter_message() or any other rasa_sdk.executor.CollectingDispatcher method.
        :param tracker: (Tracker) The state tracker for the current user. You can access slot values using tracker.
            get_slot(slot_name), the most recent user message is tracker.
            latest_message.text and any other rasa_sdk.Tracker property.
        :param domain: (Dict[Text, Any]) – the bot’s domain
        :return: (List[Dict[Text, Any]]) All the action that the bot need to do
        """
        res = []
        with io.open(SESSION_FILE, "r", encoding='utf-8') as f:
            json_data = json.load(f)

        if tracker.sender_id in json_data:
            session_type = "user_know"
            for key in json_data[tracker.sender_id]:
                res.append(SlotSet(key, value=json_data[key]))
        else:
            session_type = "new_user"
        res.append(SlotSet("session_type", session_type))
        return res


class IfCondition(Action):
    """
    if condition
    """

    def name(self):
        return IF_CONDITION

    def run(self, dispatcher, tracker, domain):
        """
        Main method to tun the action
        :param dispatcher: (CollectingDispatcher) The dispatcher which is used to send messages back to the user.
            Use dipatcher.utter_message() or any other rasa_sdk.executor.CollectingDispatcher method.
        :param tracker: (Tracker) The state tracker for the current user. You can access slot values using tracker.
            get_slot(slot_name), the most recent user message is tracker.
            latest_message.text and any other rasa_sdk.Tracker property.
        :param domain: (Dict[Text, Any]) – the bot’s domain
        :return: (List[Dict[Text, Any]]) All the action that the bot need to do
        """
        current_intent, nb_call = get_current_intent(tracker, self.name())
        if current_intent is None:
            error_txt = "Error intern: current intent search for if condition!"
            PYTHON_LOGGER.error(error_txt)
            dispatcher.utter_message(error_txt)
            return []

        condition_dic = get_action_json(tracker, self.name(), current_intent, nb_call)
        for condition in condition_dic:
            if condition == "default":
                continue
            try:
                if eval(condition):
                    eval(condition_dic[condition])
                    return []
            except Exception as e:
                PYTHON_LOGGER.error("Error in the if condition execution:"
                                    "\ncondition: {}\naction: {}\nerror message: {}".format(condition,
                                                                                            condition_dic[condition],
                                                                                            e))
        if "default" not in condition_dic:
            return []
        try:
            eval(condition_dic["default"])
        except Exception as e:
            PYTHON_LOGGER.error("Error to run the default condition:"
                                "\naction: {}\nerror message: {}".format(condition_dic["default"], e))
        return []


class TypingSleep(Action):
    """
    Sleep to simulate typing type
    """

    def name(self):
        return TYPING_SLEEP

    def run(self, dispatcher, tracker, domain):
        """
        Main method to tun the action
        :param dispatcher: (CollectingDispatcher) The dispatcher which is used to send messages back to the user.
            Use dipatcher.utter_message() or any other rasa_sdk.executor.CollectingDispatcher method.
        :param tracker: (Tracker) The state tracker for the current user. You can access slot values using tracker.
            get_slot(slot_name), the most recent user message is tracker.
            latest_message.text and any other rasa_sdk.Tracker property.
        :param domain: (Dict[Text, Any]) – the bot’s domain
        :return: (List[Dict[Text, Any]]) All the action that the bot need to do
        """
        current_intent, nb_call = get_current_intent(tracker, self.name())
        if current_intent is None:
            error_txt = "Error intern: current intent search for if condition!"
            PYTHON_LOGGER.error(error_txt)
            dispatcher.utter_message(error_txt)
            return []

        typing_dic = get_action_json(tracker, self.name(), current_intent, nb_call)
        time.sleep(int(typing_dic["time"]))
