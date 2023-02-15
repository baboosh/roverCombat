import csv
import random

class Weapon:
    def __init__(self, Name, Level, DamageType, MinDam, MaxDam, Crit, CritDamMod, Range, Mass):
        self.Name = Name
        self.Level = Level
        self.DamageType = DamageType
        self.MinDam = MinDam
        self.MaxDam = MaxDam
        self.Crit = Crit
        self.CritDamMod = CritDamMod
        self.Range = Range
        self.Mass = Mass

    def __str__(self):
        return f"Name: {self.Name}\nLevel: {self.Level}\nDamage Type: {self.DamageType}\nDamage Range: {self.MinDam}-{self.MaxDam}\nCrit Chance: {self.Crit}\nCrit Damage Modifier: {self.CritDamMod}\nRange: {self.Range}\nMass: {self.Mass}"

class Weapons:
    def __init__(self):
        self.weapons = []

        with open('roverCombat/Rover Combat/Data/weapon data/kinetic.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                weapon = Weapon(**row)
                self.weapons.append(weapon)
                self.kinetic_weapons.append(weapon)

    def generate_weapon(self, level, DamageType):
        level_weapons = [w for w in self.weapons if int(w.Level) == level]
        if len(level_weapons) == 0:
            return None
        else:
            if 
            return random.choice(level_weapons)


if __name__ == "__main__":
    newWeapons = Weapons()
    while True:
        print("\n" * 50)
        level = input("Generate weapon of level: ")
        random_leveled_weapon = newWeapons.generate_weapon(int(level))
        if random_leveled_weapon is not None:
            print(random_leveled_weapon)
        else:
            print("No weapons found for level " + level + ".")
        a = input()