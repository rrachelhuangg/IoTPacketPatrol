from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from bson import ObjectId
import pickle
from pymongo import MongoClient
import pandas as pd
from train_model import get_flows, parse_flows, process_ip_cols

from models import NetworkFlow, NetworkFlowUpdate

infer_router = APIRouter()

client = MongoClient("mongodb+srv://rachelhuang505:24uHXEpaIdqM1jEU@iotdatabase.seqo5qb.mongodb.net/?retryWrites=true&w=majority&appName=IoTDatabase")
db = client["botnet_traffic_dataset"]
collection = db["trained_single_class_model"]

document = collection.find_one({"filename": "trained_model.pkl"})

pickled_model_bytes = document["model_data"]
loaded_model, loaded_encoder, loaded_scaler = pickle.loads(pickled_model_bytes)

@infer_router.get("/infer", response_description="Test model classification on a flow")
def test_model():
    try: 
        flows = get_flows()[4522:4523]
        X_init, _ = parse_flows(flows)
        X_df = pd.DataFrame([X_init[0]], columns = ['pkSeqID', 'proto', 'saddr', 'sport', 'daddr', 'dport', 'seq', 'stddev', 'N_IN_Conn_P_SrcIP', 'min', 'state_number', 'mean', 'N_IN_Conn_P_DstIP', 'drate', 'srate', 'max', 'category', 'subcategory'])

        X_df = process_ip_cols(X_df)
        print("flow id: ", X_df['pkSeqID'])
        one_hot_x_df = pd.DataFrame(
            loaded_encoder.transform(X_df[['proto', 'category', 'subcategory']]),
            columns=loaded_encoder.get_feature_names_out(['proto', 'category', 'subcategory'])
        )
        X_df = pd.concat([X_df.drop(['proto', 'category', 'subcategory'], axis=1), one_hot_x_df], axis=1)
        X_scaled = loaded_scaler.transform(X_df)

        predictions = loaded_model.predict(X_scaled)
        return predictions.tolist()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}")
