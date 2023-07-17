from faker import Faker
import random
from neomodel import db 
from ..entities import CriminalEntity
class CriminalSeeder:


    def faker_data(self,num_samples=50):
        fake = Faker()
        criminals = []
        for _ in range(num_samples):
            name = fake.name()
            date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=70)
            height = random.randint(150, 200)
            id_number = random.randint(100000, 999999)
            image_url = "https://thispersondoesnotexist.com"
            criminals.append({'name': name, 'date_of_birth': date_of_birth, 'height': height, 'id_num': id_number,'image_url': image_url})
        return criminals
    
    def create_criminals(self, data):
        CriminalEntity.create_or_update(*data)


    def run(self):
        criminals = self.faker_data(3000)
        self.create_criminals(criminals)
        return criminals
    
