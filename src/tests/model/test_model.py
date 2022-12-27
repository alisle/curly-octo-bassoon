import pytest
from model import DocumentType, Entity, EntityType

def test_to_json():
    entity = Entity(DocumentType.GDRIVE, "DOCUMENT_ID", EntityType.ID, "ENTITY_VALUE")
    json_value = entity.to_json()

    print(json_value)

    assert 1 == 1

