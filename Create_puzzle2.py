import numpy as np
import pygame
from pygame import gfxdraw
import math
import time

pygame.init()

MAX_X = 300
MAX_Y = 200

# Building the obstacle space in pygame

pygame.init()

white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (0,255,255)

gameDisplay = pygame.display.set_mode((MAX_X,MAX_Y))
gameDisplay.fill(black)

pygame.draw.circle(gameDisplay, red, (225,50), 25)
#Drawing Polygon
pygame.draw.polygon(gameDisplay, red, ((25,15),(75,15),(100,50),(75,80),(50,50),(20,80)))
#Drawing Rectangle
pygame.draw.polygon(gameDisplay, red, ((95,170),(30,132.5),(35,124),(100,161.4)))
#Drawing Rhombus
pygame.draw.polygon(gameDisplay, red, ((200,175),(225,160),(250,175),(225,190)))

pygame.draw.ellipse(gameDisplay, red, (110, 80, 80, 40))

###########################################################################################


def updateTheStep(position, color, RADIUS):
    for inst in pygame.event.get():
        if inst.type == pygame.QUIT:
            pygame.quit()
            quit()
    if RADIUS == None or RADIUS == 0:
        pygame.gfxdraw.pixel(puzzleMap, position[0], position[1], color)
    else:
        pygame.draw.circle(puzzleMap, color, (position[0],position[1]), RADIUS)
    pygame.display.update()


def showPath(pathList, RADIUS):
	for step in pathList:
		if RADIUS == None or RADIUS == 0:
			pygame.gfxdraw.pixel(puzzleMap, step[0], step[1], pathColor)
		else:
			pygame.draw.circle(puzzleMap, pathColor, (step[0], step[1]), RADIUS)
		pygame.display.update()

    
#################################################################################################################################################
# Function to Check for Obstacles
def isValidStep(point,pad):  # def obstacleCheck_rigid
    x = point[0]
    y = point[1]
    theta = point[2]
    #Shift for rhombus
    d1=pad*math.sqrt((0.6)**2+1)
    d2=pad*math.sqrt((0.6)**2+1)
    d3=pad*math.sqrt((-0.6)**2+1)
    d4=pad*math.sqrt((-0.6)**2+1)

    #shift for rectangle

    d5=pad*math.sqrt((1.72)**2+1)
    d6=pad*math.sqrt((1.7)**2+1)
    d7=pad*math.sqrt((-0.577)**2+1)
    d8=pad*math.sqrt((-0.575)**2+1)

    #shift for Polygon part1

    d9=pad*math.sqrt((13)**2+1)
    d10=pad*math.sqrt((1)**2+1)

    #shift for Polygon part2
    d11=pad*math.sqrt((-1.4)**2+1)
    d12=pad*math.sqrt((1.2)**2+1)
    d13=pad*math.sqrt((-1.2)**2+1)

    #partition
    d14=pad*math.sqrt((1.4)**2+1)
    d15=pad*math.sqrt((1.4)**2+1)

    flag = False
    if (x < pad) or (x > 300-pad) or (y < pad) or (y > 200-pad):
        flag = True

    #check if point is in circle shaped obstacle or not

    if ((x - 225)**2 + (y-50)**2 - (25+pad)**2) <= 0:
        flag = True

    #check if point is in rhombus shaped obstacle or not

    if (0.6 * x + y - 325 - d1 <= 0) and (0.6 * x + y - 295 + d2 >= 0) and (y - 0.6 * x - 55 - d3 <= 0) and (y - 0.6 * x - 25 + d4 >= 0):
        flag = True

    #check if point is in rectangle shaped obstacle or not
    if (1.72 * x + y - 333.4 - d5 <= 0) and (1.7 * x + y - 183.5 + d6 >= 0) and (y - 0.577 * x - 115.19 - d7 <= 0) and (y - 0.575 * x - 103.862 + d8 >= 0):
        flag = True

    #check if point is in polygon shaped obstacle or not : 1st Quad
    if (y + 13 * x - 340 + d9 >= 0) and (y - (15-pad) >= 0) and (y + x - 100 - d10 <= 0) and (y + 1.4 * x - 120 - d14 <= 0):
        flag = True

    #check if point is in polygon shaped obstacle or not : 12nd Quad
    if (y - 1.4 * x + 90 + d11 >= 0) and (y + 1.2 * x - 170 - d12 <= 0) and (y - 1.2 * x + 10 - d13 <= 0) and (y + 1.4*x - 120 + d15 >= 0):
        flag = True

    #check if point is in eclipse shaped obstacle or not
    if ((x-150)/(40+pad))**2 + ((y-100)/(20+pad))**2 - 1 <=0:
        flag = True

    return flag

