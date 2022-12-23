import pygame
import inputManager as Inp
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, dynamic_sprites, gameInstance, levelUI):
        super().__init__(groups)
        
        self.gameInstance = gameInstance
        self.levelUI = levelUI
        
        self.image = pygame.transform.scale(pygame.image.load(tilePath + "player-sprite.png"), (TILESIZE, TILESIZE)).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.facing = 1

        self.inputVector = pygame.math.Vector2()
        self.movementVel = pygame.math.Vector2()
        
        self.BASE_MAX_SPEED = 12
        self.MAX_SPEED = self.BASE_MAX_SPEED
        self.ACCELERATION = 8.0
        self.FRICTION = 1.25
        self.BREAK_SPEED_MULTIPLIER = 1

        self.speedPowerup = []
        self.breakPowerup = []
        
        self.coinCount = 0
        
        self.obstacle_sprites = obstacle_sprites
        self.dynamic_sprites = dynamic_sprites

    def process(self):
        self.inputVector = pygame.math.Vector2(0, 0)
        self.inputVector.x = Inp.userInput["RIGHT"] - Inp.userInput["LEFT"]
        self.inputVector.y = Inp.userInput["DOWN"] - Inp.userInput["UP"]
        
        if (lambda x: 1 if x > 0 else -1 if x < 0 else x)(self.inputVector.x) != self.facing and self.inputVector.x != 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing *= -1
        
        if self.inputVector.magnitude() != 0: self.inputVector = self.inputVector.normalize()

        if self.inputVector != pygame.math.Vector2():
            self.movementVel += self.inputVector * self.ACCELERATION
            self.movementVel = pygame.math.Vector2.clamp_magnitude(self.movementVel, 0, self.MAX_SPEED) 
        else:
            self.movementVel = self.movementVel.move_towards(pygame.math.Vector2(), self.FRICTION)
        
        self.updateSpeedMult()
        self.updateBreakMult()
        self.levelUI.recieveCoins(self.coinCount)
        
        self.move_and_collide()

    def move_and_collide(self):
        self.hitbox.x += self.movementVel.x
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.movementVel.x > 0: 
                    self.hitbox.right = sprite.hitbox.left
                if self.movementVel.x < 0: 
                    self.hitbox.left = sprite.hitbox.right

                if(self.dynamic_sprites in sprite.groups()): sprite.onPlayerCollide(self)
        self.hitbox.y += self.movementVel.y
        for sprite in self.obstacle_sprites:

            if sprite.hitbox.colliderect(self.hitbox):
                if self.movementVel.y > 0: 
                    self.hitbox.bottom = sprite.hitbox.top
                if self.movementVel.y < 0:
                    self.hitbox.top = sprite.hitbox.bottom
                if self.dynamic_sprites in sprite.groups(): sprite.onPlayerCollide(self)
        self.rect.center = self.hitbox.center
    
    def updateSpeedMult(self):
        if self.speedPowerup == []: self.MAX_SPEED = self.BASE_MAX_SPEED; return
        
        if self.speedPowerup[1] > 0:
            self.levelUI.recievePowerup("speed", self.speedPowerup[0], self.speedPowerup[1])
            self.MAX_SPEED = self.BASE_MAX_SPEED * self.speedPowerup[0]
            self.speedPowerup[1] -= 1/FPS
            if self.speedPowerup[1] < 0: self.speedPowerup[1] = 0
        else:
            self.speedPowerup = []
            self.MAX_SPEED = self.BASE_MAX_SPEED
    
    def updateBreakMult(self):
        if self.breakPowerup == []: self.BREAK_SPEED_MULTIPLIER = 1; return
       
        if self.breakPowerup[1] > 0:
            self.levelUI.recievePowerup("break", self.breakPowerup[0], self.breakPowerup[1])
            self.BREAK_SPEED_MULTIPLIER = self.breakPowerup[0]
            self.breakPowerup[1] -= 1/FPS
            if self.breakPowerup[1] < 0: self.breakPowerup[1] = 0
        else:
            self.breakPowerup = []
            self.BREAK_SPEED_MULTIPLIER = 1
            
    def update(self):
        self.process()
