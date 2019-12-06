#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# TODO permertre de facilement changer le suelette du projet build

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
FILE_ABSOLUTE_PATH = os.path.normpath(os.path.abspath(__file__))

# _________________/BUILD PROJECT CONST\______________________
# All const to manage all output folder names, path


# Name of the intents folder of the project to build
INTENT_FOLDER = "intents"
# Name of the sentences folder of the project to build
SENTENCES_FOLDER = "sentences_data"

# Where to build the project
BUILD_FOLDER = "out"

# Rasa data folder to save nlu and stories
DATA_FOLDER = "data"
# Path to the stories folder
STORIES_FOLDER = os.path.join(DATA_FOLDER, "stories")
# Path to nlu folder
NLU_FOLDER = os.path.join(DATA_FOLDER, "nlu")

# Where to save all actions
ACTIONS_FOLDER = "actions"
# Where to save all files for the bot
BOT_DATA_FOLDER = os.path.join(ACTIONS_FOLDER, "bot_data")
# Where to save all information for all actions (Json api call, Customs cript, etc)
ACTION_CONFIG_FILE_NAME = os.path.join(BOT_DATA_FOLDER, "actions_config.json")

# Name of the user custom script file
CUSTOM_SCRIPT_FILE_NAME = "user_custom_script"

# Name of the project config json file
PROJECT_CONFIG_FILE_NAME = "project.json"

# TODO tempt const to test
SESSION_FILE = "../session.json"

# _________________/TEMPLATES NAMES\______________________
# All templates name

# DISPLAY
MENU = "menu"
TEXT = "text"

# ACTIONS
SLOT_RESET = "slot_reset"
API_CALL = "api_call"
CUSTOM_SCRIPT = "custom_script"
IF_CONDITION = "if_condition"
INTENT_REDIRECTION = "intent_redirection"
URL_REDIRECTION = "url_redirection"
SESSION_LOADER = "session_loader"
TYPING_SLEEP = "typing_sleep"
QUEST_REDIRECTION = "quest_redirection"

# Collect data
FORM = "form"

# ______________/PROJECT STRUCT CONST\_________________
# Rasa project struct to be build

# Name of the session slot
SESSION_SLOT_NAME = "session_type"

# Body of the config TODO ajouter lang dynamic
CONFIG = {
    "language": "en",
    "pipeline": [],
    "policies": []
}
# Chanel to run the bot
CREDENTIALS = {
    "rest": None
}
# Where to get the action server
ENDPOINT = {
    "action_endpoint": {
        "url": "http://localhost:5055/webhook"
    }
}
# Main domain body to save all intents, actions, forms, etc
DOMAIN = {
    "intents": [],
    "slots": {
        SESSION_SLOT_NAME: {
            "type": "categorical",
            "values": []
        }
    },
    "templates": {},
    "actions": [API_CALL, SLOT_RESET, CUSTOM_SCRIPT, IF_CONDITION, SESSION_LOADER, TYPING_SLEEP],
    "forms": []
}

# Prefix of the utter action
UTTER_NAME_PREFIX = "utter"
# Template of a name
UTTER_NAME_TEMPLATE = UTTER_NAME_PREFIX + "_{}_{}"

# Path to get all default files need to be put into the output project
DEFAULT_FILES_PATH = os.path.join(FOLDER_ABSOLUTE_PATH, "default_files")
# Path to the default action script
DEFAULT_ACTIONS_PATH = os.path.join(DEFAULT_FILES_PATH, "actions.py")
# Path to the default config
CONFIG_FILE_NAME = os.path.join(DEFAULT_FILES_PATH, "config.yml")

# Template of a call validator function. He will call the real validator function
VALIDATOR_FUNCTION_BODY = """
    def validate_{slot_name}(self, value, dispatcher, tracker, domain):
        return {validator_function}"""
# Template of a custom validator call
VALIDATOR_FUNCTION_CALL = "ac.us.{}(value, dispatcher, tracker, domain, \"{}\", \"{}\")"
# Default validator function call
DEFAULT_VALIDATOR_FUNCTION_CALL = "ac.default_validator(value, dispatcher, tracker, domain, \"{}\", \"{}\")"
# Template of session check into rasa stories
TEMPLATE_SESSION_CHECK = "slot{{\"" + SESSION_SLOT_NAME + "\":\"{}\"}}"