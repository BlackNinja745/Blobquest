import pygame
import sys

pygame.init()

userInput = {
    "UP": False,
    "DOWN": False,
    "LEFT": False,
    "RIGHT": False,
    "USE": False,
    "MOUSE_UP": False,
    "MOUSE_DOWN": False,
    "MOUSE_HELD": False
}

keys_to_inputs = {
    pygame.K_w: "UP",
    pygame.K_UP: "UP",
    pygame.K_s: "DOWN",
    pygame.K_DOWN: "DOWN",
    pygame.K_a: "LEFT",
    pygame.K_LEFT: "LEFT",
    pygame.K_d: "RIGHT",
    pygame.K_RIGHT: "RIGHT",
    pygame.K_e: "USE",
    pygame.K_SPACE: "USE"
}

mouseClicked = False

def updateInputs():
    global userInput, mouseClicked, keys_to_inputs
    
    userInput["MOUSE_DOWN"] = False
    userInput["MOUSE_UP"] = False
    getMouse = pygame.mouse.get_pressed()
    if getMouse[0]:
        userInput["MOUSE_HELD"] = True
        if not mouseClicked:
            userInput["MOUSE_DOWN"] = True
            mouseClicked = True
    else:
        userInput["MOUSE_HELD"] = False
        if mouseClicked:
            userInput["MOUSE_UP"] = True
        mouseClicked = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in keys_to_inputs:
                userInput[keys_to_inputs[event.key]] = True
        elif event.type == pygame.KEYUP:
            if event.key in keys_to_inputs:
                userInput[keys_to_inputs[event.key]] = False
