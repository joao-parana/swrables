# -*- coding: utf-8 -*-


import numpy as np
import os
import platform
import ErrorHandle as EH
import sys
from iapws import IAPWS97
from math import *
from scipy.integrate import quad
import requests
from scipy.misc import derivative
from scipy.optimize import fsolve
from scipy import optimize
from numpy.linalg import inv
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d, interp2d
from scipy.integrate import ode





from MecanismoDano import*

class Fadiga(MecanismoDano):

    def __init__(self, currentDir, fileName):  # currentDir deve terminar com '\'
        MecanismoDano.__init__(self, currentDir, fileName)



        self.numeroCiclosFadiga = 0
        self.duracaoPartidaSM = 0
        self.variacaoTemperaturaVaporPartidaSM = 0
        self.variacaoTemperaturaMetalPartidaSM = 0
        self.variacaoTemperaturaCLESM = 0
        self.fileNameCurvaVariacaoDeformacaoNumeroCiclos = 'Curva_Variacao_Deformacao_NumeroCiclos.txt'
        self.variacaoDeformacao = []
        self.numeroCiclos = []
        self.epsilonY = 0.002
        self.deltat = 0
        self.Biot = 0
        self.deltaTal = 0
        self.deltaTvapor = 0
        self.alfaRotor = 0
        self.fileNameVariacaoDeformacaoNominal = 'Variacao_Deformacao_Nominal.txt'
        self.BiotVariacaoDeformacaoNominal = []
        self.deltaTalVariacaoDeformacaoNominal = []
        self.deltaTalInferior = 0
        self.deltaTalSuperior = 0
        self.BiotInferior = 0
        self.BiotSuperior = 0
        self.indiceDeltaTalSuperior = 0
        self.indiceDeltaTalInferior = 0
        self.deltaTalTabela = []
        self.deformacaoStarInf = []
        self.deformacaoStarSup = []
        self.deformacaoNominal = 0
        self.fileNameFatorConcentracaoDeformacaoPlastica = 'FatorConcentracaoDeformacaoPlastica.txt'
        self.razaoDeformacaoNominal = []
        self.fatorK = []
        self.deformacaoTotal = 0
        self.deformacaoTotalAnalisado = 0
        self.deltaDfadiga = 0
        self.deltaDfadigaPercentual = 0
        self.danoDF = []
        self.CoefA = []
        self.CoefB = []
        self.CoefC = []
        self.limCLE = []
        self.dTdtLimInfCLE = 0
        self.dTdtLimSupCLE = 0
        self.taxaAquecimento = 0
        self.dfCLE = 0
        self.deltaDfadigaCLE = 0
        self.deltaDfadigaCLEPercentual = 0
        self.nRCLE = 0
        self.NR = 0
        self.output = []
        self.Tmint = []
        self.Tmext = []

        ### Veio de FadigaTubulacao ###

        self.matVazao = []
        self.matPressao = []
        self.matTemperatura = []
        self.matVazao1 = []
        self.matVazao2 = []
        self.matPressao1 = []
        self.matPressao2 = []
        self.matTemperatura1 = []
        self.matTemperatura2 = []
        self.indiceInicioTemperatura = 0
        self.indiceInicioVazao = 0
        self.indiceInicioPressao = 0
        self.matVazaoMod = []
        self.tVazao = 0
        self.matTemperaturaMod = []
        self.tTemperatura = 0
        self.tPressao = 0
        self.matPressaoMod = []
        self.tmin = 0
        self.nmaxElem = 0
        self.matVazaoModModificado = []
        self.matPressaoModModificado = []
        self.matTemperaturaModModificado = []
        self.fileNameCurvaAmpTensaovsAmpDeformacao = 'Curva_Amplitude_tensao_versus_amplitude_def_CrMoV_550.txt'
        self.fileNameCurvaAmpDeformacaovsNf25 = 'Curva_Amplitude_def_versus_Nf25porcento_CrMoV_550.txt'
        self.amplitudeTensao = []
        self.amplitudeDeformacao = []
        self.amplitudeDeformacaoNR = []
        self.Nf25 = []
        self.h0 = 0
        self.sol1 = 0
        self.sol2 = 0
        self.sol3 = 0
        self.alfaEq = 0
        self.NpontosTal = 0
        self.tStart = 0
        self.tEnd = 0
        self.Vstart = 0
        self.Vend = 0
        self.hiStart = 0
        self.hiEnd = 0
        self.solucao = []
        self.Tref = 25.
        self.Tvap = 600.
        self.Tar = 34.
        self.deltaR = 0
        self.ho = 19.
        self.nR = 0
        self.nt = 0
        self.U0 = []
        self.tEDP = []
        self.talStart = 0
        self.talEnd = 0
        self.dt = 0
        self.uSol = []
        self.tSol = []
        self.Uzero = []
        self.CondInicialTeste = 0
        self.R = []
        self.TempPropMec = [25, 100, 200, 300, 400, 450, 500, 550, 600, 650]
        self.TempCoefPoisson = [25, 150, 151, 340, 410, 480, 565]
        self.uInt = []
        self.tempoAdimensional = []
        self.TensaoTermicaTangencialList = []
        self.TensaoMecanicaTangencialList = []
        self.TensaoMecanicaTangencialCurvaList = []
        self.sigmaPhiMax = 0
        self.sigmaPhiMin = 0
        self.sigmaPhiMaxCurva = 0
        self.sigmaPhiMinCurva = 0
        self.variacaoTensaoTermMec = 0
        self.variacaoTensaoTermMecCurva = 0
        self.variacaoDeformacaoTotal = 0
        self.variacaoDeformacaoTotalCurva = 0
        self.numeroCiclosEstimadoTrinca = 0
        self.numeroCiclosEstimadoTrincaCurva = 0
        self.danoFadiga = 0
        self.danoFadigaCurva = 0
        self.resultadoFadigaTubulacao = []

    def getDeformacaoxCiclos(self, fileNameCurva):

        listaAux = []
        arrayAux = []
        VariacaoDeformacao = []
        NumeroCiclos = []
        VariacaoDeformacaoFloat = []
        NumeroCiclosFloat = []

        with open(self.currentDir + fileNameCurva, "rb") as ins:
            for line in ins:
                arrayAux.append(line)

        for i in range(len(arrayAux)):
            listaAux.append(arrayAux[i].strip('\r\n'))

        for i in range(len(listaAux)):
            VariacaoDeformacao.append(listaAux[i].split('\t')[0])

        for i in range(len(listaAux)):
            NumeroCiclos.append(listaAux[i].split('\t')[1])

        for i in range(len(VariacaoDeformacao)):
            VariacaoDeformacaoFloat.append(float(VariacaoDeformacao[i])/100.)

        for i in range(len(NumeroCiclos)):
            NumeroCiclosFloat.append(float(NumeroCiclos[i]))

        return (VariacaoDeformacaoFloat, NumeroCiclosFloat)

    def calcVariacoes(self):

        duracaoPartidaSM = float(self.instanteFimTransiente) - float(self.instanteInicioTransiente)
        Tstart = float(self.Tv[self.indiceInicioTransiente])

        variacaoTemperaturaVaporPartidaSM = float(self.Tic[self.indiceFimTransiente]) - float(self.Tic[self.indiceInicioTransiente])

        variacaoTemperaturaMetalPartidaSM = float(self.temperaturaFimTransiente) - float(self.temperaturaInicioTransiente)
        variacaoTemperaturaCLESM = float(self.Tv[self.indiceFimTransiente]) - float(self.temperaturaInicioTransiente)

        return (duracaoPartidaSM, variacaoTemperaturaVaporPartidaSM, variacaoTemperaturaMetalPartidaSM, variacaoTemperaturaCLESM)

    # def numeroCiclosInterpolado(self, T):

        # cNumeroCiclosInterpolado = interp1d(self.variacaoDeformacao, self.numeroCiclos, kind='cubic')

        # return cNumeroCiclosInterpolado(T)

    def lastValue(self):

        PvaporSM = self.PvaporFiltro2[len(self.PvaporFiltro2) - 1]
        TvaporSM = self.TvaporFiltro2[len(self.TvaporFiltro2) - 1]  # Tomou-se o último valor das respectivas listas no lugar da média lação a fadiga do componente
        TmediacextSM = self.TmetalFiltro2[len(self.TmetalFiltro2) - 1]  # para se ter o caso mais severo em relação a fadiga
        PWmediaSM = self.PotenciaFiltro2[len(self.PotenciaFiltro2) - 1]



        return (PvaporSM, TvaporSM, TmediacextSM, PWmediaSM)

    def setParamsForFad(self, duracaoPartidaSM, variacaoTemperaturaVaporPartidaSM, T2rotor, hRotor, r2Rotor):

        deltat = duracaoPartidaSM/60.
        deltaTvapor = variacaoTemperaturaVaporPartidaSM
        lambdaRotor = self.lambdaInterpolado(T2rotor)
        Biot = hRotor*r2Rotor / lambdaRotor
        alfaRotor = self.alphaInterpolado(T2rotor)
        deltaTal = alfaRotor*deltat*3600/r2Rotor**2

        return (deltat, deltaTvapor, lambdaRotor, Biot, alfaRotor, deltaTal)

    def getVariacaoDeformacaoNominal(self):

        listaAux = []
        arrayAux = []
        Biot = []
        deltaTal1 = []
        deltaTal2 = []
        deltaTal3 = []
        deltaTal4 = []
        deltaTal5 = []
        deltaTal6 = []
        deltaTal7 = []
        deltaTal8 = []
        BiotFloat = []
        deltaTalFloat = []
        deltaTalTabela = []


        with open(self.currentDir + self.fileNameVariacaoDeformacaoNominal, "rb") as ins:  ### Abre o arquivo controle_fluencia.txt
            for line in ins:
                arrayAux.append(line)

        arrayAux.pop(0)

        for i in range(len(arrayAux)):
            listaAux.append(arrayAux[i].strip('\r\n'))

        for i in range(len(listaAux)):
            Biot.append(listaAux[i].split('\t')[0])

        for i in range(len(listaAux)):
            deltaTal1.append(listaAux[i].split('\t')[1])

        for i in range(len(listaAux)):
            deltaTal2.append(listaAux[i].split('\t')[2])

        for i in range(len(listaAux)):
            deltaTal3.append(listaAux[i].split('\t')[3])

        for i in range(len(listaAux)):
            deltaTal4.append(listaAux[i].split('\t')[4])

        for i in range(len(listaAux)):
            deltaTal5.append(listaAux[i].split('\t')[5])

        for i in range(len(listaAux)):
            deltaTal6.append(listaAux[i].split('\t')[6])

        for i in range(len(listaAux)):
            deltaTal7.append(listaAux[i].split('\t')[7])

        for i in range(len(listaAux)):
            deltaTal8.append(listaAux[i].split('\t')[8])

        Biot.pop(0)

        for i in range(len(Biot)):
            BiotFloat.append(float(Biot[i]))


        for i in range(len(deltaTal1)):
            deltaTalFloat.append(float(deltaTal1[i]))

        for i in range(len(deltaTal2)):
            deltaTalFloat.append(float(deltaTal2[i]))

        for i in range(len(deltaTal3)):
            deltaTalFloat.append(float(deltaTal3[i]))

        for i in range(len(deltaTal4)):
            deltaTalFloat.append(float(deltaTal4[i]))

        for i in range(len(deltaTal5)):
            deltaTalFloat.append(float(deltaTal5[i]))

        for i in range(len(deltaTal6)):
            deltaTalFloat.append(float(deltaTal6[i]))

        for i in range(len(deltaTal7)):
            deltaTalFloat.append(float(deltaTal7[i]))

        for i in range(len(deltaTal8)):
            deltaTalFloat.append(float(deltaTal8[i]))

        deltaTalTabela.append(float(deltaTal1[0]))
        deltaTalTabela.append(float(deltaTal2[0]))
        deltaTalTabela.append(float(deltaTal3[0]))
        deltaTalTabela.append(float(deltaTal4[0]))
        deltaTalTabela.append(float(deltaTal5[0]))
        deltaTalTabela.append(float(deltaTal6[0]))
        deltaTalTabela.append(float(deltaTal7[0]))
        deltaTalTabela.append(float(deltaTal8[0]))



        return (BiotFloat, deltaTalFloat, deltaTalTabela)

    def deltaTalSuperiorInferior(self, deltaTal, deltaTalTabela ):

        deltaTalInferior = []
        deltaTalSuperior = []

        for i in range (len(deltaTalTabela)):

            if deltaTalTabela[i] < deltaTal:

                deltaTalInferior.append(deltaTalTabela[i])

            elif deltaTalTabela[i] > deltaTal:

                deltaTalSuperior.append(deltaTalTabela[i])


        if deltaTal < 1:

            deltaTalSuperior = deltaTalSuperior

        elif deltaTal > 1:

            deltaTalSuperior = deltaTalInferior

        return (max(deltaTalInferior), min(deltaTalSuperior))

    def biotSuperiorInferior(self, Biot, BiotVariacaoDeformacaoNominal):

        BiotInferior = []
        BiotSuperior = []

        for i in range (len(BiotVariacaoDeformacaoNominal)):

            if BiotVariacaoDeformacaoNominal[i] < Biot:

                BiotInferior.append(BiotVariacaoDeformacaoNominal[i])

            elif BiotVariacaoDeformacaoNominal[i] > Biot:

                BiotSuperior.append(BiotVariacaoDeformacaoNominal[i])

        return (max(BiotInferior), min(BiotSuperior))

    def indiceDeltaTalSuperiorInferior(self, deltaTalInferior, deltaTalSuperior, deltaTalTabela):

        indiceInferior = 0
        indiceSuperior = 0

        for i in range(len(deltaTalTabela)):

            if deltaTalTabela[i] == deltaTalInferior:

                indiceInferior = i

            elif deltaTalTabela[i] == deltaTalSuperior:

                indiceSuperior = i

        return (indiceInferior, indiceSuperior)

    def getDeformacaoStarInfSup(self, indiceInferior, indiceSuperior):

        deformacaoStarInf = []
        deformacaoStarSup = []
        deformacaoStarInfFloat = []
        deformacaoStarSupFloat = []
        arrayAux = []
        listaAux = []

        with open(self.currentDir + self.fileNameVariacaoDeformacaoNominal, "rb") as ins:  ### Abre o arquivo controle_fluencia.txt
            for line in ins:
                arrayAux.append(line)

        arrayAux.pop(0)

        for i in range(len(arrayAux)):
            listaAux.append(arrayAux[i].strip('\r\n'))

        for i in range(len(listaAux)):
            deformacaoStarInf.append(listaAux[i].split('\t')[indiceInferior+1])

        for i in range(len(deformacaoStarInf)):
            deformacaoStarInfFloat.append(float(deformacaoStarInf[i]))

        deformacaoStarInfFloat.pop(0)

        for i in range(len(listaAux)):
            deformacaoStarSup.append(listaAux[i].split('\t')[indiceSuperior+1])

        for i in range(len(deformacaoStarSup)):
            deformacaoStarSupFloat.append(float(deformacaoStarSup[i]))

        deformacaoStarSupFloat.pop(0)

        return (deformacaoStarInfFloat, deformacaoStarSupFloat)

    def deformacaoStarInfInterpolado(self, Biot):

        cDeformacaoStarInf = interp1d(self.BiotVariacaoDeformacaoNominal, self.deformacaoStarInf, kind='cubic')

        if Biot >= self.BiotVariacaoDeformacaoNominal[-1]:
            return cDeformacaoStarInf(self.BiotVariacaoDeformacaoNominal[-1])

        elif Biot <= self.BiotVariacaoDeformacaoNominal[0]:
            return cDeformacaoStarInf(self.BiotVariacaoDeformacaoNominal[0])

        else:
            return cDeformacaoStarInf(Biot)

    def deformacaoStarSupInterpolado(self, Biot):

        cDeformacaoStarSup = interp1d(self.BiotVariacaoDeformacaoNominal, self.deformacaoStarSup, kind='cubic')

        if Biot >= self.BiotVariacaoDeformacaoNominal[-1]:
            return cDeformacaoStarSup(self.BiotVariacaoDeformacaoNominal[-1])

        elif Biot <= self.BiotVariacaoDeformacaoNominal[0]:
            return cDeformacaoStarSup(self.BiotVariacaoDeformacaoNominal[0])

        else:
            return cDeformacaoStarSup(Biot)



    def calcDeformacaoNominal(self, Biot):

        deformacaoStar = self.deformacaoStarInfInterpolado(Biot) + ( (Biot - self.BiotInferior) / (self.BiotSuperior - self.BiotInferior) ) * (self.deformacaoStarSupInterpolado(Biot) - self.deformacaoStarInfInterpolado(Biot))
        a = self.deformacaoStarInfInterpolado(Biot)
        b = self.deformacaoStarSupInterpolado(Biot)
        beta = self.betaInterpolado(self.T2Rotor)

        return deformacaoStar*2*beta*self.deltaTvapor

    def getFatorConcentracaoDeformacaoPlastica(self):

        fatorK = []
        razaoDeformacaoNominal = []
        fatorKfloat = []
        razaoDeformacaoNominalFloat = []
        arrayAux = []
        listaAux = []

        with open(self.currentDir + self.fileNameFatorConcentracaoDeformacaoPlastica,
                  "rb") as ins:  ### Abre o arquivo controle_fluencia.txt
            for line in ins:
                arrayAux.append(line)

        for i in range(len(arrayAux)):
            listaAux.append(arrayAux[i].strip('\r\n'))

        for i in range(len(listaAux)):
            razaoDeformacaoNominal.append(listaAux[i].split('                              ')[0])

        for i in range(len(razaoDeformacaoNominal)):
            razaoDeformacaoNominalFloat.append(float(razaoDeformacaoNominal[i]))

        for i in range(len(listaAux)):
            fatorK.append(listaAux[i].split('                              ')[1])

        for i in range(len(fatorK)):
            fatorKfloat.append(float(fatorK[i]))


        return (razaoDeformacaoNominalFloat, fatorKfloat)

    def fatorKinterpolado(self, razaoDeformacaoNominal):

        cFatorK = interp1d(self.razaoDeformacaoNominal, self.fatorK, kind='cubic')

        if razaoDeformacaoNominal >= self.razaoDeformacaoNominal[-1]:
            return cFatorK(self.razaoDeformacaoNominal[-1])

        elif razaoDeformacaoNominal <= self.razaoDeformacaoNominal[0]:
            return cFatorK(self.razaoDeformacaoNominal[0])

        else:
            return cFatorK(razaoDeformacaoNominal)



    def calcDeformacaoTotal(self):

        razaoDeformacaoNominalValor = self.deformacaoNominal/(2*self.epsilonY)

        if razaoDeformacaoNominalValor > self.razaoDeformacaoNominal[-1]:

            razaoDeformacaoNominalValor = self.razaoDeformacaoNominal[-1]

        elif razaoDeformacaoNominalValor < self.razaoDeformacaoNominal[0]:

            razaoDeformacaoNominalValor = self.razaoDeformacaoNominal[0]



        K = self.fatorKinterpolado(razaoDeformacaoNominalValor)

        return self.deformacaoNominal*K

    def calcDeformacaoTotalAnalisado(self, deformacaoTotal):

        deformacaoTotalAnalisado = 0

        if deformacaoTotal < self.variacaoDeformacao[0]:

            deformacaoTotalAnalisado = self.variacaoDeformacao[0]

        else:

            deformacaoTotalAnalisado = deformacaoTotal

        return deformacaoTotalAnalisado

    def numeroCiclosInterpolado(self, variacaoDeformacao):

        cNumeroCiclosInterpolado = interp1d(self.variacaoDeformacao, self.numeroCiclos, kind='cubic')

        if variacaoDeformacao >= self.variacaoDeformacao[-1]:
            return cNumeroCiclosInterpolado(self.variacaoDeformacao[-1])

        elif variacaoDeformacao <= self.variacaoDeformacao[0]:
            return cNumeroCiclosInterpolado(self.variacaoDeformacao[0])

        else:
            return cNumeroCiclosInterpolado(variacaoDeformacao)




    def calcDeltaDfadiga(self):

        if self.deformacaoTotalAnalisado >= self.variacaoDeformacao[-1]:

            nR = self.numeroCiclosInterpolado(self.variacaoDeformacao[-1])
            self.deformacaoTotalAnalisado = self.variacaoDeformacao[-1]

        elif self.deformacaoTotalAnalisado <= self.variacaoDeformacao[0]:

            nR = self.numeroCiclosInterpolado(self.variacaoDeformacao[0])
            self.deformacaoTotalAnalisado = self.variacaoDeformacao[0]

        else:

            nR = self.numeroCiclosInterpolado(self.deformacaoTotalAnalisado)

        return (1/nR , 100/nR)

    def setTabelaCoefCurvaCLE(self):

        DanoDF = [1*10**-5, 3*10**-5, .01*10**-2, .05*10**-2,.1*10**-2, .3*10**-2 ]

        CoefA = [114.4, 70.3, 28.4, 34.7, 64.1, 33.7]

        CoefB = [-38.7, -40, -52.2, -61.3, -72.8, -96.2]

        CoefC = [.86, .95, 1.14, 1.13, 1.05, 1.2]

        return (DanoDF, CoefA, CoefB, CoefC)

    def coefAinterpolado(self, danoDF):

        cCoefAinterpolado = interp1d(self.danoDF, self.CoefA, kind='cubic')

        if danoDF >= self.danoDF[-1]:
            return cCoefAinterpolado(self.danoDF[-1])

        elif danoDF <= self.danoDF[0]:
            return cCoefAinterpolado(self.danoDF[0])

        else:
            return cCoefAinterpolado(danoDF)



    def coefBinterpolado(self, danoDF):

        cCoefBinterpolado = interp1d(self.danoDF, self.CoefB, kind='cubic')

        if danoDF >= self.danoDF[-1]:
            return cCoefBinterpolado(self.danoDF[-1])

        elif danoDF <= self.danoDF[0]:
            return cCoefBinterpolado(self.danoDF[0])

        else:
            return cCoefBinterpolado(danoDF)

    def coefCinterpolado(self, danoDF):

        cCoefCinterpolado = interp1d(self.danoDF, self.CoefC, kind='cubic')

        if danoDF >= self.danoDF[-1]:
            return cCoefCinterpolado(self.danoDF[-1])

        elif danoDF <= self.danoDF[0]:
            return cCoefCinterpolado(self.danoDF[0])

        else:
            return cCoefCinterpolado(danoDF)

    def limCLEf(self, variacaoTemperaturaMetalPartidaSM, duracaoPartidaSM, variacaoTemperaturaCLESM, danoDF):

        taxaAquecimento = variacaoTemperaturaMetalPartidaSM / (duracaoPartidaSM/60.)

        deltaTvap = variacaoTemperaturaCLESM

        NDF = 6

        TA = taxaAquecimento

        limite = []

        saida = ''

        dTdtList = []

        for i in range (NDF):

            dTdt = ( self.coefAinterpolado(danoDF[i]) * (deltaTvap**self.coefCinterpolado(danoDF[i])) ) / ( deltaTvap + self.coefBinterpolado(danoDF[i]) )

            dTdtList.append(dTdt)

        k = 0
        limInferior = 0
        limSuperior = 0

        while (dTdtList[k] < TA) and (k < NDF-1):
            limInferior = k
            k = k + 1

        k = NDF-1

        while (dTdtList[k] > TA) and (k > 0):
            limSuperior = k
            k = k - 1

        limite.append(limInferior)
        limite.append(limSuperior)

        if (TA > dTdtList[0]) and (TA < dTdtList[NDF-1]):

            limite[0] = limInferior + 1
            limite[1] = limSuperior + 1
            saida = limite
            return (saida, TA)


        else:
            saida = "Valor da taxa de aquecimento fora dos limites"


            return (saida, TA)

    def dTdtLimSupInfCLE(self, limCLE, danoDF, variacaoTemperaturaCLESM):

        dTdtLimInfCLE = ''
        dTdtLimSupCLE = ''
        deltaTvap = variacaoTemperaturaCLESM

        if limCLE != "Valor da taxa de aquecimento fora dos limites":

            dTdtLimInfCLE = (self.coefAinterpolado(danoDF[limCLE[0]-1]) * (deltaTvap ** self.coefCinterpolado(danoDF[limCLE[0]-1]))) / (
            deltaTvap + self.coefBinterpolado(danoDF[limCLE[0]-1]))

            dTdtLimSupCLE = (self.coefAinterpolado(danoDF[limCLE[1]-1]) * (
            deltaTvap ** self.coefCinterpolado(danoDF[limCLE[1]-1]))) / (
                                deltaTvap + self.coefBinterpolado(danoDF[limCLE[1]-1]))


        else:

            dTdtLimInfCLE = 0
            dTdtLimSupCLE = 0

        return (dTdtLimInfCLE, dTdtLimSupCLE)

    def dfCLEf(self, limCLE, danoDF, dTdtLimInfCLE, dTdtLimSupCLE, taxaAquecimento):

        dfCLE = ''

        if limCLE != "Valor da taxa de aquecimento fora dos limites":

            dfCLE = danoDF[limCLE[0]-1] + ( danoDF[limCLE[1]-1] - danoDF[limCLE[0]-1] ) *  ((taxaAquecimento - dTdtLimInfCLE) / (dTdtLimSupCLE - dTdtLimInfCLE))

        else:

            dfCLE = "Impossível de ser calculado com base nas curvas CLE fornecidas"

        return dfCLE

    def deltaDfadigaCLEf(self, limCLE, taxaAquecimento, dfCLE, deltaDfadiga, deformacaoTotalAnalisado):

        deltaDfadigaCLE = 0

        if limCLE != "Valor da taxa de aquecimento fora dos limites":

            deltaDfadigaCLE = dfCLE

        elif taxaAquecimento < 48.97959: #[K/hr]

            deltaDfadigaCLE = 10**-5

        elif taxaAquecimento > 325.8307: #[K/hr]

            deltaDfadigaCLE = 0.3*10**-2

        else:

            deltaDfadigaCLE = deltaDfadiga

        NRCLE = 1/deltaDfadigaCLE

        NR = self.numeroCiclosInterpolado(deformacaoTotalAnalisado)

        return (deltaDfadigaCLE, deltaDfadigaCLE*100, NRCLE, NR)

    def outputs(self, NR, nRCLE, deltaDfadiga, deltaDfadigaCLE, indiceInicioTransiente, numeroCiclosFadiga):

        output = []

        if indiceInicioTransiente != -1:

            output = [   [NR, deltaDfadiga*100], [nRCLE, deltaDfadigaCLE*100]   ]

        else:

            output = [ [0,0] , [0,0] ]

        return output

    def saida2f(self, indiceInicioTransiente, NR, nRCLE, numeroCiclosFadiga, deltaDfadiga, deltaDfadigaCLE):

        if indiceInicioTransiente != -1:

            saida2 = [ [40,1,0]  ,   [0,20,30]   , [4, NR, deltaDfadiga*100 ]  , [5, nRCLE, deltaDfadigaCLE*100]]

        else:

            saida2 = [ [40,0,0] , [0,20,30], [4,0,0] , [5,0,0]  ]

        return saida2

    def temperaturaStartEnd(self, indiceInicioTransiente, indiceFimTransiente):

        Tstart = 0
        Tend = 0

        if indiceInicioTransiente != -1:
            Tstart = self.Tv[indiceInicioTransiente]
        else:
            Tstart = self.Tv[0]

        if indiceFimTransiente != -1:
            Tend = self.Tv[indiceFimTransiente]
        else:
            Tend = self.Tv[len(self.Vv) - 1]

        return (Tstart, Tend)

    def convertVazaoValv(self, lista):

        listaAux = []

        for i in range(len(lista)):
            listaAux.append(float(lista[i] * .278))

        return listaAux

    def initVariaveisValv(self, t):

        h0 = 19.
        Tar = 34.
        Tint = 0.8 * self.Ts(t)
        Text = 0.9 * self.Ts(t)
        C1 = self.hiValv(t) * self.mm2m(self.Rint) * (self.Ts(t) - Tint)

        return (h0, Tar, Tint, Text, C1)

    def FunValv(self, u):
        tstart = self.tStart
        return [u[0] / self.mm2m(self.Rint) + self.hiValv(tstart) * (self.Ts(tstart) - u[1]),
                u[0] / self.mm2m(self.Rext) + self.h0 * (u[2] - self.Tar),
                self.ResultadoIntegral(u[1], u[2]) - u[0] * log(self.mm2m(self.Rext) / self.mm2m(self.Rint))]

    def jacValv(self, u):
        tstart = self.tStart
        return np.array([[1 / self.mm2m(self.Rint), -self.hiValv(tstart), 0], [1 / self.mm2m(self.Rext), 0, self.h0],
                         [-u[0], self.PartialDerivativeValv(self.ResultadoIntegral, 0, [u[1], u[2]]),
                          self.PartialDerivativeValv(self.ResultadoIntegral, 1, [u[1], u[2]])]])

    def T0Valv(self, r):  ### Essa função recebe como um dos parametros a soluçao do sistema de equações diferenciais integrais
        ### Além disso, é usada no calculo da Condição Inicial da Eq. do Calor

        Npontosr = 101
        rbar = []
        u = 0
        Trbar = []

        for i in range(Npontosr):
            rbar.append(self.mm2m(self.Rint) + (i) * ((self.mm2m(self.Rext) - self.mm2m(self.Rint)) / (Npontosr - 1)))

            u = ((self.Tint * self.mm2m(self.Rext) - self.Text * self.mm2m(self.Rint)) / (self.mm2m(self.Rext) - self.mm2m(self.Rint))) + ((
                                                                                               self.Text - self.Tint) / (
                                                                                               self.mm2m(self.Rext) - self.mm2m(self.Rint))) * \
                                                                                              rbar[i]

            Trbar.append(fsolve(self.Func, u, rbar[i])[0])

        cTrbar = interp1d(rbar, Trbar)

        if r >= rbar[-1]:
            return cTrbar(rbar[-1])

        elif r <= rbar[0]:
            return cTrbar(rbar[0])

        else:
            return cTrbar(r)






        ################################# Solucao EDP ####################################

    def NuValv(self, t):
        return 0.046 * (self.reynolds(t) ** 0.85) * (self.prandtl(t) ** 0.43)

    def hiValv(self, t):
        return self.NuValv(t) * (self.kPT(self.bar2MPa(self.Ps(t)), self.Celsius2Kelvin(self.Ts(t)))) / (2 * self.mm2m(self.Rint))

    def dkdtValv(self, T):
        return derivative(self.lambdaInterp, T)

    def ktilValv(self, theta_i):
        return self.lambdaInterp(self.Tvap - (self.Tvap - self.Tref) * theta_i)

    def wtilValv(self, theta_i):
        return self.rho * self.cPinterp(self.Tvap - (self.Tvap - self.Tref) * theta_i)

    def ftilValv(self, theta_i):

        if 0.99 <= theta_i <= 1:
            return -0.01263
        else:
            return self.dkdT(self.Tvap - (self.Tvap - self.Tref) * theta_i)

    def htilValv(self, tempoAdimensional):

        return self.hiValv(tempoAdimensional * (self.mm2m(self.Rext) ** 2 / self.alfaEq))

    def T0tilValv(self, posicaoAdimensional):

        return self.T0(self.mm2m(self.Rint) + (self.mm2m(self.Rext) - self.mm2m(self.Rint)) * posicaoAdimensional)

    def epslonValv(self):
        return float(self.mm2m(self.Rint)) / float(self.mm2m(self.Rext))

    def AValv(self, theta_i):
        return self.ktilValv(theta_i) / (self.alfaEq * self.wtilValv(theta_i) * (1 - self.epslonValv()) ** 2)

    def BValv(self, theta_i, R):
        return self.ktilValv(theta_i) / (self.alfaEq * self.wtilValv(theta_i) * (1 - self.epslonValv()) * (
        self.epslonValv() + (1 - self.epslonValv()) * R))

    def CValv(self, theta_i):
        return self.ftilValv(theta_i) * (self.Tvap - self.Tref) / (
        self.alfaEq * self.wtilValv(theta_i) * (1 - self.epslonValv()) ** 2)

    def PartialDerivativeValv(self, func, var=0, point=[]):
        args = point[:]

        def wraps(x):
            args[var] = x
            return func(*args)

        return derivative(wraps, point[var], dx=1e-6)

    def meshEDPValv(self, nR, nt):
        deltaR = 1. / (nR - 1.)
        dt = (self.talEnd - self.talStart) / nt
        return (nR, nt, deltaR, dt)

    def betazaoValv(self, theta_i, R, theta_i_mais1, theta_i_menos1):
        return ((self.AValv(theta_i) / (self.deltaR ** 2)) + (self.BValv(theta_i, R) / (2 * self.deltaR)) - (
            self.CValv(theta_i) / (4 * self.deltaR ** 2)) * theta_i_mais1 + (
                2 * self.CValv(theta_i) / (4 * self.deltaR ** 2)) * theta_i_menos1)

    def alfazaoValv(self, theta_i):
        return (-2 * self.AValv(theta_i) / (self.deltaR ** 2))

    def omegazao2Valv(self, theta_i, R, theta_i_menos1):

        A = self.AValv(theta_i)
        B = self.deltaR ** 2
        C = A / B

        D = self.BValv(theta_i, R)
        E = 2 * self.deltaR
        F = D / E

        G = self.CValv(theta_i)
        H = 4.0 * self.deltaR ** 2
        I = G / H

        J = theta_i_menos1

        return ((self.AValv(theta_i) / (self.deltaR ** 2)) - (self.BValv(theta_i, R) / (2 * self.deltaR)) - (
        self.CValv(theta_i) / (4.0 * self.deltaR ** 2)) * theta_i_menos1)

        # return ((self.A(theta_i) / (self.deltaR ** 2)) - (self.B(theta_i, R) / (2 * self.deltaR)) - (
        # self.Ca(theta_i) / (4 * self.deltaR ** 2)) * theta_i_menos1)

    def FC1Valv(self, theta_i, tempoAdimensional):
        var = self.mm2m(self.Rext) ** 2 / self.alfaEq
        return ((self.htilValv(tempoAdimensional) * (self.mm2m(self.Rext) - self.mm2m(self.Rint)) / self.ktilValv(theta_i)) * (
            (self.Ts(var * tempoAdimensional) - self.Tvap + (self.Tvap - self.Tref) * theta_i) / (
            self.Tvap - self.Tref)))

    def FC2Valv(self, theta_i):
        return (
            ((self.ho * (self.mm2m(self.Rext) - self.mm2m(self.Rint))) / self.ktilValv(theta_i)) * (
            (self.Tvap - self.Tar - (self.Tvap - self.Tref) * theta_i) / (self.Tvap - self.Tref)))

    def dFC1dthetaValv(self, theta_i, tempoAdimensional):

        dtheta = 10 ** -6

        return (self.FC1Valv(theta_i + dtheta, tempoAdimensional) - self.FC1Valv(theta_i, tempoAdimensional)) / dtheta

    def dFC2dthetaValv(self, theta_i):

        dtheta = 10 ** -6

        return (self.FC2Valv(theta_i + dtheta) - self.FC2Valv(theta_i)) / dtheta

    def dFC1dtValv(self, theta_i, tempoAdimensional):

        dt = 10 ** -6

        return (self.FC1Valv(theta_i, tempoAdimensional + dt) - self.FC1Valv(theta_i, tempoAdimensional)) / dt

    def f0Valv(self, U, t):
        theta = U
        tempoAdimensional = t
        return self.deltaR * self.dFC1dtValv(theta, tempoAdimensional)

    def vecFValv(self, t, U):

        f = np.zeros((self.nR, 1))
        f[0][0] = self.deltaR * self.dFC1dtValv(U[0], t)

        return f

    def MatrizMValv(self, t, U):

        M = np.zeros((self.nR, self.nR))

        M[0][0] = -(1 + self.deltaR * self.dFC1dthetaValv(U[0], t))
        M[0][1] = 1
        M[self.nR - 1][self.nR - 2] = - 1
        M[self.nR - 1][self.nR - 1] = (1 - self.deltaR * self.dFC2dthetaValv(U[self.nR - 1]))

        for i in range(1, self.nR - 1):
            M[i][i] = 1

        return M

    def MatrizAValv(self, t, U):

        Au = np.zeros((self.nR, self.nR))

        for i in range(1, self.nR - 1):

            if 1 <= i <= self.nR - 2:
                Au[i][i] = self.alfazaoValv(U[i])

            for j in range(self.nR):

                if (i - j == 1):

                    Au[i][j] = self.omegazao2Valv(U[i], self.R[i], U[i - 1])

                elif (j - i == 1):

                    Au[i][j] = self.betazaoValv(U[i], self.R[i], U[i + 1], U[i - 1])

        return Au

    def PendEficienteValv(self, t, U):
        return np.add(np.dot(inv(self.MatrizMValv(t, U)), np.dot(self.MatrizAValv(t, U), U)).reshape(self.nR, 1),
                      np.dot(inv(self.MatrizMValv(t, U)), self.vecFValv(t, U))).flatten()

    def CondInicialValv(self, R):
        return (self.Tvap - self.T0tilValv(R)) / (self.Tvap - self.Tref)

    def TemperaturasIniciaisU0Valv(self, nR):

        R0 = np.linspace(0, 1, nR)
        U0 = []
        for i in range(nR):
            U0.append(self.CondInicialValv(R0[i]))
        U0 = np.asarray(U0)

        return U0

    def rEDPValv(self, nR):

        R = np.linspace(0, 1, nR)
        listR = []
        for i in range(nR):
            listR.append(R[i])

        return listR

    def tEDPValv(self, nt):

        t = np.linspace(self.talStart, self.talEnd, self.nt)

        return t

    def callSolutionValv(self, talStart, talEnd, dt, nR):

        r = ode(self.PendEficienteValv).set_integrator('lsoda', method='adams', atol=1e-6,
                                                   with_jacobian=False)  # passar atol para 1e-6 depois
        # r.set_initial_value(self.TemperaturasIniciaisU0Valv(nR), talStart + 0.01)
        # talStart = (self.tempoFiltro1[1]*self.alfaEq) / self.mm2m(self.Rext)
        # talEnd = (self.tempoFiltro1[len(self.tempoFiltro1)-2]*self.alfaEq) / self.mm2m(self.Rext)

        r.set_initial_value(self.TemperaturasIniciaisU0Valv(nR), talStart)
        print "Condição Inicial: " + '\n' + '\n' + str(self.TemperaturasIniciaisU0Valv(nR))

        u = []
        t = []

        var = self.alfaEq / self.mm2m(self.Rext)**2

        while r.successful() and r.t <= talEnd - .003:
            r.integrate(r.t + dt)
            u.append(r.y)
            t.append(r.t)
            print "Tempo Adimensional -> " + str(r.t) + "    " + "Tempo Dimensional -> " + str((r.t)/var) + '\n' + '\n' + "Temperaturas Adimensionais: " + '\n' + str(r.y) + '\n' + '\n' + "Interpolação Linear da Vazao do Vapor -> " + str(self.mVapor(r.t/var)) + "\n" + "\n" + "**********" + "\n" + "\n"


        return u, t

    def mindiffF(self, lista, threshold3):

        mindiff = 1000
        posthreshold = 0
        diff = 0

        for i in range(len(lista)):

            if lista[i] >= threshold3:
                posthreshold = i
                break

        for i in range(posthreshold + 1, len(lista), 1):

            diff = abs(lista[posthreshold] - lista[i])

            if diff < mindiff:
                mindiff = diff

        a = lista[266]
        b = lista[267]
        c = lista[268]
        d = lista[269]
        e = lista[252]

        return mindiff

    def sign(self, x):
        if x > 0:
            return 1.
        elif x < 0:
            return -1.
        elif x == 0:
            return 0.
        else:
            return x

    def getIndex(self, lista, startIndex, width, threshold):

        pos = 0

        for i in range(startIndex, (len(lista) - width)):

            if (lista[i + width - 1] - lista[i]) * self.sign(threshold) > abs(threshold):
                pos = i
                break

        if pos == len(lista) - width + 1:
            pos = -1
            return pos

        else:
            return pos

    def setMats(self):

        matVazao = []
        matPressao = []
        matTemperatura = []

        matVazao = [[self.tempo], [self.Vv]]
        matPressao = [[self.tempo], [self.pv]]
        matTemperatura = [[self.tempo], [self.Tv]]

        return (matVazao, matPressao, matTemperatura)

    def matMods(self, indiceInicioVazao, indiceInicioTemperatura, indiceInicioPressao):

        matVazaoMod = []
        matVazaoMod2 = []
        tVazao = []
        matTemperaturaMod = []
        matTemperaturaMod2 = []
        tTemperatura = []
        matPressaoMod = []
        matPressaoMod2 = []
        tPressao = []

        for i in range(indiceInicioVazao + 1, len(self.Vv)):
            tVazao.append(self.tempo[i])
            matVazaoMod2.append(self.Vv[i])

        for i in range(indiceInicioTemperatura, len(self.Tv)):
            tTemperatura.append(self.tempo[i])
            matTemperaturaMod2.append(self.Tv[i])

        for i in range(indiceInicioPressao + 1, len(self.pv)):
            tPressao.append(self.tempo[i])
            matPressaoMod2.append(self.pv[i])

        tmin = int(min(tTemperatura[0], tPressao[0], tVazao[0])) + 5

        NmaxElem = max(len(matVazaoMod2), len(matPressaoMod2), len(matTemperaturaMod2))

        matVazaoMod = [tVazao, matVazaoMod2]
        matTemperaturaMod = [tTemperatura, matTemperaturaMod2]
        matPressaoMod = [tPressao, matPressaoMod2]

        return (
            tVazao[0], matVazaoMod, tTemperatura[0], matTemperaturaMod, tPressao[0], matPressaoMod, NmaxElem, tmin)

    def Npontospreench(self, Ind1):

        return int(self.nmaxElem - Ind1)

    def modifica(self, IndMin, tmin, matriz):

        vaux1 = []
        vaux2 = []
        vaux = []

        if self.Npontospreench(IndMin) == 0:
            vaux = matriz

            return vaux

        else:
            for i in range(self.Npontospreench(IndMin)):
                vaux1.append(int(tmin) + (i - 1) * 5)
                vaux2.append(matriz[1][0])

            for i in range(len(matriz[0])):
                vaux1.append(matriz[0][i])  # i+13
                vaux2.append(matriz[1][i])

            vaux = [vaux1, vaux2]

            return vaux

    def convertVazao(self, lista):

        listaAux = []

        for i in range(len(lista)):
            listaAux.append(float(lista[i] * .278 / 2.))

        return listaAux

    def calcVariacoesTubValv(self):

        duracaoPartidaSM = float(self.instanteFimTransiente) - float(self.instanteInicioTransiente)
        variacaoTemperaturaVaporPartidaSM = abs(
            float(self.TvaporFiltro1[0]) - float(self.TvaporFiltro1[len(self.TvaporFiltro1) - 1]))

        return (duracaoPartidaSM, variacaoTemperaturaVaporPartidaSM)

    def getCurva(self, fileNameCurva):

        listaAux = []
        arrayAux = []
        amplitudeTensao = []
        amplitudeDeformacao = []
        amplitudeTensaoFloat = []
        amplitudeDeformacaoFloat = []

        with open(self.currentDir + fileNameCurva, "rb") as ins:
            for line in ins:
                arrayAux.append(line)

        for i in range(len(arrayAux)):
            listaAux.append(arrayAux[i].strip('\r\n'))

        for i in range(len(listaAux)):
            amplitudeTensao.append(listaAux[i].split('\t')[0])

        for i in range(len(listaAux)):
            amplitudeDeformacao.append(listaAux[i].split('\t')[1])

        for i in range(len(amplitudeTensao)):
            amplitudeTensaoFloat.append(float(amplitudeTensao[i]))

        for i in range(len(amplitudeDeformacao)):
            amplitudeDeformacaoFloat.append(float(amplitudeDeformacao[i]))

        return (amplitudeTensaoFloat, amplitudeDeformacaoFloat)

    def variacaoDeformacaoInterpolado(self, ampTensao):

        cvariacaoDeformacaoInterpolado = interp1d(self.amplitudeTensao, self.amplitudeDeformacao)

        if ampTensao >= self.amplitudeTensao[-1]:
            return cvariacaoDeformacaoInterpolado(self.amplitudeTensao[-1])

        elif ampTensao <= self.amplitudeTensao[0]:
            return cvariacaoDeformacaoInterpolado(self.amplitudeTensao[0])

        else:
            return cvariacaoDeformacaoInterpolado(ampTensao)



        return cvariacaoDeformacaoInterpolado(ampTensao)

    def numeroCiclosNRinterpolado(self, ampDeformacao):

        cNumeroCiclosNRinterpolado = interp1d(self.amplitudeDeformacaoNR, self.Nf25)

        if ampDeformacao <= self.amplitudeDeformacaoNR[0]:

            return cNumeroCiclosNRinterpolado(self.amplitudeDeformacaoNR[0])

        elif ampDeformacao >= self.amplitudeDeformacaoNR[-1]:

            return cNumeroCiclosNRinterpolado(self.amplitudeDeformacaoNR[-1])

        else:

            return cNumeroCiclosNRinterpolado(ampDeformacao)

    def initVariaveis(self, t):

        h0 = 19.
        Tar = 34.
        Tint = 0.8 * self.Ts(t)
        Text = 0.9 * self.Ts(t)
        C1 = self.hi(t) * self.mm2m(self.Rint) * (self.Ts(t) - Tint)

        return (h0, Tar, Tint, Text, C1)

    def ResultadoIntegral(self, Tint, Text):

        integrand = lambda T: self.lambdaInterp(T)
        I, err = quad(integrand, Tint, Text)
        return I

    def Fun(self, u):
        tstart = self.tStart
        return [u[0] / self.mm2m(self.Rint) + self.hi(tstart) * (self.Ts(tstart) - u[1]),
                u[0] / self.mm2m(self.Rext) + self.h0 * (u[2] - self.Tar),
                self.ResultadoIntegral(u[1], u[2]) - u[0] * log(self.mm2m(self.Rext) / self.mm2m(self.Rint))]

    def F1(self, C1, Tint):
        return C1 / self.mm2m(self.Rint) + self.hi(self.tstart) * (self.Ts(self.tstart) - Tint)

    def F2(self, C1, Text):
        return C1 / self.mm2m(self.Rext) + self.ho * (Text - self.Tar)

    def F3(self, C1, Tint, Text):
        return self.ResultadoIntegral(Tint + 273, Text + 273) - C1 * log(self.mm2m(self.Rext) / self.mm2m(self.Rint))

    def Func(self, T, r):

        integrand = lambda T: self.lambdaInterp(T)
        I, err = quad(integrand, self.sol2, T)

        return I - self.sol1 * log(r / self.mm2m(self.Rint))  ### Resolver a questao dos sol1 sol2 e sol3

    def jac(self, u):
        tstart = self.tStart
        return np.array([[1 / self.mm2m(self.Rint), -self.hi(tstart), 0], [1 / self.mm2m(self.Rext), 0, self.h0],
                         [-u[0], self.PartialDerivative(self.ResultadoIntegral, 0, [u[1], u[2]]),
                          self.PartialDerivative(self.ResultadoIntegral, 1, [u[1], u[2]])]])

    def T0(self,r):  ### Essa função recebe como um dos parametros a soluçao do sistema de equações diferenciais integrais
        ### Além disso, é usada no calculo da Condição Inicial da Eq. do Calor

        Npontosr = 101
        rbar = []
        u = 0
        Trbar = []

        for i in range(Npontosr):
            rbar.append(self.mm2m(self.Rint) + (i) * ((self.mm2m(self.Rext) - self.mm2m(self.Rint)) / (Npontosr - 1)))

            u = ((self.Tint * self.mm2m(self.Rext) - self.Text * self.mm2m(self.Rint)) / (self.mm2m(self.Rext) - self.mm2m(self.Rint))) + ((
                                                                                                   self.Text - self.Tint) / (
                                                                                                   self.mm2m(self.Rext) - self.mm2m(self.Rint))) * \
                                                                                              rbar[i]

            Trbar.append(fsolve(self.Func, u, rbar[i])[0])

        cTrbar = interp1d(rbar, Trbar)

        if r >= rbar[-1]:
            return cTrbar(rbar[-1])

        elif r <= rbar[0]:
            return cTrbar(rbar[0])

        else:
            return cTrbar(r)

    def alfaEqs(self, T):

        return self.lambdaInterp(T) / (self.rho * self.cPinterp(T))

    def tal(self, alfa, t, R):
        return alfa * t / (R ** 2)


        ################################### Inicio das Funções implementadas na EDP ###################################

    def mVapor(self, t):

        cmVapor = interp1d(self.tempoFiltro1, self.VvaporFiltro1) # retirar essa estrutura, pois pode deixar a solução numéria da EDP lenta

        if t >= self.tempoFiltro1[-1]:
            return float(cmVapor(self.tempoFiltro1[-1]))

        elif t <= self.tempoFiltro1[0]:
            return float(cmVapor(self.tempoFiltro1[0]))

        else:
            return float(cmVapor(t))




    def Ts(self, t):

        cTs = interp1d(self.tempoFiltro1,
                       self.TvaporFiltro1)  # retirei a interpolção cúbica, pois o polinômio de interpolação não estava ok!

        if t >= self.tempoFiltro1[-1]:
            return float(cTs(self.tempoFiltro1[-1]))

        elif t <= self.tempoFiltro1[0]:
            return float(cTs(self.tempoFiltro1[0]))

        else:
            return float(cTs(t))



    def Ps(self, t):

        cPs = interp1d(self.tempoFiltro1,
                       self.PvaporFiltro1)  # retirei a interpolção cúbica, pois o polinômio de interpolação não estava ok!

        if t >= self.tempoFiltro1[-1]:
            return float(cPs(self.tempoFiltro1[-1]))

        elif t <= self.tempoFiltro1[0]:
            return float(cPs(self.tempoFiltro1[0]))

        else:
            return float(cPs(t))



    def betaInterp(self, T):

        cCoefExpansaoTerm = interp1d(self.TempPropMec, self.coefExpansaoTerm, kind='cubic')

        if T >= self.TempPropMec[-1]:
            return float(cCoefExpansaoTerm(self.TempPropMec[-1]))

        elif T <= self.TempPropMec[0]:
            return float(cCoefExpansaoTerm(self.TempPropMec[0]))

        else:
            return float(cCoefExpansaoTerm(T))



    def niInterp(self, T):

        cCoeficientePoisson = interp1d(self.TempCoefPoisson, self.CoefPoisson, kind='cubic')

        if T >= self.TempCoefPoisson[-1]:
            return float(cCoeficientePoisson(self.TempCoefPoisson[-1]))

        elif T <= self.TempCoefPoisson[0]:
            return float(cCoeficientePoisson(self.TempCoefPoisson[0]))

        else:
            return float(cCoeficientePoisson(T))



    def Einterp(self, T):

        cModuloElasticidade = interp1d(self.TempPropMec, self.moduloElasticidade, kind='cubic')

        if T >= self.TempPropMec[-1]:
            return float(cModuloElasticidade(self.TempPropMec[-1]))

        elif T <= self.TempPropMec[0]:
            return float(cModuloElasticidade(self.TempPropMec[0]))

        else:
            return float(cModuloElasticidade(T))



    def alphaInterp(self, T):

        cCondutividadeTerm = interp1d(self.TempPropMec, self.condutividadeTerm, kind='cubic')
        cCalorEspecificoPcte = interp1d(self.TempPropMec, self.calorEspecificoPcte, kind='cubic')

        if T >= self.TempPropMec[-1]:
            condutividadeTerm = cCondutividadeTerm(self.TempPropMec[-1])
            calorEspecificoPcte = cCalorEspecificoPcte(self.TempPropMec[-1])

        elif T <= self.TempPropMec[0]:
            condutividadeTerm = cCondutividadeTerm(self.TempPropMec[0])
            calorEspecificoPcte = cCalorEspecificoPcte(self.TempPropMec[0])
        else:
            condutividadeTerm = cCondutividadeTerm(T)
            calorEspecificoPcte = cCalorEspecificoPcte(T)

        return float(condutividadeTerm / (self.rho * calorEspecificoPcte))



    def lambdaInterp(self, T):

        cCondutividadeTerm = interp1d(self.TempPropMec, self.condutividadeTerm, kind='cubic')

        if T >= self.TempPropMec[-1]:
            return cCondutividadeTerm(self.TempPropMec[-1])

        elif T <= self.TempPropMec[0]:
            return cCondutividadeTerm(self.TempPropMec[0])

        else:
            return cCondutividadeTerm(T)



    def cPinterp(self, T):

        cCalorEspecificoPcte = interp1d(self.TempPropMec, self.calorEspecificoPcte, kind='cubic')

        if T >= self.TempPropMec[-1]:
            return cCalorEspecificoPcte(self.TempPropMec[-1])

        elif T <= self.TempPropMec[0]:
            return cCalorEspecificoPcte(self.TempPropMec[0])

        else:
            return cCalorEspecificoPcte(T)



    def reynolds(self, t):
        return (4 * self.mVapor(t)) / (
            pi * 2 * self.mm2m(self.Rint) * self.muPT(self.bar2MPa(self.Ps(t)), self.Celsius2Kelvin(self.Ts(t))))

    def prandtl(self, t):
        return self.niPT(self.bar2MPa(self.Ps(t)), self.Celsius2Kelvin(self.Ts(t))) / self.alfaPT(
            self.bar2MPa(self.Ps(t)), self.Celsius2Kelvin(self.Ts(t)))

    def fricFactor(self, t):

        if self.reynolds(t) < 2300.:
            return 64. / self.reynolds(t)
        else:
            return 1. / (((.79 * log(self.reynolds(t)) - 1.64)) ** 2)

    def nusselt(self, t):

        if self.reynolds(t) < 2300.:
            return 3.66
        else:
            return ((self.fricFactor(t) / 8.) * self.prandtl(t) * (self.reynolds(t) - 1000)) / (
                1 + 12.7 * ((self.fricFactor(t) / 8.) ** .5) * ((self.prandtl(t) ** (2 / 3.)) - 1))

    def dkdT(self, T):
        return derivative(self.lambdaInterp, T)

    def ktil(self, theta_i):
        return self.lambdaInterp(self.Tvap - (self.Tvap - self.Tref) * theta_i)

    def wtil(self, theta_i):
        return self.rho * self.cPinterp(self.Tvap - (self.Tvap - self.Tref) * theta_i)

    def ftil(self, theta_i):

        if 0.99 <= theta_i <= 1:
            return -0.01263
        else:
            return self.dkdT(self.Tvap - (self.Tvap - self.Tref) * theta_i)

    def htil(self, tempoAdimensional):

        return self.hi(tempoAdimensional * (self.mm2m(self.Rext) ** 2 / self.alfaEq))

    def hi(self, t):
        return self.nusselt(t) * (self.kPT(self.bar2MPa(self.Ps(t)), self.Celsius2Kelvin(self.Ts(t)))) / (
            2 * self.mm2m(self.Rint))

    def T0til(self, posicaoAdimensional):

        return self.T0(self.mm2m(self.Rint) + (self.mm2m(self.Rext) - self.mm2m(self.Rint)) * posicaoAdimensional)

    def epslon(self):
        return float(self.mm2m(self.Rint)) / float(self.mm2m(self.Rext))

    def A(self, theta_i):
        return self.ktil(theta_i) / (self.alfaEq * self.wtil(theta_i) * (1 - self.epslon()) ** 2)

    def B(self, theta_i, R):
        return self.ktil(theta_i) / (
            self.alfaEq * self.wtil(theta_i) * (1 - self.epslon()) * (self.epslon() + (1 - self.epslon()) * R))

    def Ca(self, theta_i):
        return self.ftil(theta_i) * (self.Tvap - self.Tref) / (
            self.alfaEq * self.wtil(theta_i) * (1 - self.epslon()) ** 2)

    def PartialDerivative(self, func, var=0, point=[]):
        args = point[:]

        def wraps(x):
            args[var] = x
            return func(*args)

        return derivative(wraps, point[var], dx=1e-6)

    def meshEDP(self, nR, nt):
        deltaR = 1. / (nR - 1.)
        dt = (self.talEnd - self.talStart) / nt
        return (nR, nt, deltaR, dt)

    def betazao(self, theta_i, R, theta_i_mais1, theta_i_menos1):
        return ((self.A(theta_i) / (self.deltaR ** 2)) + (self.B(theta_i, R) / (2 * self.deltaR)) - (
            self.Ca(theta_i) / (4 * self.deltaR ** 2)) * theta_i_mais1 + (
                    2 * self.Ca(theta_i) / (4 * self.deltaR ** 2)) * theta_i_menos1)

    def alfazao(self, theta_i):
        return (-2 * self.A(theta_i) / (self.deltaR ** 2))

    def omegazao2(self, theta_i, R, theta_i_menos1):

        A = self.A(theta_i)
        B = self.deltaR ** 2
        C = A / B

        D = self.B(theta_i, R)
        E = 2 * self.deltaR
        F = D / E

        G = self.Ca(theta_i)
        H = 4.0 * self.deltaR ** 2
        I = G / H

        J = theta_i_menos1

        return ((self.A(theta_i) / (self.deltaR ** 2)) - (self.B(theta_i, R) / (2 * self.deltaR)) - (
            self.Ca(theta_i) / (4.0 * self.deltaR ** 2)) * theta_i_menos1)

        # return ((self.A(theta_i) / (self.deltaR ** 2)) - (self.B(theta_i, R) / (2 * self.deltaR)) - (
        # self.Ca(theta_i) / (4 * self.deltaR ** 2)) * theta_i_menos1)

    def FC1(self, theta_i, tempoAdimensional):
        var = self.mm2m(self.Rext) ** 2 / self.alfaEq
        return ((self.htil(tempoAdimensional) * (self.mm2m(self.Rext) - self.mm2m(self.Rint)) / self.ktil(theta_i)) * (
            (self.Ts(var * tempoAdimensional) - self.Tvap + (self.Tvap - self.Tref) * theta_i) / (
                self.Tvap - self.Tref)))

    def FC2(self, theta_i):
        return (
            ((self.ho * (self.mm2m(self.Rext) - self.mm2m(self.Rint))) / self.ktil(theta_i)) * (
                (self.Tvap - self.Tar - (self.Tvap - self.Tref) * theta_i) / (self.Tvap - self.Tref)))

    def dFC1dtheta(self, theta_i, tempoAdimensional):

        dtheta = 10 ** -6

        return (self.FC1(theta_i + dtheta, tempoAdimensional) - self.FC1(theta_i, tempoAdimensional)) / dtheta

    def dFC2dtheta(self, theta_i):

        dtheta = 10 ** -6

        return (self.FC2(theta_i + dtheta) - self.FC2(theta_i)) / dtheta

    def dFC1dt(self, theta_i, tempoAdimensional):

        dt = 10 ** -6

        return (self.FC1(theta_i, tempoAdimensional + dt) - self.FC1(theta_i, tempoAdimensional)) / dt

    def f0(self, U, t):
        theta = U
        tempoAdimensional = t
        return self.deltaR * self.dFC1dt(theta, tempoAdimensional)

    def vecF(self, t, U):

        f = np.zeros((self.nR, 1))
        f[0][0] = self.deltaR * self.dFC1dt(U[0], t)

        return f

    def MatrizM(self, t, U):

        M = np.zeros((self.nR, self.nR))

        M[0][0] = -(1 + self.deltaR * self.dFC1dtheta(U[0], t))
        M[0][1] = 1
        M[self.nR - 1][self.nR - 2] = - 1
        M[self.nR - 1][self.nR - 1] = (1 - self.deltaR * self.dFC2dtheta(U[self.nR - 1]))

        for i in range(1, self.nR - 1):
            M[i][i] = 1

        return M

    def MatrizA(self, t, U):

        Au = np.zeros((self.nR, self.nR))

        for i in range(1, self.nR - 1):

            if 1 <= i <= self.nR - 2:
                Au[i][i] = self.alfazao(U[i])

            for j in range(self.nR):

                if (i - j == 1):

                    Au[i][j] = self.omegazao2(U[i], self.R[i], U[i - 1])

                elif (j - i == 1):

                    Au[i][j] = self.betazao(U[i], self.R[i], U[i + 1], U[i - 1])

        return Au

    def PendEficiente(self, t, U):
        return np.add(np.dot(inv(self.MatrizM(t, U)), np.dot(self.MatrizA(t, U), U)).reshape(self.nR, 1),
                      np.dot(inv(self.MatrizM(t, U)), self.vecF(t, U))).flatten()

    def CondInicial(self, R):
        return (self.Tvap - self.T0til(R)) / (self.Tvap - self.Tref)

    def TemperaturasIniciaisU0(self, nR):

        R0 = np.linspace(0, 1, nR)
        U0 = []
        for i in range(nR):
            U0.append(self.CondInicial(R0[i]))
        U0 = np.asarray(U0)

        return U0

    def rEDP(self, nR):

        R = np.linspace(0, 1, nR)
        listR = []
        for i in range(nR):
            listR.append(R[i])

        return listR

    def tEDP(self, nt):

        t = np.linspace(self.talStart, self.talEnd, self.nt)

        return t

    def callSolution(self, talStart, talEnd, dt, nR):

        r = ode(self.PendEficiente).set_integrator('lsoda', method='adams', atol=1e-6,
                                                   with_jacobian=False)  # passar atol para 1e-6 depois
        r.set_initial_value(self.TemperaturasIniciaisU0(nR), talStart)
        u = []
        t = []

        var = self.alfaEq / self.mm2m(self.Rext)**2

        while r.successful() and r.t <= talEnd - .05:
            r.integrate(r.t + dt)
            u.append(r.y)
            t.append(r.t)
            print "Tempo Adimensional -> " + str(r.t) + "    " + "Tempo Dimensional -> " + str((r.t)/var) + '\n' + '\n' + "Temperaturas Adimensionais: " + '\n' + str(r.y) + '\n' + '\n' + "Interpolação Cúbica da Vazao do Vapor -> " + str(self.mVapor(r.t/var)) + "\n" + "\n" + "**********" + "\n" + "\n"

        return u, t

    def min2sList(self, lista):

        for i in range(len(lista)):
            lista[i] = float(lista[i]) * 60.

        return lista


    # def checkTransienteBrusco(self):
    #
    #     retCode = -1
    #
    #     if



        #################### Pos-solução da EDP #######################################################

    def vazaoStartEnd(self, indiceInicioTransiente, indiceFimTransiente):

        Vstart = 0
        Vend = 0

        if indiceInicioTransiente != -1:
            Vstart = self.Vv[indiceInicioTransiente]
        else:
            Vstart = self.Vv[0]

        if indiceFimTransiente != -1:
            Vend = self.Vv[indiceFimTransiente]
        else:
            Vend = self.Vv[len(self.Vv) - 1]

        return (Vstart, Vend)


        # def Temperature(self, tvar, Rvar):


        # Temperature = interp2d(self.R, self.tSol, self.uSol)

        # return float(Temperature(tvar, Rvar))

    def Temperature(self, Rvar, tvar):

        Temperature = interp2d(self.R, self.tSol, self.uSol)

        return float(Temperature(Rvar, tvar))

    def TemperatureInt(self):

        uInt = []
        for i in range(len(self.uSol)):
            uInt.append(self.uSol[i][0])

        return uInt

    def thetaInt(self, tvar):

        thetaInt = interp1d(self.tSol, self.uInt)

        return float(thetaInt(tvar))


        # def Tm(self, t):

        # Rint = self.mm2m(self.Rint)
        # Rext = self.mm2m(self.Rext)
        # Tvap = self.Tvap
        # Tref = self.Tref

        # integrand = lambda R: ( Rint + (Rext - Rint)*R ) * ( Tvap - (Tvap - Tref)*self.Temperature(t, R)) # Temperature(R, t) é uma função que vai ser definida após a resolução da EDP
        # I, err = quad(integrand, 0, 1)
        # return ( 2 / (Rext + Rint)) * I

    def Tm(self, t):

        return self.Tvap - self.thetaInt(t) * (self.Tvap - self.Tref)

    def thetam(self, t):
        return (self.Tvap - self.Tm(t)) / (self.Tvap - self.Tref)

    def sigmaPhiRint(self, t):

        Tvap = self.Tvap
        Tref = self.Tref
        # A função thetaInt(t) é uma função que vai ser definida após a resolução da EDP

        A = -self.betaInterp(self.Tm(t)) * self.Einterp(self.Tm(t))

        B = (Tvap - (Tvap - Tref) * self.thetaInt(t) * 1.06 - self.Tm(t))

        C = (1 - self.niInterpolado(self.Tm(t)))

        return A * B / C

    def sigmaPhi(self, t, R):  # Substitui Temperature(t, R) por thetaInt(t)
        # Eliminei a integral que dava 0!!!

        Rint = self.mm2m(self.Rint)
        Rext = self.mm2m(self.Rext)
        Tvap = self.Tvap
        Tref = self.Tref

        A = self.betaInterp(Tvap - (Tvap - Tref) * self.Temperature(R, t)) / (
            1 - self.niInterp(Tvap - (Tvap - Tref) * self.Temperature(R, t)))
        A1 = self.betaInterp(Tvap - (Tvap - Tref) * self.Temperature(R, t))
        A2 = self.niInterp(Tvap - (Tvap - Tref) * self.Temperature(R, t))

        B = self.Einterp(Tvap - (Tvap - Tref) * self.Temperature(R, t))

        C = 1 / (Rext ** 2 - Rint ** 2)

        D = 1 + ((Rint ** 2) / ((Rint + (Rext - Rint) * R) ** 2))

        integrandE = lambda R: (Tvap - (Tvap - Tref) * self.Temperature(R, t)) * (Rint + (Rext - Rint) * R) * (
            Rext - Rint)
        IE, errE = quad(integrandE, 0, 1)

        E = IE

        integrandF = lambda X: (Rint + (Rext - Rint) * X) * (Tvap - (Tvap - Tref) * self.Temperature(X, t)) * (
            Rext - Rint)
        IF, errF = quad(integrandF, 0, R)

        F = IF / (Rint + (Rext - Rint) * R) ** 2

        G = (Tvap - (Tvap - Tref) * self.Temperature(R, t))

        Resultado = A * B * (C * D * E + F - G)

        return A * B * (C * D * E + F - G)

    def tempoAdimensionalList(self, Npontost):

        # talStart = (self.tempoFiltro1[1] * self.alfaEq) / self.mm2m(self.Rext)
        # talEnd = (self.tempoFiltro1[len(self.tempoFiltro1) - 2] * self.alfaEq) / self.mm2m(self.Rext)

        tempoAdimensionalList = np.linspace(self.talStart , self.talEnd , num=Npontost)

        # for i in range (1, Npontost+1):

        # tempoAdimensionalList.append(self.tStart + (i-1) * ( (self.talEnd - self.talStart) / (Npontost - 1)))

        return tempoAdimensionalList

    def TensaoTermicaTangencial(self, Npontost):

        TensaoTermicaTangencialList = []

        for i in range(Npontost):
            TensaoTermicaTangencialList.append(self.sigmaPhi(self.tempoAdimensional[i], 0))

        return TensaoTermicaTangencialList

    def TensaoMecanicaTangencial(self, Npontost):

        TensaoMecanicaTangencialList = []

        for i in range(Npontost):
            TensaoMecanicaTangencialList.append(self.sigmaMec(self.tempoAdimensional[i]))

        return TensaoMecanicaTangencialList

    def TensaoMecanicaTangencialCurva(self, Npontost):

        TensaoMecanicaTangencialCurvaList = []

        for i in range(Npontost):
            TensaoMecanicaTangencialCurvaList.append(self.sigmaMecCurva(self.tempoAdimensional[i]))

        return TensaoMecanicaTangencialCurvaList

    def sigmaMec(self, t):

        Rint = self.mm2m(self.Rint)
        Rext = self.mm2m(self.Rext)

        r = Rext / Rint
        var = Rext ** 2 / self.alfaEq

        return (self.Ps(var * t) * 0.1 * (r ** 2 + 1)) / (r ** 2 - 1)

    def sigmaMecCurva(self, t):

        return self.f1 * self.sigmaMec(t)

    def TensaoMaxMin(self, Npontost):

        SomaTensoes = []

        for i in range(Npontost):
            SomaTensoes.append(self.TensaoMecanicaTangencialList[i] + self.TensaoTermicaTangencialList[i])

        return (max(SomaTensoes), min(SomaTensoes))

    def TensaoMaxMinCurva(self, Npontost):

        SomaTensoesCurva = []
        TensaoMecanicaTangencialCurvaList = self.TensaoMecanicaTangencialCurva(Npontost)
        TensaoTermicaTangencialCurvaList = self.TensaoTermicaTangencial(Npontost)

        for i in range(Npontost):
            SomaTensoesCurva.append(TensaoMecanicaTangencialCurvaList[i] + TensaoTermicaTangencialCurvaList[i])

        return (max(SomaTensoesCurva), min(SomaTensoesCurva))

    def variacaoTensaoTermMecFunction(self, TensaoMax, TensaoMin):

        return abs((TensaoMax - TensaoMin) / 2.)

    def variacaoDeformacaoTotalFunction(self, variacaoTensao):

        return self.variacaoDeformacaoInterpolado(variacaoTensao)

    def numeroCiclosEstimadoTrincaFunction(self, variacaoDeformacaoTotal):

        return self.numeroCiclosNRinterpolado(variacaoDeformacaoTotal)

    def danoAcumuladoFadigaFunction(self, NRestimado):

        return 1 / NRestimado

    def resultadoFadigaTubulacaoFunction(self, NRestimado, NRestimadoc, numeroCiclosFadiga, danoAcumuladoFadiga,
                                         danoAcumuladoFadigaCurv, indiceInicioTransiente):

        resultadoFadigaTubulacao = []

        if indiceInicioTransiente != -1:

            # resultadoFadigaTubulacao = [[NRestimado - (numeroCiclosFadiga + 1), danoAcumuladoFadiga * 100],
            #                             [NRestimadoc - (numeroCiclosFadiga + 1), danoAcumuladoFadigaCurv * 100]]
            resultadoFadigaTubulacao = [[NRestimado, danoAcumuladoFadiga * 100],
                                        [NRestimadoc, danoAcumuladoFadigaCurv * 100]]

        else:

            resultadoFadigaTubulacao = [[0, 0], [0, 0]]

        return resultadoFadigaTubulacao

    def flag4FadigaTubulacao(self, resultadoFadigaTubulacao):

        if resultadoFadigaTubulacao[0][0] == 0:

            with open(self.arquivoControle, "w") as file:

                file.write('4\n5')
        else:

            with open(self.arquivoControle, "w") as file:

                file.write('5\n5')

    def saida2FunctionTubulacao(self, indiceInicioTransiente, resultadoFadigaTubulacao):

        saida2Tubulacao = []

        if indiceInicioTransiente != -1:

            saida2Tubulacao = [['40', '1', '0'], ['0', '20', '30'],
                               ['6', resultadoFadigaTubulacao[0][0], resultadoFadigaTubulacao[0][1]] , ['6', resultadoFadigaTubulacao[1][0], resultadoFadigaTubulacao[1][1]]]

            # saida2Tubulacao = [['40', '1', '0'], ['0', '20', '30'],
                           # ['6', resultadoFadigaTubulacao[0][0], resultadoFadigaTubulacao[0][1]] ]

        else:

            saida2Tubulacao = [['40', '1', '0'], ['0', '20', '30'],
                               ['6', '0', '0']]

        return saida2Tubulacao

    def writeOutfileTubulacao(self, saida2Tubulacao):

        with open(self.arquivoSaida, "w") as file:
            file.write('' + str(saida2Tubulacao[0][0]) + '  ' + str(saida2Tubulacao[0][1]) + ' ' + str(
                saida2Tubulacao[0][2]) + '\n' + '' + str(
                saida2Tubulacao[1][0]) + '  ' + str(saida2Tubulacao[1][1]) + ' ' + str(
                saida2Tubulacao[1][2]) + '\n' + '' + str(
                saida2Tubulacao[2][0]) + '  ' + str(saida2Tubulacao[2][1]) + ' ' + str(
                saida2Tubulacao[2][2]))

    def flag5Tubulacao(self):  # final do processo de cálculo OK!

        with open(self.arquivoControle, "w") as file:
            file.write('5\n5')

    def flagFimTubulacao(self):

        FlagFim = self.arquivoControle + '.over'

        with open(FlagFim, "w") as file:
            file.write('1')
