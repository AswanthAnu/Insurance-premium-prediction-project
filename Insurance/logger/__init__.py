from datetime import datetime
import logging
import os

# Defining the directory
LOG_DIR = "Insurance_log" # log will store in this file

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}" # error occured time

LOG_FILE_NAME = f"log_{CURRENT_TIME_STAMP}.log" 

os.makedirs(LOG_DIR, exist_ok = True) # if LOG_DIR is available then skip else create a file

LOG_FILE__PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(filename=LOG_FILE__PATH, 
                    filemode="w",
                    format='[%(asctime)s] %(name)s %(levelname)s %(message)s',
                    # level=logging.INFO,
                    level=logging.DEBUG)