import pandas as pd
import numpy as np
import os
import sys
from Insurance.exception import InsuranceException
from Insurance.config import mongo_client
from Insurance.logger import logging


def get_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:
    """
    This function reads the data from the database and collection specified in the input and returns it as a DataFrame
    :param database_name: name of the database
    :param collection_name: name of the collection
    :return: DataFrame
    """
    try:
        logging.info(f"Reading data from database :{database_name} and collection:{collection_name}")
        df = pd.DataFrame.from_records(mongo_client[database_name][collection_name].find())  #creating Dataframe using pandas and mongo_client
        logging.info(f"Find columns:{df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping columns: _id")
            df = df.drop("_id", axis=1)
        logging.info(f"Rows and Columns in df:{df.shape}")
        return df
    except Exception as e:
        raise InsuranceException(e, sys)
