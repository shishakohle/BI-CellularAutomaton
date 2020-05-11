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


def delay_ms(milliseconds):
    """
    # timestamp = time.time_ns()
    Replacing time.time_ns(), as time_ns() was new in python 3.7
    see also: https://github.com/raysect/source/issues/303 (2020-05-11)
    """
    time.sleep(milliseconds/1000)


while True:
    # plt.imshow(image, extent=extent)
    # plt.show()
    # plt.clf()

    myHeart.step()
    print("ping")
    delay_ms(5000)
