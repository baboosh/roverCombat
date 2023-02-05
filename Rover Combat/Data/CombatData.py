class DamageData:

    def __init__(self):
    
        self.types = ["Poisonous", "Frozen", "Burning", "Crushing", "Blunt", "Sharp", "Electrocuted", "Radiation"]

                # STATUS NAME: APPLICATION CHANCE
        self.movingStuns = {"Frozen": 30, "Crushing": 50}
        self.fightingStuns = {"Electrocuted": 20}

        self.specialDots = {"Crushing": "MovingStun"}

       

class ArmorData:

    def __init__(self):
        self.resistances = {"Heated": "Frozen",
                            "Lead-Lined": "Radiation",
                            "Grounded": "Electrocuted",
                            "Cushioning": "Blunt",
                            "Hardened": "Sharp",
                            "Fire-Suppressing": "Burning",
                            "Coated": "Poisoned",
                            "Structural": "Crushing"}

        self.weaknesses = {"Heated": "Crushing",
                            "Lead-Lined": "Sharp",
                            "Grounded": "Poisoned",
                            "Cushioning": "Burning",
                            "Hardened": "Crushing",
                            "Fire-Suppressing": "Electrocuted",
                            "Coated": "Radiation",
                            "Structural": "Blunt"}



        self.armor_prefixes = ["Cushioning", "Hardened", "Grounded", "Lead-Lined", "Heated", "Fire-Suppressing", "Coated", "Structural"]

        
