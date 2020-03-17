from Create_puzzle2 import *
from datetime import datetime
import sys

#Global Variables
START_POINT = [] # [x, y]
GOAL_POINT = [] # [x, y]
STEPS_LIST = []
STEP_OBJECT_LIST = []
STEP_SIZE = 1 			#Default step size

    
#Definition of Class Step:
class step:
	#Method to initialize the node with the values/attributes and add the step
	#self: Object of class step
	#parent: Object of class step
	#position: the x,y values of the current step
	#cost: cost of the step to move from the parent to the current position 
	def __init__(self, parent, position, cost):
		self.position = position # [x, y]
		self.parent = parent
		if parent == None:
			self.costToCome = 0.0
		else:
			self.costToCome = parent.costToCome + cost;
		self.costToGo = float(( (GOAL_POINT[0]-self.position[0])**2 + (GOAL_POINT[1]-self.position[1])**2 )**(0.5)) #Eucleadian Distance

		self.addToGraph()


	def addToGraph(self):
		if self.position in STEPS_LIST:
			index = STEPS_LIST.index(self.position)
			if self.costToCome+self.costToGo < STEP_OBJECT_LIST[index].costToCome+STEP_OBJECT_LIST[index].costToGo:
				STEP_OBJECT_LIST[index] = self
		else:
			if self.parent == None or self.costToGo < self.parent.costToGo:
				STEPS_LIST.append(self.position) 
				STEP_OBJECT_LIST.append(self)

	def moveUp(self):
		if(self.position[1] > 0):
			newPosition = [self.position[0], self.position[1]-STEP_SIZE]
			if isValidStep(newPosition, RADIUS+CLEARANCE) == True:
				try:
					if(self.parent.position == newPosition):
						pass #going back to the parent
					else:
						newStep = step(self,newPosition, float(STEP_SIZE)) #cost 1.0
				except AttributeError:
                    #if parent is not present
					newStep = step(self,newPosition, float(STEP_SIZE))
		else:
			return 

	def moveUpRight(self):
		if(self.position[1] > 0 and self.position[0] < MAX_X):
			newPosition = [self.position[0]+STEP_SIZE, self.position[1]-STEP_SIZE]
			if isValidStep(newPosition, RADIUS+CLEARANCE) == True:
				try:
					if(self.parent.position == newPosition):
						pass #going back to the parent
					else:
						newStep = step(self,newPosition, float(2*STEP_SIZE)**(0.5))
				except AttributeError:
                    #if parent is not present
					newStep = step(self,newPosition, float(2*STEP_SIZE)**(0.5))
		else:
			return 

	def moveRight(self):
		if(self.position[0] < MAX_X):
			newPosition = [self.position[0]+STEP_SIZE, self.position[1]]
			if isValidStep(newPosition, RADIUS+CLEARANCE) == True:
				try:
					if(self.parent.position == newPosition):
						pass #going back to the parent
					else:
						newStep = step(self,newPosition, float(STEP_SIZE))                        
				except AttributeError:
                    #if parent is not present
					newStep = step(self,newPosition, float(STEP_SIZE))                  
		else:

			return 

	def moveDownRight(self):
		if(self.position[1] < MAX_Y and self.position[0] < MAX_X):
			newPosition = [self.position[0]+STEP_SIZE, self.position[1]+STEP_SIZE]
			if isValidStep(newPosition, RADIUS+CLEARANCE) == True:
				try:
					if(self.parent.position == newPosition):
						pass #going back to the parent
					else:
						newStep = step(self,newPosition, float(STEP_SIZE*2)**(0.5))
				except AttributeError:
                    #if parent is not present
					newStep = step(self,newPosition, float(STEP_SIZE*2)**(0.5))
		else:
			return
	
	def moveDown(self):
		if(self.position[1] < MAX_Y):
			newPosition = [self.position[0], self.position[1]+STEP_SIZE]
			if isValidStep(newPosition, RADIUS+CLEARANCE) == True:
				try:
					if(self.parent.position == newPosition):
						pass #going back to the parent
					else:
						newStep = step(self,newPosition, float(STEP_SIZE))
				except AttributeError:
                    #if parent is not present
					newStep = step(self,newPosition, float(STEP_SIZE))
		else:
			return

	def moveDownLeft(self):
		if(self.position[1] < MAX_Y and self.position[0] > 0):
			newPosition = [self.position[0]-STEP_SIZE, self.position[1]+STEP_SIZE]
			if isValidStep(newPosition, RADIUS+CLEARANCE) == True:
				try:
					if(self.parent.position == newPosition):
						pass #going back to the parent
					else:
						newStep = step(self,newPosition, float(STEP_SIZE*2)**(0.5))
				except AttributeError:
                    #if parent is not present
					newStep = step(self,newPosition, float(STEP_SIZE*2)**(0.5))
		else:
			return

	def moveLeft(self):
		if(self.position[0] > 0):
			newPosition = [self.position[0]-STEP_SIZE, self.position[1]]
			if isValidStep(newPosition, RADIUS+CLEARANCE) == True:
				try:
					if(self.parent.position == newPosition):
						pass #going back to the parent
					else:
						newStep = step(self,newPosition, float(STEP_SIZE))
				except AttributeError:
                    #if parent is not present
					newStep = step(self,newPosition, float(STEP_SIZE))
		else:
			return

	def moveUpLeft(self):
		if(self.position[1] > 0 and self.position[0] > 0):
			newPosition = [self.position[0]-STEP_SIZE, self.position[1]-STEP_SIZE]
			if isValidStep(newPosition, RADIUS+CLEARANCE) == True:
				try:
					if(self.parent.position == newPosition):
						pass #going back to the parent
					else:
						newStep = step(self,newPosition, float(STEP_SIZE*2)**(0.5))
				except AttributeError:
                    #if parent is not present
					newStep = step(self,newPosition, float(STEP_SIZE*2)**(0.5))
		else:
			return

