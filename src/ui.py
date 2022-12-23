import pygame
from settings import *
from outlineText import *
from menu import Button

class UserInterface():
    def __init__(self, level, slideAnimation, coinRequirement, levelNum):
        self.display_surface = pygame.display.get_surface()
        self.powerupList = []
        self.coinCount = 0
        self.level = level
        self.slideAnimation = slideAnimation
        self.coinRequirement = coinRequirement
        self.levelNum = levelNum
        
        self.displayText = None
        self.textBoxTimeRemaining = 0
        
        self.menuButton = Button("menu_button", (UI_SPACING,UI_SPACING), UI_BUTTON_SIZE, False)
        self.resetButton = Button("reset_button", (WIDTH - UI_SPACING - UI_BUTTON_SIZE[0], HEIGHT - UI_SPACING - UI_BUTTON_SIZE[1]), UI_BUTTON_SIZE, False)
        
    def drawPowerupBox(self):
        bg_rect = pygame.Rect(UI_SPACING, (HEIGHT - UI_SPACING - EFFECT_BOX_HEIGHT), EFFECT_BOX_WIDTH, EFFECT_BOX_HEIGHT)
        pygame.draw.rect(self.display_surface,FILL_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface,BORDER_COLOR,bg_rect,3)
        
        self.drawPowerups()
    
    def drawPowerups(self):
        match len(self.powerupList):
            case 0:
                self.noPowerupText_1 = minecraftFontNoEffect.render("No active", True, 'white')
                self.noPowerupText_2 = minecraftFontNoEffect.render("powerups.", True, 'white')
                self.noPowerupTextPos = (UI_SPACING + EFFECT_BOX_WIDTH * 0.5, HEIGHT - UI_SPACING - EFFECT_BOX_HEIGHT * 0.5)
                self.display_surface.blit(self.noPowerupText_1, self.noPowerupText_1.get_rect(center=((lambda p,o: (p[0], p[1]-(0.5*o) ))(self.noPowerupTextPos, NO_EFFECT_TEXT))))
                self.display_surface.blit(self.noPowerupText_2, self.noPowerupText_2.get_rect(center=((lambda p,o: (p[0], p[1]+(0.5*o) ))(self.noPowerupTextPos, NO_EFFECT_TEXT))))
            case 1:
                self.powerup1 = self.powerupList[0]
                match self.powerup1.effectType:
                    case "speed":
                        self.powerup1.displayImage = tilePath + 'speed-powerup.png'
                    case "break":
                        self.powerup1.displayImage = tilePath + 'break-powerup.png'
                self.display1 = pygame.transform.scale(pygame.image.load(self.powerup1.displayImage), (ICON_SIZE,ICON_SIZE)).convert_alpha()
                self.displayRect1 = self.display1.get_rect(center=ONE_POWERUP_ACTIVE)
                self.display_surface.blit(self.display1, self.displayRect1)
                
                self.timerText = textOutline(minecraftFontEffect, str(int(round(self.powerup1.effectDuration, 0))), (255,255,255),(255,0,0))
                self.display_surface.blit(self.timerText, self.timerText.get_rect(center=(  (lambda p: (p[0] + 16, p[1] + 16))(ONE_POWERUP_ACTIVE)  )))
            case 2:
                self.powerup1 = self.powerupList[0]
                self.powerup2 = self.powerupList[1]
                
                match self.powerup1.effectType:
                    case "speed":
                        self.powerup1.displayImage = tilePath + 'speed-powerup.png'
                    case "break":
                        self.powerup1.displayImage = tilePath + 'break-powerup.png'

                match self.powerup2.effectType:
                    case "speed":
                        self.powerup2.displayImage = tilePath + 'speed-powerup.png'
                    case "break":
                        self.powerup2.displayImage = tilePath + 'break-powerup.png'

                self.display1 = pygame.transform.scale(pygame.image.load(self.powerup1.displayImage), (ICON_SIZE,ICON_SIZE)).convert_alpha()
                self.displayRect1 = self.display1.get_rect(center=TWO_POWERUP_ACTIVE_1)
                self.display_surface.blit(self.display1, self.displayRect1)
                
                self.display2 = pygame.transform.scale(pygame.image.load(self.powerup2.displayImage), (ICON_SIZE,ICON_SIZE)).convert_alpha()
                self.displayRect2 = self.display1.get_rect(center=TWO_POWERUP_ACTIVE_2)
                self.display_surface.blit(self.display2, self.displayRect2)
                
                self.timerText1 = textOutline(minecraftFontEffect, str(int(round(self.powerup1.effectDuration, 0))), (255,255,255),(255,0,0))
                self.display_surface.blit(self.timerText1, self.timerText1.get_rect(center=(  (lambda p: (p[0] + 16, p[1] + 16))(TWO_POWERUP_ACTIVE_1)  )))
                
                self.timerText2 = textOutline(minecraftFontEffect, str(int(round(self.powerup2.effectDuration, 0))), (255,255,255),(255,0,0))
                self.display_surface.blit(self.timerText2, self.timerText2.get_rect(center=(  (lambda p: (p[0] + 16, p[1] + 16))(TWO_POWERUP_ACTIVE_2)  )))
            case other:
                raise ValueError(f"Player can have a max of 2 powerups, yet {len(self.powerupList)} were given")
        
        self.powerupList.clear()

    def recievePowerup(self, effectType, effectMult, effectDuration):
        powerup = PowerupDisplay(effectType, effectMult, effectDuration)
        self.powerupList.append(powerup)    

    def drawCoinsBox(self):
        self.COIN_BOX_WIDTH_MODIFIED = COIN_BOX_WIDTH * 1.075 if len(str(self.coinRequirement)) > 1 else COIN_BOX_WIDTH
        bg_rect = pygame.Rect(UI_SPACING, (HEIGHT - (2*UI_SPACING + EFFECT_BOX_HEIGHT + COIN_BOX_HEIGHT)), self.COIN_BOX_WIDTH_MODIFIED,COIN_BOX_HEIGHT)
        pygame.draw.rect(self.display_surface, FILL_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, BORDER_COLOR, bg_rect, 3)
        
        self.drawCoins()
        
    def drawCoins(self):
        self.coinIcon = pygame.transform.scale(pygame.image.load(tilePath + "coin.png"), (UI_COIN_SIZE,UI_COIN_SIZE)).convert_alpha()
        self.coinIconRect = self.coinIcon.get_rect(center= COIN_ICON_LOCATION)
        self.display_surface.blit(self.coinIcon, self.coinIconRect)

        color = (120,245,120) if self.coinCount >= self.coinRequirement else "white"

        self.uiCoinCount = minecraftFontNoEffect.render(str(self.coinCount) + "/" + str(self.coinRequirement), True, color)
        self.display_surface.blit(self.uiCoinCount, self.uiCoinCount.get_rect(midleft=COIN_TEXT_LOCATION))

    def recieveCoins(self, coinCount):
        self.coinCount = coinCount

    def drawLevelBox(self):
        bg_rect = pygame.Rect(UI_SPACING, (HEIGHT - (3*UI_SPACING + EFFECT_BOX_HEIGHT + COIN_BOX_HEIGHT + LEVEL_BOX_HEIGHT)), LEVEL_BOX_WIDTH, LEVEL_BOX_HEIGHT)
        pygame.draw.rect(self.display_surface, FILL_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, BORDER_COLOR, bg_rect, 3)
        
        self.uiLevelNum = minecraftFontNoEffect.render("Level " + str(self.levelNum), True, 'white')
        self.display_surface.blit(self.uiLevelNum, self.uiLevelNum.get_rect(center=LEVEL_TEXT_LOCATION))

    def drawTextBox(self):
        if type(self.displayText) != list:
            raise TypeError(f"{type(self.displayText)} was passed into text box, instead of list")
        
        bg_rect = pygame.Rect(0,0,TEXT_BOX_WIDTH,TEXT_BOX_HEIGHT)
        bg_rect.center = (WIDTH/2, TEXT_BOX_CENTER_Y)
        
        pygame.draw.rect(self.display_surface, FILL_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, BORDER_COLOR, bg_rect, 3)
        
        match len(self.displayText):
            case 1:
                self.textBoxText_1 = minecraftFont.render(str(self.displayText[0]), True, "white")
                self.display_surface.blit(self.textBoxText_1, self.textBoxText_1.get_rect(center=(WIDTH/2, TEXT_BOX_CENTER_Y)))
            case 2:
                self.textBoxText_1 = minecraftFont.render(str(self.displayText[0]), True, "white")
                self.textBoxText_2 = minecraftFont.render(str(self.displayText[1]), True, "white")
                self.display_surface.blit(self.textBoxText_1, self.textBoxText_1.get_rect(center=((lambda p,o: (p[0], p[1]-(0.5*o) ))((WIDTH/2, TEXT_BOX_CENTER_Y), TEXT_SIZE))))
                self.display_surface.blit(self.textBoxText_2, self.textBoxText_2.get_rect(center=((lambda p,o: (p[0], p[1]+(0.5*o) ))((WIDTH/2, TEXT_BOX_CENTER_Y), TEXT_SIZE))))
            case _:
                raise Exception(f"{len(self.displayText)} lines of text were passed into the textbox, which is not 1-2.")
        
    def startDrawTextBox(self, displayText, holdTime):
        self.displayText = displayText
        self.textBoxTimeRemaining = holdTime
        
    def drawUI(self):
        self.drawPowerupBox()
        self.drawCoinsBox()
        self.drawLevelBox()

        if self.menuButton.update():
            self.slideAnimation.startAnim(0)
        
        if self.resetButton.update():
            self.slideAnimation.startAnim(self.levelNum, resetLevel = True)
        
        if self.textBoxTimeRemaining > 0:
            self.drawTextBox()
            self.textBoxTimeRemaining -= 1/FPS
            if self.textBoxTimeRemaining < 0: self.textBoxTimeRemaining = 0

