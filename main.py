# character functions
def accessCharacters():
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

        return dict(zip(charName, tuple(zip(charBaseStats, charMaxAscensionStats, charAscensionStat, charWeapon))))


def accessCharacterMultipliers():
    with open("CharacterData\\CharacterLevelMultipliers.txt") as file:
        file = file.read().split("\n")
        rawInfo = [level.split(" : ") for level in file]

        level = [int(level[0]) for level in rawInfo]
        fourStar = [float(level[1]) for level in rawInfo]
        fiveStar = [float(level[2]) for level in rawInfo]

        return dict(zip(level, tuple(zip(fourStar, fiveStar))))


def selectCharacter():
    while True:
        character = input("Select a character: ")
        try:
            accessCharacters()[character]
        except KeyError:
            print("Invalid character. Please try again.")
        else:
            return character


def selectCharacterLevel(character):
    while True:
        try:
            level = int(input(f"Level of {character}: "))
            if 90 >= int(level) > 0:
                return int(level)
            print("Invalid level. Please try again.")
        except ValueError:
            print("Invalid level. Please try again.")


def checkCharacterAscension(level, ascension):
    ascensionCheck = {20: (0, 1), 40: (1, 2), 50: (2, 3), 60: (3, 4), 70: (4, 5), 80: (5, 6), 90: (6,)}
    return True if ascension in ascensionCheck[level] else False


def selectCharacterAscension(character, level):
    sectionDict = {0: 0, 1: 38, 2: 65, 3: 101, 4: 128, 5: 155, 6: 182}
    while True:
        try:
            charAscension = int(input(f"Number of ascension stars for {character}: "))
            isValid = checkCharacterAscension(level, charAscension)
            if 6 >= charAscension > 0:
                section = sectionDict[charAscension]
                if isValid:
                    return section
            print("Invalid number of ascension stars. Please try again.")
        except ValueError:
            print("Invalid number of ascension stars. Please try again.")


# weapon functions
def accessWeapons(API):
    with open(f"WeaponData\\{API}") as file:
        file = file.read().split("\n")
        rawInfo = [weapon.split(" | ") for weapon in file]

        weaponName = [weapon[0] for weapon in rawInfo]
        weaponRarity = [int(weapon[1]) for weapon in rawInfo]
        weaponBaseATKType = [weapon[2] for weapon in rawInfo]
        weaponAscensionStat = [tuple([str(weapon[3].split(" : ")[0]), float(weapon[3].split(" : ")[1])])
                               for weapon in rawInfo]

        return dict(zip(weaponName, tuple(zip(weaponRarity, weaponBaseATKType, weaponAscensionStat))))


def accessWeaponBaseATKValues():
    with open("WeaponData\\WeaponBaseATKScaling.txt") as file:
        file = file.read().split("\n")
        rawInfo = [rarity.split(" | ") for rarity in file]

        baseATKtype = [rarity[0] for rarity in rawInfo]
        ATKValues = [tuple(map(int, rarity[1].split(" : "))) for rarity in rawInfo]

        return dict(zip(baseATKtype, ATKValues))


def accessWeaponSubstatValues():
    with open("WeaponData\\WeaponSubstatScaling.txt") as file:
        file = file.read().split("\n")
        rawInfo = [value.split(" | ") for value in file]

        startingValue = [value[0] for value in rawInfo]
        substatValues = [tuple(map(float, value[1].split(" : "))) for value in rawInfo]

        return dict(zip(startingValue, substatValues))


def getWeaponAPI(character):
    weaponType = accessCharacters()[character][3][0]
    match weaponType:
        case "sword":
            return accessWeapons("Swords.txt")
        case "claymore":
            return accessWeapons("Claymores.txt")
        case "polearm":
            return accessWeapons("Polearms.txt")
        case "bow":
            return accessWeapons("Bows.txt")
        case "catalyst":
            return accessWeapons("Catalysts.txt")


def selectWeapon(weaponTypeAPI):
    while True:
        weapon = input("Select a weapon: ")
        try:
            weaponTypeAPI[weapon]
        except KeyError:
            print("Invalid weaon. Please try again.")
        else:
            return weapon


def selectWeaponLevel(weapon):
    while True:
        try:
            level = int(input(f"Level of {weapon} (must be a multiple of 10): "))
            if 90 >= level > 0 and level % 10 == 0:
                return level
            print("Invalid level. Please try again.")
        except ValueError:
            print("Invalid level. Please try again.")


def selectWeaponAscension(weapon):
    while True:
        try:
            ascension = int(input(f"Number of ascension stars for {weapon}: "))
            if 6 >= ascension > 0:
                return ascension
            print("Invalid number of ascension stars. Please try again.")
        except ValueError:
            print("Invalid level. Please try again.")


