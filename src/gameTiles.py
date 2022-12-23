import pygame
from settings import *


class GameTile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.transform.scale(pygame.image.load(self.imagePath), (TILESIZE, TILESIZE)).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)
        self.display_surface = pygame.display.get_surface()
     
    def drawInfoText(self, player, text):
        width, height = self.display_surface.get_size()
        half_width = width // 2
        half_height = height // 2
        offset = pygame.math.Vector2()
        offset.x = player.rect.centerx - half_width
        offset.y = player.rect.centery - half_height
        offset_pos = self.rect.center - offset + pygame.math.Vector2(0, 3)
        infoText = minecraftFont.render(text, True, 'white')
        self.display_surface.blit(infoText, infoText.get_rect(center=offset_pos))
    

class RockTile(GameTile):
    def __init__(self, pos, groups):
        self.imagePath = tilePath + 'rock.png'
        super().__init__(pos, groups)


class DirtTile(GameTile):
    def __init__(self, pos, groups):
        self.imagePath = tilePath + 'dirt.png'
        super().__init__(pos, groups)
        
        self.healthSeconds = 1.5

    def onPlayerCollide(self, player):
        if self.healthSeconds <= 0: self.kill()
        
        if self.healthSeconds > 0:
            self.healthSeconds -= (1/FPS) * player.BREAK_SPEED_MULTIPLIER
        else: self.healthSeconds = 0
        
        self.scaledHealthSeconds = self.healthSeconds / player.BREAK_SPEED_MULTIPLIER
        super().drawInfoText(player, str(round(self.scaledHealthSeconds, 1)))


class Coin(GameTile):
    def __init__(self, pos, groups):
        self.imagePath = tilePath + 'coin.png'
        super().__init__(pos, groups)
     
    def onPlayerCollide(self, player):
        player.coinCount += 1; self.kill()


class Powerup(GameTile):
    def __init__(self, pos, groups, effectMult, effectDuration):
        self.powerup = [effectMult, effectDuration]
        super().__init__(pos, groups)
    
    def onPlayerCollide(self, player):
        match self.type:
            case "speed": player.speedPowerup = self.powerup
            case "break": player.breakPowerup = self.powerup
        self.kill()


class SpeedPowerup(Powerup):
    def __init__(self, pos, groups, effectMult, effectDuration):
        self.imagePath = tilePath + 'speed-powerup.png'
        self.type = "speed"
        super().__init__(pos, groups, effectMult, effectDuration)

     
class BreakPowerup(Powerup):
    def __init__(self, pos, groups, effectMult, effectDuration):
        self.imagePath = tilePath + 'break-powerup.png'
        self.type = "break"
        super().__init__(pos, groups, effectMult, effectDuration)


class LevelEndTile(GameTile):
    def __init__(self, pos, groups, slideAnimation, sendLevel, coinRequirement):
        self.imagePath = tilePath + 'level-trophy.png'
        self.slideAnimation = slideAnimation
        self.sendLevel = sendLevel
        self.coinRequirement = coinRequirement
        super().__init__(pos, groups)
    
    def onPlayerCollide(self, player):
        if player.coinCount >= self.coinRequirement:
            self.slideAnimation.startAnim(self.sendLevel)
        else:         
            self.coinsPlural  = "coin" if self.coinRequirement - player.coinCount == 1 else "coins"
            player.levelUI.startDrawTextBox([f"You need {self.coinRequirement-player.coinCount} more " + self.coinsPlural, "to continue."], 0.5)