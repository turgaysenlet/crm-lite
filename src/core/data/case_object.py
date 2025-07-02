import logging
from typing import List

from src.core.data.data_field import DataField
from src.core.data.data_object import DataObject

logging.basicConfig()
logger = logging.getLogger("CaseObject")
logger.setLevel(logging.DEBUG)


class Case(DataObject):
    @classmethod
    def get_fields(cls) -> List[DataField]:
        return []

    def __init__(self, **data):
        super().__init__(name="Case",
                         api_name="case",
                         description="Case",
                         fields=Case.get_fields())
        logger.debug(f"Creating case: {self}")
