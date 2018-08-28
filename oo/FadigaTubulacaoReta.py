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

from FadigaTubulacao import*




class FadigaTubulacaoReta(FadigaTubulacao):

    def __init__(self, currentDir, fileName):

        FadigaTubulacao.__init__(self, currentDir, fileName)

    def JustDoItFadTubReta(self, arrayAux2, fatigueCycles, operationTime):

        # (self.arquivoEntrada, self.arquivoSaida, self.arquivoControle) = self.setupNameFileInputParams(self.currentDir, self.fileName)

        # (self.tempo, self.Vv, self.pv, self.Tv) = self.setupInputParamsFromSoma(arrayAux2, self.tempo, self.Vv, self.pv, self.Tv)

        try:
            (self.tempo, self.Vv, self.pv, self.Tv) = self.setupInputParamsFromSoma(arrayAux2, self.tempo, self.Vv,
                                                                                    self.pv, self.Tv)
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o sistema!' + '\n' + 'O dano por fadiga na tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'


            self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(
                self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Reta']['Fadiga'] = strOut
            MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Curva']['Fadiga'] = strOut

            return
            # (self.tempoOperacaoBase, self.tempo, self.Vv, self.pv, self.Tv) = self.setupInputParams(self.arquivoEntrada, self.tempo, self.Vv, self.pv, self.Tv)


        # for i in range (len(self.Tv) -1):
            # print "Temperatura: " + str(self.Tv[i]),  i +1
        # As listas estão sendo lidas de forma correta, os valores estão de acordo com o Mathcad.
        self.numeroCiclosFadiga = fatigueCycles
        # self.flag0()

        self.Vv = self.medSmoothParams(self.Vv)
        self.pv = self.medSmoothParams(self.pv)
        self.Tv = self.medSmoothParams(self.Tv)

        errorCode = self.firstBlock('Fadiga', 'Tubulacao', 'Reta')
        errorCode = self.firstBlock('Fadiga', 'Tubulacao', 'Curva')
        if errorCode > 0:
            return

        self.indiceInicioTransiente = self.getStartIndexTrans(self.Tv, 5, 200, 20)
        self.indiceFimTransiente = self.getEndIndexTrans(self.Tv, 5, 520, 1, self.indiceInicioTransiente)
        # Pequena diferença no indice do fim do transiente devido as diferenças dos valores de temperatura gerados pela medsmooth
        # errorCode = self.checkParamsForFlu('Fadiga', 'Rotor')

        # TODO: INTRODUZIR UM FILTRO DE TRANSIENTES SEVEROS NESSE PONTO DO CÓDIGO




        #self.fracVazao(self.Vv) # parece q essa funçao nao esta sendo aplicada no mathcad


        (self.matVazao, self.matPressao, self.matTemperatura) = self.setMats()
        self.indiceInicioTemperatura = self.getIndex(self.Tv, 0, 5, 20)
        self.indiceInicioPressao = self.getIndex(self.pv, 0, 2, 0.75)
        self.indiceInicioVazao = self.getIndex(self.Vv, 0, 2, 20) # falar com o bruno ou fred sobre a questao do threshold da vazao!!!

        errorCode = self.checkParamsForFlu('Fadiga', 'Tubulacao', 'Reta')
        errorCode = self.checkParamsForFlu('Fadiga', 'Tubulacao', 'Curva')

        if errorCode > 0:
            return

        # self.flag5()


        # Deu uma diferença estranha no indice de inicio do tansiente na VAZAO: O Mathcad usa 20 como threshold, acho um valor muito elevado para dados que foram
        # suavizados, parece que os dados do mathcad nao foram suavizados

        try:

            (self.tVazao, self.matVazaoMod, self.tTemperatura, self.matTemperaturaMod, self.tPressao,
             self.matPressaoMod, self.nmaxElem, self.tmin) = self.matMods(self.indiceInicioVazao,
                                                                              self.indiceInicioTemperatura,
                                                                              self.indiceInicioPressao)


            # Os matMods nao apresentam grandes discrepancia, pois os indices de inicio de transiente estão razoavelmente compativeis
            # contudo ha uma discrepancia nao identificada nos valores das grandezas medidas: vazao, pressao e temperatura.


            self.matPressaoModModificado = self.modifica(len(self.matPressaoMod[0]), self.tmin, self.matPressaoMod)
            self.matVazaoModModificado = self.modifica(len(self.matVazaoMod[0]), self.tmin, self.matVazaoMod)  # Os valores de vazao nao estao batendo nada!!!!!
            self.matTemperaturaModModificado = self.modifica(len(self.matTemperaturaMod[0]), self.tmin,
                                                               self.matTemperaturaMod)
            # A funçao modifica é muito importante, pois ela vai modificar os valores das listas que vão passar pelos filtros!!!
            (self.tempo, self.pv, self.Tv) = (
            self.matVazaoModModificado[0], self.matPressaoModModificado[1], self.matTemperaturaModModificado[1])

            self.Vv = self.convertVazao(self.matVazaoModModificado[1])
            self.tempo = self.min2sList(self.tempo)

        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no tratamento dos dados!' + '\n' + 'O dano por fadiga na tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'
            self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(
                self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Reta']['Fadiga'] = strOut
            MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Curva']['Fadiga'] = strOut

            return


        ## Novo calculo dos indices de inicio e fim de transiente
        ## Mudança do threshold4
        self.indiceInicioTransiente = self.getStartIndexTrans(self.Tv, 5, 200, 20) # 250 # self.getStartIndexTrans(self.Tv, 5, 200, 20)
        self.indiceFimTransiente = self.getEndIndexTrans(self.Tv, 5, 520, 0.029, self.indiceInicioTransiente) # 400 # self.getEndIndexTrans(self.Tv, 5, 520, 0.029)

        self.instanteInicioTransiente = self.setStartInstantTrans()
        self.instanteFimTransiente = self.setEndInstantTrans()
        self.temperaturaInicioTransiente = self.setStartTempTrans(self.Tv)
        self.temperaturaFimTransiente = self.setEndTempTrans(self.Tv)

        # Os valores de tStart e tEnd interferem muito nos calculos das tensões termicas, visto que eles são utilizados para o calculo das varias
        # propriedades termofisicas.


        try:
            (self.tempoFiltro1, self.VvaporFiltro1, self.PvaporFiltro1, self.TvaporFiltro1) = self.filtro1('Fadiga',
                                                                                                           self.tempo,
                                                                                                           self.Vv,
                                                                                                           self.pv,
                                                                                                           self.Tv)
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro na filtragem dos dados!' + '\n' + 'O dano por fadiga na tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'


            self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(
                self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Reta']['Fadiga'] = strOut
            MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Curva']['Fadiga'] = strOut

            return
        # self.flag1()
        try:

            (self.duracaoPartidaSM, self.variacaoTemperaturaVaporSM) = self.calcVariacoesTubValv()
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no tratamento dos dados!' + '\n' + 'O dano por fadiga na tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'
            self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(
                self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Reta']['Fadiga'] = strOut
            MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Curva']['Fadiga'] = strOut

            return

        # self.flag2()
        self.tStart = self.instanteInicioTransiente
        self.tEnd = self.instanteFimTransiente
        (self.Vstart, self.Vend) = self.vazaoStartEnd(self.indiceInicioTransiente, self.indiceFimTransiente)

        (self.TemperaturaPropMec, self.moduloElasticidade, self.coefExpansaoTerm, self.condutividadeTerm,
         self.calorEspecificoPcte) = self.getPropMec()
        (self.TemperaturaCoefPoisson, self.CoefPoisson) = self.getCoefPoisson()
        (self.amplitudeTensao, self.amplitudeDeformacao) = self.getCurva(self.fileNameCurvaAmpTensaovsAmpDeformacao)
        (self.amplitudeDeformacaoNR, self.Nf25) = self.getCurva(self.fileNameCurvaAmpDeformacaovsNf25)
        self.Paramslist2arrayMH('Fadiga', 'Tubulacao')
        (self.Dint, self.Rint, self.Dext, self.Rext, self.rc, self.t, self.f1,
         self.f2) = self.setGeometriaTubulacao()





        self.hiStart = self.hi(self.tStart)
        self.hiEnd = self.hi(self.tEnd)

        (self.h0, self.Tar, self.Tint, self.Text, self.C1) = self.initVariaveis(self.instanteInicioTransiente)


        sol = optimize.root(self.Fun, [-400, 190, 190])
        (self.sol1, self.sol2, self.sol3) = (sol.x[0], sol.x[1], sol.x[2])
        # print(sol.x)




        self.alfaEq = self.alfaEqs(650)

        # self.talStart = self.tal(self.alfaEq, self.tStart, self.Rext)
        # self.talEnd = self.tal(self.alfaEq, self.tEnd, self.Rext)
        self.talStart = self.tal(self.alfaEq, self.tempoFiltro1[1], self.Rext)
        self.talEnd = self.tal(self.alfaEq, self.tempoFiltro1[len(self.tempoFiltro1)-2], self.Rext)




        # %%%%%%%%%%%%%%%%%%%% INICIO DOS COMENTÁRIOS DA SOLUÇÃO DE FADIGA %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




        # (self.nR, self.nt, self.deltaR, self.dt) = self.meshEDP(20,200)
        # self.R = self.rEDP(20)
        #
        # #j = np.linspace(0.18, 0.7, num=100)
        #
        # #for i in range(100):
        #     #print(self.betaInterp((self.Tvap - (self.Tvap - self.Tref) * j[i])), j[i], self.Tvap - (self.Tvap - self.Tref) * j[i])
        #
        #
        # print("\nDEBUG - iniciou callSolution")
        # (self.uSol, self.tSol) = self.callSolution(self.talStart, self.talEnd, self.dt, self.nR)
        # print("\nDEBUG - terminou callSolution")
        #
        #
        # print(self.uSol)
        #
        #
        #
        #
        # #print(self.uSol)
        #
        # #print(self.tSol)
        #
        # self.uInt = self.TemperatureInt()
        #
        # self.tempoAdimensional = self.tempoAdimensionalList(int(self.talEnd/0.1)) #int(self.talEnd/0.01)
        #
        #
        # # k = np.linspace(10, 17, num=100)
        # #for i in range (100):
        #     #print(self.Temperature(k[i], 0), 'Temperature')
        #
        # #for i in range(len(self.uSol)):
        #     #print(self.uSol[i][0], 'uSol[0]')
        #     #print(self.uSol[i][19], 'uSol[19]')
        #
        #
        #
        # # for i in range (100):
        #     # print(self.thetaInt(k[i]), 'thetaInt')
        #
        # # for i in range(100):
        #     # print(self.Temperature(0, k[i]), k[i], 'Temperature')
        #
        # # for i in range (100):
        #     # print (self.sigmaPhi(k[i], 0), 'sigmaPhi')
        #
        #
        # #print(self.Tm(15), 'Tm(15)')
        #
        #
        # #print(self.thetam(15), 'thetam(15)')
        #
        #
        #
        # #print(self.sigmaPhiRint(15), 'sigmaPhiRint')
        #
        # #A = -self.betaInterpolado(self.Tm(15)) * self.Einterpolado(self.Tm(15))
        # #print(A, 'A de sigmaPhiRint')
        #
        # #B = (self.Tvap - (self.Tvap - self.Tref) * self.thetaInt(15) - self.Tm(15))
        # #print(B, 'B de sigmaPhiRint')
        #
        # #C = (1 - self.niInterpolado(self.Tm(15)))
        # #print(C, 'C de sigmaPhiRint' )
        #
        #
        # # print(self.thetaInt(15), 'thetaInt')
        # # print(self.Temperature(15, 0), 'Temperature')
        # # print(self.Tvap - (self.Tvap - self.Tref) * self.thetaInt(15), 'thetaIntDimensional')
        #
        # # A = self.betaInterp(self.Tvap - (self.Tvap - self.Tref) * self.thetaInt(15)) / (
        # # 1 - self.niInterp(self.Tvap - (self.Tvap - self.Tref) * self.thetaInt(15)))
        # # print(A, 'A') # Ok -> Conferido com o Mathcad
        #
        # # A1 = self.betaInterp(self.Tvap - (self.Tvap - self.Tref) * self.thetaInt(15))
        # # print(A1, 'betaInterp')
        # # A2 = (1 - self.niInterp(self.Tvap - (self.Tvap - self.Tref) * self.thetaInt(15)))
        # # print(A2, '1 - niInterp')
        #
        # # B = self.Einterp(self.Tvap - (self.Tvap - self.Tref) * self.thetaInt(15))
        # # print(B, 'B') # Ok -> Conferido com o Mathcad
        #
        # # C = 1 / (self.Rext ** 2 - self.Rint ** 2)
        # # print(C, 'C') # Ok -> Conferido com o Mathcad
        #
        # # D = 1 + ((self.Rint ** 2) / ((self.Rint + (self.Rext - self.Rint) * 0) ** 2))
        # # print(D, 'D') # Ok -> Conferido com o Mathcad
        #
        # # integrandE = lambda R: (self.Tvap - (self.Tvap - self.Tref) * self.thetaInt(15)) * (self.Rint + (self.Rext - self.Rint) * 0) * (
        #     # self.Rext - self.Rint)
        # # IE, errE = quad(integrandE, 0, 1)
        #
        # # E = IE
        # # print(E, 'E') # Ok -> Conferido com o Mathcad
        #
        # #integrandF = lambda X: (self.Rint + (self.Rext - self.Rint) * X) * (self.Tvap - (self.Tvap - self.Tref) * self.Temperature(15, X)) * (
        #     #self.Rext - self.Rint)
        # #IF, errF = quad(integrandF, 0, 0.5)
        #
        # #F = IF / (self.Rint + (self.Rext - self.Rint) * 0.5) ** 2
        # #print(F, 'F')
        #
        # # G = (self.Tvap - (self.Tvap - self.Tref) * self.thetaInt(15))
        # # print(G, 'G')
        # #
        # # print((A * B * ( (C)*(D)*(E) - G)), 'Produto A * B * ( (C*D*E) - G)')
        # #
        # # print(self.sigmaPhi(15, 0), 'sigmaPhi') # checar essa função quando as temperaturas estiverem ok (atol=1e-5)
        #
        #
        #
        # self.TensaoTermicaTangencialList = self.TensaoTermicaTangencial(int(self.talEnd/0.1)-1) #int(self.talEnd/0.01) # checar se essa lista esta ok qnd sigmaphi estiver ok
        #
        # #for i in range (100):
        #     #print(self.TensaoTermicaTangencialList[700+i], 'TensaoTermicaTangencial 700 ~ 800')
        #
        # #for i in range (100):
        #     #print(self.TensaoTermicaTangencialList[1000+i], 'TensaoTermicaTangencial 1000 ~ 1100')
        #
        #
        # self.TensaoMecanicaTangencialList = self.TensaoMecanicaTangencial(int(self.talEnd/0.1)-1) #int(self.talEnd/0.01)
        # self.TensaoMecanicaTangencialCurvaList = self.TensaoMecanicaTangencialCurva(int(self.talEnd/0.1)-1)
        #
        #
        # #for i in range (100):
        #     #print(self.TensaoMecanicaTangencialList[700+i], 'TensaoMecanicaTangencial 700 ~ 800')
        #
        # #for i in range (100):
        #     #print(self.TensaoMecanicaTangencialList[1000+i], 'TensaoMecanicaTangencial 1000 ~ 1100')
        #
        # (self.sigmaPhiMax, self.sigmaPhiMin) = self.TensaoMaxMin(int(self.talEnd/0.1)-1) #(6.739, -66.55) #self.TensaoMaxMin(100) #int(self.talEnd/0.01)
        # (self.sigmaPhiMaxCurva, self.sigmaPhiMinCurva) = self.TensaoMaxMinCurva(int(self.talEnd/0.1)-1)
        #
        # # print(self.sigmaPhiMax, self.sigmaPhiMin, 'MaxMin')
        # # print(self.sigmaPhiMaxCurva, self.sigmaPhiMinCurva, 'MaxMinCurva')
        #
        # self.variacaoTensaoTermMec = self.variacaoTensaoTermMecFunction(self.sigmaPhiMax, self.sigmaPhiMin) # entender porque a Tensão Máxima está dando tão diferente
        # self.variacaoTensaoTermMecCurva = self.variacaoTensaoTermMecFunction(self.sigmaPhiMaxCurva, self.sigmaPhiMinCurva)
        # # ver se o problema está na Tensão Térmica ou Mecânica
        #
        # # print(self.variacaoTensaoTermMec, 'variacaoTensaoTermMec')
        # # print(self.variacaoTensaoTermMecCurva, 'variacaoTensaoTermMecCurva')


        # %%%%%%%%%%%%%%%%%%%% FIM DOS COMENTÁRIOS DA SOLUÇÃO DE FADIGA %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


        self.variacaoDeformacaoTotal = 1.028*10**-3 # self.variacaoDeformacaoTotalFunction(self.variacaoTensaoTermMec)
        self.variacaoDeformacaoTotalCurva = 1.031*10**-3 # self.variacaoDeformacaoTotalFunction(self.variacaoTensaoTermMecCurva)

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
            self.putDanoFromLocalFile('CurvaFadiga_FadigaTubulacaoReta', self.danoFadiga * 100)  # OBS!!! -> está hardcoded
            self.putNumeroCiclosFromLocalFile('CurvaFadiga_FadigaTubulacaoReta', 1)  # OBS!!! -> está hardcoded

            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('CurvaFadiga_FadigaTubulacaoReta')
            self.NCRegLin, self.NC = self.getNumeroCiclosFromLocalFile('CurvaFadiga_FadigaTubulacaoReta')

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
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no procedimento de cálculo da vida remanescente!' + '\n' + 'A vida remanescente em fadiga do trecho reto da tubulação dada pela curva de fadiga não foi computada neste dia.' + '\n' + '***********************************************************'
            self.numeroCiclosCurvaFadiga_RegLin = 0




        try:
            self.putDanoFromLocalFile('CurvaFadiga_FadigaTubulacaoCurva',
                                      self.danoFadigaCurva * 100)  # OBS!!! -> está hardcoded
            self.putNumeroCiclosFromLocalFile('CurvaFadiga_FadigaTubulacaoCurva', 1)  # OBS!!! -> está hardcoded

            self.danoAcumuladoRegLinCurva = self.getDanoFromLocalFile('CurvaFadiga_FadigaTubulacaoCurva')
            self.NCRegLinCurva, self.NCcurva = self.getNumeroCiclosFromLocalFile('CurvaFadiga_FadigaTubulacaoCurva')

            self.mean_x_RegLinCurva = self.mean(self.NCRegLinCurva)
            self.mean_y_RegLinCurva = self.mean(self.danoAcumuladoRegLinCurva)

            self.variance_x_RegLinCurva = self.variance(self.NCRegLinCurva, self.mean_x_RegLinCurva)
            self.variance_y_RegLinCurva = self.variance(self.danoAcumuladoRegLinCurva, self.mean_y_RegLinCurva)

            self.covariance_RegLinCurva = self.covariance(self.NCRegLinCurva, self.mean_x_RegLinCurva,
                                                          self.danoAcumuladoRegLinCurva,
                                                          self.mean_y_RegLinCurva)

            self.coefficients_RegLinCurva = self.coefficients(self.mean_x_RegLinCurva, self.mean_y_RegLinCurva,
                                                              self.variance_x_RegLinCurva,
                                                              self.covariance_RegLinCurva)

            self.numeroCiclos90Curva = self.simple_linear_regression(self.coefficients_RegLinCurva)

            self.numeroCiclosCurvaFadiga_RegLinCurva = self.numeroCiclos90Curva - self.NCcurva
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no procedimento de cálculo da vida remanescente!' + '\n' + 'A vida remanescente em fadiga do trecho curvo da tubulação dada pela curva de fadiga não foi computada neste dia.' + '\n' + '***********************************************************'
            self.numeroCiclosCurvaFadiga_RegLinCurva = 0


        self.resultadoFadigaTubulacao = self.resultadoFadigaTubulacaoFunction(self.numeroCiclosCurvaFadiga_RegLin, self.numeroCiclosCurvaFadiga_RegLinCurva , self.numeroCiclosFadiga, self.danoFadiga, self.danoFadigaCurva, self.indiceInicioTransiente)
        print(self.resultadoFadigaTubulacao)

        # self.flag4FadigaTubulacao(self.resultadoFadigaTubulacao)

        self.saida2 = self.saida2FunctionTubulacao(self.indiceInicioTransiente, self.resultadoFadigaTubulacao)

        # self.writeOutfileTubulacao(self.saida2)

        try:
            self.writeOutfile('Tubulacao', 'Fadiga', 'Reta')
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fadiga do trecho reto da tubulação foi enviado neste dia.' + '\n' + '***********************************************************'


        try:
            self.writeOutfile('Tubulacao', 'Fadiga', 'Curva')
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fadiga do trecho curvo da tubulação foi enviado neste dia.' + '\n' + '***********************************************************'
            return


        # self.flag5Tubulacao()

        # self.flagFimTubulacao()


    @staticmethod
    def create():
        # currentDir = 'C:\\SOMATURBODIAG\\tubulacaoreta\\'
        currentDir = MecanismoDano.APP_ROOT + '/../DATA/tubulacaoreta/'
        if platform.system() == "Windows":
            currentDir = MecanismoDano.APP_ROOT + '\\..\\DATA\\tubulacaoreta\\'

        fileName = 'controle_fadiga.txt'

        return FadigaTubulacaoReta(currentDir, fileName)


# def touchObjectFadRotor():
#
#     currentDir = 'C:\\SOMATURBODIAG\\tubulacaoreta\\'
#     fileName = 'controle_fadiga.txt'
#
#     return FadigaTubulacaoReta(currentDir, fileName)
#
# fadTR = touchObjectFadRotor()
# fadTR.JustDoItFadTubReta([1], 324, 10)


# fadTR = touchObjectFadTubReta()
# self.JustDoItFadTubReta()
