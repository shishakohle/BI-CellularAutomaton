"""
TODO: Some comments on this project.
"""

from Heart import Heart

import numpy as np
import time

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation





def animate(frame):
    im.set_data(visualizationStorage[frame])
    return im


def delay_ms(milliseconds):
    time.sleep(milliseconds / 1000)


# colormap
cmap = colors.ListedColormap(['#2e4a1e', '#00baff', '#000b34', '#fff313', '#7b7b00', '#fcc926', '#bf7600',
                              '#FFFFFF', '#E9967A', '#8B0000', '#605acd', '#3e135e', '#A2CD5A'])
boundaries = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
norm = colors.BoundaryNorm(boundaries, cmap.N, clip=True)

# scale image and matrix
dx, dy = 0.05, 0.05
x = np.arange(0, 67, dx)
y = np.arange(0, 49, dy)
X, Y = np.meshgrid(x, y)
extent = np.min(X), np.max(X), np.min(Y), np.max(Y)

image = plt.imread("heart.png")

frequency = range(0, 1000, 1)

rows = 49  # the resolution of the y-axis in a carthesian coordinate system
columns = 67  # the resolution of the x-axis in a carthesian coordinate system

heart = Heart()

# initial settings for plot
plt.title("Cellular Automaton of the Heart")
plt.axis('off')
plt.imshow(image, extent=extent)

# initializing plot
fig = plt.gcf()

visualizationStorage = []

heartVis = visualizationStorage[0]
im = plt.imshow(heartVis, extent=extent, cmap=cmap, alpha=0.8)

# actual animation
anim = animation.FuncAnimation(fig, animate, frames=800, interval=1)
plt.show()
