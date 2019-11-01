#!/usr/bin/env python
#-*- coding: utf-8 -*-
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.model import Metadata, Interpreter
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.agent import Agent

interpreter = RasaNLUInterpreter("models/current/nlu")
print(interpreter.parse("你好"))
agent = Agent.load('models/dialogue', interpreter=interpreter)
#print(agent.handle_message('你好呀'))
print(agent.handle_message('你好呀')[0].get('text'))
