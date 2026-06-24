# config.py

import os
from pathlib import Path
from dotenv import load_dotenv
 
# __file__ is the path for current file
# .parent is src folder
# .parent.parent is the project root (vis_mon_system) 
base_dir = Path(__file__).resolve().parent.parent

#path to .env
env_file_path = base_dir/".env"

# loading variables from the .env
load_dotenv(dotenv_path=env_file_path)

# get variables
class Config:
	base_url = os.getenv("base_url")
	user_name = os.getenv("user_name")
	user_password = os.getenv("user_password")
	DB_PATH = os.getenv("DB_PATH")
