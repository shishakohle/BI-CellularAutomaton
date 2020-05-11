"""
TODO: Some comments on this project.
"""

from Heart import Heart
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import time
from Cell import Celltype
import matplotlib.animation as animation

# colormap
cmap = colors.ListedColormap(['#2e4a1e', '#00baff', '#000b34', '#fff313', '#7b7b00', '#fcc926', '#bf7600',
                              '#FFFFFF', '#E9967A', '#8B0000', '#605acd', '#3e135e', '#A2CD5A'])
boundaries = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
norm = colors.BoundaryNorm(boundaries, cmap.N, clip=True)

# steps for animation 10 ms (Zyklus: 0 - 200ms + 300ms Pause = 500ms gesamter Zyklus)
# Cells look to neighbour and start contracting if neighbour has reached its mV
# no-heart-cell || heart-cell

# scale image and matrix
dx, dy = 0.05, 0.05
x = np.arange(0, 67, dx)
y = np.arange(0, 49, dy)
X, Y = np.meshgrid(x, y)
extent = np.min(X), np.max(X), np.min(Y), np.max(Y)

image = plt.imread("heart.png")


def delay_ms(milliseconds):
    """
    # timestamp = time.time_ns()
    Replacing time.time_ns(), as time_ns() was new in python 3.7
    see also: https://github.com/raysect/source/issues/303 (2020-05-11)
    """
    time.sleep(milliseconds / 1000)


frequency = range(0, 1000, 1)
# for step in frequency:
#    print(step)
# print(frequency[2])

rows = 49  # the resolution of the y-axis in a carthesian coordinate system
columns = 67  # the resolution of the x-axis in a carthesian coordinate system


def createVisualizationMatrix(matrix):
    visualization = []

    for i in range(int(rows)):  # loop as many times as variable rows

        r = []  # create a row list

        for j in range(int(columns)):  # loop as many times as variable columns
            r.append(matrix[i][j].get_color_state())

        visualization.append(r)

    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
    visualization.pop(48)
    visualization.append(x)
    return visualization


def testString(matrix):
    visualization = []

    for i in range(int(rows)):  # loop as many times as variable rows

        r = []  # create a row list

        for j in range(int(columns)):  # loop as many times as variable columns
            r.append(matrix[i][j].getState())
            if matrix[i][j].celltype == Celltype.SINUS_KNOT:
                print("is triggered") if matrix[i][j].isTriggered else print("Is not triggered")
                print(matrix[i][j].getState())

        visualization.append(r)

    for line in visualization:
        print(line)

    NeighbourIsDepolarized = False
    row = 14
    column = 19
    # neighbourhood: Moore
    north = 13 if 13 in range(len(matrix)) else row
    south = 15 if 15 in range(len(matrix)) else row
    east = 20 if 20 in range(len(matrix[row])) else column
    west = 18 if 18 in range(len(matrix[row])) else column

    # for all 8 neighbours: check if they are depolirated (if they exist)#
    if matrix[north][column].getState() == 3: NeighbourIsDepolarized = True
    print("North is", matrix[north][column].getState())
    if matrix[north][east].getState() == 3: NeighbourIsDepolarized = True
    print("North-east is", matrix[north][east].getState())
    if matrix[row][east].getState() == 3: NeighbourIsDepolarized = True
    print("East is", matrix[row][east].getState())
    if matrix[south][east].getState() == 3: NeighbourIsDepolarized = True
    print("South-East is", matrix[south][east].getState())
    if matrix[south][column].getState() == 3: NeighbourIsDepolarized = True
    print("South is", matrix[south][column].getState())
    if matrix[south][west].getState() == 3: aNeighbourIsDepolarized = True
    print("South-west is", matrix[south][west].getState())
    if matrix[row][west].getState() == 3: NeighbourIsDepolarized = True
    print("West is", matrix[row][west].getState())
    if matrix[north][west].getState() == 3: NeighbourIsDepolarized = True
    print("North-west is", matrix[north][west].getState())

    return visualization


heart = Heart()

# create initial state of visualization
#heartVis = createVisualizationMatrix(heart.heart)

# initial settings for plot
plt.title("Cellular Automaton of the Heart")
plt.axis('off')
plt.imshow(image, extent=extent)

# initializing plot
fig = plt.gcf()

# Show first image - which is the initial board
#im = plt.imshow(heartVis, extent=extent, cmap=cmap, alpha=0.8)


# Helper function that updates visualization -> function that FuncAnimation calls
"""
def animate(frame):
    heart.step()
    im.set_data(createVisualizationMatrix(heart.heart))
    return im
"""

# actual animation
#anim = animation.FuncAnimation(fig, animate, frames=1, interval=1)
#plt.show()

visualizationStorage = []


for miliSec in range(1, 801, 1):
    heart.step()
    visualizationStorage.append(createVisualizationMatrix(heart.heart))
    print("step: " , miliSec)


heartVis = visualizationStorage[0]
im = plt.imshow(heartVis, extent=extent, cmap=cmap, alpha=0.8)

def animate(frame):
    im.set_data(visualizationStorage[frame])
    return im


# actual animation
anim = animation.FuncAnimation(fig, animate, frames=800, interval=1)
plt.show()




# LOOP
#while True:
    # print( [ [1,2], [3,4] ] )
    # print(heart.test())
   # testString(heart.heart)
    #heart.step()
    #delay_ms(1000)

# print (heart.heart[0][0].stateMachine.currentState.stateName)
# test anna
# for step in frequency:
#    if(step == 10):
#        cell_test = Cell(1,-70)
#        cell_test.trigger(step)
#        print("stop")
