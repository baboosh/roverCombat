import random
import Mechanics.Damage as Damage
from math import floor

class Weapon:

    def __init__(self):
        self.names = ["Launcher", "Cannon", "Arm", "Grabber"]

        self.name = ""
        self.armor = False
        self.slot = ""
        self.range = ""

        self.slots = ["Front", "Side", "Rear"]
        self.ranges = ["Front", "Radial"]

        self.dots = []

        self.cooldown = 0
        self.max_cooldown = 0

        self.damage = 0
        self.health = 0
        self.max_health = 0 
        self.health_percent = 0
        self.weapon_type = ""
        self.damage_type = []

        self.damage_parallels = {"Nitrogen Bolt": "Frozen",
                                "Plutonoim Core": "Radiation",
                                "Arcing": "Electrocuted",
                                "Ball Bearing": "Blunt",
                                "Saw-blade": "Sharp",
                                "Napalm": "Burning",
                                "Poison": "Poisoned",
                                "Serrated Clamp": "Crushing"}

        self.support_parallels = {"Extinguisher": "Cleansing",
                                "Nanite": "Repairing",
                                "Deployable Shield": "Guarding"}

    def generateWeapon(self, type_count=1, damage=11, max_health = 5, slot="Random"):
        self.name = random.choice(self.names)
        if slot == "Random":
            self.slot = random.choice(self.slots)
        else:
            self.slot = slot
        
        self.range = random.choice(self.ranges)
        if self.slot != "Front":
            self.range = "Radial"


        weapon_type_roll = random.randint(1, 100)
        if weapon_type_roll >= 80:
            self.weapon_type = "Defensive"
        else:
            self.weapon_type = "Offensive"

        self.damage = damage
        self.health = max_health
        self.max_health = max_health
        self.max_cooldown = random.randint(2, 4)
        self.damage += self.max_cooldown * (self.damage * 0.1)
        self.health_percent = (self.health / self.max_health * 100)

        if self.weapon_type == "Offensive":
            if self.range == "Front":
                self.damage += self.damage * 0.4
            else:
                self.damage -= self.damage * 0.2
            selectedWeaponType = self.damage_parallels
        else:
            if self.range == "Front":
                self.damage += 2
            selectedWeaponType = self.support_parallels
            self.damage = floor(self.damage - self.damage * 0.8)
            if self.damage == 0:
                self.damage = 1
    
        for _ in range(0, type_count):
            newWeaponType = random.choice(list(selectedWeaponType.keys()))
            
            identical = selectedWeaponType[newWeaponType] in self.damage_type
            tries = 0
            while identical and tries <= 100:
                tries += 1
                newWeaponType = random.choice(list(selectedWeaponType.keys()))
            if tries < 101:
                self.damage_type.append(selectedWeaponType[newWeaponType])
                self.name = newWeaponType + " " + self.name

    def generateDamage(self):
        generatedDamage = Damage.Damage(self.damage, self.damage_type)
        return generatedDamage
       
    def takeDamage(self, damage):
        incomingDamage = damage.damage * 2
        modifiers = {}

        

        if damage.dot:
            dot_chance = (random.randint(1, 100))
            if dot_chance <= damage.dot.application_chance:
                print("STATUS EFFECT APPLIED!")
                print(damage.dot)
                self.dots.append(damage.dot)
                if damage.dot.tick_damage_type == "Crushing":
                    modifiers["Crushing"] = damage.dot.duration

        if "Electrocuted" in damage.damage_type or "Frozen" in damage.damage_type:

            if "Electrocuted" in damage.damage_type:
                modifier_chance = random.randint(1, 100)
                if modifier_chance <= 30:
                    modifiers["Electrocuted"] = 1

            if "Frozen" in damage.damage_type:
                modifier_chance = random.randint(1, 100)
                if modifier_chance <= 30:
                    modifiers["Electrocuted"] = 1
        print("--- DAMAGE RESULT -----------")
        print("{} TOOK {}{} DAMAGE! (!WEAPON HIT X2!)".format(self.name.upper(), int(incomingDamage), damage.printed_type))
        print(" INTEGRITY AT {}".format(int(self.health_percent)) +"% !")
        print("-----------------------------")


        self.health -= incomingDamage
        if self.health <= 0:
            extraDamage = -self.health
            self.dots = []
            print("Weapon piece broken! ({} Overkill!)".format(int(extraDamage)))
            self.health = 0
        else:
            extraDamage = 0

        self.health_percent = (self.health / self.max_health * 100)

        return [extraDamage, modifiers]
       

    def getCondition(self):
        if self.health_percent == 100:
            return "Nominal"
        elif self.health_percent >= 80 and self.health_percent < 100:
            return "Minor Damage"
        elif self.health_percent >= 60 and self.health_percent < 80:
            return "Medium Damage"
        elif self.health_percent >= 40 and self.health_percent < 60:
            return "* Compromised *"
        elif self.health_percent >= 20 and self.health_percent < 40:
            return "! CRITICAL !"
        elif self.health_percent >= 1 and self.health_percent < 20:
            return "!! EXTREME DAMAGE !!"
        else:
            return "!!! BROKEN !!!"

    def __str__(self):
        hyphens = "-" * (80 - len(self.name))   
        typeString = ""
        for damage_type in self.damage_type:
            typeString = typeString + " " + damage_type
        weaponDisplay = """
-- {} {}
Slot: {}
Effective Range: {}
Condition: {}
Health: {}% ({}/{} HP)
Cooldown: {} Turns

Gear Type:{}
Gear Value: {}

----{} 
        
        """.format(self.name, hyphens, self.slot, self.range, self.getCondition(), int(self.health_percent),
         floor(self.health*10)/10, self.max_health, self.max_cooldown, typeString, self.damage, "-" * 80)
        return weaponDisplay



if __name__ == "__main__":
    newWeapon = Weapon()
    newWeapon.generateWeapon()
    print(newWeapon)