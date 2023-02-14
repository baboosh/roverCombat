import Data.CombatData as CombatData
import random

class Combat:

    def __init__(self, enemyRover, playerRover):
        self.enemyRover = enemyRover
        self.playerRover = playerRover
        self.damageData = CombatData.DamageData()
        self.orientations = ["Left-Exposed", "Forward", "Right-Exposed", "Rear-Exposed"]
        self.maneuvered = False
        self.fought = False
        self.fighting = False

        self.winnings_credits = 0
        self.winnings_xp = 0
        self.winnings_items = []

        self.frontDisplay = """
    /#######\ 
   []       []
    |       |
    |       |
   []       []
    \-------/
        """

        self.backDisplay = """
    /-------\ 
   []       []
    |       |
    |       |
   []       []
    \#######/
        """
        self.rightDisplay = """
      __---______---____
    /   ---      ---    \ 
    |                   #
    |                   #
    \___---______---____/ 
        ---      ---
        
        """
                
        self.leftDisplay = """
      __---______---____
    /   ---      ---     \ 
    #                    |
    #                    |
    \___---______---____/ 
        ---      ---
        
        """

        self.orientationDirectory = {"Left-Exposed":self.leftDisplay, "Forward": self.frontDisplay,
                                    "Right-Exposed":self.rightDisplay, "Rear-Exposed":self.backDisplay}

    def failedInput(self):
        print("Unrecognised Command! Please Try Again!")

    def clear_screen(self):
        count = 1
        while count < 100:
            count += 1
            print("\n")

    def handle_ticks(self):
        self.clear_screen()
        didTick = False
        rovers = [self.playerRover, self.enemyRover]
        for rover in rovers:
            for armor_slot in rover.armor_slots.values():
                for dot in armor_slot.dots:
                    didTick = True
                    print("\n\n\n! --- DOT TICK --- !")
                    print(" VICTIM: " + rover.name)
                    print(armor_slot.name)
                    combatResults = armor_slot.takeDamage(dot.doTick())
                    overkillTarget = self.getExposedSlot(rover)
                    if overkillTarget.health == 0:
                        rover.health -= combatResults[0]
                        rover.health_percent = (rover.health / rover.max_health * 100)
                    else:
                        overkillTarget.health -= combatResults[0]
                        overkillTarget.health_percent = (rover.health / rover.max_health * 100)
                    if dot.duration <= 0:
                        armor_slot.dots.remove(dot)
                    print(str(dot.duration) + " TURNS LEFT.")
            for weapon_slot in rover.weapon_slots.values():
                weapon_slot.cooldown -= 1
                if weapon_slot.cooldown < 0:
                    weapon_slot.cooldown = 0
        if didTick is False:
            print("(--- NO DAMAGE TICKS THIS TURN. ---)")

        newModifiers = {}
        for rover in rovers:
            if len(rover.modifiers) > 0:
                for modifier in rover.modifiers.keys():
                    newModifiers[modifier] = rover.modifiers[modifier] - 1
                    if newModifiers[modifier] <= 0:
                        del newModifiers[modifier]
                rover.modifiers = newModifiers
        
        a = input()
        return

    def view_rover(self, rover):
        inputChosen = False
        while not inputChosen:
            self.clear_screen()
            print(rover)
            print("[T] TOGGLE SLOTS VIEW")
            print("[#] MODIFY SLOT")
            print("[R] RETURN TO TURN ")
            playerInput = input(">")
            if playerInput.upper() == "T":
                rover.displayingArmor = not rover.displayingArmor
                self.clear_screen()
                self.view_rover(rover)
                inputChosen = True
            elif playerInput.upper() == "R":
                self.clear_screen()
                self.player_choices()
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


    def viewing_slot(self, slotid, viewingSlots, slotDirectory, rover):
        self.clear_screen()
        print(viewingSlots[slotDirectory[slotid]])
        print("[V] Back to View")
        playerInput = input()
        self.clear_screen()

    def adjustOrientationIndex(self, startingIndex, indexToCheck):
        startingIndex += indexToCheck
        if startingIndex < 0:
            startingIndex = 3
        if startingIndex > 3:
            startingIndex = 0
        return startingIndex


    def getExposedSlotAtOrientation(self, rover, orientation):
        if orientation == "Forward":
            if rover.armor_slots["Front"].health != 0:
                return rover.armor_slots["Front"]
            else:
                return rover.weapon_slots["Front"]

        if orientation == "Left-Exposed":
            if rover.armor_slots["Left"].health != 0:
                return rover.armor_slots["Left"]
            else:
                return rover.weapon_slots["Left"]    

        if orientation == "Right-Exposed":
            if rover.armor_slots["Right"].health != 0:
                return rover.armor_slots["Right"]
            else:
                return rover.weapon_slots["Right"]        

        if orientation == "Rear-Exposed":
            if rover.armor_slots["Rear"].health != 0:
                return rover.armor_slots["Rear"]
            else:
                return rover.weapon_slots["Rear"]    
        
    
    def getExposedSlot(self, rover):
        return self.getExposedSlotAtOrientation(rover, rover.orientation)

    def do_enemy_turn(self):
        print("DOING ENEMY TURN...")

        canManeuver = True
        canFight = True

        didManeuver = False
        didFight = False

        exposedSlot = self.getExposedSlot(self.enemyRover)

        exposedSlot.health_percent = int((exposedSlot.health / exposedSlot.max_health) * 100)
        self.enemyRover.health_percent = int((self.enemyRover.health / self.enemyRover.max_health) * 100)


        for modifier in self.enemyRover.modifiers.keys():
            if modifier in self.damageData.fightingStuns:
                canFight = False
            elif modifier in self.damageData.movingStuns:
                canManeuver = False

        armorPlateInjured = exposedSlot.health_percent <= 30 and exposedSlot.armor is True
        weaponSlotExposed = exposedSlot.armor is False

        if (armorPlateInjured or weaponSlotExposed) and canManeuver:

            orientationIndex = self.orientations.index(self.enemyRover.orientation)
            slotToMyLeft = self.getExposedSlotAtOrientation(self.enemyRover, self.orientations[self.adjustOrientationIndex(orientationIndex, -1)])
            slotToMyRight = self.getExposedSlotAtOrientation(self.enemyRover, self.orientations[self.adjustOrientationIndex(orientationIndex, 1)])
            furthestSlot = self.getExposedSlotAtOrientation(self.enemyRover, self.orientations[self.adjustOrientationIndex(orientationIndex, 2)])

            slotToMyLeft.health_percent = int((slotToMyLeft.health / slotToMyLeft.max_health) * 100)
            slotToMyRight.health_percent = int((slotToMyRight.health / slotToMyRight.max_health) * 100)
            furthestSlot.health_percent = int((furthestSlot.health / furthestSlot.max_health) * 100)

            left_slot_healthy_and_armor = slotToMyLeft.health_percent >= 30 and slotToMyLeft.armor is True
            right_slot_healthy_and_armor = slotToMyRight.health_percent >= 30 and slotToMyLeft.armor is True
            far_slot_healthy_and_armor = furthestSlot.health_percent >= 30 and furthestSlot.armor is True

            if left_slot_healthy_and_armor:
                self.doEnemyTurning("Left")
                didManeuver = True
            elif right_slot_healthy_and_armor:
                self.doEnemyTurning("Right")
                didManeuver = True
            

            elif far_slot_healthy_and_armor:
                if slotToMyLeft.health_percent >= slotToMyRight.health_percent:
                    self.doEnemyTurning("Left")
                    didManeuver = True
                else:
                    self.doEnemyTurning("Right")
                    didManeuver = True
            else:
                if weaponSlotExposed:
                    if slotToMyLeft.armor is False:
                        self.doEnemyTurning("Left")
                        didManeuver = True
                    elif slotToMyRight.armor is False:
                        self.doEnemyTurning("Right")
                        didManeuver = True

        if canFight:
            chosenSlot = None
            offensive_slots = []
            defensive_slots = []
            for weapon_slot in self.enemyRover.weapon_slots.values():
                front_weapon_and_facing_away = weapon_slot.range == "Front" and self.enemyRover.orientation == "Forward"
                if weapon_slot.health != 0 and not front_weapon_and_facing_away and weapon_slot.cooldown == 0:
                    if weapon_slot.weapon_type == "Offensive":
                        offensive_slots.append(weapon_slot)
                    else:
                        defensive_slots.append(weapon_slot)

            if (len(offensive_slots) + len(defensive_slots)) > 0:
                injured = (self.enemyRover.health_percent <= 30 or exposedSlot.health_percent <= 30)
                if injured and len(defensive_slots) > 0:
                    for weapon_slot in defensive_slots:
                        if "Repairing" in weapon_slot.damage_type:
                            chosenSlot = weapon_slot
                            break
                        elif "Guarding" in weapon_slot.damage_type:
                            chosenSlot = weapon_slot
                            break
                        elif "Cleansing" in weapon_slot.damage_type and self.hasDots(self.enemyRover):
                            chosenSlot = weapon_slot
                            break
                if not chosenSlot:
                    if len(offensive_slots) > 0:
                        chosenSlot = random.choice(offensive_slots)
                    elif len(defensive_slots) > 0:
                        chosenSlot = random.choice(defensive_slots)
            if chosenSlot:
                didFight = True
                target = self.getExposedSlot(self.playerRover)
                if self.isCoreExposed(self.playerRover):
                    target = self.playerRover
                self.use_slot(chosenSlot, self.enemyRover, target, self.playerRover)

        if not didFight and not didManeuver:
            print("Enemy Rover Passes!")
        pass               

    def hasDots(self, rover):
        if len(rover.modifiers) > 0:
            return True
        
        for slot in rover.armor_slots.values():
            if len(slot.dots) > 0:
                return True

        return False

    def doEnemyTurning(self, direction):
        self.enemyRover.orientation = self.turn(self.enemyRover.orientation, direction)
        print(self.enemyRover.name.upper() + " ROTATES " + direction.upper() + "!")
        a = input()

    def isCoreExposed(self, rover):

        frontVulnerable = (rover.orientation == "Forward") and (rover.armor_slots["Front"].health == 0 and rover.weapon_slots["Front"].health == 0)
        leftVulnerable = (rover.orientation == "Left-Exposed") and (rover.armor_slots["Left"].health == 0 and rover.weapon_slots["Left"].health == 0)
        rightVulnerable = (rover.orientation == "Right-Exposed") and (rover.armor_slots["Right"].health == 0 and rover.weapon_slots["Right"].health == 0)
        rearVulnerable = (rover.orientation == "Rear-Exposed") and (rover.armor_slots["Rear"].health == 0 and rover.weapon_slots["Rear"].health == 0)

        coreVulnerable = frontVulnerable or leftVulnerable or rightVulnerable or rearVulnerable

        if coreVulnerable:
            return True
        else:
            return False

    def player_manevuer(self):
        print("###### = FRONT")
        print(self.orientationDirectory[self.playerRover.orientation])
        print("Facing: {}".format(self.playerRover.orientation))
        print("[L] Turn Left -- NEW ROTATION: {}".format(self.turn(self.playerRover.orientation, "Left")))
        print("[R] Turn Right -- NEW ROTATION: {}".format(self.turn(self.playerRover.orientation, "Right")))
        print("[A] Abort Maneuver")

        inputChosen = False
        while not inputChosen:
            playerInput = input(">")
            if playerInput.upper() == "L":
                inputChosen = True
                self.clear_screen()
                self.playerRover.orientation = self.turn(self.playerRover.orientation, "Left")
                self.maneuvered = True
                self.player_choices()
                
            elif playerInput.upper() == "R":
                self.clear_screen()
                inputChosen = True
                self.playerRover.orientation = self.turn(self.playerRover.orientation, "Right")
                self.maneuvered = True
                self.player_choices()
        
            elif playerInput.upper() == "A":
                inputChosen = True
                self.clear_screen()
                self.player_choices()
            else:
                self.failedInput()
        

    def turn(self, orientation, direction="Left"):
        startingIndex = self.orientations.index(orientation)
        # ["Left", "Front", "Right", "Rear"]
        if direction == "Left":
            startingIndex -= 1
            if startingIndex < 0:
                startingIndex = 3
        else:
            startingIndex += 1
            if startingIndex > 3:
                startingIndex = 0
        return self.orientations[startingIndex]

    def startup(self):
        self.playerRover.orientation = "Forward"
        self.enemyRover.orientation = "Forward"
        print("START UP!")
        self.combat_turn()
        return [self.winnings_credits, self.winnings_xp, self.winnings_items]


    def combat_turn(self):
        self.fighting = True
        while self.fighting:
            self.player_choices()

    def use_slot(self, weapon_slot, sourceRover, target, targetRover):
        print(sourceRover.name.upper() + " USES " + weapon_slot.name.upper() + "!" + "\n\n")
        weapon_slot.cooldown = weapon_slot.max_cooldown
        if weapon_slot.weapon_type == "Offensive":
            damage = weapon_slot.generateDamage()
            if "Guarded" in targetRover.modifiers.keys():
                damage.damage = damage.damage * 0.2
            combatResults = target.takeDamage(damage)
            overkillTarget = self.getExposedSlot(targetRover)
            if overkillTarget.health == 0:
                targetRover.health -= combatResults[0]
            else:
                overkillTarget.health -= combatResults[0]
                overkillTarget.health_percent = (targetRover.health / targetRover.max_health * 100)
            targetRover.health_percent = (targetRover.health / targetRover.max_health * 100)
            modifiers = combatResults[1]
            for modifier in modifiers:
                try:
                    targetRover.modifiers[modifier] += modifiers[modifier]
                except KeyError:
                    targetRover.modifiers[modifier] = 1
        
        else:
            self.use_support_slot(weapon_slot, sourceRover)
        waitForInput = input("[PRESS ENTER TO CONTINUE]")

        if self.enemyRover.health <= 0:
            self.win()
        
        if self.playerRover.health <= 0:
            self.lose()

    def use_support_slot(self, weapon_slot, rover):
        
        for support_type in weapon_slot.damage_type:
                if support_type == "Cleansing":
                    for slot in rover.armor_slots.values():
                        slot.dots = []
                    rover.modifiers = {}
                    print("[ ALL DOTS CLEANSED ]")

                elif support_type == "Repairing":
                    for slot in rover.armor_slots.values():
                        if slot.health != 0 and slot.health != slot.max_health:
                            slot.health += slot.max_health * 0.3
                            print("30% HP RESTORED TO " + slot.name.upper() + "!")

                        if slot.health > slot.max_health:
                            slot.health = slot.max_health

                    for slot in rover.weapon_slots.values():
                        if slot.health != 0 and slot.health != slot.max_health:
                            slot.health += slot.max_health * 0.3
                            
                        if slot.health > slot.max_health:
                            slot.health = slot.max_health

                    if rover.health != rover.max_health:
                        print("[20% HP RESTORED TO " + rover.name.upper() + "'S CORE!]")
                        rover.health += rover.health * 0.2
                        if rover.health > rover.max_health:
                            rover.health = rover.max_health
                    

                elif support_type == "Guarding":
                    try:
                        rover.modifiers["Guarded"] += 1
                    except KeyError:
                        rover.modifiers["Guarded"] = 1
                    print("+1 GUARDING (-80% DAMAGE TAKEN) TO ENTIRE ROVER.")
                else:
                    print("ERROR: ACTIVATED DEFENSIVE WEAPON WITH NO DEFENSIVE TYPE.")
                    

        weapon_slot.health -= weapon_slot.health / weapon_slot.damage
        weapon_slot.health_percent = (weapon_slot.health / weapon_slot.max_health) * 100
        if weapon_slot.health <= 0:
            weapon_slot.health = 0

    def lose(self):
        print("YOUR ROVER'S CORE HAS BEEN DESTROYED!")
        print("RETURNING TO THE WORKSHOP.")
        self.playerRover.health = self.playerRover.max_health * 0.2
        self.fighting = False
        a = input()
        return

    def win(self):
        self.winnings_credits = random.randint(50, 200)
        self.winnings_xp = random.randint(40, 100)
        print("YOU DESTROYED THE ENEMY ROVER'S CORE!")
        print("RETURNING TO THE WORKSHOP.")
        print("+" + str(self.winnings_credits) + "¢")
        print("+" + str(self.winnings_xp) + "XP")
        self.fighting = False
        a = input()
        return

    def use_slots(self):
        target = ""
        targetObj = None
        conditionText = ""
        print("-------- CHOOSE A WEAPON TO USE -----------\n")
        if self.isCoreExposed(self.enemyRover):
            targetObj = self.enemyRover
            target = "> !" + targetObj.name.upper() + " CORE IS TARGETTED ! <"
            
            conditionText = "INTEGRITY: " + str(self.enemyRover.health_percent) + "%"
        else:
            targetObj = self.getExposedSlot(self.enemyRover)
            target = "> !" + targetObj.name.upper() + " IS TARGETTED ! <"
            conditionText = "INTEGRITY: " + str(self.getExposedSlot(self.enemyRover).health_percent) + "%"

        print(target + "\n")
        print(conditionText + "\n\n")
        index = 1

        valid_slots = {}
        for weapon_slot in self.playerRover.weapon_slots.values():
            indexText = str(index)
            if weapon_slot.health == 0:
                indexText = "OFFLINE"
            elif weapon_slot.range == "Front" and self.playerRover.orientation != "Forward":
                indexText = "CANT HIT"
            elif weapon_slot.cooldown > 0:
                indexText = "COOLING DOWN"
            else:
                valid_slots[index] = weapon_slot
            print("[{}] {}".format(indexText, weapon_slot.name))
            index += 1

        print("\n[A] ABORT SLOT USE")
        inputChosen = False
        while not inputChosen:
            playerInput = input(">![")
            if playerInput.upper() == "A":
                inputChosen = True
                self.clear_screen()
                return
            elif playerInput.isdigit():
                if int(playerInput) in valid_slots.keys():
                    inputChosen = True
                    self.fought = True
                    self.clear_screen()
                    print("----- PLAYER ATTACK -----")
                    self.use_slot(valid_slots[int(playerInput)], self.playerRover, targetObj, targetRover=self.enemyRover)
            else:
                self.failedInput()


    def player_choices(self):
        if not self.fighting:
            return
        self.clear_screen()
        canManeuver = self.playerRover.can_move()
        canFight = self.playerRover.can_fight()

        fightButtonTXT = "U"
        manevuerButtonTXT = "M"
        passTXT = "P"

        if self.fought:
            fightButtonTXT = "USED"
        
        if not canFight:
            fightButtonTXT = "STUNNED"
        
        if self.maneuvered:
            manevuerButtonTXT = "USED"

        if not canManeuver:
            manevuerButtonTXT = "STUNNED"

        if fightButtonTXT != "U" and manevuerButtonTXT != "M":
            passTXT = ">!P!<"

        displayText = """
 /---------------- YOUR TURN ---------------\ 
|
|
| ENEMY ROVER:
| ---- {}-------------
| FACING {}!
| ROVER HEALTH AT {}%
| SLOT EXPOSED AT {}% --- {}
| STATUS: {}
| MODIFIERS: {}
| --------------------------------------
|
| YOUR ROVER:
| ---- {}-------------
| FACING {}!
| ROVER HEALTH AT {}%
| SLOT EXPOSED AT {}% --- {}
| STATUS: {}
| MODIFIERS: {}
| -----------------------------------------------
| 
| [E] VIEW THE ENEMY'S ROVER
| [R] VIEW YOUR OWN ROVER
|
| [{}] USE SLOT
| [{}] MANEUVER
| [{}] PASS
\_____________________________________________/

        """.format(self.enemyRover.name, self.enemyRover.orientation, int(self.enemyRover.health / self.enemyRover.max_health * 100),
         int(self.getExposedSlot(self.enemyRover).health / self.getExposedSlot(self.enemyRover).max_health * 100), self.getExposedSlot(self.enemyRover).name, self.enemyRover.getCondition(), self.enemyRover.getModifiers(),
         self.playerRover.name, self.playerRover.orientation, int(self.playerRover.health_percent),
          int(self.getExposedSlot(self.playerRover).health / self.getExposedSlot(self.playerRover).max_health * 100), self.getExposedSlot(self.playerRover).name,
          self.playerRover.getCondition(), self.playerRover.getModifiers(), fightButtonTXT, manevuerButtonTXT, passTXT)

        print(displayText)
        inputChosen = False
        while not inputChosen:
            if not self.fighting:
                break
            playerInput = input("]")
            if playerInput.upper() == "E":
                self.clear_screen()
                self.view_rover(self.enemyRover)
                inputChosen = True
                self.player_choices()
            elif playerInput.upper() == "R":
                self.clear_screen()
                self.view_rover(self.playerRover)
                inputChosen = True
                self.player_choices()
            elif playerInput.upper() == "U":
                self.clear_screen()
                if self.fought:
                    print(">| !WEAPONS CHARGING!")
                else:
                    inputChosen = True
                    self.clear_screen()
                    self.use_slots()
                    self.player_choices()
            elif playerInput.upper() == "M":
                self.clear_screen()
                if self.maneuvered:
                    print(">| !WHEELS SPOOLING UP!")
                    self.player_choices()
                else:
                    inputChosen = True
                    self.player_manevuer()
            elif playerInput.upper() == "P":
                inputChosen = True
                self.maneuvered = False
                self.fought = False
                self.clear_screen()
                self.do_enemy_turn()
                self.handle_ticks()
            else:
                inputChosen = True
                self.player_choices()