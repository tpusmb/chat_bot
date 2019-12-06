#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json
import logging.handlers
import os
from copy import deepcopy
from string import Formatter

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/actions_utils.log",
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


def get_current_intent(tracker, action_name):
    current_intent = None
    nb = 0
    # TODO bug du welcome intent
    for i in range(len(tracker.events) - 1, 0, -1):
        event = tracker.events[i]
        if event["event"] == "user" and event["parse_data"]["intent"]["name"] is not None:
            current_intent = event["parse_data"]["intent"]["name"]
            break
        elif event["event"] == "action" and event["name"] == action_name:
            nb += 1
    return current_intent, nb


def format_var_parser(text):
    return [fn for _, fn, _, _ in Formatter().parse(text) if fn is not None]


def change_format_var_parser(text, tracker):
    """
    Remplace all tag slot with his own value
    :param text: (string) text to replace the tag need to be like this "{my_slot_name}"
    :param tracker: Rasa tracker to get slot value
    :return: (string) the text with replace value
    """
    param_names = format_var_parser(text)
    param_vars = {}
    for param_name in param_names:
        try:
            param_vars[param_name] = tracker.get_slot(param_name)
        except Exception as e:
            PYTHON_LOGGER.error("Error to get var name {}: {}".format(param_name, e))
    return text.format(**param_vars)


def dict_change_format_var_parser(dictionary, tracker):
    """
    Change all tag slot into the given dictionary (recursively).
    :param dictionary: (dict) dictionary to process
    :param tracker: Rasa tracker to get slot value
    :return: (dict) dictionary with all replace values
    """
    dictionary = deepcopy(dictionary)
    pile = [dictionary]
    while len(pile) > 0:
        dictionary_to_process = pile.pop(0)
        for key in dictionary_to_process:
            if type(dictionary_to_process[key]) is dict:
                pile.append(dictionary_to_process[key])
            elif type(dictionary_to_process[key]) is str:
                dictionary_to_process[key] = change_format_var_parser(dictionary_to_process[key], tracker)
    return dictionary
