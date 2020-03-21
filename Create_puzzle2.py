import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
plt.style.use('seaborn-pastel')
import numpy as np
import math

MAX_X = 300
MAX_Y = 200

plotPolygon = np.array([(25, 185), (75, 185), (100, 150), (75, 120), (50, 150), (20, 120)], dtype='int')

plotRectangle = np.array([(30, 67.5), (35, 76), (100, 38.6), (95, 30)], dtype='int')

plotRhombus = np.array([(225, 40), (250, 25), (225, 10), (200, 25)], dtype='int')

plotCircle = [(25), (225, 150)]

plotEllipse = [(80, 40), (150, 100)]

def solveLine(obsCoords1, obsCoords2, x, y):
    x1 = obsCoords1[0]
    y1 = obsCoords1[1]

    x2 = obsCoords2[0]
    y2 = obsCoords2[1]

    if y1 == y2:
        slope = y - y2
        return slope
    if x1 == x2:
        slope = x - x2
        return slope
    slope = (y - y2) - ((x - x2) * (y1 - y2)) / (x1 - x2)
    return slope

def isValidStep(position, stretch):
    x = position[0]
    y = position[1]

    flag = 0

    # check if point is in circle shaped obstacle or not
    if ((x - 225) ** 2 + (y - 150) ** 2 - 25 ** 2) <= 0:
        flag = False
        return flag

    if ((x - 150) / (40 + stretch)) ** 2 + ((y - 100) / (20 + stretch)) ** 2 - 1 <= 0:
        flag = False
        return flag

    rhombusCoords = [(200 - stretch,25),(225,(40 + stretch)),( 250 + stretch,25),(225,(10 - stretch))]

    rectangleCoords = [(95 - math.floor((75 + stretch) * math.sqrt(3)/2), 30 - math.floor((75 + stretch)/2)),
                        (95 - math.floor((75 + stretch)*math.sqrt(3)/2) + math.floor((10 + stretch)*math.sqrt(1)/2),30 - math.floor((75 + stretch)/2) - math.floor((10 + stretch)*math.sqrt(3)/2)),
                        (95 + math.floor((10 + stretch)/2),30 - math.floor(10*math.sqrt(3)/2)),
                        (95 - math.floor(stretch/2),30 + math.floor(stretch*math.sqrt(3)/2))]

    # Polygon divided into 4 triangles:

    firstTriangleCoords = [(20 - stretch,120 + stretch),(25 - stretch,185 - stretch), (50,150 + stretch)]
    secondTriangleCoords = [(25 - stretch,185 - stretch),(75 + stretch,185 - stretch), (50,150 + stretch)]
    thirdTriangleCoords = [(75 + stretch,185 - stretch),(100 + stretch,150 - stretch), (50,150 + stretch)]
    fourthTriangleCoords = [(100 + stretch,150 - stretch),(75 + stretch,120 + stretch), (50,150 + stretch)]


    # Obstacle check for robot in first traingle

    planeTriag1 = []

    for i in range(len(firstTriangleCoords)):
        if i == len(firstTriangleCoords)-1:
            planeTriag1.append(solveLine(firstTriangleCoords[i], firstTriangleCoords[0], x, y))
            break
        planeTriag1.append(solveLine(firstTriangleCoords[i],firstTriangleCoords[i+1],x,y))

    if planeTriag1[0]>=0 and planeTriag1[1]>=0 and planeTriag1[2]<=0 :
        flag = False
        return flag

    # Obstacle check for robot in second traingle

    planeTriag2 = []
    for i in range(len(secondTriangleCoords)):
        if i == len(secondTriangleCoords) - 1:
            planeTriag2.append(solveLine(secondTriangleCoords[i], secondTriangleCoords[0], x, y))
            break
        planeTriag2.append(solveLine(secondTriangleCoords[i], secondTriangleCoords[i + 1], x, y))
    if (planeTriag2[0] >= 0 and planeTriag2[1] <= 0 and planeTriag2[2] <= 0):
        flag = False
        return flag

    # Obstacle check for robot in third traingle

    planeTriag3 = []
    for i in range(len(thirdTriangleCoords)):
        if i == len(thirdTriangleCoords) - 1:
            planeTriag3.append(solveLine(thirdTriangleCoords[i], thirdTriangleCoords[0], x, y))
            break
        planeTriag3.append(solveLine(thirdTriangleCoords[i], thirdTriangleCoords[i + 1], x, y))

    if (planeTriag3[0] >= 0 and planeTriag3[1] <= 0 and planeTriag3[2] >= 0):
        flag = False
        return flag

    # Obstacle check for robot in fourth traingle

    planeTriag4 = []
    for i in range(len(fourthTriangleCoords)):
        if i == len(fourthTriangleCoords) - 1:
            planeTriag4.append(solveLine(fourthTriangleCoords[i], fourthTriangleCoords[0], x, y))
            break
        planeTriag4.append(solveLine(fourthTriangleCoords[i], fourthTriangleCoords[i + 1], x, y))

    if (planeTriag4[0] <= 0 and planeTriag4[1] <= 0 and planeTriag4[2] >= 0):
        flag = False
        return flag

    # Obstacle check for the Rhombus

    planeRhombus = []
    for i in range(len(rhombusCoords)):
        if i == len(rhombusCoords) - 1:
            planeRhombus.append(solveLine(rhombusCoords[i], rhombusCoords[0], x, y))
            break
        planeRhombus.append(solveLine(rhombusCoords[i], rhombusCoords[i + 1], x, y))
    if (planeRhombus[0] >= 0 and planeRhombus[1] >= 0 and planeRhombus[2] <= 0 and planeRhombus[3] <= 0 ):
        flag = False
        return flag

    # Obstacle check for the Rectangle

    planeRectangle = []
    for i in range(len(rectangleCoords)):
        if i == len(rectangleCoords) - 1:
            planeRectangle.append(solveLine(rectangleCoords[i], rectangleCoords[0], x, y))
            break
        planeRectangle.append(solveLine(rectangleCoords[i], rectangleCoords[i + 1], x, y))
    if (planeRectangle[0] >= 0 and planeRectangle[1] >= 0 and planeRectangle[2] <= 0 and planeRectangle[3] <= 0):
        flag = False
        return flag
    else:
        flag = True
        return flag

