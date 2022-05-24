# character functions
class Character:
    # init function
    def __init__(self):
        # access character API
        with open("CharacterData\\CharacterStats.txt") as file:
            file = file.read().split("\n")
            rawInfo = [character.split(" | ") for character in file]

            charName = [character[0] for character in rawInfo]
            charBaseStats = [tuple(map(float, character[1].split(" : "))) for character in rawInfo]
            charMaxAscensionStats = [tuple(map(float, character[2].split(" : "))) for character in rawInfo]
            charAscensionStat = [tuple([str(character[3].split(" : ")[0]), float(character[3].split(" : ")[1])])
                                 for character in rawInfo]
            charWeapon = [tuple([str(character[4].split(" : ")[0]), int(character[4].split(" : ")[1])])
                          for character in rawInfo]

            self.characterAPI = dict(zip(charName, tuple(zip(charBaseStats, charMaxAscensionStats, charAscensionStat,
                                                             charWeapon))))

        # access character multipliers
        with open("CharacterData\\CharacterLevelMultipliers.txt") as file:
            file = file.read().split("\n")
            rawInfo = [level.split(" : ") for level in file]

            level = [int(level[0]) for level in rawInfo]
            fourStar = [float(level[1]) for level in rawInfo]
            fiveStar = [float(level[2]) for level in rawInfo]

            self.characterMultipliers = dict(zip(level, tuple(zip(fourStar, fiveStar))))

        self.selectedCharacter = ""
        self.characterLevel = 0
        self.characterAscension = 0
        self.ascensionSection = 0
        self.baseHP = 0
        self.baseATK = 0
        self.baseDEF = 0
        self.ascensionStat = ()

    # select character
    def selectCharacter(self):
        while True:
            character = input("Select a character: ")
            try:
                self.characterAPI[character]
            except KeyError:
                print("Invalid character. Please try again.")
            else:
                self.selectedCharacter = character
                break

    # select level
    def selectCharacterLevel(self):
        while True:
            try:
                level = int(input(f"Level of {self.selectedCharacter}: "))
                if 90 >= int(level) > 0:
                    self.characterLevel = int(level)
                    break
                print("Invalid level. Please try again.")
            except ValueError:
                print("Invalid level. Please try again.")

    # select ascension and find ascension section
    def selectCharacterAscension(self):
        sectionDict = {0: 0, 1: 38, 2: 65, 3: 101, 4: 128, 5: 155, 6: 182}
        ascensionCheck = {20: (0, 1), 40: (1, 2), 50: (2, 3), 60: (3, 4), 70: (4, 5), 80: (5, 6), 90: (6,)}
        while True:
            try:
                ascension = int(input(f"Number of ascension stars for {self.selectedCharacter}: "))
                isValid = True if ascension in ascensionCheck[self.characterLevel] else False
                if 6 >= ascension > 0 and isValid:
                    self.characterAscension = ascension
                    self.ascensionSection = sectionDict[ascension]
                    break
                print("Invalid number of ascension stars. Please try again.")
            except ValueError:
                print("Invalid number of ascension stars. Please try again.")

    # calculate base stats
    def getCharacterBaseStats(self):
        self.baseHP = self.characterAPI[self.selectedCharacter][0][0] * self.characterMultipliers[self.characterLevel][
            0 if self.characterAPI[self.selectedCharacter][3][1] == 4 else 1] + self.characterAPI[
            self.selectedCharacter][1][0] * self.ascensionSection / 182
        self.baseATK = self.characterAPI[self.selectedCharacter][0][1] * self.characterMultipliers[self.characterLevel][
            0 if self.characterAPI[self.selectedCharacter][3][1] == 4 else 1] + self.characterAPI[
            self.selectedCharacter][1][1] * self.ascensionSection / 182
        self.baseDEF = self.characterAPI[self.selectedCharacter][0][2] * self.characterMultipliers[self.characterLevel][
            0 if self.characterAPI[self.selectedCharacter][3][1] == 4 else 1] + self.characterAPI[
            self.selectedCharacter][1][2] * self.ascensionSection / 182
        self.ascensionStat = (self.characterAPI[self.selectedCharacter][2][0], self.characterAPI[
            self.selectedCharacter][2][1] * (0, 1, 2, 2, 3, 4)[self.characterAscension - 1])


