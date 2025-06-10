from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from bson import ObjectId
import pickle
from pymongo import MongoClient
import pandas as pd
from train_model import parse_flows, process_ip_cols

from methods import parse_input_flow
import traceback

infer_router = APIRouter()

client = MongoClient("mongodb+srv://rachelhuang505:24uHXEpaIdqM1jEU@iotdatabase.seqo5qb.mongodb.net/?retryWrites=true&w=majority&appName=IoTDatabase")
db = client["botnet_traffic_dataset"]
collection = db["trained_single_class_model"]

document = collection.find_one({"filename": "trained_model.pkl"})

pickled_model_bytes = document["model_data"]
loaded_model, loaded_encoder, loaded_scaler = pickle.loads(pickled_model_bytes)

@infer_router.post("/infer", response_description="Test model classification on a flow")
async def test_model(request:Request):
    try: 
        flow = await request.json()
        flow_data = parse_input_flow(flow)
        X_init, _ = parse_flows([flow_data])
        X_df = pd.DataFrame([X_init[0]], columns = ['pkSeqID', 'proto', 'saddr', 'sport', 'daddr', 'dport', 'seq', 'stddev', 'N_IN_Conn_P_SrcIP', 'min', 'state_number', 'mean', 'N_IN_Conn_P_DstIP', 'drate', 'srate', 'max', 'category', 'subcategory'])

        X_df = process_ip_cols(X_df)
        one_hot_x_df = pd.DataFrame(
            loaded_encoder.transform(X_df[['proto', 'category', 'subcategory']]),
            columns=loaded_encoder.get_feature_names_out(['proto', 'category', 'subcategory'])
        )
        X_df = pd.concat([X_df.drop(['proto', 'category', 'subcategory'], axis=1), one_hot_x_df], axis=1)
        X_scaled = loaded_scaler.transform(X_df)

        predictions = loaded_model.predict(X_scaled)
        return predictions.tolist()
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}")
