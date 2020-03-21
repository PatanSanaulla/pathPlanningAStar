from Create_puzzle2 import *
from datetime import datetime
import math
import sys

#Global Variables
START_POINT = [] # [x, y]
GOAL_POINT = [] # [x, y]
#STEPS_LIST = set([])
EXPLORED = []
VISITED = []
THRESHOLD = 0.5
STEP_OBJECT_LIST = []
STEP_SIZE = 1 			#Default step size
THETA = math.pi/6       #Default 30 degrees

    
#Definition of Class Step:
class step:
	#Method to initialize the node with the values/attributes and add the step
	#self: Object of class step
	#parent: Object of class step
	#position: the x,y values of the current step
	#cost: cost of the step to move from the parent to the current position 
	def __init__(self, parent, position, angle, cost):
		self.position = position # [x, y]
		self.parent = parent
		self.angle = angle%(2*math.pi)
		self.xPoint = int(position[0]/THRESHOLD)-1
		self.yPoint = int(position[1]/THRESHOLD)-1
		self.anglePoint = (int(angle/THETA)%12)-1
		if parent == None:
			self.costToCome = 0.0
		else:
			self.costToCome = parent.costToCome + cost;
		self.cost = self.costToCome + float(( (GOAL_POINT[0]-self.position[0])**2 + (GOAL_POINT[1]-self.position[1])**2 )**(0.5)) #Eucleadian Distance
		#abs(self.position[0]-GOAL_POINT[0])+abs(self.position[1]-GOAL_POINT[1]) #Manhattan Distance
		#max(abs(self.position[0] - GOAL_POINT[0]), abs(self.position[1] - GOAL_POINT[1]))  # Diagonal Distance
		self.addToGraph()

	def __lt__(self, other):
		return self.cost < other.cost


	def addToGraph(self): 
		STEP_OBJECT_LIST.append(self)


	def generateSteps(self):
		EXPLORED.append(self)
		for i in range(int(180/30)-1):
			angle = (THETA*i)+self.angle#math.radians(self.angle)
			newX = thresholding((math.cos(angle)*STEP_SIZE)+self.position[0])
			newY = thresholding((math.sin(angle)*STEP_SIZE)+self.position[1])
			newPosition = [newX, newY]
			if newX >= 0 and newX <= MAX_X and newY >= 0 and newY <= MAX_Y and (isValidStep(newPosition, RADIUS+CLEARANCE) == True):
				try:
					if(self.parent.position == newPosition):
						pass
					else:
						newStep = step(self, newPosition, angle, float(STEP_SIZE)) #cost 1.0
				except AttributeError:
					newStep = step(self, newPosition, angle, float(STEP_SIZE)) #cost 1.0
			else:
				return

def backtrack(stepObj):
	pathValues = []
	while stepObj.parent != None:
		pathValues.append([stepObj.position[0], stepObj.position[1], stepObj.angle])
		stepObj = stepObj.parent
	pathValues.append([stepObj.position[0], stepObj.position[1], stepObj.angle])
    
	pathValues.reverse()
	showPath(START_POINT, GOAL_POINT, EXPLORED, pathValues)


def inGoal(position):
	x, y = position[0], position[1]
	if ((x - GOAL_POINT[0]) ** 2 + (y - GOAL_POINT[1]) ** 2 <= (1.5)**2):
		return True
	else:
		return False

def isVisited(stepObj):
    #posAndAngle = [stepObj.position[0], stepObj.position[1]), round(stepObj.angle)]
    try:
        if VISITED[stepObj.xPoint][stepObj.yPoint][stepObj.anglePoint] == 1:
            #if posAndAngle in STEPS_LIST:
            return True
        else:
            VISITED[stepObj.xPoint][stepObj.yPoint][stepObj.anglePoint] = 1
            #STEPS_LIST.add(posAndAngle)
            return False
    except IndexError:
        print("index issue")

def thresholding(val):
	splitData = str(val).split('.')
	intData = int(splitData[0])
	decimalData = int(splitData[1][0])
	if decimalData > 7:
		return intData+1.0
	else:
		if decimalData > 2:
			return intData+0.5
		else:
			return intData+0.0

#MAIN CODE
try:
    startPoints = input("Enter the Start Points (x,y,theta) position: ")
    START_POINT = [int(each) for each in startPoints.split(" ")] 
    #Start or goal points have 3 Values: START_POINT[0] -> x, START_POINT[1] -> y, and START_POINT[2] -> theta
    goalPoints = input("Enter the Goal Points (x,y,theta) position: ")
    GOAL_POINT = [int(each) for each in goalPoints.split(" ")]
    RADIUS = int(input("Enter the Radius of the robot: "))
    CLEARANCE = int(input("Enter the Clearance of the robot: "))
    STEP_SIZE = int(input("Enter the Step Size for the robot: "))

except:
    print("Please enter the proper points: Example: 200 30 30")
    print("Exiting the Algorithm")
    sys.exit(0)
    
isPossible = 0

if START_POINT[0] >= 0 and START_POINT[0] <= MAX_X and START_POINT[1] >= 0 and START_POINT[1] <= MAX_Y and (isValidStep(START_POINT, RADIUS+CLEARANCE) == True):
    isPossible += 1
else:
    print("Invalid Start Point")
    
if GOAL_POINT[0] >= 0 and GOAL_POINT[0] <= MAX_X and GOAL_POINT[1] >= 0 and GOAL_POINT[1] <= MAX_Y and (isValidStep(GOAL_POINT, RADIUS+CLEARANCE) == True):
    isPossible += 1
else:
    print("Invalid Goal Point")

#To check if both the values are possible to work with in the puzzle
if isPossible == 2: 
	now = datetime.now().time()
	print("start time: ",now)
    
	VISITED = [ [ [ 0 for i in range(int(2*math.pi/THETA)) ] for j in range(int(MAX_Y/THRESHOLD)) ] for k in range(int(MAX_X/THRESHOLD)) ]
	#Starting the linked list with start point as the root
	root = step(None, START_POINT[:2], math.radians(START_POINT[2]), 0) 

	eachStep = STEP_OBJECT_LIST.pop(0)
	isVisited(eachStep) 

	while inGoal(eachStep.position) == False:#to keep traversing until the goal area is found
		eachStep.generateSteps()
		print(eachStep.position, math.degrees(eachStep.angle))
		STEP_OBJECT_LIST.sort()

		while True:
			eachStep = STEP_OBJECT_LIST.pop(0) #to Keep popping until a unvisted node is found
			if isVisited(eachStep) == False:
				break
        
	print("Total Cost to reach the final Point:",eachStep.costToCome)
	#stepsTakenToCompute() #Once the whole generation is completed begin the animation

    
	backtrack(eachStep) #To show the backtrack on the graph
	now = datetime.now().time()
	print("end time: ",now)
else:
    print("Exiting the Algorithm")
    sys.exit(0)