# get character data
def getCharacterData():
    print("Character:")
    character = Character()

    character.selectCharacter()
    character.selectCharacterLevel()
    character.selectCharacterAscension()

    return character


# weapon functions
class Weapon:
    # init function
    def __init__(self, selectedCharacter):
        # access weapon API
        character = Character()
        weaponType = character.characterAPI[selectedCharacter][3][0]
        match weaponType:
            case "sword":
                API = "Swords.txt"
            case "claymore":
                API = "Claymores.txt"
            case "polearm":
                API = "Polearms.txt"
            case "bow":
                API = "Bows.txt"
            case "catalyst":
                API = "Catalysts.txt"
            case _:
                API = ""
                print("wtf happened to your code")
        with open(f"WeaponData\\{API}") as file:
            file = file.read().split("\n")
            rawInfo = [weapon.split(" | ") for weapon in file]

            weaponName = [weapon[0] for weapon in rawInfo]
            weaponRarity = [int(weapon[1]) for weapon in rawInfo]
            weaponBaseATKType = [weapon[2] for weapon in rawInfo]
            weaponSubstat = [tuple(map(str, weapon[3].split(" : "))) for weapon in rawInfo]

            self.weaponAPI = dict(zip(weaponName, tuple(zip(weaponRarity, weaponBaseATKType, weaponSubstat))))

        # access weapon base ATK values
        with open("WeaponData\\WeaponBaseATKScaling.txt") as file:
            file = file.read().split("\n")
            rawInfo = [rarity.split(" | ") for rarity in file]

            baseATKtype = [rarity[0] for rarity in rawInfo]
            ATKValues = [tuple(map(int, rarity[1].split(" : "))) for rarity in rawInfo]

            self.weaponBaseATKValues = dict(zip(baseATKtype, ATKValues))

        # access weapon substat values
        with open("WeaponData\\WeaponSubstatScaling.txt") as file:
            file = file.read().split("\n")
            rawInfo = [value.split(" | ") for value in file]

            startingValue = [value[0] for value in rawInfo]
            substatValues = [tuple(map(float, value[1].split(" : "))) for value in rawInfo]

            self.weaponSubstatValues = dict(zip(startingValue, substatValues))

        # access weapon substat values for EM
        with open("WeaponData\\WeaponSubstatScalingEM.txt") as file:
            file = file.read().split("\n")
            rawInfo = [value.split(" | ") for value in file]

            startingValue = [value[0] for value in rawInfo]
            substatValues = [tuple(map(float, value[1].split(" : "))) for value in rawInfo]

            self.weaponSubstatValuesEM = dict(zip(startingValue, substatValues))

        self.selectedWeapon = ""
        self.weaponLevel = 0
        self.weaponAscension = 0
        self.weaponBaseATK = 0
        self.weaponSubstat = ()

    # select weapon
    def selectWeapon(self):
        while True:
            weapon = input("Select a weapon: ")
            try:
                self.weaponAPI[weapon]
            except KeyError:
                print("Invalid weaon. Please try again.")
            else:
                self.selectedWeapon = weapon
                break

    # select level
    def selectWeaponLevel(self):
        while True:
            try:
                level = int(input(f"Level of {self.selectedWeapon} (must be a multiple of 10): "))
                if 90 >= level > 0 and level % 10 == 0:
                    self.weaponLevel = level
                    break
                print("Invalid level. Please try again.")
            except ValueError:
                print("Invalid level. Please try again.")

    # select ascension
    def selectWeaponAscension(self):
        ascensionCheck = {20: (0, 1), 40: (1, 2), 50: (2, 3), 60: (3, 4), 70: (4, 5), 80: (5, 6), 90: (6,)}
        while True:
            try:
                ascension = int(input(f"Number of ascension stars for {self.selectedWeapon}: "))
                isValid = True if ascension in ascensionCheck[self.weaponLevel] else False
                if 6 >= ascension > 0 and isValid:
                    self.weaponAscension = ascension
                    break
                print("Invalid number of ascension stars. Please try again.")
            except ValueError:
                print("Invalid number of ascension stars. Please try again.")

    # calculate weapon base atk
    def getWeaponBaseATK(self):
        ascensionCheck = {20: (0, 1), 40: (1, 2), 50: (2, 3), 60: (3, 4), 70: (4, 5), 80: (5, 6), 90: (6,)}
        self.weaponBaseATK = self.weaponBaseATKValues[self.weaponAPI[self.selectedWeapon][1]][
            2 * self.weaponAscension - (0 if ascensionCheck[self.weaponLevel][0] == self.weaponAscension else 1)]

    # calculate weapon secondary stat
    def getWeaponSubstat(self):
        if self.weaponAPI[self.selectedWeapon][3][0] == "EM":
            self.weaponSubstat = (self.weaponAPI[self.selectedWeapon][3][0], self.weaponSubstatValuesEM[self.weaponAPI[
                self.selectedWeapon][3][1]][(20, 40, 50, 60, 70, 80, 90).index(self.weaponLevel)])
        else:
            self.weaponSubstat = (self.weaponAPI[self.selectedWeapon][3][0], self.weaponSubstatValues[self.weaponAPI[
                self.selectedWeapon][3][1]][(20, 40, 50, 60, 70, 80, 90).index(self.weaponLevel)])