def checkWeaponAscension(level, ascension):
    ascensionCheck = {20: (0, 1), 40: (1, 2), 50: (2, 3), 60: (3, 4), 70: (4, 5), 80: (5, 6), 90: (6,)}
    return 0 if ascensionCheck[level][0] == ascension else 1


# artifact functions
def accessArtifactSets():
    with open("ArtifactData\\ArtifactSets.txt") as file:
        file = file.read().split("\n")
        rawInfo = [artifactSet.split(" | ") for artifactSet in file]

        artifactSetName = [artifactSet[0] for artifactSet in rawInfo]
        artifactRarities = [tuple(map(int, artifactSet[1].split(" : "))) for artifactSet in rawInfo]
        artifact2Piece = [artifactSet[2] for artifactSet in rawInfo]
        artifact4Piece = [artifactSet[3] for artifactSet in rawInfo]
        artifactStats = [tuple([tuple([str(stat.split(" / ")[0]), float(stat.split(" / ")[1])])
                                for stat in artifactSet[4].split(" : ")]) for artifactSet in rawInfo]

        return dict(zip(artifactSetName, tuple(zip(artifactRarities, artifact2Piece, artifact4Piece, artifactStats))))


def accessArtifactMainstatValues(rarity):
    with open(f"ArtifactData\\{rarity}") as file:
        file = file.read().split("\n")
        rawInfo = [mainstat.split(" | ") for mainstat in file]

        mainstat = [mainstat[0] for mainstat in rawInfo]
        levelValues = [tuple(map(float, mainstat[1].split(" : "))) for mainstat in rawInfo]

        return dict(zip(mainstat, levelValues))


def selectArtifactSet():
    while True:
        pieceSet = input("Artifact set: ")
        try:
            accessArtifactSets()[pieceSet]
        except KeyError:
            print("Invalid artifact set. Please try again.")
        else:
            return pieceSet


def selectArtifactRarity(artifactSet):
    while True:
        try:
            rarity = int(input("Artifact rarity (number of stars): "))
            if rarity in accessArtifactSets()[artifactSet][0]:
                return rarity
            print("Invalid artifact rarity. Please try again.")
        except ValueError:
            print("Invalid artifact rarity. Please try again.")


def checkArtifactLevel(artifactRarity):
    rarityCheck = {1: 4, 2: 4, 3: 12, 4: 16, 5: 20}
    return rarityCheck[artifactRarity]


def selectArtifactLevel(rarity):
    while True:
        try:
            level = int(input("Artifact level (must be a multiple of 4): "))
            if level % 4 == 0 and checkArtifactLevel(rarity) >= level >= 0:
                return level
            print("Invalid artifact level. Please try again.")
        except ValueError:
            print("Invalid artifact level. Please try again.")


def selectArtifactMainstat(pieceType):
    artifactMainstats = {"Sands of Eon": ("HP%", "ATK%", "DEF%", "EM", "ER"),
                         "Goblet of Eonothem": ("HP%", "ATK%", "DEF%", "EM", "PHYS", "ANEMO", "GEO", "ELECTRO",
                                                "DENDRO", "HYDRO", "PYRO", "CRYO"),
                         "Circlet of Logos": ("HP%", "ATK%", "DEF%", "EM", "CR", "CD", "HB")}
    match pieceType:
        case "Flower of Life":
            return "HP"
        case "Plume of Death":
            return "ATK"
        case _:
            while True:
                mainstat = input("Artifact mainstat: ")
                if mainstat in artifactMainstats[pieceType]:
                    return mainstat
                print("Invalid mainstat. Please try again.")


def getArtifactMainstatAPI(rarity):
    match rarity:
        case 5:
            return accessArtifactMainstatValues("Legendary.txt")
        case 4:
            return accessArtifactMainstatValues("Epic.txt")
        case 3:
            return accessArtifactMainstatValues("Rare.txt")
        case 2:
            return accessArtifactMainstatValues("Uncommon.txt")
        case 1:
            return accessArtifactMainstatValues("Common.txt")


def selectInitialSubstatAmount(rarity):
    while True:
        try:
            initial = int(input("Number of initial substats: "))
            if initial in (rarity - 2, rarity - 1):
                return initial
            print("Invalid number of substats. Please try again.")
        except ValueError:
            print("Invalid number of substats. Please try again.")


def selectArtifactSubstats(rolls, mainstat):
    if rolls > 4:
        rolls = 4
    substats = []
    possibleSubstats = ["HP", "ATK", "DEF", "HP%", "ATK%", "DEF%", "EM", "ER", "CR", "CD"]
    possibleSubstats.remove(mainstat)
    for el in range(rolls):
        while True:
            substat = input(f"Substat #{el + 1}: ")
            if substat in possibleSubstats:
                substats.append(substat)
                break
            print("Invalid substat. Please try again.")
    return substats


