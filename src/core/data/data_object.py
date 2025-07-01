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
    fields: List[DataField] = []
    _type_counts: ClassVar[Dict[Type, int]] = {}

    def __init__(self, **data):
        super().__init__(**data)
        cls = type(self)
        cls._type_counts[cls] = cls._type_counts.get(cls, 0) + 1
        logger.debug(f"Creating data object: {self} for {self.__class__.__name__} class")

    @classmethod
    def type_counts(cls):
        return cls._type_counts
