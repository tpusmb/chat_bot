# Nuits de l'info 2019 ChatBot

## Installation

### Apt to install

You will need the following package:
    
    sudo apt install python3
    sudo apt install virtualenv
    sudo apt install python3-pip
    sudo apt install python3-tk
    sudo apt install cmake
    sudo apt install rabbitmq-server

### Installation crous & info bot

Prepare your virtualenv:

    virtualenv -p python3 venv
    . venv/bin/activate

Il faut simplement installer rasa
    
    pip install rasa

### Installation de open_bot

Prepare your virtualenv:

    virtualenv -p python3 venv
    . venv/bin/activate

Puis installer les requirements

    pip install -r requirements.txt

### Installation de duckling

Pour installer duckling

    sudo docker run -p 8000:8000 rasa/duckling

## Quick start

### Start info or crous bot

Il faut aller dans `chat_bot/info`

Pour entrainer le model taper

    rasa train
    
Puis pour le tester

    rasa shell
    
Il faut aussi lancer le server actions & open_bot dans`chat_bot/open_bot`

    rasa run actions --actions actions
    python application.py
    
 
Pour crous bot c'est exatement pareille

### Start open_bot

Open bot peut être sois utiliser a l'aide d'un server REST ou sois via le terminal

Pour le server REST

    python application.py

Via le terminal 

    python interact.py
