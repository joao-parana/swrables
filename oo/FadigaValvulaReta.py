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


class FadigaValvulaReta(FadigaValvula):

    def __init__(self, currentDir, fileName):

        FadigaValvula.__init__(self, currentDir, fileName)
        

    def JustDoItFadValvReta(self, arrayAux2, fatigueCycles, operationTime):
        # (self.arquivoEntrada, self.arquivoSaida, self.arquivoControle) = self.setupNameFileInputParams(self.currentDir, self.fileName)


        try:
            (self.tempo, self.Vv, self.pv, self.Tv, self.Tmint, self.Tmext) = self.setupInputParamsFromSoma(arrayAux2, self.tempo, self.Vv, self.pv, self.Tv, self.Tmint, self.Tmext)
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o sistema!' + '\n' + 'O dano por fadiga na tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'

            self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(
                self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Reta']['Fadiga'] = strOut
            MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Curva']['Fadiga'] = strOut

            return

        self.numeroCiclosFadiga = fatigueCycles
        # self.flag0()
        self.Vv = self.medSmoothParams(self.Vv)
        self.pv = self.medSmoothParams(self.pv)
        self.Tv = self.medSmoothParams(self.Tv)
        self.Tmint = self.medSmoothParams(self.Tmint)
        self.Tmext = self.medSmoothParams(self.Tmext)

        errorCode = self.firstBlock('Fadiga', 'Valvula', 'Reta')
        errorCode = self.firstBlock('Fadiga', 'Valvula', 'Curva')

        if errorCode > 0:
            return

        self.indiceInicioTransiente = self.getStartIndexTrans(self.Tv, 5, 200, 25)
        self.indiceFimTransiente = self.getEndIndexTrans(self.Tv, 5, 520, 1, self.indiceInicioTransiente)





        (self.matVazao, self.matPressao, self.matTemperatura) = self.setMats()
        self.indiceInicioTemperatura = self.getIndex(self.Tv, 0, 5, 20)
        self.indiceInicioPressao = self.getIndex(self.pv, 0, 2, 0.75)
        self.indiceInicioVazao = self.getIndex(self.Vv, 0, 2, 20)

        errorCode = self.checkParamsForFlu('Fadiga', 'Valvula', 'Reta')
        errorCode = self.checkParamsForFlu('Fadiga', 'Valvula', 'Curva')

        if errorCode > 0:
            return

        # self.flag5()

        try:

            (self.tVazao, self.matVazaoMod, self.tTemperatura, self.matTemperaturaMod, self.tPressao,
             self.matPressaoMod, self.nmaxElem, self.tmin) = self.matMods(self.indiceInicioVazao,
                                                                              self.indiceInicioTemperatura,
                                                                              self.indiceInicioPressao)

            self.matPressaoModModificado = self.modifica(len(self.matPressaoMod[0]), self.tmin, self.matPressaoMod)
            self.matVazaoModModificado = self.modifica(len(self.matVazaoMod[0]), self.tmin,
                                                         self.matVazaoMod)
            self.matTemperaturaModModificado = self.modifica(len(self.matTemperaturaMod[0]), self.tmin,
                                                               self.matTemperaturaMod)

            (self.tempo, self.pv, self.Tv) = (
                self.matVazaoModModificado[0], self.matPressaoModModificado[1], self.matTemperaturaModModificado[1])
            self.Vv = self.convertVazaoValv(self.matVazaoModModificado[1])
            self.tempo = self.min2sList(self.tempo)
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no tratamento dos dados para o sistema!' + '\n' + 'O dano por fadiga na tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'

            self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(
                self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Reta']['Fadiga'] = strOut
            MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Curva']['Fadiga'] = strOut

            return

        self.indiceInicioTransiente = self.getStartIndexTrans(self.Tv, 5, 200, 20)
        self.indiceFimTransiente = self.getEndIndexTrans(self.Tv, 5, 520, 0.232, self.indiceInicioTransiente)

        self.instanteInicioTransiente = self.setStartInstantTrans()
        self.instanteFimTransiente = self.setEndInstantTrans()
        self.temperaturaInicioTransiente = self.setStartTempTrans(self.Tv)
        self.temperaturaFimTransiente = self.setEndTempTrans(self.Tv)



        (self.Tstart, self.Tend) = self.temperaturaStartEnd(self.indiceInicioTransiente, self.indiceFimTransiente)



        try:
            (self.tempoFiltro1, self.VvaporFiltro1, self.PvaporFiltro1, self.TvaporFiltro1) = self.filtro1('Fadiga',
                                                                                                           self.tempo,
                                                                                                           self.Vv,
                                                                                                           self.pv,
                                                                                                           self.Tv)
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro na filtragem dos dados!' + '\n' + 'O dano por fadiga na válvula não foi avaliado neste dia.' + '\n' + '***********************************************************'


            self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(
                self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Reta']['Fadiga'] = strOut
            MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Curva']['Fadiga'] = strOut

            return

        # self.flag1()


        try:
            (self.duracaoPartidaSM, self.variacaoTemperaturaVaporSM) = self.calcVariacoesTubValv()
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no tratamento dos dados!' + '\n' + 'O dano por fadiga na válvula não foi avaliado neste dia.' + '\n' + '***********************************************************'


            self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(
                self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Reta']['Fadiga'] = strOut
            MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Curva']['Fadiga'] = strOut

            return


        # self.flag2()

        self.tStart = self.instanteInicioTransiente
        self.tEnd = self.instanteFimTransiente

        (self.TemperaturaPropMec, self.moduloElasticidade, self.coefExpansaoTerm, self.condutividadeTerm,
         self.calorEspecificoPcte) = self.getPropMec()
        (self.TemperaturaCoefPoisson, self.CoefPoisson) = self.getCoefPoisson()
        (self.amplitudeTensao, self.amplitudeDeformacao) = self.getCurva(self.fileNameCurvaAmpTensaovsAmpDeformacao)
        (self.amplitudeDeformacaoNR, self.Nf25) = self.getCurva(self.fileNameCurvaAmpDeformacaovsNf25)

        self.Paramslist2arrayMH('Fadiga', 'Valvula')

        (self.Dint, self.Rint, self.Dext, self.Rext, self.t, self.f1, self.f2) = self.setGeometriaValvula()



        self.hiStart = self.hiValv(self.tStart)
        self.hiEnd = self.hiValv(self.tEnd)

        (self.h0, self.Tar, self.Tint, self.Text, self.C1) = self.initVariaveisValv(self.instanteInicioTransiente)

        sol = optimize.root(self.FunValv, [-2000, 300, 300], jac=self.jacValv, method='hybr')
        (self.sol1, self.sol2, self.sol3) = (sol.x[0], sol.x[1], sol.x[2])

        self.alfaEq = self.alfaEqs(650)

        # self.talStart = self.tal(self.alfaEq, self.tStart, self.Rext)
        # self.talEnd = self.tal(self.alfaEq, self.tEnd, self.Rext)
        self.talStart = self.tal(self.alfaEq, self.tStart, self.Rext)
        self.talEnd = self.tal(self.alfaEq, self.tempoFiltro1[len(self.tempoFiltro1)-2], self.Rext)

        (self.nR, self.nt, self.deltaR, self.dt) = self.meshEDPValv(20, 200)
        self.R = self.rEDPValv(20)

        Rteste = np.linspace(0, 1, num=20)



        # %%%%%%%%%%%%%%%%%%%% INICIO DOS COMENTÁRIOS DA SOLUÇÃO DE FADIGA %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



        # print("\nDEBUG - iniciou callSolutionValv")
        # (self.uSol, self.tSol) = self.callSolutionValv(self.talStart, self.talEnd, self.dt, self.nR)
        # print("\nDEBUG - terminou callSolutionValv")
        #
        #
        # # print(self.uSol)
        # # print(self.tSol)
        #
        # self.uInt = self.TemperatureInt()
        #
        #
        #
        # self.tempoAdimensional = self.tempoAdimensionalList(int(self.talEnd / 0.01)-1)
        #
        # # k = np.linspace(0.062, 0.303, num=100)
        #
        #
        # # for i in range(100):
        #     # print(self.thetaInt(k[i]), 'thetaInt')
        #
        # # for i in range (100):
        #     # print (self.sigmaPhi(0, k[i]), 'sigmaPhi')
        #
        #
        # #print(self.Tm(0.3))
        #
        # #print(self.thetam(0.3))
        #
        # #print(self.thetaInt(0.3), 'thetaInt')
        #
        # #print(self.sigmaPhiRint(0.3), 'sigmaPhiRint')
        #
        # #A = -self.betaInterpolado(self.Tm(0.3)) * self.Einterpolado(self.Tm(0.3))
        # #print(A, 'A de sigmaPhiRint')
        #
        # #B = (self.Tvap - (self.Tvap - self.Tref) * self.thetaInt(0.3) - self.Tm(0.3))
        # #print(B, 'B de sigmaPhiRint')
        #
        # #C = (1 - self.niInterpolado(self.Tm(0.3)))
        # #print(C, 'C de sigmaPhiRint')
        #
        #
        #
        #
        #
        # self.TensaoTermicaTangencialList = self.TensaoTermicaTangencial(int(self.talEnd / 0.01)-1)
        # self.TensaoMecanicaTangencialList = self.TensaoMecanicaTangencial(int(self.talEnd / 0.01)-1)  # int(self.talEnd/0.01)
        # self.TensaoMecanicaTangencialCurvaList = self.TensaoMecanicaTangencialCurva(int(self.talEnd / 0.01)-1)
        #
        #
        #
        #
        #
        #
        #
        # # for i in range(int(self.talEnd / 0.01)-1):
        #     # print(self.TensaoTermicaTangencialList[i], 'TensaoTermicaTangencial 700 ~ 800')
        #
        # # for i in range(int(self.talEnd / 0.01)-1):
        #     # print(self.TensaoTermicaTangencialList[i], 'TensaoTermicaTangencial 1000 ~ 1100')
        #
        #
        #
        #
        # (self.sigmaPhiMax, self.sigmaPhiMin) = self.TensaoMaxMin(int(self.talEnd / 0.01)-1)
        # (self.sigmaPhiMaxCurva, self.sigmaPhiMinCurva) = self.TensaoMaxMinCurva(int(self.talEnd / 0.01)-1)
        #
        # # print(self.sigmaPhiMax, self.sigmaPhiMin, 'MaxMin')
        # # print(self.sigmaPhiMaxCurva, self.sigmaPhiMinCurva, 'MaxMinCurva')
        #
        # self.variacaoTensaoTermMec = self.variacaoTensaoTermMecFunction(self.sigmaPhiMax, self.sigmaPhiMin)
        # self.variacaoTensaoTermMecCurva = self.variacaoTensaoTermMecFunction(self.sigmaPhiMaxCurva, self.sigmaPhiMinCurva)
        #
        # # print(self.variacaoTensaoTermMec, 'variacaoTensaoTermMec')
        # # print(self.variacaoTensaoTermMecCurva, 'variacaoTensaoTermMecCurva')
        #
        self.variacaoDeformacaoTotal = 1.087*10**-3 # self.variacaoDeformacaoTotalFunction(self.variacaoTensaoTermMec)
        self.variacaoDeformacaoTotalCurva = 1.11*10**-3 # self.variacaoDeformacaoTotalFunction(self.variacaoTensaoTermMecCurva)

        # print(self.variacaoDeformacaoTotal, 'variacaoDeformacaoTotal')
        # print(self.variacaoDeformacaoTotalCurva, 'variacaoDeformacaoTotalCurva')

        self.numeroCiclosEstimadoTrinca = self.numeroCiclosEstimadoTrincaFunction(self.variacaoDeformacaoTotal)
        self.numeroCiclosEstimadoTrincaCurva = self.numeroCiclosEstimadoTrincaFunction(self.variacaoDeformacaoTotalCurva)

        # print(self.numeroCiclosEstimadoTrinca, 'numeroCiclosEstimadoTrinca')
        # print(self.numeroCiclosEstimadoTrincaCurva, 'numeroCiclosEstimadoTrincaCurva')

        self.danoFadiga = self.danoAcumuladoFadigaFunction(self.numeroCiclosEstimadoTrinca)
        self.danoFadigaCurva = self.danoAcumuladoFadigaFunction(self.numeroCiclosEstimadoTrincaCurva)

        # print(self.danoAcumuladoFadiga, 'danoAcumuladoFadiga')
        # print(self.danoAcumuladoFadigaCurva, 'danoAcumuladoFadigaCurva')


        ### Regressão linear para estimar o número de cilos até a falha em fadiga por meio da Curva de Fadiga ###

        try:
            self.putDanoFromLocalFile('CurvaFadiga_FadigaValvulaReta', self.danoFadiga*100)  # OBS!!! -> está hardcoded
            self.putNumeroCiclosFromLocalFile('CurvaFadiga_FadigaValvulaReta', 1)  # OBS!!! -> está hardcoded

            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('CurvaFadiga_FadigaValvulaReta')
            self.NCRegLin, self.NC = self.getNumeroCiclosFromLocalFile('CurvaFadiga_FadigaValvulaReta')

            self.mean_x_RegLin = self.mean(self.NCRegLin)
            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)

            self.variance_x_RegLin = self.variance(self.NCRegLin, self.mean_x_RegLin)
            self.variance_y_RegLin = self.variance(self.danoAcumuladoRegLin, self.mean_y_RegLin)

            self.covariance_RegLin = self.covariance(self.NCRegLin, self.mean_x_RegLin, self.danoAcumuladoRegLin,
                                                     self.mean_y_RegLin)

            self.coefficients_RegLin = self.coefficients(self.mean_x_RegLin, self.mean_y_RegLin, self.variance_x_RegLin,
                                                         self.covariance_RegLin)

            self.numeroCiclos90 = self.simple_linear_regression(self.coefficients_RegLin)

            self.numeroCiclosCurvaFadiga_RegLin = self.numeroCiclos90 - self.NC
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no procedimento de cálculo da vida remanescente!' + '\n' + 'A vida remanescente em fadiga do trecho reto da válvula dada pela curva de fadiga não foi computada neste dia.' + '\n' + '***********************************************************'
            self.numeroCiclosCurvaFadiga_RegLin = 0



        try:

            self.putDanoFromLocalFile('CurvaFadiga_FadigaValvulaCurva', self.danoFadigaCurva * 100)  # OBS!!! -> está hardcoded
            self.putNumeroCiclosFromLocalFile('CurvaFadiga_FadigaValvulaCurva', 1)  # OBS!!! -> está hardcoded

            self.danoAcumuladoRegLinCurva = self.getDanoFromLocalFile('CurvaFadiga_FadigaValvulaCurva')
            self.NCRegLinCurva, self.NCcurva = self.getNumeroCiclosFromLocalFile('CurvaFadiga_FadigaValvulaCurva')

            self.mean_x_RegLinCurva = self.mean(self.NCRegLinCurva)
            self.mean_y_RegLinCurva = self.mean(self.danoAcumuladoRegLinCurva)

            self.variance_x_RegLinCurva = self.variance(self.NCRegLinCurva, self.mean_x_RegLinCurva)
            self.variance_y_RegLinCurva = self.variance(self.danoAcumuladoRegLinCurva, self.mean_y_RegLinCurva)

            self.covariance_RegLinCurva = self.covariance(self.NCRegLinCurva, self.mean_x_RegLinCurva, self.danoAcumuladoRegLinCurva,
                                                     self.mean_y_RegLinCurva)

            self.coefficients_RegLinCurva = self.coefficients(self.mean_x_RegLinCurva, self.mean_y_RegLinCurva, self.variance_x_RegLinCurva,
                                                         self.covariance_RegLinCurva)

            self.numeroCiclos90Curva = self.simple_linear_regression(self.coefficients_RegLinCurva)

            self.numeroCiclosCurvaFadiga_RegLinCurva = self.numeroCiclos90Curva - self.NCcurva
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no procedimento de cálculo da vida remanescente!' + '\n' + 'A vida remanescente em fadiga do trecho curvo da válvula dada pela curva de fadiga não foi computada neste dia.' + '\n' + '***********************************************************'
            self.numeroCiclosCurvaFadiga_RegLin = 0

        self.resultadoFadigaTubulacao = self.resultadoFadigaTubulacaoFunction(self.numeroCiclosCurvaFadiga_RegLin, self.numeroCiclosCurvaFadiga_RegLinCurva , self.numeroCiclosFadiga, self.danoFadiga, self.danoFadigaCurva, self.indiceInicioTransiente)
        print(self.resultadoFadigaTubulacao)

        # self.flag4FadigaTubulacao(self.resultadoFadigaTubulacao)

        self.saida2 = self.saida2FunctionTubulacao(self.indiceInicioTransiente, self.resultadoFadigaTubulacao)

        # self.writeOutfileTubulacao(self.saida2)
        try:
            self.writeOutfile('Valvula', 'Fadiga', 'Reta')
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fadiga do trecho reto da válvula foi enviado neste dia.' + '\n' + '***********************************************************'

        try:
            self.writeOutfile('Valvula', 'Fadiga', 'Curva')
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fadiga do trecho curvo da válvula foi enviado neste dia.' + '\n' + '***********************************************************'
            return


        # self.flag5Tubulacao()

        # self.flagFimTubulacao()


    @staticmethod
    def create():
        # currentDir = 'C:\\Users\\victorv\\Desktop\\Desenv\\SOMA-Turbodiag\\DATA\\valvulareta\\'
        currentDir = MecanismoDano.APP_ROOT + '/../DATA/valvulareta/'
        if platform.system() == "Windows":
            currentDir = MecanismoDano.APP_ROOT + '\\..\\DATA\\valvulareta\\'

        fileName = 'controle_fadiga.txt'

        return FadigaValvulaReta(currentDir, fileName)

# fadVR = touchObjectFadValvReta()
# self.JustDoItFadValvReta()
