from pymongo import MongoClient
import pandas as pd

def get_database(): #executed once
   #creates database and fetches database
   CONNECTION_STRING = ""
   client = MongoClient(CONNECTION_STRING)
   return client['botnet_traffic_dataset']

def csv_to_df(file_name):
   df = pd.read_csv(file_name)
   return pd.Series(df.to_dict(orient='records'))

def create_collection(data): #executed once
   #creates collection in atlas cluster
   db = get_database()
   collection = db['botnet_traffic_data']
   entries = {}
   i = 0
   for row in data:
      entries[i] = row
      i += 1
   collection.insert_many(entries.values())

def get_elements(collection):
   #get collection elements in the form of a pandas dataframe
    item_details = collection.find()
    items_df = pd.DataFrame(item_details)
    return items_df

def index_data(collection, idx):
    #create index on collection based on idx parameter
    pkSeqID_index = collection.create_index(idx)
    item_details = collection.find({"pkSeqID": "792371"})
    return item_details
    
