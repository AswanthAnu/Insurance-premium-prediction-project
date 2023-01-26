import pandas as pd
import numpy as np 
import pymongo
import json
import os, sys
from dataclasses import dataclass
import urllib

@dataclass
class EnvironmentVariable:
    mongodb_client_url_1:str = os.getenv("MONGODB_CLIENT_URL_1")
    mongodb_client_url_2:str = os.getenv("MONGODB_CLIENT_URL_2") 
    mongodb_client_url_3:str = os.getenv("MONGODB_CLIENT_URL_3")
    mongodb_client_url = mongodb_client_url_1+urllib.parse.quote(mongodb_client_url_2)+mongodb_client_url_3  
    print(mongodb_client_url)  # assign the value of the environment variable named "MONGODB_CLIENT_URL_1 , 2, 3" to the class variable "mongodb_client_url"

env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongodb_client_url)
TARGET_COLUMN = "expenses"
print("env_var.mongo_db_url")