from ..entities import CriminalEntity
from neomodel import db
import random
from users.models import Station
class ArrestSeeder:

    def create_arrest(self,station,criminal:CriminalEntity):
        query = """
            MATCH (s:Station),(c:Criminal)
            WHERE s.entity_id = $stationID AND c.id_num = $criminalID
            MERGE (s)-[a:ARRESTED]->(c)
            RETURN a
        """
        params = {
            "stationID": station.id,
            "criminalID": criminal.id_num
        }
        results, meta = db.cypher_query(query, params)
        return results
    
    #seeder to connect a random criminal to a random station in the graph db
    def run(self):
        stations = Station.objects.all()
        criminals = CriminalEntity.nodes.all()
        for criminal in criminals:
            random_station = random.choice(stations)
            self.create_arrest(station=random_station,criminal=criminal)


            print(f"Arrested {criminal.name} at {random_station.name}")