def showPath(START_POINT, GOAL_POINT, STEP_OBJECT_LIST, pathValues):
    fig = plt.figure()
    fig.set_dpi(100)
    fig.set_size_inches(8.5, 6)

    axis = plt.axes(xlim=(0, MAX_X), ylim=(0, MAX_Y))
    xTrace = []
    yTrace = []

    xTrack = []
    yTrack = []

    traced, = plt.plot([], [], 'o', color = 'red')
    tracked, = plt.plot([], [], 'o', color = 'blue')

    def init():
        axis.set_xlim(0,MAX_X)
        axis.set_ylim(0,MAX_Y)
        return traced, tracked,

    def animate(itr):
        if itr < len(STEP_OBJECT_LIST):
            for eachNode in STEP_OBJECT_LIST:
                xTrace.append(eachNode.position[0])
                yTrace.append(eachNode.position[1])
                traced.set_data(xTrace,yTrace)

            for trackNode in pathValues:
                xTrack.append(trackNode[0])
                yTrack.append(trackNode[1])
                tracked.set_data(xTrack,yTrack)

        return traced, tracked,

    anim = FuncAnimation(fig, animate, frames = len(STEP_OBJECT_LIST)+1, init_func = init, interval = 10, blit = False, repeat = False)
    circle = plt.Circle((plotCircle[1]), plotCircle[0], fc=None)
    rectangle = plt.Polygon(plotRectangle)
    rhombus = plt.Polygon(plotRhombus)
    polygon = plt.Polygon(plotPolygon)
    ellipse = Ellipse((plotEllipse[1]), plotEllipse[0][0], plotEllipse[0][1], 0)
    obstacles = [circle, rectangle, rhombus, polygon, ellipse]
    goalLoc = plt.scatter(GOAL_POINT[0], GOAL_POINT[1], s = 10, color = 'g')
    startLoc = plt.scatter(START_POINT[0], START_POINT[1], s = 10, color = 'black')

    for item in obstacles:
        plt.gca().add_patch(item)
    plt.show()
