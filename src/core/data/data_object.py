import time
import uuid
import logging
from typing import Optional, List, ClassVar, Dict, Type

from pydantic import BaseModel, Field

from src.core.data.data_field import DataField

logging.basicConfig()
logger = logging.getLogger("DataObject")
logger.setLevel(logging.DEBUG)


class DataObject(BaseModel):
    name: str
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    api_name: str
    description: Optional[str] = None
    created_at: float = 0
    updated_at: float = 0
    fields: List[DataField] = []
    _type_counts: ClassVar[Dict[Type, int]] = {}

    def __init__(self, **data):
        super().__init__(**data)
        now = time.time()
        self.created_at = data.get("created_at", now)
        self.updated_at = data.get("updated_at", now)
        cls = type(self)
        cls._type_counts[cls] = cls._type_counts.get(cls, 0) + 1
        logger.debug(f"Creating data object: {self} for {self.__class__.__name__} class")

    @classmethod
    def type_counts(cls):
        return cls._type_counts