def stepsTakenToCompute():
	for eachStep in STEP_OBJECT_LIST:
		updateTheStep(eachStep.position, startColor, RADIUS)
		if eachStep.position == GOAL_POINT:
			break
        

def backtrack(stepObj):
	pathValues = []
	while stepObj.parent != None:
		pathValues.append(stepObj.position)
		stepObj = stepObj.parent
	pathValues.append(stepObj.position)
    
	pathValues.reverse()
	showPath(pathValues, RADIUS) 




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
    pygame.quit()
    sys.exit(0)
    
#To switch the orgin to the top
START_POINT[1] = MAX_Y - START_POINT[1]
GOAL_POINT[1] = MAX_Y - GOAL_POINT[1]

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

	#Starting the linked list with start point as the root
	root = step(None, START_POINT[:2], 0) 

	for eachStep in STEP_OBJECT_LIST:

		if eachStep.position == GOAL_POINT:
			print("Reached the Goal Node!!")
			now = datetime.now().time()
			print("Found at time: ",now)
			break
		else:
			eachStep.moveLeft()
			eachStep.moveDown()
			eachStep.moveRight()
			eachStep.moveUp()
			eachStep.moveUpLeft()
			eachStep.moveDownLeft()
			eachStep.moveDownRight()
			eachStep.moveUpRight()

	index = STEPS_LIST.index(GOAL_POINT[:2])
	print("Total Cost to reach the final Point:",STEP_OBJECT_LIST[index].costToCome)
	#Once the whole generation is completed begin the animation
	stepsTakenToCompute()
	#To show the backtrack on the graph
	backtrack(STEP_OBJECT_LIST[index])
	now = datetime.now().time()
	print("end time: ",now)
else:
    print("Exiting the Algorithm")
    pygame.quit()
    sys.exit(0)

while True:
	for inst in pygame.event.get():
		if inst.type == pygame.QUIT:
			pygame.quit()
			quit()

	pygame.display.update()