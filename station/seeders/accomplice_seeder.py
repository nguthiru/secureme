from neomodel import db
from ..entities import CriminalEntity
import random
class AccompliceSeeder:

    def connect_accomplice(self,criminal1,criminal2):
        query = """
            MATCH (c1:Criminal),(c2:Criminal)
            WHERE c1.id_num = $criminalID AND c2.id_num = $accompliceID
            MERGE (c1)-[ac:ACCOMPLICE]->(c2)
            RETURN ac,c2,c1

        """
        params = {
            "criminalID": int(criminal1.id_num),
            "accompliceID": int(criminal2.id_num)
        }
        results, meta = db.cypher_query(query, params)

        return results

    def run(self):

        nodes = CriminalEntity.nodes.all()

        for _ in range(1500):
            criminal1 = random.choice(nodes)
            criminal2 = random.choice(nodes)
            while criminal1.id_num == criminal2.id_num:
                criminal2 = random.choice(nodes)
            
            print(f"Connecting {criminal1.name} to {criminal2.name}")
            self.connect_accomplice(criminal1,criminal2)


