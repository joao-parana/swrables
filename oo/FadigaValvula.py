# -*- coding: utf-8 -*-


import numpy as np
import os
import ErrorHandle as EH
import sys
from iapws import IAPWS97
from math import *
from scipy.integrate import quad
from scipy.interpolate import interp1d
from scipy.misc import derivative
from scipy.optimize import fsolve
from scipy import optimize
from numpy.linalg import inv
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from Fadiga import*

class FadigaValvula(Fadiga):

    def __init__(self, currentDir, fileName):

        Fadiga.__init__(self, currentDir, fileName)
        #FluenciaValvula.__init__(self, currentDir, fileName)

        self.Tstart = 0
        self.Tend = 0
        self.NuV = 0

