import pygame 
from sys import exit
from settings import *
from outlineText import *
import inputManager as Inp

pygame.init()

class MenuLevel:
    def __init__(self, levelIdx, gameInstance, slideAnimation) -> None:
        self.gameInstance = gameInstance
        self.slideAnimation = slideAnimation
        self.levelIdx = levelIdx
        
        self.display_surface = pygame.display.get_surface()
        
        self.createButtons()
    
    def createButtons(self): pass
    def process(self): pass 
        
    def run(self):
        self.display_surface.fill((129, 212, 250))
        self.process()
    
class Button:
    def __init__(self, fileNamePrefix, pos, size, centerButton:bool = True) -> None:
        self.imagePaths = {
            "base": buttonsPath + fileNamePrefix + "_base.png",
            "hover": buttonsPath + fileNamePrefix + "_hover.png",
            "pressed": buttonsPath + fileNamePrefix + "_pressed.png"
        }
        
        self.images = {
            "base": pygame.transform.scale(pygame.image.load(self.imagePaths["base"]).convert_alpha(), size),
            "hover": pygame.transform.scale(pygame.image.load(self.imagePaths["hover"]).convert_alpha(), size),
            "pressed": pygame.transform.scale(pygame.image.load(self.imagePaths["pressed"]).convert_alpha(), size),
        }
        
        match centerButton:
            case True:
                self.imageRects = {
                    "base": self.images["base"].get_rect(center=pos),
                    "hover": self.images["hover"].get_rect(center=pos),
                    "pressed": self.images["pressed"].get_rect(center=pos)
                }
            case False:
                self.imageRects = {
                    "base": self.images["base"].get_rect(topleft=pos),
                    "hover": self.images["hover"].get_rect(topleft=pos),
                    "pressed": self.images["pressed"].get_rect(topleft=pos)
                }
            case _:
                raise Exception("centerButton must be a boolean.")

        self.currentImage = "base"
        self.display_surface = pygame.display.get_surface()
        
    def update(self):
        mouse_position = pygame.mouse.get_pos()
        pointer_rect = pygame.draw.rect(self.display_surface, (0,0,0), (mouse_position[0], mouse_position[1], 1,1))

        if pointer_rect.colliderect(self.imageRects["base"]):
            if Inp.userInput["MOUSE_HELD"]:
                self.currentImage = "pressed"
            else:
                self.currentImage = "hover"
            if Inp.userInput["MOUSE_UP"]:
                self.display_surface.blit(self.images[self.currentImage], self.imageRects[self.currentImage])
                return True
        else:
            self.currentImage = "base"
            
        self.display_surface.blit(self.images[self.currentImage], self.imageRects[self.currentImage])
        return False
    
class MainMenuLevel(MenuLevel):
    def __init__(self, levelIdx, gameInstance, slideAnimation) -> None:
        super().__init__(levelIdx, gameInstance, slideAnimation)

    def createButtons(self):
        self.startButton_1 = Button("start_button", (UI_BUTTON_CENTER_X, MENU_Y_OFFSET - MENU_BUTTON_SPACING), MENU_BUTTON_SIZE)
        self.helpButton_1 = Button("help_button", (UI_BUTTON_CENTER_X, MENU_Y_OFFSET), MENU_BUTTON_SIZE)
        self.quitButton_1 = Button("quit_button", (UI_BUTTON_CENTER_X, MENU_Y_OFFSET + MENU_BUTTON_SPACING), MENU_BUTTON_SIZE)
        
        self.startButton_2 = Button("start_button", (UI_BUTTON_CENTER_X, MENU2_Y_OFFSET - 1.5 * MENU_BUTTON_SPACING_REDUCED), MENU_BUTTON_SIZE_REDUCED)
        self.helpButton_2 = Button("help_button", (UI_BUTTON_CENTER_X, MENU2_Y_OFFSET - 0.5 * MENU_BUTTON_SPACING_REDUCED), MENU_BUTTON_SIZE_REDUCED)
        self.levelButton = Button("level_button", (UI_BUTTON_CENTER_X, MENU2_Y_OFFSET + 0.5 * MENU_BUTTON_SPACING_REDUCED), MENU_BUTTON_SIZE_REDUCED)
        self.quitButton_2 = Button("quit_button", (UI_BUTTON_CENTER_X, MENU2_Y_OFFSET + 1.5 * MENU_BUTTON_SPACING_REDUCED), MENU_BUTTON_SIZE_REDUCED)

    def process(self):
        self.menuTitle = textOutline(minecraftFontMenu, "Blobquest", (255,255,255), (1,1,1))
        self.display_surface.blit(self.menuTitle, self.menuTitle.get_rect(center=(UI_BUTTON_CENTER_X, 1.5 * MENU_BLANK_SLICE)))

        self.passedSeconds = round((pygame.time.get_ticks() - self.gameInstance.startTick)/1000)
        self.timePlayed_min, self.timePlayed_sec = divmod(self.passedSeconds, FPS)
        self.timePlayed_hr, self.timePlayed_min = divmod(self.timePlayed_min, FPS)
        
        self.formattedTimePlayed = f'{self.timePlayed_hr:d}:{self.timePlayed_min:02d}:{self.timePlayed_sec:02d}'
        
        self.timePlayedText = textOutline(minecraftFont, "Time Played: " + self.formattedTimePlayed, (255,255,255), (1,1,1))
        self.display_surface.blit(self.timePlayedText, self.timePlayedText.get_rect(bottomright=(WIDTH-UI_SPACING, HEIGHT-UI_SPACING)))

        if self.gameInstance.maxUnlockedLevel == 0:
            if self.startButton_1.update():
                self.slideAnimation.startAnim(1)
            if self.helpButton_1.update():
                self.slideAnimation.startAnim(-1)
            if self.quitButton_1.update():
                pygame.quit(); exit()
        else:
            if self.startButton_2.update():
                self.slideAnimation.startAnim(1)
                if self.gameInstance.maxUnlockedLevel <= self.gameInstance.currentLevel: self.gameInstance.maxUnlockedLevel += 1
            if self.helpButton_2.update():
                self.slideAnimation.startAnim(-1)
            if self.levelButton.update():
                self.slideAnimation.startAnim(-2)
            if self.quitButton_2.update():
                pygame.quit(); exit()
            
