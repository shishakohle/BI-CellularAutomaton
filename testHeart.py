from Heart import Heart
import time
import matplotlib.pyplot as plt
import numpy as np


# scale image and matrix
dx, dy = 0.05, 0.05
x = np.arange(0, 67, dx)
y = np.arange(0, 49, dy)
X, Y = np.meshgrid(x, y)
extent = np.min(X), np.max(X), np.min(Y), np.max(Y)

myHeart = Heart()
image = plt.imread("heart.png")


def wait(milliseconds):
    threshold = time.time_ns() + milliseconds * 1000000

    while time.time_ns() < threshold:
        pass


while True:
    # myHeart.step()
    plt.imshow(image, extent=extent)
    plt.show()
    wait(1000)
    plt.clf()
    wait(1000)





