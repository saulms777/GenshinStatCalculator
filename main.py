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
        self.ascensionSection = 0

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
                    self.ascensionSection = sectionDict[ascension]
                    break
                print("Invalid number of ascension stars. Please try again.")
            except ValueError:
                print("Invalid number of ascension stars. Please try again.")


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
            weaponAscensionStat = [tuple([str(weapon[3].split(" : ")[0]), float(weapon[3].split(" : ")[1])])
                                   for weapon in rawInfo]

            self.weaponAPI = dict(zip(weaponName, tuple(zip(weaponRarity, weaponBaseATKType, weaponAscensionStat))))

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

        self.selectedWeapon = ""
        self.weaponLevel = 0
        self.weaponAscension = 0
        self.weaponBaseATK = 0

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
            self.substats = []
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

        # select substats
        def selectArtifactSubstats(self):
            possibleSubstats = ["HP", "ATK", "DEF", "HP%", "ATK%", "DEF%", "EM", "ER", "CR", "CD"]
            possibleSubstats.remove(self.artifactMainstat)

            rolls = self.initialSubstatAmount + int(self.artifactLevel / 4)
            if rolls > 4:
                rolls = 4

            substats = []
            for el in range(rolls):
                while True:
                    substat = input(f"Substat #{el + 1}: ")
                    if substat in possibleSubstats:
                        substats.append(substat)
                        break
                    print("Invalid substat. Please try again.")
            self.substats = substats

        # select artifact roll
        def selectArtifactRollType(self):
            rollTypes = {1: ((1, 2), (0.8, 1.0)), 2: ((1, 2, 3), (0.7, 0.85, 1.0)),
                         3: ((1, 2, 3, 4), (0.7, 0.8, 0.9, 1.0)),
                         4: ((1, 2, 3, 4), (0.7, 0.8, 0.9, 1.0)), 5: ((1, 2, 3, 4), (0.7, 0.8, 0.9, 1.0))}
            while True:
                try:
                    rollType = int(input("Type of roll: "))
                    if rollType in rollTypes[self.artifactRarity][0]:
                        return rollTypes[self.artifactRarity][1][rollType - 1]
                    print("Invalid roll type. Please try again.")
                except ValueError:
                    print("Invalid roll type. Please try again.")

        # calculate total substat roll value
        def getArtifactSubstatRolls(self):
            rolls = self.initialSubstatAmount + int(self.artifactLevel / 4)
            substatRolls = dict.fromkeys(self.substats, 0)
            for substat in self.substats:
                substatRolls[substat] += self.selectArtifactRollType()

            if rolls <= 4:
                self.substatRolls = substatRolls
            rolls -= 4

            for el in range(rolls):
                while True:
                    substat = input(f"\nRoll #{el + 1}: ")
                    if substat in self.substats:
                        substatRolls[substat] += self.selectArtifactRollType()
                        break
                    print("Invalid substat. Please try again.")
            self.substatRolls = substatRolls

    # get substats and roll value
    def getArtifactSubstatData(self):
        substats = self.Substats(self.artifactRarity, self.artifactLevel, self.artifactMainstat)

        substats.selectInitialSubstatAmount()
        substats.selectArtifactSubstats()
        substats.getArtifactSubstatRolls()

        self.substatRolls = substats.substatRolls


# main code
def main():
    # character
    print(f"Character:")
    character = Character()

    character.selectCharacter()
    character.selectCharacterLevel()
    character.selectCharacterAscension()

    # weapon
    print(f"\n\nWeapon:")
    weapon = Weapon(character.selectedCharacter)

    weapon.selectWeapon()
    weapon.selectWeaponLevel()
    weapon.selectWeaponAscension()
    weapon.getWeaponBaseATK()

    # artifacts
    print(f"\n\nArtifacts:")
    flower = Artifact("Flower of Life")
    plume = Artifact("Plume of Death")
    sands = Artifact("Sands of Eon")
    goblet = Artifact("Goblet of Eonothem")
    circlet = Artifact("Circlet of Logos")

    artifactPieces = (flower, plume, sands, goblet, circlet)
    for piece in artifactPieces:
        print(f"\n{piece.piece}:")
        piece.selectArtifactSet()
        piece.selectArtifactRarity()
        piece.selectArtifactLevel()
        piece.selectArtifactMainstat()
        piece.getArtifactSubstatData()


if __name__ == "__main__":
    main()
