from neomodel import (StructuredNode, StringProperty, IntegerProperty,)
from neomodel.contrib.spatial_properties import PointProperty
class StationEntity(StructuredNode):
    entity_id = IntegerProperty(unique_index=True)
    name = StringProperty(unique_index=True)
    location = PointProperty(crs='wgs-84')