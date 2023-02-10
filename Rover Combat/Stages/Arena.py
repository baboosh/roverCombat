import Objects.Rover as Rover
import Objects.Weapon as Weapon
import Objects.Armor as Armor
import random
import Mechanics.Combat as Combat
import Workshop as Workshop


class Arena:

    def __init__(self, rover):
        self.playerRover = rover
        self.enemyRover = None
        self.enemy_firstnames = ["Starlight", "MH-1", "ChatGPT", "Starbase", "Deimos", "Phobos"]
        self.enemy_lastnames = ["The Brave", "The Runt", "The Coward", "The Fighter", "The Lost"]
        self.winnings_xp = 0
        self.winnings_credits = 0
        self.winnings_items = []

    def failedInput(self):
        print("Unrecognised Command! Please Try Again!")

    def clear_screen(self):
        count = 1
        while count < 100:
            count += 1
            print("\n")

    def view_rover(self, rover):
        print(rover)
        print("[T] TOGGLE SLOTS VIEW")
        print("[#] MODIFY SLOT")
        print("[A] ARENA MENU ")

        inputChosen = False
        while not inputChosen:
            playerInput = input(">")
            if playerInput.upper() == "T":
                rover.displayingArmor = not rover.displayingArmor
                self.clear_screen()
                self.view_rover(rover)
                inputChosen = True
            elif playerInput.upper() == "A":
                self.clear_screen()
                self.main()
                inputChosen = True
            elif playerInput == "1" or playerInput == "2" or playerInput == "3" or playerInput == "4":
                self.clear_screen()
                self.view_slot(playerInput, rover)
            else:
                self.failedInput()

    def view_slot(self, slotid, rover):
        slotDirectory = {"1": "Front",
                        "2": "Left",
                        "3": "Right",
                        "4": "Rear"}
        

        if rover.displayingArmor:
            viewingSlots = rover.armor_slots
        else:
            viewingSlots = rover.weapon_slots
        self.viewing_slot(slotid, viewingSlots, slotDirectory,rover)

        return

    def viewing_slot(self, slotid, viewingSlots, slotDirectory, rover):
        self.clear_screen()
        print(viewingSlots[slotDirectory[slotid]])
        print("[V] Back to View")
        playerInput = input()
        self.clear_screen()
        self.view_rover(rover)

    def generate_enemy(self):
        enemyRover = Rover.Rover(random.choice(self.enemy_firstnames) + " " + random.choice(self.enemy_lastnames))
        enemyRover.health = 15
        enemyRover.max_health = 15
        slot_list = ["Front", "Left", "Right", "Rear"]
        index = 0
        for slot in enemyRover.armor_slots:
            newArmor = Armor.Armor()
            newArmor.generateArmor("Light",slot_list[index],type_count=2)
            enemyRover.armor_slots[slot] = newArmor
            index += 1
        
        index = 0
        for weapon in enemyRover.weapon_slots:
            newWeapon = Weapon.Weapon()
            newWeapon.generateWeapon(2,random.randint(2,5), 5, slot_list[index])
            enemyRover.weapon_slots[weapon] = newWeapon
            index += 1
        self.enemyRover = enemyRover
        self.main()

    def fight(self):
        newArena = Combat.Combat(self.enemyRover, self.playerRover)
        winnings = newArena.startup()
        self.enemyRover = None

        self.winnings_credits = winnings[0]
        self.winnings_xp = winnings[1]
        self.wininngs_items = winnings[2]

    def main(self):
        if not self.playerRover:
            name = "NONE SELECTED!"
        else:
            name = self.playerRover.name

        spaces = ((21 - int(len(name))) * " ")

        if not self.enemyRover:
            name2 = "NONE CHOSEN!"
        else:
            name2 = self.enemyRover.name

        spaces2 = ((21 - int(len(name2))) * " ")


        displayString = ("""
 _______________________       
/                        \.
| WELCOME TO THE         |
| TIGER ROVERWORKS'      |
| ARENA   !              |
|                        |
| -* CURRENT ROVER:      |
|   {}{}| 
|                        | 
|                        | 
| -* CURRENT ENEMY:      |
|   {}{}| 
|                        | 
| [E] VIEW ENEMY         | 
| [V] VIEW ROVER         | 
| [G] GENERATE ENEMY     | 
| [F] !FIGHT!            |
| [R] RETURN TO WORKSHOP |
\________________________/
        """).format(name, spaces, name2, spaces2)
        print(displayString)
        inputChosen = False
        while not inputChosen:
            playerInput = input(">")
            if playerInput.upper() == "E":
                inputChosen = True
                self.clear_screen()
                if self.enemyRover is None:
                    inputChosen = True
                    self.clear_screen()
                    self.main()
                self.view_rover(self.enemyRover)
            elif playerInput.upper() == "V":
                self.clear_screen()
                self.view_rover(self.playerRover)
                inputChosen = True
            elif playerInput.upper() == "G":
                self.clear_screen()
                self.generate_enemy()
                inputChosen = True
            elif playerInput.upper() == "F":
                if self.enemyRover is None:
                    print("No Enemies to Fight!")
                else:
                    self.clear_screen()
                    self.fight()
                    inputChosen = True
            elif playerInput.upper() == "R":
                inputChosen = True
            else:
                self.failedInput()