import pygame
from settings import *
from level import PlayableLevel
from menu import *
import inputManager as Inp
from ui import SlideAnimation


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption('Blobquest')
        pygame.display.set_icon(pygame.transform.scale(pygame.image.load(tilePath + "player-sprite.png"), (TILESIZE, TILESIZE)).convert_alpha())
        
        self.gameClock = pygame.time.Clock()
        self.gameInstance = GameInstance()
        self.slideAnimation = SlideAnimation(self.gameInstance)
        self.mapList, self.mapCoins = createMaps()
        
        self.levelDictionary = {
            -2: LevelMenuLevel(-2, self.gameInstance, self.slideAnimation),
            -1: HelpMenuLevel(-1, self.gameInstance, self.slideAnimation),
            0: MainMenuLevel(0, self.gameInstance, self.slideAnimation),
            **{i: PlayableLevel(i, self.gameInstance, self.slideAnimation, map, coins) for i, (map, coins) in enumerate(zip(self.mapList, self.mapCoins), start=1)}
        }


    def runGame(self):
        while True:
            self.activeLevel = self.levelDictionary.get(self.gameInstance.currentLevel, None)

            if self.activeLevel is not None:
                self.activeLevel.run()
            else:
                print(f"Level {self.gameInstance.currentLevel} was not found, so sending to menu.")
                self.slideAnimation.nextLevel = 0

            if self.slideAnimation.callReset and self.slideAnimation.nextLevel == self.gameInstance.currentLevel:
                self.activeLevel.resetLevel()

            if self.gameInstance.resetAllCall:
                self.gameInstance.resetAllCall = False

                for level in self.levelDictionary:
                    if level <= 0: continue
                    self.levelDictionary[level].resetLevel()

            self.gameClock.tick(FPS)
            Inp.updateInputs()
            self.slideAnimation.update()
            pygame.display.update()


class GameInstance:
    def __init__(self):
        self.currentLevel = 0
        self.maxUnlockedLevel = 0
        self.startTick = pygame.time.get_ticks()
        self.resetAllCall = False


if __name__ == '__main__':
    Game().runGame()
