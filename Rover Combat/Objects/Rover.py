from math import floor
import Data.CombatData as CombatData

class Rover:


    def __init__(self, name):
        self.name = name
        self.health = 30
        self.max_health = 30
        self.health_percent = (self.health / self.max_health * 100)
        self.displayingArmor = True
        self.damageData = CombatData.DamageData()
        self.modifiers = {}

        # Orientations: Forward, Left-Exposed, Right-Exposed, Rear-Exposed.
        self.orientation = ""
        
        self.armor_slots = {"Front": None, "Left":None,
         "Right":None, "Rear":None,}

        self.weapon_slots = {"Front": None, "Left":None,
         "Right":None, "Rear":None,}

    def getModifiers(self):
        # ELECTRIC (4 TURNS) CRYOGENIC (1 TURN)
        modifierDisplay = ""

        for modifier in self.modifiers.keys():
            plurality = ""
            if self.modifiers[modifier] > 1:
                plurality = "S"
            modifierDisplay += " " + modifier.upper() + " (" + str(self.modifiers[modifier]) + " TURN{})".format(plurality)

        if modifierDisplay == "":
            return "NO MODIFIERS"

        return modifierDisplay
            
            
    def takeDamage(self, damage):
        incomingDamage = damage.damage * 2
        self.health -= incomingDamage
        print("ROVER CORE HIT, 2X ALL DAMAGE.")
        print("--- FINAL DAMAGE RESULT ----")
        print("TOOK {}{} DAMAGE. (2X ALL DAMAGE))".format(incomingDamage, damage.printed_type.upper()))
        print("INTEGRITY AT {}".format(self.health_percent) +"% !")
        print("-----------------------------")
        return [0, {}]

    def getCondition(self):

        if self.health_percent == 100:
            return "Optimal"
        elif self.health_percent >= 80 and self.health_percent < 100:
            return "Functional"
        elif self.health_percent >= 60 and self.health_percent < 80:
            return "Malfunctioning"
        elif self.health_percent >= 40 and self.health_percent < 60:
            return "Crippled"
        elif self.health_percent >= 20 and self.health_percent < 40:
            return "! CRITICAL !"
        else:
            return "!! EXTREME DAMAGE !!"

    def getArmorStatus(self):
        total_health = "Missing Slots!"
        hp_percent = 0
        if None not in self.armor_slots.values():
            for armor in self.armor_slots:
                hp_percent += self.armor_slots[armor].health_percent
            total_health = str(floor((hp_percent / 4)*10)/10)
        return total_health

    def getWeaponStatus(self):
        hp_percent = 0
        total_health = "Missing Slots!"
        if None not in self.weapon_slots.values():
            for armor in self.weapon_slots:
                hp_percent += self.weapon_slots[armor].health_percent
            total_health = str(floor((hp_percent / 4)*10)/10)
        return total_health

    def can_move(self):
        for damage_type in self.damageData.movingStuns:
            if self.modifiers.get(damage_type) is not None:
                return False
        return True

    def can_fight(self):
        for damage_type in self.damageData.fightingStuns:
            if self.modifiers.get(damage_type) is not None:
                return False
        return True
    
    def __str__(self):
    
        hyphens = "-" * (40 - len(self.name))
        hyphens2 = "-" * 45 


        if self.displayingArmor:
            currentDisplay = "ARMOR"
            slot1 = self.armor_slots["Front"]
            
            slot2 = self.armor_slots["Left"]
            slot3 = self.armor_slots["Right"]
            slot4 = self.armor_slots["Rear"]
        else:
            currentDisplay = "WEAPONS"
            slot1 = self.weapon_slots["Front"]
            slot2 = self.weapon_slots["Left"]
            slot3 = self.weapon_slots["Right"]
            slot4 = self.weapon_slots["Rear"]
        

        if slot1 is not None:
            slot1hp = int(slot1.health / slot1.max_health * 100)
            slot1 = slot1.name
        if slot2 is not None:
            slot2hp = int(slot2.health / slot2.max_health * 100)
            slot2 = slot2.name
        if slot3 is not None:
            slot3hp = int(slot3.health / slot3.max_health * 100)
            slot3 = slot3.name
        if slot4 is not None:
            slot4hp = int(slot4.health / slot4.max_health * 100)
            slot4 = slot4.name
        
       
        roverDisplay = """
-- {} {}
Condition: {}
Health: {}% ({}/{} HP)
Armor Status: {}%
Weapon Status: {}%

{}
SLOT VIEW:
[T] TOGGLE BETWEEN ARMOR/WEAPON

[   {}    ]    
- FRONT          
  - [1] [{}%] {}         

- LEFT SIDE      
  - [2] [{}%] {}          

- RIGHT SIDE 
  - [3] [{}%] {}         

- REAR     
  - [4] [{}%] {}      

{}

        """.format(self.name, hyphens, self.getCondition(), int(self.health_percent), int(self.health),
         int(self.max_health), self.getArmorStatus(), self.getWeaponStatus(), hyphens2, currentDisplay, int(slot1hp),
          slot1, int(slot2hp), slot2, int(slot3hp), slot3, int(slot4hp), slot4, hyphens2)
        return roverDisplay