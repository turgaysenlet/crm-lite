import logging
from typing import List, Optional

from src.core.access.access_type import AccessType
from src.core.data.data_field import DataField
from src.core.data.data_object import DataObject

logging.basicConfig()
logger = logging.getLogger("AccessRule")
logger.setLevel(logging.DEBUG)


class AccessRule(DataObject):
    dataObject: Optional[DataObject] = None
    dataField: Optional[DataField] = None
    accessType: AccessType

    def __init__(self, **data):
        super().__init__(**data)
        logger.debug(f"Creating profile {self}...")
