from dotenv import load_dotenv

import os

'''Configuration'''
load_dotenv()

path = os.path.dirname(os.path.realpath(__file__))

PAGE = os.getenv('PAGE')
USER_NAME = os.getenv('USER_NAME')
USER_PASSWORD = os.getenv('USER_PASSWORD')
IDS = os.getenv('IDS')