# get weapon data
def getWeaponData(character):
    # weapon
    print("\n\n\nWeapon:")
    weapon = Weapon(character.selectedCharacter)

    weapon.selectWeapon()
    weapon.selectWeaponLevel()
    weapon.selectWeaponAscension()
    weapon.getWeaponBaseATK()
    weapon.getWeaponSubstat()

    return weapon


# artifact functions
class Artifact:
    # init function
    def __init__(self, piece):
        # access artifact sets
        with open("ArtifactData\\ArtifactSets.txt") as file:
            file = file.read().split("\n")
            rawInfo = [artifactSet.split(" | ") for artifactSet in file]

            artifactSetName = [artifactSet[0] for artifactSet in rawInfo]
            artifactRarities = [tuple(map(int, artifactSet[1].split(" : "))) for artifactSet in rawInfo]
            artifact2Piece = [artifactSet[2] for artifactSet in rawInfo]
            artifact4Piece = [artifactSet[3] for artifactSet in rawInfo]
            artifactStats = [tuple([tuple([str(stat.split(" / ")[0]), float(stat.split(" / ")[1])])
                                    for stat in artifactSet[4].split(" : ")]) for artifactSet in rawInfo]

            self.artifactSets = dict(zip(artifactSetName, tuple(zip(artifactRarities, artifact2Piece, artifact4Piece,
                                                                    artifactStats))))

        self.piece = piece
        self.artifactSet = ""
        self.artifactRarity = 0
        self.artifactLevel = 0
        self.artifactMainstat = ""
        self.mainstatValues = None
        self.substatRolls = None

    # select artifact set
    def selectArtifactSet(self):
        while True:
            pieceSet = input("Artifact set: ")
            try:
                self.artifactSets[pieceSet]
            except KeyError:
                print("Invalid artifact set. Please try again.")
            else:
                self.artifactSet = pieceSet
                break

    # select rarity (number of stars)
    def selectArtifactRarity(self):
        while True:
            try:
                rarity = int(input("Artifact rarity (number of stars): "))
                if rarity in self.artifactSets[self.artifactSet][0]:
                    self.artifactRarity = rarity
                    break
                print("Invalid artifact rarity. Please try again.")
            except ValueError:
                print("Invalid artifact rarity. Please try again.")

    # select level
    def selectArtifactLevel(self):
        rarityCheck = {1: 4, 2: 4, 3: 12, 4: 16, 5: 20}
        while True:
            try:
                level = int(input("Artifact level (must be a multiple of 4): "))
                if level % 4 == 0 and rarityCheck[self.artifactRarity] >= level >= 0:
                    self.artifactLevel = level
                    break
                print("Invalid artifact level. Please try again.")
            except ValueError:
                print("Invalid artifact level. Please try again.")

    # select mainstat
    def selectArtifactMainstat(self):
        artifactMainstats = {"Sands of Eon": ("HP%", "ATK%", "DEF%", "EM", "ER"),
                             "Goblet of Eonothem": ("HP%", "ATK%", "DEF%", "EM", "PHYS", "ANEMO", "GEO", "ELECTRO",
                                                    "DENDRO", "HYDRO", "PYRO", "CRYO"),
                             "Circlet of Logos": ("HP%", "ATK%", "DEF%", "EM", "CR", "CD", "HB")}
        match self.piece:
            case "Flower of Life":
                self.artifactMainstat = "HP"
            case "Plume of Death":
                self.artifactMainstat = "ATK"
            case _:
                while True:
                    mainstat = input("Artifact mainstat: ")
                    if mainstat in artifactMainstats[self.piece]:
                        self.artifactMainstat = mainstat
                        break
                    print("Invalid mainstat. Please try again.")

    # access mainstat API
    def accessArtifactMainstatValues(self):
        match self.artifactRarity:
            case 5:
                API = "Legendary.txt"
            case 4:
                API = "Epic.txt"
            case 3:
                API = "Rare.txt"
            case 2:
                API = "Uncommon.txt"
            case 1:
                API = "Common.txt"
            case _:
                API = ""
                print("wtf happened to your code")

        with open(f"ArtifactData\\{API}") as file:
            file = file.read().split("\n")
            rawInfo = [mainstat.split(" | ") for mainstat in file]

            mainstat = [mainstat[0] for mainstat in rawInfo]
            levelValues = [tuple(map(float, mainstat[1].split(" : "))) for mainstat in rawInfo]

            self.mainstatValues = dict(zip(mainstat, levelValues))

    # substat inner class
    class Substats:
        # init function
        def __init__(self, rarity, level, mainstat):
            self.artifactRarity = rarity
            self.artifactLevel = level
            self.artifactMainstat = mainstat
            self.initialSubstatAmount = 0
            self.substatRolls = None

        # select number of initial substats
        def selectInitialSubstatAmount(self):
            while True:
                try:
                    initial = int(input("Number of initial substats: "))
                    if initial in (self.artifactRarity - 2, self.artifactRarity - 1):
                        self.initialSubstatAmount = initial
                        break
                    print("Invalid number of substats. Please try again.")
                except ValueError:
                    print("Invalid number of substats. Please try again.")

        # select artifact roll
        def selectArtifactRollType(self):
            rollTypes = {1: ((1, 2), (0.8, 1.0)), 2: ((1, 2, 3), (0.7, 0.85, 1.0)),
                         3: ((1, 2, 3, 4), (0.7, 0.8, 0.9, 1.0)),
                         4: ((1, 2, 3, 4), (0.7, 0.8, 0.9, 1.0)), 5: ((1, 2, 3, 4), (0.7, 0.8, 0.9, 1.0))}
            while True:
                try:
                    rollType = int(input("Roll value: "))
                    if rollType in rollTypes[self.artifactRarity][0]:
                        return rollTypes[self.artifactRarity][1][rollType - 1]
                    print("Invalid roll type. Please try again.")
                except ValueError:
                    print("Invalid roll type. Please try again.")

        # select substats and base rolls
        def selectArtifactSubstats(self):
            possibleSubstats = ("HP", "ATK", "DEF", "HP%", "ATK%", "DEF%", "EM", "ER", "CR", "CD")

            rolls = self.initialSubstatAmount + int(self.artifactLevel / 4)
            if rolls > 4:
                rolls = 4

            substats = []
            values = []
            for el in range(rolls):
                while True:
                    substat = input(f"Substat #{el + 1}: ")
                    if substat in possibleSubstats and substat != self.artifactMainstat:
                        substats.append(substat)
                        break
                    print("Invalid substat. Please try again.")
                values.append(self.selectArtifactRollType())
            self.substatRolls = dict(zip(substats, values))

        # select substat rolls
        def selectArtifactSubstatRolls(self):
            rolls = self.initialSubstatAmount + int(self.artifactLevel / 4)

            if rolls > 4:
                rolls -= 4
                for el in range(rolls):
                    while True:
                        substat = input(f"Artifact roll #{el + 1}: ")
                        if substat in self.substatRolls.keys():
                            self.substatRolls[substat] += self.selectArtifactRollType()
                            break
                        print("Invalid substat. Please try again.")

    # get substats and roll value
    def getArtifactSubstatData(self):
        substats = self.Substats(self.artifactRarity, self.artifactLevel, self.artifactMainstat)

        substats.selectInitialSubstatAmount()
        print("\nFor each substat, there are different values of rolls.\nEach artifact rarity has its own roll types:"
              "\n - 1 star: 2 types\n - 2 star: 3 types\n - 3-5 star: 4 types"
              "\nFor example, an input of 4 for a 5 star artifact substat would give it a maxroll.")
        substats.selectArtifactSubstats()
        substats.selectArtifactSubstatRolls()

        self.substatRolls = substats.substatRolls


