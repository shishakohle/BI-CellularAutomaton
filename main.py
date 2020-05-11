"""
TODO: Some comments on this project.
"""

from Heart import Heart
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import time
import matplotlib.animation as animation


# colormap
cmap = colors.ListedColormap(['#FFFFFF', '#E9967A','#8B0000', '#AB82FF', '#5D478B', '#A2CD5A', '#556B2F', '#87CEFA',
                              '#00008B', '#FFFF00', '#8B8B00', '#FF8C00', '#8B4500'])
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


def wait(milliseconds):
    threshold = time.time_ns() + milliseconds * 1000000

    while time.time_ns() < threshold:
        pass


frequency = range(0, 1000, 1)
#for step in frequency:
#    print(step)
#print(frequency[2])

rows = 49  # the resolution of the y-axis in a carthesian coordinate system
columns = 67  # the resolution of the x-axis in a carthesian coordinate system

def createVisualizationMatrix(matrix):
    visualization = []

    for i in range(int(rows)):  # loop as many times as variable rows

        r = []  # create a row list

        for j in range(int(columns)):  # loop as many times as variable columns
            r.append(matrix[i][j].get_color_state())

        visualization.append(r)

    return visualization

heart = Heart()

# create initial state of visualization
heartVis = createVisualizationMatrix(heart.heart)

# initial settings for plot
plt.title("Cellular Automata of the Heart")
plt.axis('off')
plt.imshow(image, extent=extent)

# initializing plot
fig = plt.gcf()

# Show first image - which is the initial board
im = plt.imshow(heartVis, extent=extent, cmap=cmap, alpha= 0.7)


# Helper function that updates visualization -> function that FuncAnimation calls
def animate(frame):
    im.set_data(createVisualizationMatrix(heart.heart))
    return im


# actual animation
anim = animation.FuncAnimation(fig, animate, frames=200, interval=50)

plt.show()

# LOOP
#while True:
   #heart.step()
   # wait(1)



#test anna
#for step in frequency:
#    if(step == 10):
#        cell_test = Cell(1,-70)
#        cell_test.trigger(step)
#        print("stop")
