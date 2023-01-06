from enum import Enum

class StreamName(str, Enum):
    NEW_ENTITY : str = "new-entity"
    NEW_DOCUMENT : str = "new-document"
    NEW_USER : str = "new-user"

    