class HelpMenuLevel(MenuLevel):
    def __init__(self, levelIdx, gameInstance, slideAnimation) -> None:
        super().__init__(levelIdx, gameInstance, slideAnimation)
        self.drawPosArray()
        
    def createButtons(self):
        self.backButton = Button("back_button", (UI_SPACING,UI_SPACING), UI_BUTTON_SIZE, False)
        
    def drawPosArray(self):
        self.horizSpacing = WIDTH/(HELP_PAGE_LOCATION_COUNT[0] + 1)
        self.vertSpacing = HEIGHT/(HELP_PAGE_LOCATION_COUNT[1] + 1)
        
        self.uiItemCoords = []
        
        for self.x in range(1, HELP_PAGE_LOCATION_COUNT[0] + 1):
            self.row = []
            for self.y in range(1, HELP_PAGE_LOCATION_COUNT[1] + 1):
                self.row.append( (self.x * self.horizSpacing, self.y * self.vertSpacing) )
            self.uiItemCoords.append(self.row)
    
    def process(self):
        if self.backButton.update():
            self.slideAnimation.startAnim(0)
        
        # 0,0            
        self.WASDimage = pygame.image.load(tutorialPath + "WASD.png")
        self.WASDimage = pygame.transform.scale(self.WASDimage, (self.WASDimage.get_width() * 4,self.WASDimage.get_height() * 4)).convert_alpha()
        self.WASDiamgeRect = self.WASDimage.get_rect(center=self.uiItemCoords[0][0])
        self.display_surface.blit(self.WASDimage, self.WASDiamgeRect)
        
        # 1,0
        self.WASDimageText_1 = textOutline(minecraftFontHelpMenu, "Use W, A, S, D to move", (255,255,255), (1,1,1))
        self.WASDimageText_2 = textOutline(minecraftFontHelpMenu, "your character.", (255,255,255), (1,1,1))
        self.display_surface.blit(self.WASDimageText_1, self.WASDimageText_1.get_rect(center=(lambda p,o: (p[0], p[1]-(0.5*o) ))(self.uiItemCoords[1][0], HELP_TEXT_SIZE)))
        self.display_surface.blit(self.WASDimageText_2, self.WASDimageText_2.get_rect(center=(lambda p,o: (p[0], p[1]+(0.5*o) ))(self.uiItemCoords[1][0], HELP_TEXT_SIZE)))
        
        # 2,0
        self.breakDiagramScale = 1
        self.playerBreakImg_player = pygame.transform.scale(pygame.image.load(tilePath + "player-sprite.png"), (TILESIZE, TILESIZE)).convert_alpha()
        self.playerBreakImg_player = pygame.transform.scale(self.playerBreakImg_player, (self.playerBreakImg_player.get_width() * self.breakDiagramScale,self.playerBreakImg_player.get_height() * self.breakDiagramScale)).convert_alpha()
        
        self.playerBreakImg_dirt = pygame.transform.scale(pygame.image.load(tilePath + "dirt.png"), (TILESIZE, TILESIZE)).convert_alpha()
        self.playerBreakImg_dirt = pygame.transform.scale(self.playerBreakImg_dirt, (self.playerBreakImg_dirt.get_width() * self.breakDiagramScale,self.playerBreakImg_dirt.get_height() * self.breakDiagramScale)).convert_alpha()
        
        self.playerBreakImg_player_Rect = self.playerBreakImg_player.get_rect(center=((lambda p,o: (p[0]-(0.45*o), p[1]))(self.uiItemCoords[2][0], self.playerBreakImg_player.get_width() * self.breakDiagramScale)))
        self.playerBreakImg_dirt_Rect = self.playerBreakImg_dirt.get_rect(center=((lambda p,o: (p[0]+(0.45*o), p[1]))(self.uiItemCoords[2][0], self.playerBreakImg_player.get_width() * self.breakDiagramScale)))
        
        self.display_surface.blit(self.playerBreakImg_player, self.playerBreakImg_player_Rect)
        self.display_surface.blit(self.playerBreakImg_dirt, self.playerBreakImg_dirt_Rect)
        
        self.breakDiagramTimeText = minecraftFont.render("0.6", True, 'white')
        self.display_surface.blit(self.breakDiagramTimeText, self.breakDiagramTimeText.get_rect(center=( ((lambda p,o: (p[0]+(0.45*o), p[1]))(self.uiItemCoords[2][0], self.playerBreakImg_player.get_width() * self.breakDiagramScale))+ pygame.math.Vector2(0,3))))
        
        # 3,0
        self.breakDiagramText_1 = textOutline(minecraftFontHelpMenu, "Continuously walk into", (255,255,255), (1,1,1))
        self.breakDiagramText_2 = textOutline(minecraftFontHelpMenu, "dirt to break it.", (255,255,255), (1,1,1))
        self.display_surface.blit(self.breakDiagramText_1, self.breakDiagramText_1.get_rect(center=(lambda p,o: (p[0], p[1]-(0.5*o) ))(self.uiItemCoords[3][0], HELP_TEXT_SIZE)))
        self.display_surface.blit(self.breakDiagramText_2, self.breakDiagramText_2.get_rect(center=(lambda p,o: (p[0], p[1]+(0.5*o) ))(self.uiItemCoords[3][0], HELP_TEXT_SIZE)))
        
        # 0,1
        self.coinDiagramScale = 1
        self.coinDiagram_player = pygame.transform.scale(pygame.image.load(tilePath + "player-sprite.png"), (TILESIZE, TILESIZE)).convert_alpha()
        self.coinDiagram_player = pygame.transform.scale(self.coinDiagram_player, (self.coinDiagram_player.get_width() * self.coinDiagramScale,self.coinDiagram_player.get_height() * self.coinDiagramScale)).convert_alpha()
        
        self.coinDiagram_coin = pygame.transform.scale(pygame.image.load(tilePath + "coin.png"), (TILESIZE, TILESIZE)).convert_alpha()
        self.coinDiagram_coin = pygame.transform.scale(self.coinDiagram_coin, (self.coinDiagram_coin.get_width() * self.coinDiagramScale,self.coinDiagram_coin.get_height() * self.coinDiagramScale)).convert_alpha()
        
        self.coinDiagram_player_Rect = self.coinDiagram_player.get_rect(center=((lambda p,o: (p[0]-(0.45*o), p[1]))(self.uiItemCoords[0][1], self.coinDiagram_player.get_width() * self.coinDiagramScale)))
        self.coinDiagram_coin_Rect = self.coinDiagram_coin.get_rect(center=((lambda p,o: (p[0]+(0.45*o), p[1]))(self.uiItemCoords[0][1], self.coinDiagram_player.get_width() * self.coinDiagramScale)))
        
        self.display_surface.blit(self.coinDiagram_player, self.coinDiagram_player_Rect)
        self.display_surface.blit(self.coinDiagram_coin, self.coinDiagram_coin_Rect)
        
        # 1,1
        self.coinDiagram_playerText_1 = textOutline(minecraftFontHelpMenu, "Walk into coins", (255,255,255), (1,1,1))
        self.coinDiagram_playerText_2 = textOutline(minecraftFontHelpMenu, "to collect them.", (255,255,255), (1,1,1))
        self.display_surface.blit(self.coinDiagram_playerText_1, self.coinDiagram_playerText_1.get_rect(center=(lambda p,o: (p[0], p[1]-(0.5*o) ))(self.uiItemCoords[1][1], HELP_TEXT_SIZE)))
        self.display_surface.blit(self.coinDiagram_playerText_2, self.coinDiagram_playerText_2.get_rect(center=(lambda p,o: (p[0], p[1]+(0.5*o) ))(self.uiItemCoords[1][1], HELP_TEXT_SIZE)))
        
        # 2,1
        self.levelEndDiagramScale = 1
        self.levelEndDiagram_player = pygame.transform.scale(pygame.image.load(tilePath + "player-sprite.png"), (TILESIZE, TILESIZE)).convert_alpha()
        self.levelEndDiagram_player = pygame.transform.scale(self.levelEndDiagram_player, (self.levelEndDiagram_player.get_width() * self.levelEndDiagramScale,self.levelEndDiagram_player.get_height() * self.levelEndDiagramScale)).convert_alpha()
        
        self.levelEndDiagram_end = pygame.transform.scale(pygame.image.load(tilePath + "level-trophy.png"), (TILESIZE, TILESIZE)).convert_alpha()
        self.levelEndDiagram_end = pygame.transform.scale(self.levelEndDiagram_end, (self.levelEndDiagram_end.get_width() * self.levelEndDiagramScale,self.levelEndDiagram_end.get_height() * self.levelEndDiagramScale)).convert_alpha()
        
        self.levelEndDiagram_player_Rect = self.levelEndDiagram_player.get_rect(center=((lambda p,o: (p[0]-(0.45*o), p[1]))(self.uiItemCoords[2][1], self.levelEndDiagram_player.get_width() * self.levelEndDiagramScale)))
        self.levelEndDiagram_end_Rect = self.levelEndDiagram_end.get_rect(center=((lambda p,o: (p[0]+(0.45*o), p[1]))(self.uiItemCoords[2][1], self.levelEndDiagram_end.get_width() * self.levelEndDiagramScale)))
        
        self.display_surface.blit(self.levelEndDiagram_player, self.levelEndDiagram_player_Rect)
        self.display_surface.blit(self.levelEndDiagram_end, self.levelEndDiagram_end_Rect)
        
        # 3,1
        self.levelEndDiagramText_1 = textOutline(minecraftFont, "If you have enough coins,", (255,255,255), (1,1,1))
        self.levelEndDiagramText_2 = textOutline(minecraftFont, "this takes you to the next level.", (255,255,255), (1,1,1))
        self.display_surface.blit(self.levelEndDiagramText_1, self.levelEndDiagramText_1.get_rect(center=(lambda p,o: (p[0], p[1]-(0.5*o) ))(self.uiItemCoords[3][1], TEXT_SIZE)))
        self.display_surface.blit(self.levelEndDiagramText_2, self.levelEndDiagramText_2.get_rect(center=(lambda p,o: (p[0], p[1]+(0.5*o) ))(self.uiItemCoords[3][1], TEXT_SIZE)))
        
        # 0,2
        self.speedPowerupScale = 1.45
        self.speedPowerupImage = pygame.transform.scale(pygame.image.load(tilePath + "speed-powerup.png"), (TILESIZE, TILESIZE)).convert_alpha()
        self.speedPowerupImage = pygame.transform.scale(self.speedPowerupImage, (self.speedPowerupImage.get_width() * self.speedPowerupScale,self.speedPowerupImage.get_height() * self.speedPowerupScale)).convert_alpha()
        
        self.speedPowerupImageRect = self.speedPowerupImage.get_rect(center=self.uiItemCoords[0][2])
        
        self.display_surface.blit(self.speedPowerupImage, self.speedPowerupImageRect)
        
        # 1,2
        self.speedPowerupText_1 = textOutline(minecraftFontHelpMenu, "Collect speed powerups", (255,255,255), (1,1,1))
        self.speedPowerupText_2 = textOutline(minecraftFontHelpMenu, "to move faster.", (255,255,255), (1,1,1))
        self.display_surface.blit(self.speedPowerupText_1, self.speedPowerupText_1.get_rect(center=(lambda p,o: (p[0], p[1]-(0.5*o) ))(self.uiItemCoords[1][2], HELP_TEXT_SIZE)))
        self.display_surface.blit(self.speedPowerupText_2, self.speedPowerupText_2.get_rect(center=(lambda p,o: (p[0], p[1]+(0.5*o) ))(self.uiItemCoords[1][2], HELP_TEXT_SIZE)))
        
        # 2,2
        self.breakPowerupScale = 1.45
        self.breakPowerupImage = pygame.transform.scale(pygame.image.load(tilePath + "break-powerup.png"), (TILESIZE, TILESIZE)).convert_alpha()
        self.breakPowerupImage = pygame.transform.scale(self.breakPowerupImage, (self.breakPowerupImage.get_width() * self.breakPowerupScale,self.breakPowerupImage.get_height() * self.breakPowerupScale)).convert_alpha()
        
        self.breakPowerupImageRect = self.breakPowerupImage.get_rect(center=self.uiItemCoords[2][2])
        
        self.display_surface.blit(self.breakPowerupImage, self.breakPowerupImageRect)
        
        # 3,2
        self.breakPowerupText_1 = textOutline(minecraftFontHelpMenu, "Collect break powerups", (255,255,255), (1,1,1))
        self.breakPowerupText_2 = textOutline(minecraftFontHelpMenu, "to break dirt faster.", (255,255,255), (1,1,1))
        self.display_surface.blit(self.breakPowerupText_1, self.breakPowerupText_1.get_rect(center=(lambda p,o: (p[0], p[1]-(0.5*o) ))(self.uiItemCoords[3][2], HELP_TEXT_SIZE)))
        self.display_surface.blit(self.breakPowerupText_2, self.breakPowerupText_2.get_rect(center=(lambda p,o: (p[0], p[1]+(0.5*o) ))(self.uiItemCoords[3][2], HELP_TEXT_SIZE)))

