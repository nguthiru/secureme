from neomodel import (StructuredNode, StringProperty, IntegerProperty,FloatProperty)
from neomodel.contrib.spatial_properties import PointProperty
class StationEntity(StructuredNode):
    entity_id = IntegerProperty(unique_index=True)
    name = StringProperty(unique_index=True)
    longitude = FloatProperty()
    latitude = FloatProperty()
    location = PointProperty(crs='wgs-84')

    def __dict__(self):
        properties = {
            "entity_id": self.entity_id,
            "name": self.name,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "location": self.location
        }
        return properties