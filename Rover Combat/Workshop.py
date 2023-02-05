import Objects.Rover as Rover
import Objects.Armor as Armor
import Stages.Arena as Arena
import Objects.Weapon as Weapon
import random


class Workshop:

    def __init__(self):
        self.xp = 0
        self.level = 1
        self.credits = 100
        self.rovers = []
        self.rover_cost = 100
        self.repair_cost = 10
        self.selected_rover = None
        self.arenaObj = Arena.Arena(self.selected_rover)

        self.playerData = {"credits":100,
                            "xp": 0,
                            "level": 1,
                            "selected rover": None,
                            "rovers": []}


    def failedInput(self):
        print("Unrecognised Command! Please Try Again!")

    def getCreditDisplay(self):
        return str(self.credits) + "¢"

    def doLevelUp(self):
        xpToNextLevel = (self.level / 0.07) * 2
        if self.xp >= xpToNextLevel:
            self.xp -= xpToNextLevel
            self.level += 1
            self.doLevelUp()
            print("! -- LEVEL UP -- !")        

    def getXPDisplay(self):
        xpProgress = "["
        remainingFill = "----------"
        xpToNextLevel = (self.level / 0.07) * 2
        xpPercent = (self.xp / xpToNextLevel) * 100
        while xpPercent >= 10:
            xpPercent -= 10
            xpProgress += "*"
            remainingFill = remainingFill[:-1]
        xpProgress += remainingFill
        xpProgress += "]"
        return "LVL " + str(self.level) + xpProgress

    def clear_screen(self):
        count = 1
        while count < 100:
            count += 1
            print("\n")

    def create_new_rover(self):
        roverDisplay = """
  ___________________________________________
 /                                           \ 
 |  Are you sure you want to create a Rover?  |
 |   COST: {}¢                               |
 |   [Y] Yes    [N] No                        |
 \___________________________________________/
        
        """.format(self.rover_cost)
        print(roverDisplay)
        playerInput = input()
        if playerInput.upper() == "Y":
            if self.credits < self.rover_cost:
                print("ERROR: NOT ENOUGH CREDITS!")
                a = input()
                self.clear_screen()
                self.garage()
            self.credits -= self.rover_cost
            print("... Creating New Rover! ...")
            roverName = input("Name: ")

            newRover = Rover.Rover(roverName)
            newRover.health = 30
            newRover.max_health = 30
            slot_list = ["Front", "Left", "Right", "Rear"]
            index = 0
            for slot in newRover.armor_slots:
                newArmor = Armor.Armor()
                newArmor.generateArmor("Medium",slot_list[index],type_count=1)
                newRover.armor_slots[slot] = newArmor
                index += 1
            
            index = 0
            for weapon in newRover.weapon_slots:
                newWeapon = Weapon.Weapon()
                newWeapon.generateWeapon(1,random.randint(3,8), 10, slot_list[index])
                newRover.weapon_slots[weapon] = newWeapon
                index += 1
        
            self.selected_rover = newRover
            self.arenaObj.playerRover = self.selected_rover
            self.rovers.append(self.selected_rover)
            self.clear_screen()
            self.garage()
        else:
            self.garage()

    def viewing_slot(self, slotid, viewingSlots, slotDirectory):
        self.clear_screen()
        slot = viewingSlots[slotDirectory[slotid]]
        print(slot)
        print("[R] Repair [M] Return to Rover Display")
        playerInput = input()
        if playerInput.upper() == "R":
            if slot.health == slot.max_health:
                print(slot.name + " is at full condition.")
                a = input()
                self.clear_screen()
                self.viewing_slot(slotid, viewingSlots, slotDirectory)
            else:
                percentage_full = 100 - slot.health_percent 
                repairCost = (self.repair_cost * 0.01) * percentage_full
                print("Current Credits: " + self.getCreditDisplay())
                print("Are you sure you want to repair " + slot.name + " for {}¢ credits?".format(int(repairCost)))
                print("[Y] Yes [N] No")
                playerInput = input()
                if playerInput.upper() == "Y":
                    if self.credits < self.repair_cost:
                        print("ERROR: NOT ENOUGH CREDITS!")
                        a = input()
                        self.clear_screen()
                        self.viewing_slot(slotid, viewingSlots, slotDirectory)
                    else:
                        print(slot.name + " fully repaired.")
                        self.credits -= repairCost
                        slot.health = slot.max_health
                        slot.dots = {}
                        a = input()
                        self.clear_screen()
                        self.viewing_slot(slotid, viewingSlots, slotDirectory)
                else:
                    self.viewing_slot(slotid, viewingSlots, slotDirectory)


        else:
            self.clear_screen()
            self.modify_rover()

    def modify_slot(self, slotid):
        slotDirectory = {"1": "Front",
                        "2": "Left",
                        "3": "Right",
                        "4": "Rear"}
        

        if self.selected_rover.displayingArmor:
            viewingSlots = self.selected_rover.armor_slots
        else:
            viewingSlots = self.selected_rover.weapon_slots

        if viewingSlots[slotDirectory[slotid]] is None:
            
            if self.selected_rover.displayingArmor:
                newArmor = Armor.Armor()
                newArmor.generateArmor("Medium",slotDirectory[slotid],type_count=2)
                self.selected_rover.armor_slots[slotDirectory[slotid]] = newArmor
                self.modify_rover()
            else:
                newWeapon = Weapon.Weapon()
                newWeapon.generateWeapon(2,random.randint(3,8), 10, slotDirectory[slotid])
                self.selected_rover.weapon_slots[slotDirectory[slotid]] = newWeapon
                self.modify_rover()
        else:
            self.viewing_slot(slotid,viewingSlots, slotDirectory)
           
    def arena(self):
        self.arenaObj.main()

    def modify_rover(self):
        print(self.selected_rover)
        print("[T] TOGGLE SLOTS VIEW")
        print("[#] MODIFY/REPAIR SLOT")
        print("[R] REPAIR ROVER CORE")
        print("[A] REPAIR ALL SLOTS")
        print("[G] GARAGE ")

        inputChosen = False
        while not inputChosen:
            playerInput = input(">")
            if playerInput.upper() == "T":
                self.selected_rover.displayingArmor = not self.selected_rover.displayingArmor
                self.clear_screen()
                self.modify_rover()
                inputChosen = True
            elif playerInput.upper() == "G":
                self.clear_screen()
                self.garage()
                inputChosen = True
            elif playerInput == "1" or playerInput == "2" or playerInput == "3" or playerInput == "4":
                self.clear_screen()
                self.modify_slot(playerInput)
            elif playerInput.upper() == "R":
                if self.selected_rover.health != self.selected_rover.max_health:
                    inputChosen = True
                    percentage_full = 100 - self.selected_rover.health_percent 
                    repairCost = (self.repair_cost * 0.01) * percentage_full
                    print("Current Credits: " + self.getCreditDisplay())
                    print("Are you sure you want to repair " + self.selected_rover + " for {}¢ credits?".format(int(repairCost)))
                    print("[Y] Yes [N] No")
                    playerInput = input()
                    if playerInput.upper() == "Y":
                        if self.credits < repairCost:
                            print("ERROR: NOT ENOUGH CREDITS!")
                            a = input()
                            self.clear_screen()
                            self.modify_rover()
                        else:
                            self.credits -= repairCost
                            print(self.selected_rover.name + "'s core is fully repaired.")
                            self.selected_rover.health = self.selected_rover.max_health
                            self.selected_rover.modifiers = {}
                            a = input()
                            self.clear_screen()
                            self.modify_rover()
                    else:
                        self.clear_screen()
                        self.modify_rover()
            elif playerInput.upper() == "A":
                damaged_slots = []
                for slot in self.selected_rover.armor_slots.values():
                    if slot.health != slot.max_health:
                        damaged_slots.append(slot)

                for slot in self.selected_rover.weapon_slots.values():
                    if slot.health != slot.max_health:
                        damaged_slots.append(slot)

                if len(damaged_slots) == 0:
                    print("All slots are in full condition.")
                    a = input()
                    self.clear_screen()
                    self.modify_rover()
                else:
                    repairCost = 0
                    for slot in damaged_slots:
                        percentage_full = 100 - slot.health_percent 
                        repairCost += (self.repair_cost * 0.01) * percentage_full
                    print("Current Credits: " + self.getCreditDisplay())
                    print("Are you sure you want to repair all slots for {}¢ credits?".format(int(repairCost)))
                    print("[Y] Yes [N] No")
                    playerInput = input()
                    if playerInput.upper() == "Y":
                        if self.credits < repairCost:
                            print("ERROR: NOT ENOUGH CREDITS!")
                            a = input()
                            self.clear_screen()
                            self.modify_rover()
                        else:
                            self.credits -= repairCost
                            for slot in damaged_slots:
                                print(slot.name + " is fully repaired.")
                                slot.health = slot.max_health
                                slot.dots = {}
                            a = input()
                            self.clear_screen()
                            self.modify_rover()
                    else:
                        self.clear_screen()
                        self.modify_rover()
            else:
                self.failedInput()
        

    def garage(self):
        if not self.selected_rover:
            name = "NONE SELECTED!"
        else:
            name = self.selected_rover.name

        spaces = ((21 - int(len(name))) * " ")

        displayString = ("""
 _______________________       
/                        \.
| WELCOME TO THE         |
| GARAGE!                |
|                        |
|                        |
| -* CURRENT ROVER:      |
|   {}{}| 
|                        | 
|                        | 
| [C] CREATE NEW ROVER   | 
| [M] MODIFY ROVER       |
| [S] SELECT ROVER       |
| [W] WORKSHOP           |
\________________________/
        """).format(name, spaces)

        print(displayString)
        inputChosen = False
        while not inputChosen:
            playerInput = input(">")
            if playerInput.upper() == "C":
                inputChosen = True
                self.clear_screen()
                self.create_new_rover()
            elif playerInput.upper() == "W":
                self.clear_screen()
                self.main()
                inputChosen = True
            elif playerInput.upper() == "M":
                if self.selected_rover is not None:
                    self.clear_screen()
                    self.modify_rover()
                    inputChosen = True
                else:
                    print("No rover selected.")
            elif playerInput.upper() == "S":
                if len(self.rovers) != 0:
                    self.clear_screen()
                    self.select_rover()
                    inputChosen = True
                else:
                    print("No rovers in garage.")
            else:
                self.failedInput()

    def select_rover(self):
        if not self.selected_rover:
            name = "NONE SELECTED!"
        else:
            name = self.selected_rover.name

        spaces = ((21 - int(len(name))) * " ")

        displayString = ("""
 _______________________       
/                        \.
| SELECT YOUR ROVER      |
| !.../---\...!          |
|                        |
| -* CURRENT ROVER:      |
|   {}{}| 
|                        | 
|                        |""").format(name, spaces)

        print(displayString)
        count = 1

        for rover in self.rovers:
            spaces = (19 - len(rover.name)) * " "
            roverRow = "| [{}] {}{}|".format(count, rover.name, spaces)
            print(roverRow)
            count += 1
        print("| [G] GARAGE             |")
        print("\________________________/")
        inputChosen = False
        while not inputChosen:
            playerInput = input(">")
            if playerInput.upper() == "G":
                inputChosen = True
                self.clear_screen()
                self.garage()
            elif playerInput.isdigit():
                selectedIndex = int(playerInput) - 1
                if selectedIndex >= 0 and selectedIndex < len(self.rovers):
                    self.selected_rover = self.rovers[selectedIndex]
                    self.arenaObj.playerRover = self.selected_rover
                    self.clear_screen()
                    self.select_rover()
                else:
                    self.failedInput()
            else:
                self.failedInput()
            

    def main(self):
        self.xp += self.arenaObj.winnings_xp
        self.credits += self.arenaObj.winnings_credits
        self.arenaObj.winnings_xp = 0
        self.arenaObj.winnings_credits = 0
        self.doLevelUp()

        self.clear_screen()
        if not self.selected_rover:
            name = "NONE SELECTED!"
        else:
            name = self.selected_rover.name

        spaces = (21 - int(len(name))) * " "

        xpSpaces = (23 - int(len(self.getXPDisplay()))) * " "
        creditSpaces = (23 - int(len(self.getCreditDisplay()))) * " "


        displayString = ("""
 _______________________       
/                        \.
| {}{}|
| {}{}|
|                        |
| WELCOME TO THE         |
| TIGER ROVERWORKS'      |
| WORKSHOP!              |
|                        |
| -* CURRENT ROVER:      |
|   {}{}| 
|                        | 
|                        | 
| [A] ARENA              | 
| [G] GARAGE             |
\________________________/
        """).format(self.getXPDisplay(), xpSpaces, self.getCreditDisplay(), creditSpaces, name, spaces)

        print(displayString)
        inputChosen = False
        while not inputChosen:
            playerInput = input(">")
            if playerInput.upper() == "G":
                inputChosen = True
                self.clear_screen()
                self.garage()
            elif playerInput.upper() == "A":
                inputChosen = True
                if self.selected_rover == None:
                    self.clear_screen()
                    self.main()
                else:
                    self.clear_screen()
                    self.arena()
                    self.clear_screen()
                    self.main()
            else:
                self.failedInput()

if __name__ == "__main__":
    newWorkshop = Workshop()
    newWorkshop.main()