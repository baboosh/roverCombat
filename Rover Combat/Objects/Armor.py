import random
import Mechanics.Damage as Damage
import Data.CombatData as CombatData
from math import floor

class Armor:

    def __init__(self):
        self.armorData = CombatData.ArmorData()
        self.damageData = CombatData.DamageData()
        self.name = "Armor Plate"
        self.armor = True
        self.slot = ""

        self.slots = ["Front", "Side", "Rear"]

        self.armor_types = self.armorData.armor_prefixes

        self.strongResistances = self.armorData.resistances
        self.weakResistances = self.armorData.weaknesses

        self.resistances = []
        self.weaknesses = []
        self.dots = []

        self.weaknessModifier = 1.5
        self.resistanceModifier = 0.5

        self.type = []
        self.health = 0
        self.max_health = 0
        self.health_percent = 0

    def calculate_modifier_chance(self, application_chance_modifier, damage_data, damage_type):
        try:
            modifier_chance = random.randint(1, 100) * application_chance_modifier
            return modifier_chance <= damage_data[damage_type]
        except KeyError:
            return False

    def generateArmor(self, strength="Medium",slot="Random",type_count=3):
        self.max_health = 10

        if strength == "Light":
            self.max_health += 5
        elif strength == "Medium":
            self.max_health += 10
        elif strength == "Heavy":
            self.max_health += 15

        self.health = self.max_health

        for _ in range(0, type_count):
            newArmorType = random.choice(self.armor_types)
            identical = self.strongResistances[newArmorType] in self.resistances or self.weakResistances[newArmorType] in self.weaknesses
            conflicting = self.strongResistances[newArmorType] in self.weaknesses or self.weakResistances[newArmorType] in self.resistances

            tries = 0
            while (identical or conflicting) and tries < 100:
                tries += 1
                newArmorType = random.choice(self.armor_types)

            if tries <= 99:
                self.resistances.append(self.strongResistances[newArmorType])
                self.weaknesses.append(self.weakResistances[newArmorType])
                self.type.append(newArmorType)

        
        typeString = ""
        for type in self.type:
            typeString += " " + type
        self.name = typeString + " " + self.name

        if slot == "Random":
            self.slot = random.choice(self.slots)
        else:
            self.slot = slot
        
        self.health_percent = (self.health / self.max_health * 100)

    def calculate_resisted_damage(self, dmg, resistance_modifier):
        return floor(dmg - dmg * resistance_modifier)

    def calculate_critical_damage(self, dmg, weakness_modifier):
        return floor(dmg * weakness_modifier - dmg)

    def round_to_tenths(self, value):
        return floor(value * 10) / 10
        
    def takeDamage(self, damage):
        incomingDamage = damage.damage
        resistedDamage = 0
        criticalDamage = 0


        damageList = []
        modifiers = {}

        for _ in range(0, len(damage.damage_type)):
            damageList.append(incomingDamage / len(damage.damage_type))

        count = 0
        newDamageList = []
        application_chance_modifier = 1
        for count, dmg in enumerate(damageList):
            damage_type = damage.damage_type[count]

            if damage_type in self.resistances:
                resistedDamage = self.calculate_resisted_damage(dmg, self.resistanceModifier)
                dmg = self.round_to_tenths(dmg * self.resistanceModifier)
                application_chance_modifier -= 1
                
            elif damage_type in self.weaknesses:
                criticalDamage = self.calculate_critical_damage(dmg, self.weaknessModifier)
                dmg = self.round_to_tenths(dmg * self.weaknessModifier)
                application_chance_modifier += 0.5     

            newDamageList.append(self.round_to_tenths(dmg))
            count += 1

        for damage_type in damage.damage_type:
            if self.calculate_modifier_chance(application_chance_modifier, self.damageData.fightingStuns, damage_type):
                try:
                    modifiers[damage_type] += 1
                except KeyError:
                    modifiers[damage_type] = 1
            elif self.calculate_modifier_chance(application_chance_modifier, self.damageData.movingStuns, damage_type):
                try:
                    modifiers[damage_type] += 1
                except KeyError:
                    modifiers[damage_type] = 1

        if damage.dot:
            dot_chance = (random.randint(1, 100) * application_chance_modifier)
            if dot_chance <= damage.dot.application_chance:
                print("STATUS EFFECT APPLIED!")
                print(damage.dot)
                self.dots.append(damage.dot)
                if damage.dot.tick_damage_type[0] in self.damageData.specialDots:
                    try:
                        modifiers[damage.dot.tick_damage_type[0]] += damage.dot.duration
                    except KeyError:
                        modifiers[damage.dot.tick_damage_type[0]] = damage.dot.duration

        incomingDamage = 0
        for dmg in newDamageList:
            incomingDamage += dmg


        self.health -= incomingDamage
        if self.health <= 0:
            extraDamage = -self.health
            print("ARMOR PIECE BROKEN! ({} OVERKILL!)".format(int(extraDamage)))
            self.health = 0
        else:
            extraDamage = 0

        self.health_percent = (self.health / self.max_health * 100)

        print("--- DAMAGE RESULT -----------")
        print("{} TOOK {}{} DAMAGE. ({} RESISTED, {} CRITICAL)".format(self.name.upper(), int(incomingDamage), damage.printed_type.upper(), int(resistedDamage), int(criticalDamage)))
        print(" INTEGRITY AT {}".format(int(self.health_percent)) +"% !")
        print("-----------------------------")

        return [extraDamage, modifiers]

    

    def getCondition(self):
        
        if self.health_percent == 100:
            return "Healthy"
        elif self.health_percent >= 80:
            return "Minor Damage"
        elif self.health_percent >= 60:
            return "Medium Damage"
        elif self.health_percent >= 40:
            return "* Compromised *"
        elif self.health_percent >= 20:
            return "! CRITICAL !"
        elif self.health_percent >= 1:
            return "!! EXTREME DAMAGE !!"
        else:
            return "!!! BROKEN !!!"

    def __str__(self):
        resistancesString = "| "
        weaknessesString = "| "
        status = "ALL CLEAR"
        

        for resistance in self.resistances:
            resistancesString += resistance + " | "

        
        for weakness in self.weaknesses:
            weaknessesString += weakness + " | "

        if len(self.dots) > 0:
            status = "| "
            
            
            for dot in self.dots:
                plurality = ""
                if dot.duration > 1:
                    plurality = "s"
                status += dot.tick_damage_type[0] + " (" + str(dot.duration) + " turn{}) | ".format(plurality)
        
        
        hyphens = "-" * (80 - len(self.name))   
        armorDisplay = """
-- {} {}
Slot: {}
Condition: {}
Health: {}% ({}/{} HP)
Resistant To: {}
Weak To: {}

STATUS: {}
----{} 
        """.format(self.name, hyphens, self.slot, self.getCondition(), int(self.health / self.max_health * 100), floor(self.health*10)/10, self.max_health, 
        resistancesString, weaknessesString, status, "-" * 80)
        return armorDisplay



if __name__ == "__main__":
    damageTypes = ["Toxic", "Crushing", "Burning"]
    damage1 = Damage.Damage(5, damageTypes)

    damageTypes = ["Blunt"]
    damage2 = Damage.Damage(6, damageTypes)

    armorSlot = Armor()
    armorSlot.generateArmor()
    print(armorSlot)
    armorSlot.takeDamage(damage1)
    print(armorSlot)
    armorSlot.takeDamage(damage2)
    print(armorSlot)