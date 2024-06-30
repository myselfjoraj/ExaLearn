import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

DB_URL = os.getenv('DB_URL')

STORAGE_URL = os.getenv('STORAGE_URL')

SMTP_EMAIL = os.getenv('SMTP_EMAIL')

SMTP_PASS = os.getenv('SMTP_PASS')

SMTP_SERVER = os.getenv('SMTP_SERVER')

SMTP_PORT = os.getenv('SMTP_PORT')

