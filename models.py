import uuid
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handle: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.any_schema()
        )
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        return ObjectId(v)

class NetworkFlow(BaseModel):
    id: PyObjectId = Field(alias="_id")
    pkSeqID: int = Field(...)
    proto: str = Field(...)
    saddr: str = Field(...)
    sport: str = Field(...)
    daddr: str = Field(...)
    dport: str = Field(...)
    seq: int = Field(...)
    stddev: float = Field(...)
    N_IN_Conn_P_SrcIP: int = Field(...)
    min: float = Field(...)
    state_number: int = Field(...)
    mean: float = Field(...)
    N_IN_Conn_P_DstIP: int = Field(...)
    drate: float = Field(...)
    srate: float = Field(...)
    max: float = Field(...)
    attack: int = Field(...)
    category: str = Field(...)
    subcategory: str = Field(...)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str
        }
    }

class NetworkFlowUpdate(BaseModel):
    pkSeqID: int = Field(...)
    proto: str = Field(...)
    saddr: str = Field(...)
    sport: str = Field(...)
    daddr: str = Field(...)
    dport: str = Field(...)
    seq: int = Field(...)
    stddev: float = Field(...)
    N_IN_Conn_P_SrcIP: int = Field(...)
    min: float = Field(...)
    state_number: int = Field(...)
    mean: float = Field(...)
    N_IN_Conn_P_DstIP: int = Field(...)
    drate: float = Field(...)
    srate: float = Field(...)
    max: float = Field(...)
    attack: int = Field(...)
    category: str = Field(...)
    subcategory: str = Field(...)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str
        }
    }