from enum import Enum

class StreamName(str, Enum):
    NEW_ENTITY : str = "new-document-entity"
    NEW_DOCUMENT : str = "new-document"
    NEW_API_HUMAN : str = "new-api-human"  
    NEW_API_ENTIY : str = "new-api-entity"    
    

    
