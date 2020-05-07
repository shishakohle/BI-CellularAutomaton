"""
TODO: Some comments on this project.
"""

from Heart import Heart
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors

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

frequency = range(0, 1000, 1)
#for step in frequency:
#    print(step)
#print(frequency[2])

#myHeart = Heart()

heart = Heart()

# plt.clf() clears window

plt.imshow(image, extent=extent)
plt.imshow(heart.heart, extent=extent, cmap=cmap, alpha= 0.7)
#plt.imshow(heart.getState(), extent=extent, cmap="Reds", alpha= 0.7)
plt.title("Cellular Automata of the Heart")
# TODO: remove axis labels
plt.show()

#test anna
#for step in frequency:
#    if(step == 10):
#        cell_test = Cell(1,-70)
#        cell_test.trigger(step)
#        print("stop")
