from django.db import models
from django.contrib.gis.db.models import PointField,PolygonField
from django.db.models.signals import post_save
from django.dispatch import receiver
from neomodel import db
# # Create your models here.
# class Station(models.Model):
#     name = models.CharField(max_length=255)
#     jurisdicton = PolygonField()
    
class Crime(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    def __str__(self) -> str:
        return self.name
    
@receiver(post_save, sender=Crime)
def add_crime_to_graph(sender,instance,created,*args,**kwargs):

    if created:
        query = """
            CREATE (c:Crime {name: $name, description: $description,entity_id: $entity_id})
            RETURN c
        """
        params = {
            "name": instance.name,
            "description": instance.description,
            "entity_id": instance.id,
        }
        db.cypher_query(query, params)
    else:
        query = """
            MATCH (c:Crime {entity_id: $entity_id})
            SET c.description = $description
            RETURN c
        """
        params = {
            "entity_id": instance.id}