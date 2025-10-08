# core/loader.py

from dotenv import load_dotenv
import os

def load_env():
    load_dotenv(dotenv_path=".env")
    return dict(os.environ)
