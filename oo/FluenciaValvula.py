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

class FluenciaValvula(Fluencia):

    def __init__(self, currentDir, fileName):
        Fluencia.__init__(self, currentDir, fileName)


        self.Tmint = []
        self.Tmext = []
        self.TmetalintFiltro1 = []
        self.TmetalextFiltro1 = []
        self.TmetalintFiltro2 = []
        self.TmetalextFiltro2 = []
        self.TmetalintSM = 0
        self.TmetalextSM = 0
        self.TmetalIntMedia = 0
        self.TmetalExtMedia = 0
        self.tensaoPLMvalv = []
        self.PLMvalv = []
        self.hext = 16.0










