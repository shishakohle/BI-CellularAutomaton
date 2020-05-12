from Cell import *

import os
import csv
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation


class Heart:
    def __init__(self):  # constructor
        # TODO read count of rows and columns from CSV directly
        self.rows = 49  # the resolution of the y-axis in a carthesian coordinate system
        self.columns = 67  # the resolution of the x-axis in a carthesian coordinate system
        self.heart = self.init_matrix()
        # self.visualization = self.createVisualizationMatrix(self.heart)
        self.simulationSamples = []

    def init_matrix(self):
        matrix = []

        with open("heart.csv", 'r') as f:  # TODO filename as function argument
            heart = list(csv.reader(f, delimiter=";"))  # TODO check: what if open() has failed for some reason?

        # TODO read count of rows and columns from CSV directly

        for i in range(int(self.rows)):  # loop as many times as variable rows

            r = []  # create a row list

            for j in range(int(self.columns)):  # loop as many times as variable columns

                # TODO replace the if-elif tree by a switcher. Such a switcher already exists in Cell.
                if heart[i][j] == '0':
                    no_heart_cell = Cell(Celltype.NO_HEART_CELL)
                    r.append(no_heart_cell)
                elif heart[i][j] == '1':
                    right_atrium = Cell(Celltype.RIGHT_ATRIUM)
                    r.append(right_atrium)
                elif heart[i][j] == '2':
                    sinus_knot = Cell(Celltype.SINUS_KNOT)
                    sinus_knot.trigger()  # sine knot immediately triggered.
                    r.append(sinus_knot)
                elif heart[i][j] == '3':
                    av_knot = Cell(Celltype.AV_KNOT)
                    r.append(av_knot)
                elif heart[i][j] == '4':
                    his_bundle = Cell(Celltype.HIS_BUNDLE)
                    r.append(his_bundle)
                elif heart[i][j] == '5':
                    tawara = Cell(Celltype.TAWARA)
                    r.append(tawara)
                elif heart[i][j] == '6':
                    purkinje = Cell(Celltype.PURKINJE)
                    r.append(purkinje)
                elif heart[i][j] == '7':
                    left_atrium = Cell(Celltype.LEFT_ATRIUM)
                    r.append(left_atrium)
                elif heart[i][j] == '8':
                    myokard = Cell(Celltype.MYOKARD)
                    r.append(myokard)

            matrix.append(r)  # add the rows filled with columns to existing matrix list

        return matrix

    def currentSample(self):
        sample = []

        for i in range(int(self.rows)):  # loop as many times as variable rows

            r = []  # create a row list

            for j in range(int(self.columns)):  # loop as many times as variable columns
                r.append(self.heart[i][j].get_color_state())

            sample.append(r)

        # add the whole color map to sample (plot needs each color present at last once in each sample)
        x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
             7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
        # sample.pop()
        # sample.append(x)
        sample.pop(0)
        sample.insert(0, x)

        return sample

    def simulateCycle(self):
        simSteps = 800  # total of simulation steps TODO: hardcoded. maybe take this is a paramter?
        for step in range(simSteps):
            print("simulating heart cycle ... [ sample", step + 1, "of", simSteps, "|", int((step+1)/simSteps*100),
                  "% completed ]")
            self.simulationSamples.append(self.currentSample())
            self.step()

    def plotSimulation(self):
        # colormap
        cmap = colors.ListedColormap(['#2e4a1e', '#00baff', '#000b34', '#fff313', '#7b7b00', '#fcc926', '#bf7600',
                                      '#FFFFFF', '#E9967A', '#8B0000', '#605acd', '#3e135e', '#A2CD5A'])
        boundaries = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        norm = colors.BoundaryNorm(boundaries, cmap.N, clip=True)

        # scale image and matrix
        dx, dy = 0.05, 0.05
        x = np.arange(0, self.columns, dx)
        y = np.arange(0, self.rows, dy)
        X, Y = np.meshgrid(x, y)
        extent = np.min(X), np.max(X), np.min(Y), np.max(Y)

        # initialize plot
        # initial settings for plot
        plt.title("Cellular Automaton of the Heart")
        plt.axis('off')
        image = plt.imread("heart.png")  # TODO: what if file could not be read?
        plt.imshow(image, extent=extent)  # TODO: what if image could not be read?
        fig = plt.gcf()

        im = plt.imshow(self.simulationSamples[0], extent=extent, cmap=cmap, alpha=0.8)

        def animate(frame):
            im.set_data(self.simulationSamples[frame])
            return im

        # actual animation
        anim = animation.FuncAnimation(fig, animate, frames=800, interval=1)
        plt.show()

        return

    def step(self):  # one step transits the heart simulation 1 time step ahead

        for row in range(9,len(self.heart),1):
            for column in range(13,55,1):

                if self.heart[row][column].celltype == Celltype.HIS_BUNDLE:
                    # trigger if: (1) all AV knots are depolarized and (2) neighbourhood contains an depolarized cell
                    if self.allDepolarized(Celltype.AV_KNOT) and self.aNeighbourIsDepolarized(row, column):
                        self.heart[row][column].trigger()

                elif self.heart[row][column].celltype == Celltype.MYOKARD:
                    # trigger if all Purkinje Fibres are depolarized
                    if self.allDepolarized(Celltype.PURKINJE):
                        self.heart[row][column].trigger()

                elif self.heart[row][column].celltype != Celltype.NO_HEART_CELL:
                    # trigger if neighbourhood contains an depolarized cell
                    if self.aNeighbourIsDepolarized(row, column):
                        self.heart[row][column].trigger()

                self.heart[row][column].step()

    def aNeighbourIsDepolarized(self, row, column):
        aNeighbourIsDepolarized = False

        # neighbourhood: Moore
        north = row-1 if row-1 in range(len(self.heart)) else row
        south = row+1 if row+1 in range(len(self.heart)) else row
        east = column+1 if column+1 in range(len(self.heart[row])) else column
        west = column-1 if column-1 in range(len(self.heart[row])) else column

        # for all 8 neighbours: check if they are depolirated (if they exist)#
        if self.heart[north][column].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[north][east].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[row][east].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[south][east].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[south][column].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[south][west].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[row][west].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[north][west].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True

        return aNeighbourIsDepolarized

    def allDepolarized(self, cellytpe):
        allDepolarized = True

        for row in range(21,len(self.heart),1):
            for column in range(19,53,1):

                if self.heart[row][column].celltype == cellytpe:
                    if self.heart[row][column].getState() != 3: allDepolarized = False

        return allDepolarized
