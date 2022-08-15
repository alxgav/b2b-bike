from dotenv import load_dotenv

import os

'''Configuration'''
load_dotenv()

path = os.path.dirname(os.path.realpath(__file__))

PAGE = os.getenv('PAGE')
USER_NAME = os.getenv('USER_NAME')
USER_PASSWORD = os.getenv('USER_PASSWORD')
IDS = os.getenv('IDS')

USER_MAIL = os.getenv('USER_MAIL')
USER_MAIL_PASSWORD = os.getenv('USER_MAIL_PASSWORD')
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = os.getenv('MAIL_PORT')
MAIL_TO = os.getenv('MAIL_TO')

