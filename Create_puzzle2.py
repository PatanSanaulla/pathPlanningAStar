import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.font_manager import FontProperties
import matplotlib.lines as mlines
plt.style.use('seaborn-pastel')
import numpy as np
import math
import cv2
import glob

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

    # check if point is in ellipse shaped object or not
    if ((x - 150) / (40 + stretch)) ** 2 + ((y - 100) / (20 + stretch)) ** 2 - 1 <= 0:
        flag = False
        return flag

    rhombusCoords = [(200 - stretch,25),(225,(40 + stretch)),( 250 + stretch,25),(225,(10 - stretch))]

    rectangleCoords = np.array([(30 - stretch, 67.5 + stretch), (35 + stretch, 76 + stretch), (100 + stretch, 38.6 - stretch), (95 - stretch, 30 - stretch)], dtype='int')

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

    if planeTriag1[0]<=0 and planeTriag1[1]<=0 and planeTriag1[2]>=0 :
        flag = False
        return flag

    # Obstacle check for robot in second traingle
    planeTriag2 = []
    for i in range(len(secondTriangleCoords)):
        if i == len(secondTriangleCoords) - 1:
            planeTriag2.append(solveLine(secondTriangleCoords[i], secondTriangleCoords[0], x, y))
            break
        planeTriag2.append(solveLine(secondTriangleCoords[i], secondTriangleCoords[i + 1], x, y))
    if (planeTriag2[0] <= 0 and planeTriag2[1] >= 0 and planeTriag2[2] >= 0):
        flag = False
        return flag

    # Obstacle check for robot in third traingle
    planeTriag3 = []
    for i in range(len(thirdTriangleCoords)):
        if i == len(thirdTriangleCoords) - 1:
            planeTriag3.append(solveLine(thirdTriangleCoords[i], thirdTriangleCoords[0], x, y))
            break
        planeTriag3.append(solveLine(thirdTriangleCoords[i], thirdTriangleCoords[i + 1], x, y))

    if (planeTriag3[0] <= 0 and planeTriag3[1] >= 0 and planeTriag3[2] <= 0):
        flag = False
        return flag

    # Obstacle check for robot in fourth traingle
    planeTriag4 = []
    for i in range(len(fourthTriangleCoords)):
        if i == len(fourthTriangleCoords) - 1:
            planeTriag4.append(solveLine(fourthTriangleCoords[i], fourthTriangleCoords[0], x, y))
            break
        planeTriag4.append(solveLine(fourthTriangleCoords[i], fourthTriangleCoords[i + 1], x, y))

    if (planeTriag4[0] >= 0 and planeTriag4[1] >= 0 and planeTriag4[2] <= 0):
        flag = False
        return flag

    # Obstacle check for the Rhombus
    planeRhombus = []
    for i in range(len(rhombusCoords)):
        if i == len(rhombusCoords) - 1:
            planeRhombus.append(solveLine(rhombusCoords[i], rhombusCoords[0], x, y))
            break
        planeRhombus.append(solveLine(rhombusCoords[i], rhombusCoords[i + 1], x, y))
    if (planeRhombus[0] <= 0 and planeRhombus[1] <= 0 and planeRhombus[2] >= 0 and planeRhombus[3] >= 0 ):
        flag = False
        return flag

    # Obstacle check for the Rectangle
    planeRectangle = []
    for i in range(len(rectangleCoords)):
        if i == len(rectangleCoords) - 1:
            planeRectangle.append(solveLine(rectangleCoords[i], rectangleCoords[0], x, y))
            break
        planeRectangle.append(solveLine(rectangleCoords[i], rectangleCoords[i + 1], x, y))
    if (planeRectangle[0] <= 0 and planeRectangle[1] <= 0 and planeRectangle[2] >= 0 and planeRectangle[3] >= 0):
        flag = False
        return flag
    else:
        flag = True
        return flag

def showPath(START_POINT, GOAL_POINT, STEP_OBJECT_LIST, pathValues, fileLocation):
    fig = plt.figure()
    fig.set_dpi(100)
    fig.set_size_inches(8.5, 6)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    xTracepoint1 = []
    yTracepoint2 = []

    yTracepoint1 = []
    xTracepoint2 = []

    xTrackpoint1 = []
    yTrackpoint1 = []

    xTrackpoint2 = []
    yTrackpoint2 = []

    axis = fig.add_subplot(111, aspect = 'equal', autoscale_on = False, xlim = (0,MAX_X), ylim = (0, MAX_Y))
    #axis = plt.axes(xlim=(0, MAX_X), ylim=(0, MAX_Y))
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times New Roman')
    font.set_style('italic')
    axis.set_xlabel('x coordinate',  fontproperties = font)
    axis.set_ylabel('y coordinate', fontproperties = font)
    count = 0
    circle = plt.Circle((plotCircle[1]), plotCircle[0], fc=None)
    rectangle = plt.Polygon(plotRectangle)
    rhombus = plt.Polygon(plotRhombus)
    polygon = plt.Polygon(plotPolygon)
    ellipse = Ellipse((plotEllipse[1]), plotEllipse[0][0], plotEllipse[0][1], 0)
    obstacles = [circle, rectangle, rhombus, polygon, ellipse]

    goalLoc = plt.plot(GOAL_POINT[0], GOAL_POINT[1], color='green', markersize=1)

    startLoc = plt.plot(START_POINT[0], START_POINT[1], color='black', markersize=1)
    for itr in range(1, len(STEP_OBJECT_LIST)):
        startTrace = STEP_OBJECT_LIST[itr].parent
        xTracepoint1.append(startTrace.position[0])
        yTracepoint1.append(startTrace.position[1])
        xTracepoint2.append(STEP_OBJECT_LIST[itr].position[0] - startTrace.position[0])
        yTracepoint2.append(STEP_OBJECT_LIST[itr].position[1] - startTrace.position[1])
        axis.quiver(np.array((xTracepoint1)), np.array((yTracepoint1)), np.array((xTracepoint2)), np.array((yTracepoint2)), units='xy', scale=1, color='yellow')
        plt.savefig("example"+str(count)+".png", dpi=1920)
        print(len(STEP_OBJECT_LIST))
        count = count + 1
    if (len(pathValues) > 0):
        for itr in range(1, len(pathValues)):
            xTrackpoint1.append(pathValues[itr - 1][0])
            yTrackpoint1.append(pathValues[itr - 1][1])
            xTrackpoint2.append(pathValues[itr][0] - pathValues[itr - 1][0])
            yTrackpoint2.append(pathValues[itr][1] - pathValues[itr - 1][1])
            axis.quiver(np.array((xTrackpoint1)), np.array((yTrackpoint1)), np.array((xTrackpoint2)), np.array((yTrackpoint2)), units='xy', scale=1, color='blue')
            plt.savefig("example"+str(count)+".png", dpi=1920)
            count = count + 1



    images = glob.glob(str(fileLocation) + "/*")
    sortedImages = np.sort(images)
    output = cv2.VideoWriter("Simulation Video.avi", cv2.VideoWriter_fourcc(*'XVID'), 20.0, (300, 200))
    for image in sortedImages:
        display = cv2.imread(file)
        display = cv2.resize(display, (300, 200))
        output.write(display)
    output.release()

    for item in obstacles:
        axis.add_patch(item)

    plt.show()
