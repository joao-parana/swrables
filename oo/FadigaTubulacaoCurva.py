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
from Fluencia import*
from FadigaRotor import*
from FluenciaTubulacao import*
from FadigaTubulacao import*


class FadigaTubulacaoCurva(FadigaTubulacao):

    def __init__(self, currentDir, fileName):
        FadigaTubulacao.__init__(self, currentDir, fileName)





    def JustDoItFadTubCurva(self):

        (fadTC.arquivoEntrada, fadTC.arquivoSaida, fadTC.arquivoControle) = fadTC.setupNameFileInputParams(fadTC.currentDir, fadTC.fileName)
        (fadTC.numeroCiclosFadiga, fadTC.tempo, fadTC.Vv, fadTC.pv, fadTC.Tv) = fadTC.setupInputParams(fadTC.arquivoEntrada, fadTC.tempo, fadTC.Vv, fadTC.pv, fadTC.Tv)

        fadTC.flag0()
        
        fadTC.Vv = fadTC.medSmoothParams(fadTC.Vv)
        fadTC.pv = fadTC.medSmoothParams(fadTC.pv)
        fadTC.Tv = fadTC.medSmoothParams(fadTC.Tv)

        fadTC.indiceInicioTransiente = fadTC.getStartIndexTrans(fadTC.Tv, 5, 200, 20)
        fadTC.indiceFimTransiente = fadTC.getEndIndexTrans(fadTC.Tv, 5, 520, 1)  # indiceFimTransiente esta dando 0, era pra dar -1, isso esta ocorrendo talvez
                                                                                 # por um pos + 1 na funçao getEndIndexTrans

        fadTC.checkParamsForFlu('Fadiga', 'Tubulacao')
        fadTC.flag5()

        (fadTC.matVazao, fadTC.matPressao, fadTC.matTemperatura) = fadTC.setMats()
        fadTC.indiceInicioTemperatura = fadTC.getIndex(fadTC.Tv, 0, 5, 20)
        fadTC.indiceInicioPressao = fadTC.getIndex(fadTC.pv, 0, 5, 0.75) ## Avisar para Bruno a diferença nesses filtros!!!!
        fadTC.indiceInicioVazao = fadTC.getIndex(fadTC.Vv, 0, 5, 20)

        (fadTC.tVazao, fadTC.matVazaoMod, fadTC.tTemperatura, fadTC.matTemperaturaMod, fadTC.tPressao,
         fadTC.matPressaoMod, fadTC.nmaxElem, fadTC.tmin) = fadTC.matMods(fadTC.indiceInicioVazao,
                                                                          fadTC.indiceInicioTemperatura,
           
                                                                          fadTC.indiceInicioPressao)
        
        # Somar -1 a nmaxElem pode resolver a questao do tStart em cascata!!!!!!!!!!!
        # Fazer esse teste depois.

        
        fadTC.matPressaoModModificado = fadTC.modifica(len(fadTC.matPressaoMod[0]), fadTC.tmin, fadTC.matPressaoMod)
        fadTC.matVazaoModModificado = fadTC.modifica(len(fadTC.matVazaoMod[0]), fadTC.tmin,
                                                     fadTC.matVazaoMod)  # Os valores de vazao nao estao batendo nada!!!!!
        fadTC.matTemperaturaModModificado = fadTC.modifica(len(fadTC.matTemperaturaMod[0]), fadTC.tmin,
                                                           fadTC.matTemperaturaMod)

        (fadTC.tempo, fadTC.pv, fadTC.Tv) = (
            fadTC.matVazaoModModificado[0], fadTC.matPressaoModModificado[1], fadTC.matTemperaturaModModificado[1])
        fadTC.Vv = fadTC.convertVazao(fadTC.matVazaoModModificado[1])
        fadTC.tempo = fadTC.min2sList(fadTC.tempo)

        fadTC.indiceInicioTransiente = fadTC.getStartIndexTrans(fadTC.Tv, 5, 200, 20)
        fadTC.indiceFimTransiente = fadTC.getEndIndexTrans(fadTC.Tv, 5, 520, 0.029)

        # falar com o Bruno sobre o indiceFimTransiente no código do mathcad


        fadTC.instanteInicioTransiente = fadTC.setStartInstantTrans()
        fadTC.instanteFimTransiente = fadTC.setEndInstantTrans()
        fadTC.temperaturaInicioTransiente = fadTC.setStartTempTrans(fadTC.Tv)
        fadTC.temperaturaFimTransiente = fadTC.setEndTempTrans(fadTC.Tv)

        fadTC.tStart = fadTC.instanteInicioTransiente
        fadTC.tEnd = fadTC.instanteFimTransiente

        (fadTC.Vstart, fadTC.Vend) = fadTC.vazaoStartEnd(fadTC.indiceInicioTransiente, fadTC.indiceFimTransiente)

        (fadTC.tempoFiltro1, fadTC.VvaporFiltro1, fadTC.PvaporFiltro1, fadTC.TvaporFiltro1) = fadTC.filtro1('Fadiga',
                                                                                                            fadTC.tempo,
                                                                                                            fadTC.Vv,
                                                                                                            fadTC.pv,
                                                                                                            fadTC.Tv)
        fadTC.flag1()

        (fadTC.duracaoPartidaSM, fadTC.variacaoTemperaturaVaporSM) = fadTC.calcVariacoesTubValv()

        fadTC.flag2()

        (fadTC.TemperaturaPropMec, fadTC.moduloElasticidade, fadTC.coefExpansaoTerm, fadTC.condutividadeTerm,
         fadTC.calorEspecificoPcte) = fadTC.getPropMec()
        (fadTC.TemperaturaCoefPoisson, fadTC.CoefPoisson) = fadTC.getCoefPoisson()
        (fadTC.amplitudeTensao, fadTC.amplitudeDeformacao) = fadTC.getCurva(fadTC.fileNameCurvaAmpTensaovsAmpDeformacao)
        (fadTC.amplitudeDeformacaoNR, fadTC.Nf25) = fadTC.getCurva(fadTC.fileNameCurvaAmpDeformacaovsNf25)

        fadTC.Paramslist2arrayMH('Fadiga', 'Tubulacao')

        (fadTC.Dint, fadTC.Rint, fadTC.Dext, fadTC.Rext, fadTC.rc, fadTC.t, fadTC.f1,
         fadTC.f2) = fadTC.setGeometriaTubulacao()

        fadTC.hiStart = fadTC.hi(fadTC.tStart)
        fadTC.hiEnd = fadTC.hi(fadTC.tEnd)

        (fadTC.h0, fadTC.Tar, fadTC.Tint, fadTC.Text, fadTC.C1) = fadTC.initVariaveis(fadTC.instanteInicioTransiente)

        sol = optimize.root(self.Fun, [-400, 196, 192], jac=self.jac, method='hybr')
        (fadTC.sol1, fadTC.sol2, fadTC.sol3) = (sol.x[0], sol.x[1], sol.x[2])

        fadTC.alfaEq = fadTC.alfaEqs(650)

        fadTC.talStart = fadTC.tal(fadTC.alfaEq, fadTC.tStart, fadTC.mm2m(fadTC.Rext))
        fadTC.talEnd = fadTC.tal(fadTC.alfaEq, fadTC.tEnd, fadTC.mm2m(fadTC.Rext))




        # Tudo OK ate aqui!


        # Implementaçao do algoritmo de resoluçao da EDP

    @staticmethod
    def create():
        # currentDir = 'C:\\SOMATURBODIAG\\tubulacaocurva\\'
        currentDir = os.getcwd() + '/../DATA/tubulacaocurva/'
        if platform.system() == "Windows":
            currentDir = '..\\tubulacaocurva\\'

        fileName = 'controle_fadiga.txt'

        return FadigaTubulacaoCurva(currentDir, fileName)

# fadTC = touchObjectFadTubCurva()
# fadTC.JustDoItFadTubCurva()
