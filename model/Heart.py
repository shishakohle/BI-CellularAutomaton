from model.Cell import *

import csv
import time
import imageio
import numpy as np
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation


class Heart:
    def __init__(self):  # constructor
        # TODO read count of rows and columns from CSV directly
        self.rows = 49  # the resolution of the y-axis in a carthesian coordinate system
        self.columns = 67  # the resolution of the x-axis in a carthesian coordinate system
        self.heart = self.initialHeartMatrix()
        self.simulationSamples = []

    def initialHeartMatrix(self):
        matrix = []

        with open("./resources/heart.csv", 'r') as f:  # TODO filename as function argument
            heart = list(csv.reader(f, delimiter=";"))  # TODO check: what if open() has failed for some reason?

        # TODO read count of rows and columns from CSV directly

        for i in range(int(self.rows)):  # loop as many times as variable rows

            r = []  # create a row list

            for j in range(int(self.columns)):  # loop as many times as variable columns

                # TODO replace the if-elif tree by a switcher.
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
        # --> we'll exploit this circumstance as a plot legend indicating the celltypes by color

        def drawLegend(celltype, positionX, positionY):
            row = sample.pop(positionY)
            row.pop(positionX)
            row.insert(positionX, Cell.color_state_polarized[celltype])
            row.pop(positionX+1)
            row.insert(positionX+1, Cell.color_state_depolarized[celltype])
            sample.insert(positionY, row)

        drawLegend(Celltype.SINUS_KNOT, 49, 6 )  # draw legend for sine knot
        drawLegend(Celltype.AV_KNOT   , 49, 8 )  # draw legend for AV node
        drawLegend(Celltype.HIS_BUNDLE, 49, 10)  # draw legend for his bundle
        drawLegend(Celltype.TAWARA    , 49, 12)  # draw legend for tawara (bundle branches)
        drawLegend(Celltype.PURKINJE  , 49, 14)  # draw legend for purkinje fibres
        drawLegend(Celltype.MYOKARD   , 49, 16)  # draw legend for muscle cells

        return sample

    def simulateCycle(self):
        simSteps = 1000  # total of simulation steps TODO: hardcoded. maybe take this is a parameter?
        timestamp = time.time()

        for step in range(simSteps):
            print("simulating heart cycle ... [ sample", step + 1, "of", simSteps, "|", int((step+1)/simSteps*100),
                  "% complete ]")
            self.simulationSamples.append(self.currentSample())
            self.step()

        duration = time.time() - timestamp
        print("simulating heart cycle ... [ complete. (", int(duration/60), "min", int(duration % 60), "sec ) ]")

        # TODO: take destination path as a parameter
        np.save("./simulations/heart_cycle.npy", self.simulationSamples)    # TODO: create directory if it does not exist
        # TODO: what if file could not be saved? and: files will be overwritten -> ok?
        filesize = Path("./simulations/heart_cycle.npy").stat().st_size  # file size in bytes
        print("simulating heart cycle ... [ saved samples to file (", "{:.2f}".format(filesize/1000000), "MB ) ]")
        # TODO: compress file (e.g. one test run resulted in a file of 21.01 MB, but 214 kB if zipped)

    def plotSimulation(self):
        boundaries = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        norm = colors.BoundaryNorm(boundaries, Cell.cmap.N, clip=True)

        # scale image and matrix
        dx, dy = 0.05, 0.05
        x = np.arange(0, self.columns, dx)
        y = np.arange(0, self.rows, dy)
        X, Y = np.meshgrid(x, y)
        extent = np.min(X), np.max(X), np.min(Y), np.max(Y)

        # initialize plot
        plt.title("Cellular Automaton of the Heart")
        plt.axis('off')
        image = plt.imread("./resources/Conductive System of the Heart_background.png")  # TODO: what if file could not be read?
        plt.imshow(image, extent=extent)  # TODO: what if image could not be read?
        fig = plt.gcf()

        # plot the first sample
        im = plt.imshow(self.simulationSamples[0], extent=extent, cmap=Cell.cmap, alpha=0.6)

        # inner helper for animation, interates over samples
        def animate(frame):
            im.set_data(self.simulationSamples[frame])
            return im

        # actual animation
        anim = animation.FuncAnimation(fig, animate, frames=len(self.simulationSamples), interval=1)
        plt.show()

    def createSimulationGIF(self):
        frames = []
        timestamp = time.time()

        for i in range(0, len(self.simulationSamples), 20):

            print("creating simulation GIF ... [ sample", i + 1, "of", len(self.simulationSamples), "|",
                  int((i + 1) / len(self.simulationSamples) * 100), "% complete ]")

            image = np.array(self.simulationSamples[i])
            # create new array of zeros, 10 times bigger than actual image array
            resized_image = np.zeros(np.array(image.shape) * 10)

            # fill resized_image with data of actual image, but resize it 10 times
            for j in range(image.shape[0]):
                for k in range(image.shape[1]):
                    resized_image[j * 10: (j + 1) * 10, k * 10: (k + 1) * 10] = image[j, k]

            filename = './simulations/GIF_frames/frame' + str(i) + '.png'  # TODO: create directory if it does not exist
            plt.imsave(filename, resized_image, cmap=Cell.cmap)  # TODO: what if file could not be saved?
            frames.append(imageio.imread(filename))
            # TODO remove file, as it's not needed any longer

        # TODO remove gif frame directory, as it's not needed any longer

        duration = time.time() - timestamp
        print("creating simulation GIF ... [ complete. (", int(duration/60), "min", int(duration % 60), "sec ) ]")

        # TODO: take destination path as a parameter
        imageio.mimsave('./simulations/heart_simulation.gif', frames)
        # TODO: what if file could not be saved? and: files will be overwritten -> ok?
        filesize = Path('./simulations/heart_simulation.gif').stat().st_size  # file size in bytes
        print("creating simulation GIF ... [ saved GIF to file (", "heart_simulation.gif", ", {:.2f}".format(filesize / 1000), "kB ) ]")

    def step(self):  # one step transits the heart simulation 1 time step ahead

        for row in range(9, len(self.heart), 1):  # iterate only over rows where cells change their state (efficiency)
            for column in range(13, 55, 1):  # iterate only over columns where cells change their state (efficiency)

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
        north = row    - 1 if row    - 1 in range(len(self.heart))      else row
        south = row    + 1 if row    + 1 in range(len(self.heart))      else row
        east  = column + 1 if column + 1 in range(len(self.heart[row])) else column
        west  = column - 1 if column - 1 in range(len(self.heart[row])) else column

        # for all 8 neighbours: check if they are depolarized (if they exist)
        if self.heart[north][column].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[north][east]  .getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[row]  [east]  .getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[south][east]  .getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[south][column].getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[south][west]  .getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[row]  [west]  .getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True
        if self.heart[north][west]  .getState() == StateName.DEPOLARIZED: aNeighbourIsDepolarized = True

        return aNeighbourIsDepolarized

    def allDepolarized(self, cellytpe):
        allDepolarized = True

        # iterate only over cells where we actually will check on allDepolarized (efficiency)
        for row in range(21, len(self.heart), 1):
            for column in range(19, 53, 1):

                if self.heart[row][column].celltype == cellytpe:
                    if self.heart[row][column].getState() != StateName.DEPOLARIZED: allDepolarized = False

        return allDepolarized
