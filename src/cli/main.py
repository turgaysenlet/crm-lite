import logging
import uuid

from src.core.access.profile import Profile
from src.core.access.user import User
from src.core.data.case_object import Case
from src.core.data.data_field import DataField
from src.core.data.data_object import DataObject
from src.storage.database import DataBase

logging.basicConfig()
logger = logging.getLogger("CLI Main")
logger.setLevel(logging.INFO)


def main():
    logger.debug("Starting CLI")
    logger.info("Welcome to CRM-Lite CLI")

    # Create objects
    case1: Case = Case(name="Case 1")
    user1: User = User(name="User 1 - All access")
    user2: User = User(name="User 2 - Limited access")
    profile1: Profile = Profile(name="Profile 1 - All access")
    profile2: Profile = Profile(name="Profile 1 - Limited access")

    # Assign object relations
    profile1.users.append(user1)
    profile2.users.append(user2)

    # Log objects
    logger.info(f"{user1}")
    logger.info(f"{user2}")
    logger.info(f"{profile1}")
    logger.info(f"{profile2}")

    logger.info(f"Data Object count: {DataObject.type_counts()}")
    logger.info(f"Data Field count: {DataField.count}")

    db: DataBase = DataBase(db_name="../../database/crm.db")
    db.init_db_schema()

    db.connect()
    rows = db.list_table("ObjectDefinition")
    logger.info(f"ObjectDefinition list: {rows}")

    logger.debug("Stopping CLI")


if __name__ == "__main__":
    main()
