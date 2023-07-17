from neomodel import db
from ..entities import CriminalEntity,CrimeEntity
from faker import Faker
import random
class CommittedSeeder:
    def connect_crime(self,criminal_id:int,crime_id:int,datetime:str,casualities:int):
        query = """
        MATCH (c:Criminal),(cr:Crime) 
        WHERE c.id_num = $criminalID AND cr.entity_id = $crimeID
        MERGE (c)-[com:COMMITTED]->(cr)
        ON CREATE SET com.datetime = datetime($datetime), com.casualities = $casualities
        RETURN com
        """
        params = {
            "criminalID": int(criminal_id),
            "crimeID": int(crime_id),
            "datetime": datetime,
            "casualities": int(casualities)
        }
        results, meta = db.cypher_query(query, params)

    
    def run(self):
        
        criminals = CriminalEntity.nodes.all()
        crimes = CrimeEntity.nodes.all()

        for criminal in criminals:
            date_time = Faker().date_time().isoformat()
            crime = random.choice(crimes)
            casualities = random.randint(0,10)
            self.connect_crime(criminal.id_num,crime.entity_id,date_time,casualities)
            print(f"Connecting {criminal.name} to {crime.name}")

