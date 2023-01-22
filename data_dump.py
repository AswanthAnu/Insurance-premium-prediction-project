import pymongo
import pandas as pd
import json
import urllib # escape special characters in the MongoDB connection string, because my password contains "@"

# create a client object to connect to mongoDB server
client = pymongo.MongoClient("mongodb+srv://aswanthanu:"+ urllib.parse.quote("Aswanth@123") +"@cluster0.kiy2tzw.mongodb.net/?retryWrites=true&w=majority")
db = client.test

# save the path of csv file to a variable
DATA_PATH = (r"C:\Users\aswan\Documents\Insurance premium prediction\Insurance-premium-prediction-project\medicall.csv")

# create database
INSURANCE_DATABASE = 'Insurance_DB'

# create collection
COLLECTION_NAME = 'Insurance_collection'


if __name__ == '__main__':

    # create dataframe using pandas read_csv
    df = pd.read_csv(DATA_PATH)

    # printing the shape of rows and columns in the dataframe
    print(f'No of rows : {df.shape[0]}\nNo of columns : {df.shape[1]}')

    # dropping the index of the dataframe
    df.reset_index(drop=True, inplace=True)

    # Transpose the data and then convert it into json format
    load_json = list(json.loads(df.T.to_json()).values())
    print(load_json[0])

    # inserting the data into database
    client[INSURANCE_DATABASE][COLLECTION_NAME].insert_many(load_json)

