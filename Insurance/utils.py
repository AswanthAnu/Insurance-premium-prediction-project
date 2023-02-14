import pandas as pd
import numpy as np
import os
import sys
import dill
import yaml
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

def write_yaml_file(file_path, data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)

        with open(file_path, "w") as file_writer:
            yaml.dump(data, file_writer)

    except Exception as e:
        raise InsuranceException(e, sys)


def convert_columns_float(df:pd.DataFrame, exclude_columns:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_columns:
                if df[column].dtypes != "O":
                    df[column] = df[column].astype('float')
        return df
            
    except Exception as e:
        raise InsuranceException(e, sys)

def save_object(file_path:str, obj:object)->None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise InsuranceException(e, sys)


def load_object(file_path: str,)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not available")
        with open(file_path, "rb") as file_obj:
            return dill.open(file_obj)
    except Exception as e:
        raise InsuranceException(e, sys)


def save_numpy_array_data(file_path:str, array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise InsuranceException(e, sys)


def load_numpy_array_data(file_path:str)->np.array:
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise InsuranceException(e, sys)