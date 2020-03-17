import pygame
import pygame.gfxdraw
import math

pygame.init()

MAX_X = 300
MAX_Y = 200

# Building the obstacle space in pygame

pygame.init()

white = (255,255,255)
backgroundColor = (0,0,0) #black
obstacleColor = (255,0,0) #red
startColor = (0,255,0) #green
pathColor = (0,0,255) #blue
traverseColor = (255,255,0) #yellow

gameDisplay = pygame.display.set_mode((MAX_X,MAX_Y))
gameDisplay.fill(backgroundColor)

pygame.draw.circle(gameDisplay, obstacleColor, (225,50), 25)
#Drawing Polygon
pygame.draw.polygon(gameDisplay, obstacleColor, ((25,15),(75,15),(100,50),(75,80),(50,50),(20,80)))
#Drawing Rectangle
pygame.draw.polygon(gameDisplay, obstacleColor, ((95,170),(30,132.5),(35,124),(100,161.4)))
#Drawing Rhombus
pygame.draw.polygon(gameDisplay, obstacleColor, ((200,175),(225,160),(250,175),(225,190)))

pygame.draw.ellipse(gameDisplay, obstacleColor, (110, 80, 80, 40))

###########################################################################################



def colorTheStep(position, color, RADIUS):
    for inst in pygame.event.get():
        if inst.type == pygame.QUIT:
            pygame.quit()
            quit()
    if RADIUS == None or RADIUS == 0:
        pygame.gfxdraw.pixel(gameDisplay, position[0], position[1], color)
    else:
        pygame.draw.circle(gameDisplay, color, (position[0],position[1]), RADIUS)
    pygame.display.update()


def showPath(pathList, RADIUS):
	for step in pathList:
		if RADIUS == None or RADIUS == 0:
			pygame.gfxdraw.pixel(gameDisplay, step[0], step[1], pathColor)
		else:
			pygame.draw.circle(gameDisplay, pathColor, (step[0], step[1]), RADIUS)
		pygame.display.update()
    
#################################################################################################################################################
# Function to Check for Obstacles
def isValidStep(point,pad):  # def obstacleCheck_rigid
    x = point[0]
    y = point[1]
    #theta = point[2]
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

    flag = True
    if (x < pad) or (x > 300-pad) or (y < pad) or (y > 200-pad):
        flag = False

    #check if point is in circle shaped obstacle or not

    if ((x - 225)**2 + (y-50)**2 - (25+pad)**2) <= 0:
        flag = False

    #check if point is in rhombus shaped obstacle or not

    if (0.6 * x + y - 325 - d1 <= 0) and (0.6 * x + y - 295 + d2 >= 0) and (y - 0.6 * x - 55 - d3 <= 0) and (y - 0.6 * x - 25 + d4 >= 0):
        flag = False

    #check if point is in rectangle shaped obstacle or not
    if (1.72 * x + y - 333.4 - d5 <= 0) and (1.7 * x + y - 183.5 + d6 >= 0) and (y - 0.577 * x - 115.19 - d7 <= 0) and (y - 0.575 * x - 103.862 + d8 >= 0):
        flag = False

    #check if point is in polygon shaped obstacle or not : 1st Quad
    if (y + 13 * x - 340 + d9 >= 0) and (y - (15-pad) >= 0) and (y + x - 100 - d10 <= 0) and (y + 1.4 * x - 120 - d14 <= 0):
        flag = False

    #check if point is in polygon shaped obstacle or not : 12nd Quad
    if (y - 1.4 * x + 90 + d11 >= 0) and (y + 1.2 * x - 170 - d12 <= 0) and (y - 1.2 * x + 10 - d13 <= 0) and (y + 1.4*x - 120 + d15 >= 0):
        flag = False

    #check if point is in eclipse shaped obstacle or not
    if ((x-150)/(40+pad))**2 + ((y-100)/(20+pad))**2 - 1 <=0:
        flag = False

    return flag


def isValidStep2(position, CLEARANCE):
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
