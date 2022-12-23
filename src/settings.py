from pygame import init as pygameInit
from pygame.font import Font
from PIL import Image
from mapDictionary  import *

pygameInit()

WIDTH = 1280
HEIGHT = 720

FPS = 60

TILESIZE = 64

BORDER_COLOR = "#111111"
FILL_COLOR = "#222222"


UI_SIZE = 16
TEXT_SIZE = 25
HELP_TEXT_SIZE = round(TEXT_SIZE * 1.15)

ICON_SIZE = UI_SIZE * 3
ICON_PADDING = 0.25
EFFECT_BOX_HEIGHT = (1+ICON_PADDING) * ICON_SIZE
HORIZONTAL_PADDING = 0.125
EFFECT_BOX_WIDTH = (2 + HORIZONTAL_PADDING) * EFFECT_BOX_HEIGHT
UI_SPACING = 5
NO_EFFECT_TEXT = int(ICON_SIZE * 0.4)
EFFECT_TEXT = int(ICON_SIZE * 0.5)

ONE_POWERUP_ACTIVE = (UI_SPACING + 0.5 * EFFECT_BOX_WIDTH, HEIGHT - (UI_SPACING + 0.5 * EFFECT_BOX_HEIGHT))
TWO_POWERUP_ACTIVE_1 = (UI_SPACING + (EFFECT_BOX_HEIGHT * HORIZONTAL_PADDING / 3) + 0.5 * ICON_SIZE * (ICON_PADDING + 1), HEIGHT - UI_SPACING - EFFECT_BOX_HEIGHT + (EFFECT_BOX_HEIGHT) / 2)
TWO_POWERUP_ACTIVE_2 = (UI_SPACING + (EFFECT_BOX_HEIGHT * HORIZONTAL_PADDING / 3) + 0.5 * ICON_SIZE * (ICON_PADDING + 1) + (EFFECT_BOX_HEIGHT * HORIZONTAL_PADDING / 3) + EFFECT_BOX_HEIGHT, HEIGHT - UI_SPACING - EFFECT_BOX_HEIGHT + (EFFECT_BOX_HEIGHT) / 2)

UI_COIN_SIZE = UI_SIZE * 2
COIN_BOX_HEIGHT = (1+ICON_PADDING) * UI_COIN_SIZE
COIN_BOX_TEXT_SPACE_SCALE = 2.25
COIN_BOX_WIDTH = (COIN_BOX_TEXT_SPACE_SCALE + HORIZONTAL_PADDING) * COIN_BOX_HEIGHT 
COIN_ICON_LOCATION = (0.5 * UI_COIN_SIZE * (1 + ICON_PADDING) + HORIZONTAL_PADDING * (1/3) + UI_SPACING, HEIGHT - (2*UI_SPACING + EFFECT_BOX_HEIGHT + COIN_BOX_HEIGHT * 0.5))
COIN_TEXT_LOCATION = (COIN_BOX_HEIGHT + HORIZONTAL_PADDING * (2/3) + UI_SPACING, COIN_ICON_LOCATION[1]) 

LEVEL_BOX_HEIGHT = (1+ICON_PADDING) * UI_SIZE * 1.5
LEVEL_BOX_WIDTH = (2.85 + HORIZONTAL_PADDING) * LEVEL_BOX_HEIGHT
LEVEL_TEXT_LOCATION = (UI_SPACING + 0.5 * LEVEL_BOX_WIDTH, HEIGHT - (3*UI_SPACING + EFFECT_BOX_HEIGHT + COIN_BOX_HEIGHT + LEVEL_BOX_HEIGHT * 0.5))

TEXT_BOX_CENTER_Y = ((HEIGHT - (3*UI_SPACING + EFFECT_BOX_HEIGHT + COIN_BOX_HEIGHT + LEVEL_BOX_HEIGHT)) + HEIGHT)/2
TEXT_BOX_WIDTH = 24 * UI_SIZE
TEXT_BOX_HEIGHT = 6 * UI_SIZE

