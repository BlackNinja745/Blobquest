import pygame 
from settings import *
from gameTiles import *
from player import Player
from ui import UserInterface as UI

class PlayableLevel:
	def __init__(self, levelIdx, gameInstance, slideAnimation, levelMap, coinRequirement):
		self.gameInstance = gameInstance
		self.slideAnimation = slideAnimation
		self.levelIdx = levelIdx
		self.coinRequirement = coinRequirement
		self.levelMap = levelMap

		self.ui = UI(self, self.slideAnimation, self.coinRequirement, self.levelIdx)

		self.display_surface = pygame.display.get_surface()

		self.visible_sprites = YSortCamGroup()
		self.dynamic_sprites = DynamicYSortCamGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		self.create_map()

	def create_map(self):
		for row_index,row in enumerate(self.levelMap):
			for col_index, col in enumerate(row):
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				match col:
					case 'rock':
						RockTile((x, y), [self.visible_sprites, self.obstacle_sprites])
					case 'dirt':
						DirtTile((x, y), [self.visible_sprites, self.dynamic_sprites, self.obstacle_sprites])
					case "next_level":
						LevelEndTile((x, y), [self.visible_sprites, self.dynamic_sprites, self.obstacle_sprites], self.slideAnimation, self.levelIdx + 1, self.coinRequirement)
					case "speed_powerup":
						SpeedPowerup((x, y), [self.visible_sprites, self.dynamic_sprites, self.obstacle_sprites], 1.2, 10)
					case "break_powerup":
						BreakPowerup((x, y), [self.visible_sprites, self.dynamic_sprites, self.obstacle_sprites], 3, 15)
					case "coin":
						Coin((x, y), [self.visible_sprites, self.dynamic_sprites, self.obstacle_sprites])
					case 'player':
						self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites, self.dynamic_sprites, self.gameInstance, self.ui)

	def resetLevel(self):
		for sprite in self.visible_sprites:
			sprite.kill()
		self.create_map()

	def run(self):
		self.display_surface.fill((125,179,134))
     
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		self.ui.drawUI()

class YSortCamGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()

		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

	def custom_draw(self,player):
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)


class DynamicYSortCamGroup(YSortCamGroup):
	pass
