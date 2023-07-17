from ..models import Crime


class CrimeSeeder:
    def create_crimes(self, crime_data):
        crimes = [
            Crime(name=data["name"], description=data["description"])
            for data in crime_data
        ]
        Crime.objects.bulk_create(crimes,ignore_conflicts=True)
        return crimes

    def run(self):
        # Sample crime data
        sample_data = [
            {
                "name": "Robbery",
                "description": "The act of taking someone's property by force or threat of force.",
            },
            {
                "name": "Burglary",
                "description": "Unlawful entry into a building with the intent to commit a crime.",
            },
            {
                "name": "Assault",
                "description": "Intentionally causing physical harm or threat of physical harm to another person.",
            },
            {
                "name": "Fraud",
                "description": "Deception or misrepresentation for personal gain or to cause harm to others.",
            },
            {
                "name": "Drug trafficking",
                "description": "Illegally trading or distributing controlled substances.",
            },
            {
                "name": "Arson",
                "description": "The act of intentionally setting fire to property.",
            },
            {"name": "Homicide", "description": "The act of killing another person."},
            {
                "name": "Identity theft",
                "description": "Fraudulently using another person's personal information.",
            },
            {
                "name": "Kidnapping",
                "description": "The unlawful abduction and holding of a person against their will.",
            },
            {
                "name": "Embezzlement",
                "description": "Misappropriation or theft of funds entrusted to one's care.",
            },
            {
                "name": "Forgery",
                "description": "Creating or altering a document with the intent to deceive or defraud.",
            },
            {
                "name": "Cybercrime",
                "description": "Criminal activities carried out using computers or the internet.",
            },
            {
                "name": "Extortion",
                "description": "Coercing or obtaining something through threats or intimidation.",
            },
            {
                "name": "Money laundering",
                "description": "Concealing the origins of illegally obtained money.",
            },
            {
                "name": "Sexual assault",
                "description": "Non-consensual sexual contact or behavior.",
            },
            {
                "name": "Counterfeiting",
                "description": "Creating fake currency, documents, or goods.",
            },
            {
                "name": "Vandalism",
                "description": "Deliberate destruction or damage to property.",
            },
            {
                "name": "Carjacking",
                "description": "Stealing a motor vehicle by force or threat of force.",
            },
            {
                "name": "Racketeering",
                "description": "Engaging in organized criminal activities, often involving extortion, fraud, and intimidation.",
            },
            {
                "name": "Environmental crime",
                "description": "Violations of laws and regulations related to the protection of the environment.",
            },
            {
                "name": "Illegal immigration",
                "description": "Entering or residing in a country without proper authorization from the government.",
            },
            {
                "name": "Public indecency",
                "description": "Engaging in offensive or lewd behavior in public places.",
            },
            {
                "name": "Human trafficking",
                "description": "Illegal trade and exploitation of human beings for forced labor, sexual exploitation, or other purposes.",
            },
            {
                "name": "Assault with a deadly weapon",
                "description": "Causing harm or injury to another person using a weapon that can cause serious bodily harm or death.",
            },
            {
                "name": "Rape",
                "description": "Non-consensual sexual penetration or intercourse.",
            },
            {
                "name": "Gang violence",
                "description": "Criminal activities carried out by organized groups or gangs, often involving violence and illegal activities.",
            },
            {
                "name": "Hijacking",
                "description": "Seizing control of a vehicle, aircraft, or vessel by force or threat of force.",
            },
        ]

        # Create crimes in bulk
        created_crimes = self.create_crimes(sample_data)

        # Print created crime objects
        for crime in created_crimes:
            print(f"Created crime: {crime.name} - {crime.description}")