class LevelMenuLevel(MenuLevel):
    def __init__(self, levelIdx, gameInstance, slideAnimation) -> None:
        super().__init__(levelIdx, gameInstance, slideAnimation)
        self.selectionNum = 1

    def createButtons(self):
        self.backButton = Button("back_button", (UI_SPACING, UI_SPACING), UI_BUTTON_SIZE, False)
        self.upButton = Button("up_button", (WIDTH/2 - 1.5 * SMALL_MENU_BUTTON_SPACING, MENU_LEVEL_SELECTOR_CENTER_Y), SMALL_MENU_BUTTON_SIZE)
        self.downButton = Button("down_button", (WIDTH/2 + 1.5 * SMALL_MENU_BUTTON_SPACING, MENU_LEVEL_SELECTOR_CENTER_Y), SMALL_MENU_BUTTON_SIZE)
        self.goButton = Button("go_button", (WIDTH/2, MENU_LEVEL_SELECTOR_CENTER_Y + 1.5 * SMALL_MENU_BUTTON_SPACING), SMALL_MENU_BUTTON_SIZE)
        self.resetAllButton = Button("resetAll_button", (WIDTH - UI_SPACING - UI_BUTTON_SIZE[0], HEIGHT - UI_SPACING - UI_BUTTON_SIZE[1]), UI_BUTTON_SIZE, False)

    def process(self):
        bg_rect = pygame.Rect(0,0, MENU_LEVEL_SELECTOR_BOX_SIZE,MENU_LEVEL_SELECTOR_BOX_SIZE)
        bg_rect.center = (WIDTH/2, MENU_LEVEL_SELECTOR_CENTER_Y)
        pygame.draw.rect(self.display_surface, FILL_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, BORDER_COLOR, bg_rect, int(UI_SIZE * 0.5))

        self.menuTitle = textOutline(minecraftFontMenu, "Level Selection", (255,255,255), (1,1,1))
        self.display_surface.blit(self.menuTitle, self.menuTitle.get_rect(center=(UI_BUTTON_CENTER_X, 1.5 * MENU_BLANK_SLICE)))
        
        self.selectionNumber = textOutline(minecraftFontLevelSelection, str(self.selectionNum), (255,255,255), (255, 211, 65))
        self.display_surface.blit(self.selectionNumber, self.selectionNumber.get_rect(center=bg_rect.center))
        
        self.levelRange = [1,self.gameInstance.maxUnlockedLevel]

        if self.backButton.update():
            self.slideAnimation.startAnim(0)
        if self.upButton.update():
            if self.selectionNum + 1 <= self.levelRange[1]: self.selectionNum += 1
        if self.downButton.update():
            if self.selectionNum - 1 >= self.levelRange[0]: self.selectionNum -= 1
        if self.goButton.update():
            self.slideAnimation.startAnim(self.selectionNum)
        if self.resetAllButton.update():
            self.gameInstance.resetAllCall = True