## start 0
* start
	- session_loader
	- utter_intent_redirection_welcome

## welcome 1
* welcome
	- slot{"session_type":"user_know"}
	- utter_welcome_1
	- utter_welcome_2
	- utter_welcome_3
	- utter_welcome_4

## welcome 2
* welcome
	- slot{"session_type":"user_know"}
	- utter_welcome_1
	- utter_welcome_2
	- utter_welcome_3
	- utter_welcome_4
* crous
	- utter_crous_12
	- utter_crous_13

## welcome 3
* welcome
	- slot{"session_type":"user_know"}
	- utter_welcome_1
	- utter_welcome_2
	- utter_welcome_3
	- utter_welcome_4
* crous
	- utter_crous_12
	- utter_crous_13
* welcome
	- slot{"session_type":"user_know"}
	- utter_welcome_1
	- utter_welcome_2
	- utter_welcome_3
	- utter_welcome_4
* crous
	- utter_crous_12
	- utter_crous_13

## welcome 4
* welcome
	- slot{"session_type":"new_user"}
	- form_welcome_0
	- form{"name": "form_welcome_0"}
	- form{"name": null}
	- custom_script
	- utter_welcome_8
	- utter_welcome_9
	- utter_welcome_10
	- utter_welcome_11

## welcome 5
* welcome
	- slot{"session_type":"new_user"}
	- form_welcome_0
	- form{"name": "form_welcome_0"}
	- form{"name": null}
	- custom_script
	- utter_welcome_8
	- utter_welcome_9
	- utter_welcome_10
	- utter_welcome_11
* crous
	- utter_crous_12
	- utter_crous_13

## welcome 6
* welcome
	- slot{"session_type":"new_user"}
	- form_welcome_0
	- form{"name": "form_welcome_0"}
	- form{"name": null}
	- custom_script
	- utter_welcome_8
	- utter_welcome_9
	- utter_welcome_10
	- utter_welcome_11
* crous
	- utter_crous_12
	- utter_crous_13
* welcome
	- slot{"session_type":"new_user"}
	- form_welcome_0
	- form{"name": "form_welcome_0"}
	- form{"name": null}
	- custom_script
	- utter_welcome_8
	- utter_welcome_9
	- utter_welcome_10
	- utter_welcome_11
* crous
	- utter_crous_12
	- utter_crous_13