def selectArtifactRollType(rarity):
    rollTypes = {1: ((1, 2), (0.8, 1.0)), 2: ((1, 2, 3), (0.7, 0.85, 1.0)), 3: ((1, 2, 3, 4), (0.7, 0.8, 0.9, 1.0)),
                 4: ((1, 2, 3, 4), (0.7, 0.8, 0.9, 1.0)), 5: ((1, 2, 3, 4), (0.7, 0.8, 0.9, 1.0))}
    while True:
        try:
            rollType = int(input("Type of roll: "))
            if rollType in rollTypes[rarity][0]:
                return rollTypes[rarity][1][rollType - 1]
            print("Invalid roll type. Please try again.")
        except ValueError:
            print("Invalid roll type. Please try again.")


def getArtifactSubstatRolls(rarity, substats, rolls):
    substatRolls = dict.fromkeys(substats, 0)
    for substat in substats:
        substatRolls[substat] += selectArtifactRollType(rarity)

    if rolls <= 4:
        return substatRolls
    rolls -= 4
    for el in range(rolls):
        while True:
            substat = input(f"\nRoll #{el + 1}: ")
            if substat in substats:
                substatRolls[substat] += selectArtifactRollType(rarity)
                break
            print("Invalid substat. Please try again.")
    return substatRolls


def getArtifactSubstatData(rarity, level, mainstat):
    initialSubstats = selectInitialSubstatAmount(rarity)
    totalRolls = initialSubstats + int(level / 4)
    artifactSubstats = selectArtifactSubstats(totalRolls, mainstat)
    substatRolls = getArtifactSubstatRolls(rarity, artifactSubstats, totalRolls)

    return substatRolls


def getArtifactStats(pieceType):
    print(f"\n{pieceType}:")
    pieceSet = selectArtifactSet()
    pieceRarity = selectArtifactRarity(pieceSet)
    pieceLevel = selectArtifactLevel(pieceRarity)
    pieceMainstat = selectArtifactMainstat(pieceType)
    pieceMainstatValue = getArtifactMainstatAPI(pieceRarity)[pieceMainstat][int(pieceLevel / 4)]
    pieceSubstats = getArtifactSubstatData(pieceRarity, pieceLevel, pieceMainstat)

    return pieceSet, pieceRarity, pieceLevel, (pieceMainstat, pieceMainstatValue), pieceSubstats


# main code
def main():
    # character input
    print("Character:\n")
    charAPI = accessCharacters()
    selectedChar = selectCharacter()
    charLevel = selectCharacterLevel(selectedChar)
    ascensionSection = selectCharacterAscension(selectedChar, charLevel)

    # weapon input
    print("\n\nWeapon:\n")
    weaponAPI = getWeaponAPI(selectedChar)
    selectedWeapon = selectWeapon(weaponAPI)
    weaponLevel = selectWeaponLevel(selectedWeapon)
    weaponAscension = selectWeaponAscension(selectedWeapon)
    weaponBaseATK = accessWeaponBaseATKValues()[weaponAPI[selectedWeapon][1]][
        2 * weaponAscension - checkWeaponAscension(weaponLevel, weaponAscension)]

    # artifact input
    print("\n\nArtifacts:")
    for piece in ("Flower of Life", "Plume of Death", "Sands of Eon", "Goblet of Eonothem", "Circlet of Logos"):
        print(getArtifactStats(piece))

    levelMultipliers = accessCharacterMultipliers()
    baseHP = charAPI[selectedChar][0][0] * \
        levelMultipliers[charLevel][0 if accessCharacters()[selectedChar][3][1] == 4 else 1] + \
        charAPI[selectedChar][1][0] * ascensionSection / 182
    baseATK = charAPI[selectedChar][0][1] * \
        levelMultipliers[charLevel][0 if accessCharacters()[selectedChar][3][1] == 4 else 1] + \
        charAPI[selectedChar][1][1] * ascensionSection / 182 + weaponBaseATK
    baseDEF = charAPI[selectedChar][0][2] * \
        levelMultipliers[charLevel][0 if accessCharacters()[selectedChar][3][1] == 4 else 1] + \
        charAPI[selectedChar][1][2] * ascensionSection / 182

    stats = {"HP": 0, "BaseATK": 0, "ATK": 0, "DEF": 0, "EM": 0, "CR": 5, "CD": 50, "HB": 0, "IHB": 0, "ER": 0, "SS": 0,
             "ANEMO": 0, "GEO": 0, "ELECTRO": 0, "DENDRO": 0, "HYDRO": 0, "PYRO": 0, "CRYO": 0, "ANEMORES": 0,
             "GEORES": 0, "ELECTRORES": 0, "DENDRORES": 0, "HYDRORES": 0, "PYRORES": 0, "CRYORES": 0}


if __name__ == "__main__":
    main()
