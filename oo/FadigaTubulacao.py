# -*- coding: utf-8 -*-


import numpy as np
import os
import ErrorHandle as EH
import sys
from iapws import IAPWS97
from math import *
from scipy.integrate import quad
from scipy.interpolate import interp1d, interp2d
from scipy.misc import derivative
from scipy.optimize import fsolve
from scipy.integrate import ode
from scipy import optimize
from numpy.linalg import inv
import matplotlib.pyplot as plt
from Fadiga import*


class FadigaTubulacao(Fadiga):

    def __init__(self, currentDir, fileName):
        Fadiga.__init__(self, currentDir, fileName)

