# find set bonuses
def getSetBonuses(artifactSets):
    if len(artifactSets) == len(set(artifactSets)):
        return {}
    else:
        setNames = []
        setAmount = []
        for artifactSet in set(artifactSets):
            amount = artifactSets.count(artifactSet)
            match amount:
                case 2 | 3:
                    setNames.append(artifactSet)
                    setAmount.append(2)
                case 4 | 5:
                    setNames.append(artifactSet)
                    setAmount.append(4)

        return dict(zip(setNames, setAmount))


# get artifact data
def getArtifactData():
    print("\n\n\nArtifacts:")
    flower = Artifact("Flower of Life")
    plume = Artifact("Plume of Death")
    sands = Artifact("Sands of Eon")
    goblet = Artifact("Goblet of Eonothem")
    circlet = Artifact("Circlet of Logos")

    artifactPieces = (flower, plume, sands, goblet, circlet)
    artifactSets = []
    for piece in artifactPieces:
        print(f"\n\n{piece.piece}:")
        piece.selectArtifactSet()
        piece.selectArtifactRarity()
        piece.selectArtifactLevel()
        piece.selectArtifactMainstat()
        piece.getArtifactSubstatData()
        artifactSets.append(piece.artifactSet)
    setBonuses = getSetBonuses(artifactSets)

    return setBonuses, flower, plume, sands, goblet, circlet


# main code
def main():
    characterData = getCharacterData()
    weaponData = getWeaponData(characterData)
    artifactData = getArtifactData()

    stats = {"HP": 0, "BaseATK": 0, "ATK": 0, "DEF": 0, "EM": 0, "CR": 5, "CD": 50, "HB": 0, "IHB": 0, "ER": 0, "SS": 0,
             "ANEMO": 0, "GEO": 0, "ELECTRO": 0, "DENDRO": 0, "HYDRO": 0, "PYRO": 0, "CRYO": 0, "ANEMORES": 0,
             "GEORES": 0, "ELECTRORES": 0, "DENDRORES": 0, "HYDRORES": 0, "PYRORES": 0, "CRYORES": 0}


if __name__ == "__main__":
    main()
