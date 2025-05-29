from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from bson import ObjectId

from models import NetworkFlow, NetworkFlowUpdate

router = APIRouter()

@router.get("/", response_description="List all network flow elements", response_model=List[NetworkFlow])
def list_flows(request: Request):
    network_flows = list(request.app.database["botnet_traffic_data"].find(limit=733705))
    return network_flows

@router.post("/", response_description="Add a new network flow", status_code=status.HTTP_201_CREATED, response_model=NetworkFlow)
def create_flow(request: Request, flow: NetworkFlow = Body(...)):
    flow = jsonable_encoder(flow)
    new_flow = request.app.database["botnet_traffic_data"].insert_one(flow)
    created_flow = request.app.database["botnet_traffic_data"].find_one(
        {"_id": new_flow.inserted_id}
    )
    return created_flow

@router.get("/{id}", response_description="Get a single flow by id", response_model=NetworkFlow)
def find_flow(id: str, request: Request):
    if (flow := request.app.database["botnet_traffic_data"].find_one({"_id": id})) is not None:
        return flow
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flow with ID {id} not found")

@router.delete("/{id}", response_description="Delete a flow")
def delete_flow(id: str, request: Request, response: Response):
    delete_result = request.app.database["botnet_traffic_data"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flow with ID {id} not found")