class PowerupDisplay():
    def __init__(self, effectType, effectMult, effectDuration):
        self.effectType = effectType
        self.effectMult = effectMult
        self.effectDuration = effectDuration
        self.displayImage = None

class SlideAnimation():
    def __init__(self, gameInstance, animSpeed = 75):
        self.isActive = False
        self.isAnimating = False
        self.wipeOffset = WIDTH
        self.nextLevel = None
        self.animSpeed = animSpeed
        self.gameInstance = gameInstance
        self.display_surface = pygame.display.get_surface()
        self.callReset = False
    
    def startAnim(self, animateTo, updateMaxLevel = True, resetLevel = False):
        if self.isActive: return
        
        self.isActive = True
        self.isAnimating = True
        self.nextLevel = animateTo
        self.updateMaxLevel = updateMaxLevel
        self.resetLevel = resetLevel
        
        
    def animate(self):
        if not self.wipeOffset <= -WIDTH:
            self.wipeOffset -= self.animSpeed
            pygame.draw.rect(self.display_surface, (0,0,0), (self.wipeOffset, 0, WIDTH, HEIGHT))
            if self.wipeOffset <= 0:
                self.gameInstance.currentLevel = self.nextLevel
                if self.resetLevel:
                    if self.callReset:
                        self.resetLevel = False
                    self.callReset = not self.callReset

        else:
            self.isActive = False
            self.isAnimating = False
            self.wipeOffset = WIDTH
            if self.updateMaxLevel:
                if self.nextLevel > self.gameInstance.maxUnlockedLevel:
                    self.gameInstance.maxUnlockedLevel = self.nextLevel
            
    def update(self):
        if self.isAnimating:
            self.animate()