BUTTON_SRC_SIZE = (46, 17)
MENU_BUTTON_SIZE = (lambda sz,sc: (sz[0]*sc, sz[1]*sc))(BUTTON_SRC_SIZE, UI_SIZE * 0.35)
MENU_BUTTON_SPACING = BUTTON_SRC_SIZE[1] * UI_SIZE * 0.45

MENU_BUTTON_SIZE_REDUCED = (lambda sz,sc: (sz[0]*sc, sz[1]*sc))(BUTTON_SRC_SIZE, UI_SIZE * 0.3)
MENU_BUTTON_SPACING_REDUCED = BUTTON_SRC_SIZE[1] * UI_SIZE * 0.4

SMALL_BUTTON_SRC_SIZE = (17,17)
SMALL_MENU_BUTTON_SIZE = (lambda sz,sc: (sz[0]*sc, sz[1]*sc))(SMALL_BUTTON_SRC_SIZE, UI_SIZE * 0.35)
SMALL_MENU_BUTTON_SPACING = SMALL_BUTTON_SRC_SIZE[1] * UI_SIZE * 0.45

UI_BUTTON_CENTER_X = WIDTH/2
UI_BUTTON_SIZE = (lambda sz,sc: (sz[0]*sc, sz[1]*sc))(BUTTON_SRC_SIZE, UI_SIZE * 0.155)

MENU_BLANK_SLICE = 0.25 * (HEIGHT - (3 * UI_BUTTON_SIZE[1] + 2 * MENU_BUTTON_SPACING))

MENU_Y_OFFSET = (HEIGHT/2) + 0.75 * MENU_BLANK_SLICE
MENU2_Y_OFFSET = (HEIGHT/2) + 1 * MENU_BLANK_SLICE

HELP_PAGE_LOCATION_COUNT = (4,3)

MENU_LEVEL_SELECTOR_BOX_SIZE = UI_SIZE * 12
MENU_LEVEL_SELECTOR_CENTER_Y = HEIGHT/2

#paths
resourcesPath = "resources\\"
mapsPath = resourcesPath + "maps\\"
buttonsPath = resourcesPath + "buttons\\"
tutorialPath = resourcesPath + "tutorial\\"
tilePath = resourcesPath + "tiles\\"
codePath = ""

#create fonts
minecraftFontPath = resourcesPath + r"Minecraft.ttf"
minecraftFont = Font(minecraftFontPath,TEXT_SIZE)
minecraftFontMenu = Font(minecraftFontPath,TEXT_SIZE * 3)
minecraftFontLevelSelection = Font(minecraftFontPath, int(TEXT_SIZE * 3.85))
minecraftFontNoEffect = Font(minecraftFontPath,NO_EFFECT_TEXT)
minecraftFontEffect = Font(minecraftFontPath,EFFECT_TEXT)
minecraftFontHelpMenu = Font(minecraftFontPath,HELP_TEXT_SIZE)

pixelTable = {
    "81b386": "empty",
    "595959": "rock",
    "7f3f0e": "dirt",
    "4b826f": "player",
    "d4af37": "coin",
    "96ffdc": "next_level",
    "00cc8e": "break_powerup",
    "ffefa3": "speed_powerup"
}

def convertTilemapToList(file_path):
    image = Image.open(file_path).convert('RGBA')
    width, height = image.size

    convertedMap = []
    coinCount = 0

    for y in range(height):
        row = []
        for x in range(width):
            r,g,b,a = image.getpixel((x, y))
            identifier = pixelTable['{:02x}{:02x}{:02x}'.format(r, g, b)]
            row.append(identifier)
            if identifier == "coin": coinCount += 1
        convertedMap.append(row)

    return convertedMap, coinCount

def createMaps():
    returnMapList = []
    returnMapCoins = []

    for eachMapPath in mapDictionary.keys():
        convertMap, coins = convertTilemapToList(mapsPath + eachMapPath)
        returnMapList.append(convertMap)
        match mapDictionary[eachMapPath]:
            case True:
                returnMapCoins.append(coins)
            case _:
                returnMapCoins.append(mapDictionary[eachMapPath])

    return returnMapList, returnMapCoins