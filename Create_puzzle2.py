import pygame
import pygame.gfxdraw
import math

pygame.init()

MAX_X = 300
MAX_Y = 200

obs1_pts = set()
obs2_pts = set()
obs3_pts = set()
obs4_pts = set()
obs5_pts = set()

startColor = (255,255,0)
goalColor = (255, 0, 0)
obstacleColor = (0, 0, 0)
pathColor = (0, 0, 255)

puzzleMap = pygame.display.set_mode((MAX_X, MAX_Y))
puzzleMap.fill((255, 255, 255))
pygame.draw.circle(puzzleMap, obstacleColor, (225,50), 25)
pygame.draw.ellipse(puzzleMap, obstacleColor, (110, 80, 80, 40))

pygame.draw.polygon(puzzleMap, obstacleColor, ((95,170),(100,161),(35,124),(30,133)))
pygame.draw.polygon(puzzleMap, obstacleColor, ((20,80),(50,50),(75,80),(100,50),(75,15),(25,15)))
pygame.draw.polygon(puzzleMap, obstacleColor, ((225,190),(250,175),(225,160),(200,175)))


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


def isValidStep(position, CLEARANCE):
	pos = tuple(position)
	if(inObs1(pos, CLEARANCE) == True) or (inObs2(pos, CLEARANCE) == True) or (inObs3(pos, CLEARANCE) == True) or (inObs4(pos, CLEARANCE) == True) or (inObs5(pos, CLEARANCE) == True):
		return False
	else:
		return True


def inObs1(pos, CLEARANCE):
	if pos in obs1_pts:
		return True
	else:
		x, y = pos[0], pos[1]
		if ((8 * x + 5 * y <= 1610+math.ceil(CLEARANCE*10.67)) and (-38 * x + 65 * y >= 6730-math.ceil(CLEARANCE*106.16)) and (9 * x + 5 * y >= 935-math.ceil(CLEARANCE*10.67)) and (37 * x - 65 * y >= -7535-math.ceil(CLEARANCE*106.16))):
            #if ((8 * x + 5 * y <= 1610+(CLEARANCE**3)) and (-38 * x + 65 * y >= 6730-((CLEARANCE+1)**4)) and (9 * x + 5 * y >= 935-(CLEARANCE**3)) and (37 * x - 65 * y >= -7535-((CLEARANCE+1)**4))):
			obs1_pts.add(pos)
			return True
		else:
			return False

def inObs2(pos, CLEARANCE):
	if pos in obs2_pts:
		return True
	else:
		x, y = pos[0], pos[1]
		if ((13 * x + y >= 340-math.ceil(CLEARANCE*12)) and (x + y <= 100+math.ceil(CLEARANCE)) and (-7 * x + 5 * y >= -100-math.ceil(CLEARANCE*90.16)) and (y >= 15-(CLEARANCE)) or (-6 * x + 5 * y <= -50+math.ceil(CLEARANCE*10)) and (6 * x + 5 * y <= 850+math.ceil(CLEARANCE*10.67)) and (7 * x - 5 * y <= 450+math.ceil(CLEARANCE*10.67)) and \
		 (y >= 15-(CLEARANCE)) and (-7 * x + 5 * y <= -100+math.ceil(CLEARANCE*15))):
			obs2_pts.add(pos)
			return True
		else:
			return False
			
def inObs3(pos, CLEARANCE):
	if pos in obs3_pts:
		return True
	else:
		x, y = pos[0], pos[1]
		if (((x - 150) ** 2) / ((40+CLEARANCE)**2) + ((y - 100) ** 2) / ((20+CLEARANCE)**2) <= 1):
			obs3_pts.add(pos)
			return True
		else:
			return False

def inObs4(pos, CLEARANCE):
	if pos in obs4_pts:
		return True
	else:
		x, y = pos[0], pos[1]
		if ((x - 225) ** 2 + (y - 50) ** 2 <= (25+CLEARANCE)**2):
			obs4_pts.add(pos)
			return True
		else:
			return False

def inObs5(pos, CLEARANCE):
	if pos in obs5_pts:
		return True
	else:
		x, y = pos[0], pos[1] 
		if (3 * x + 5 * y <= 1625+(CLEARANCE*7)) and  (5 * y - 3 * x <= 275+(CLEARANCE*7)) and (3 * x + 5 * y >= 1475-(CLEARANCE*5)) and (5 * y - 3 * x >= 125-(CLEARANCE*5)):
			obs5_pts.add(pos)
			return True
		else:
			return False