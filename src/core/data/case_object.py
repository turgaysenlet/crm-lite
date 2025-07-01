import logging

from src.core.data.data_object import DataObject

logging.basicConfig()
logger = logging.getLogger("CaseObject")
logger.setLevel(logging.DEBUG)


class CaseObject(DataObject):
    def __init__(self, **data):
        super().__init__(**data)
        logger.debug(f"Creating data object: {self} for {self.__class__.__name__} class")
