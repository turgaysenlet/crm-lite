import logging
from typing import List

from src.core.access.access_rule import AccessRule
from src.core.access.user import User
from src.core.data.data_object import DataObject

logging.basicConfig()
logger = logging.getLogger("Profile")
logger.setLevel(logging.DEBUG)


class Profile(DataObject):
    users: List[User] = []
    accessRules: List[AccessRule] = []

    def __init__(self, **data):
        super().__init__(**data)
        logger.debug(f"Creating profile {self}...")
