"""
    BI-CellularAutomaton - A graphical model for the excitation propagation
    at the myocardium, implemented as a Cellular Automaton.
    Copyright (C) 2020  Anna Friedl, Kerstin Pegler, Ingo Weigel

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see https://www.gnu.org/licenses/ .
"""
"""
BI-CellularAutomaton

A graphical model for the excitation propagation at the myocardium,
implemented as a Cellular Automaton in Python.

Written by Anna Friedl, Kerstin Pegler and Ingo Weigel.

May 13th, 2020

Find this project on GitHub: https://github.com/shishakohle/BI-CellularAutomaton

This project was carried out in the "Bioinformatics" course at
University of Applied Sciences Technikum Wien (Vienna, Austria)
under the guidance of lecturer Mariia Gonta.
"""

from model.Heart import Heart

heart = Heart()
heart.simulateCycle()
heart.createSimulationGIF()
heart.plotSimulation()
