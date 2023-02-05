#        self.types = ["Toxic", "Cryogenic", "Burning", "Crushing", "Blunt", "Sharp", "Electronic", "Radiation"]
import random

class DOT:

    def __init__(self, application_chance, duration, tick_damage, tick_damage_type):
        self.application_chance = application_chance
        self.duration = duration
        self.tick_damage = tick_damage
        self.tick_damage_type = tick_damage_type
        
    def doTick(self):
        if self.duration == 0:
            return 0
        self.duration -= 1
        newDamage = Damage(self.tick_damage, self.tick_damage_type, dot=False)
        return newDamage
    
    def __str__(self):
        # -- BURNING! -- 
        # Damage per Tick: Y
        # Duration: X
        dotDisplay = """--{}!--
Damage Per Tick: {}        
Duration: {}
--------
        """.format(self.tick_damage_type[0].upper(), self.tick_damage, self.duration)
        return dotDisplay

class Damage:

    def __init__(self, damage, types, dot=True):
        self.damage = damage
        self.damage_type = types
        typeString = ""
        for damage_type in self.damage_type:
            typeString = typeString + " " + damage_type
        self.printed_type = typeString

        self.dots = {"Toxic":2, "Burning":3, "Radiation":1, "Crushing":1}
        self.dot = dot
        
        if self.dot:
            self.generate_dot_information()


    def generate_dot_information(self):
        application_chance = 0
        tick_damage = 0
        duration = 0
        tick_damage_type = []

        dot_types = []
        for damage_type in self.damage_type:
            if damage_type in self.dots:
                dot_types.append(damage_type)

        if len(dot_types) > 0:
            application_chance = len(dot_types*25)

            tick_damage_type.append(random.choice(dot_types))
            duration = 5 - self.dots[tick_damage_type[0]]

            if tick_damage_type == "Crushing":
                duration -= 3
            
            tick_damage = self.dots[tick_damage_type[0]]
            
            newDot = DOT(application_chance, duration, tick_damage, tick_damage_type)
            self.dot = newDot
        else:
            self.dot = False
        
    def __str__(self):
        
        damageDisplay = """
-- Incoming Damage! --
Damage: {}
Damage Type: {}
DOT:
{}
        """.format(self.damage, self.printed_type, str(self.dot))


# -- Incoming Damage! -- 
# Damage: 4
# Damage Type: Toxic Crushing
# DOT:
        # 4 Toxic Crushing Damage
        return damageDisplay
        

if __name__ == "__main__":
    damageTypes = ["Burning", "Freezing", "Crushing"]
    currentDamage = Damage(10, damageTypes)
    print(currentDamage)