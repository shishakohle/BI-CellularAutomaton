class Heart:
    def __init__(self):
        self.cells = []
        self.reset()

    def reset(self):
        polarizedCell = Heart.Cell(1, 0, Heart.Cell.Polarization.POLARIZED)
        CellRow = [polarizedCell, polarizedCell, polarizedCell]
        self.cells.append(CellRow)
        self.cells.append(CellRow)
        self.cells.append(CellRow)
        print(self.cells)
        print(self.cells[0][0].delay)
        print(self.cells[2][1].delay)
        self.cells[0][0].delay = 5
        print(self.cells[0][0].delay)
        print(self.cells[2][1].delay)

    def step(self):
        return 0

    class Cell:
        def __init__(self, density, delay, polarization):
            self.density = density
            self.polarization = polarization
            self.delay = delay

        class Polarization:
            POLARIZED = 1
            DEPOLARIZED = 2
            REFRACTORY = 3
