from pydantic import BaseModel
from typing import Dict, Any, Optional


class DialogflowRequest(BaseModel):
    fulfillmentInfo: Dict[str, Any]
    sessionInfo: Dict[str, Any]


class DialogflowResponse(BaseModel):
    fulfillment_response: Dict[str, Any]
    sessionInfo: Optional[Dict[str, Any]] = None