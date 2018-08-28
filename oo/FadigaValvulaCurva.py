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

from FadigaValvula import*



class FadigaValvulaCurva(FadigaValvula):

    def __init__(self, currentDir, fileName):
        FadigaValvula.__init__(self, currentDir, fileName)



    def JustDoItFadValvCurv(self):

        (fadVC.arquivoEntrada, fadVC.arquivoSaida, fadVC.arquivoControle) = fadVC.setupNameFileInputParams(
            fadVC.currentDir, fadVC.fileName)
        (fadVC.tempoOperacaoBase, fadVC.tempo, fadVC.Vv, fadVC.pv, fadVC.Tv, fadVC.Tmint,
         fadVC.Tmext) = fadVC.setupInputParams(fadVC.arquivoEntrada, fadVC.tempo, fadVC.Vv, fadVC.pv, fadVC.Tv,
                                               fadVC.Tmint, fadVC.Tmext)

        fadVC.flag0()

        fadVC.Vv = fadVC.medSmoothParams(fadVC.Vv)
        fadVC.pv = fadVC.medSmoothParams(fadVC.pv)
        fadVC.Tv = fadVC.medSmoothParams(fadVC.Tv)
        fadVC.Tmint = fadVC.medSmoothParams(fadVC.Tmint)
        fadVC.Tmext = fadVC.medSmoothParams(fadVC.Tmext)





    @staticmethod
    def create():
        # currentDir = 'C:\\SOMATURBODIAG\\valvulacurva\\'
        currentDir = os.getcwd() + '/../DATA/valvulacurva/'
        if platform.system() == "Windows":
            currentDir = '..\\valvulacurva\\'

        fileName = 'controle_fadiga.txt'

        return FadigaValvulaCurva(currentDir, fileName)



# fadVC = touchObjectFadValvCurv()
# fadVC.JustDoItFadValvCurv()


