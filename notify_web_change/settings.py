import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Accessing variables.
WEB_LIST = os.getenv("WEB_LIST")
THRESHOLD = os.getenv("THRESHOLD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
MAIL_ACCOUNT = os.getenv("MAIL_ACCOUNT")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
NOTIFY_MAILS = os.getenv("NOTIFY_MAILS")
