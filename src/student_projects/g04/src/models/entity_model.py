from datetime import datetime
from abc import ABC, abstractmethod
from typing import Dict, Any

from bson import ObjectId


class Entity(ABC):
    def __init__(self, id: str | None = None, created_at: datetime | None = None, updated_at: datetime | None = None):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at

    @abstractmethod
    def to_dict(self, for_db: bool = False) -> Dict[str, Any]:
        data: Dict[str, Any] = {}

        if for_db:
            if self.id:
                data['_id'] = ObjectId(self.id)

            if not self.created_at:
                data['created_at'] = datetime.now()
                data['updated_at'] = None
            elif not self.updated_at:
                data['updated_at'] = datetime.now()
        else:
            data['id'] = self.id if self.id else None

        return data
