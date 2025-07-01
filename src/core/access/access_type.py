from enum import Enum


class AccessType(str, Enum):
    CREATE = "create",
    READ = "read",
    WRITE = "write",
    DELETE = "delete"