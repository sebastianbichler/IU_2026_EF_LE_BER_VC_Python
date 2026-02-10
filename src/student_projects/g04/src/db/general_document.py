from datetime import datetime
from typing import TypedDict
from bson import ObjectId

class GeneralDoc(TypedDict):
    id: ObjectId
    created_at: datetime
    updated_at: datetime