# -*- coding: utf-8 -*-


import numpy as np
import os
import ErrorHandle as EH
import sys
from iapws import IAPWS97
from math import *
from scipy.integrate import quad
from scipy.interpolate import interp1d
from Fluencia import*



class FluenciaTubulacao(Fluencia):

    def __init__(self, currentDir, fileName):
        Fluencia.__init__(self, currentDir, fileName)


















