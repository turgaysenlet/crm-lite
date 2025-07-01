import logging

from pydantic import BaseModel

from src.core.data.data_object import DataObject

logging.basicConfig()
logger = logging.getLogger("User")
logger.setLevel(logging.DEBUG)


class User(DataObject):

    def __init__(self, **data):
        super().__init__(**data)
        logger.debug(f"Creating user {self}...")
