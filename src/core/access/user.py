import logging
from typing import List

from pydantic import BaseModel

from src.core.data.data_field import DataField
from src.core.data.data_object import DataObject
from src.core.data.field_type import FieldType

logging.basicConfig()
logger = logging.getLogger("User")
logger.setLevel(logging.DEBUG)


class User(DataObject):

    @classmethod
    def get_fields(cls) -> List[DataField]:
        return [DataField(name="First Name", api_name="first_name", field_type=FieldType.TEXT),
                DataField(name="Last Name", api_name="last_name", field_type=FieldType.TEXT)]

    def __init__(self, **data):
        super().__init__(name="User",
                         api_name="user",
                         description="User object",
                         fields=User.get_fields())
        logger.debug(f"Creating user {self}...")
