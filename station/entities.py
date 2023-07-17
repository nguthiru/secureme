from neomodel import (StructuredNode,StructuredRel, StringProperty, IntegerProperty,DateProperty,DateTimeProperty,RelationshipTo)

class CrimeEntity(StructuredNode):
    entity_id = IntegerProperty(unique_index=True)
    name = StringProperty(unique_index=True)
    description = StringProperty()

    __label__ = "Crime"

    def __dict__(self):
        properties = {
            "entity_id": self.entity_id,
            "name": self.name,
            "description": self.description,
        }
        return properties
    
class CommitedRelationship(StructuredRel):
    datetime = DateTimeProperty()
    casualities = IntegerProperty()
    __label__ = "Commited"

class CriminalEntity(StructuredNode):
    # entity_id = IntegerProperty(unique_index=True)
    name = StringProperty()
    # nickname = StringProperty()
    date_of_birth = DateProperty()
    image_url = StringProperty()
    height = IntegerProperty()
    id_num = IntegerProperty(unique_index=True)
    # crime_commited = RelationshipTo(CrimeEntity,'COMMITTED',model=CommitedRelationship)

    __label__ = "Criminal"

    def __dict__(self):
        properties = {
            # "entity_id": self.entity_id,
            "name": self.name,
            # "nickname": self.nickname,
            "dateOfBirth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "imageUrl": self.image_url,
            "height": self.height,
            "idNumber": self.id_num
        }
        return properties

