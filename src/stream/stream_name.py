from enum import Enum

from model import EntityType

class StreamName(str, Enum):
    NEW_DOCUMENT : str = "new-document"
    NEW_API_HUMAN : str = "new-api-human"  
    NEW_API_ENTIY : str = "new-api-entity"    
    NEW_API_COMPANY : str = "new-api-company"
    NEW_API_COMPANY_HUMAN : str = "new-api-company-human" 
    

    
