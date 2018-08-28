# -*- coding: utf-8 -*-

import numpy as np
import os
import platform
import ErrorHandle as EH
import sys
from iapws import IAPWS97
from math import *
from scipy.integrate import quad
from scipy.interpolate import interp1d


from Fadiga import*

class FadigaRotor(Fadiga): # Fluencia, FluenciaRotor

    def __init__(self, currentDir, fileName):
        Fadiga.__init__(self, currentDir, fileName)
        # FluenciaRotor.__init__(self, currentDir, fileName)



    ### Passo a Passo para retomar a estrutura de integração ###

    # 1 - Voltar a utilizar o método self.setupNameFileInputParams(self.currentDir, self.fileName)
    # 2 - Voltar a utilizar o método self.setupInputParamsFromSoma(arrayAux2, self.tempo, self.pv, self.Tv, self.Tic, self.Wturb)
    # 3 - Remover touchObjectFadRotor() no final do código e o objeto criado





    def JustDoItFad(self, arrayAux2, fatigueCycles, operationTime):
        # currentDir = 'C:\\SOMATURBODIAG\\rotor\\'
        """
        self.currentDir = os.getcwd() + '/../DATA/rotor/'
        if platform.system() == "Windows":
            currentDir = os.getcwd() + '\\DATA\\rotor\\'

        fileName = 'controle_fadiga.txt'
        """

        # (self.arquivoEntrada, self.arquivoSaida, self.arquivoControle) = self.setupNameFileInputParams(self.currentDir, self.fileName)

        # OBS:

        # (self.arquivoEntrada, self.arquivoSaida, self.arquivoControle) = self.setupNameFileInputParams(self.currentDir, self.fileName)

        self.numeroCiclosFadiga = fatigueCycles
        # self.arquivoEntrada = self.getFromSoma("getFatigue", 470, 1363046400000, "10.0.2.125")

        # (self.tempo, self.pv, self.Tv, self.Tic, self.Wturb) = self.setupInputParamsFromSoma(arrayAux2, self.tempo, self.pv, self.Tv, self.Tic, self.Wturb)

        try:
            (self.tempo, self.pv, self.Tv, self.Tic, self.Wturb) = self.setupInputParamsFromSoma(arrayAux2, self.tempo,
                                                                                                 self.pv, self.Tv,
                                                                                                 self.Tic, self.Wturb)
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o sistema!' + '\n' + 'O dano por fadiga no rotor não foi avaliado neste dia.' + '\n' + '***********************************************************'
            self.saida2 = np.matrix('40 0 0; 0 20 30; 4 0 0; 5 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                self.saida2.item((2, 2))) + '\n' + '' + str(self.saida2.item((3, 0))) + '\t' + str(
                self.saida2.item((3, 1))) + '\t' + str(self.saida2.item((3, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR]['normal']['Fadiga'] = strOut

            return
        # (self.tempoOperacaoBase, self.tempo, self.pv, self.Tv, self.Tic, self.Wturb) = self.setupInputParams(self.arquivoEntrada, self.tempo, self.pv, self.Tv, self.Tic, self.Wturb)

        # self.flag0()
        self.pv = self.medSmoothParams(self.pv)
        self.Tv = self.medSmoothParams(self.Tv)
        self.Tic = self.medSmoothParams(self.Tic)
        self.Wturb = self.medSmoothParams(self.Wturb)


        errorCode = self.firstBlock('Fadiga', 'Rotor')
        if errorCode > 0:
            return


        # falhou =
        #if falhou == True:
            #return


        self.indiceInicioTransiente = self.getStartIndexTrans(self.Tic, 5, 175, 50)
        self.indiceFimTransiente = self.getEndIndexTrans(self.Tic, 5, 505, 1, self.indiceInicioTransiente)

        if self.indiceInicioTransiente == -1:

            self.saida2 = np.matrix('40 0 0; 0 20 30; 4 0 0; 5 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                self.saida2.item((2, 2))) + '\n' + '' + str(self.saida2.item((3, 0))) + '\t' + str(
                self.saida2.item((3, 1))) + '\t' + str(self.saida2.item((3, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR]['normal']['Fadiga'] = strOut

            return



        # self.flag5()


        self.instanteInicioTransiente = self.setStartInstantTrans()
        self.instanteFimTransiente = self.setEndInstantTrans()
        self.temperaturaInicioTransiente = self.setStartTempTrans(self.Tic)
        self.temperaturaFimTransiente = self.setEndTempTrans(self.Tic)



        try:
            (self.tempoFiltro1, self.PvaporFiltro1, self.TvaporFiltro1, self.TmetalFiltro1,
             self.PotenciaFiltro1) = self.filtro1('Fadiga', self.tempo, self.pv, self.Tv, self.Tic, self.Wturb)
            (self.tempoFiltro2, self.PvaporFiltro2, self.TvaporFiltro2, self.TmetalFiltro2,
             self.PotenciaFiltro2) = self.filtro2('Fadiga', self.tempoFiltro1, self.PvaporFiltro1, self.TvaporFiltro1,
                                                  self.TmetalFiltro1, self.PotenciaFiltro1)
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro na filtragem dos dados!' + '\n' + 'O dano por fadiga no rotor não foi avaliado neste dia.' + '\n' + '***********************************************************'
            self.saida2 = np.matrix('40 0 0; 0 20 30; 4 0 0; 5 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                self.saida2.item((2, 2))) + '\n' + '' + str(self.saida2.item((3, 0))) + '\t' + str(
                self.saida2.item((3, 1))) + '\t' + str(self.saida2.item((3, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR]['normal']['Fadiga'] = strOut

            return

        # self.flag1()
        try:

            (self.PvaporSM, self.TvaporSM, self.TmediacextSM, self.PWmediaSM) = self.lastValue()
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no tratamento dos dados!' + '\n' + 'O dano por fadiga no rotor não foi avaliado neste dia.' + '\n' + '***********************************************************'
            self.saida2 = np.matrix('40 0 0; 0 20 30; 4 0 0; 5 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                self.saida2.item((2, 2))) + '\n' + '' + str(self.saida2.item((3, 0))) + '\t' + str(
                self.saida2.item((3, 1))) + '\t' + str(self.saida2.item((3, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR]['normal']['Fadiga'] = strOut

            return

        errorCode = self.checkParamsForFlu('Fadiga', 'Rotor')
        if errorCode > 0:
            return

        # self.block('Fadiga', 'Rotor') # Ultima barreira inserida para não trabalhar com dados que nao sejam representativos de dano
                                      # O único segmento que tem essa barreira para a Fadiga é o rotor

        (self.PmediaVapor, self.TmediaVapor, self.Tmediacext, self.PWmedia) = self.redefParams(self.PvaporSM, self.TvaporSM, self.TmediacextSM, self.PWmediaSM)
        (self.duracaoPartidaSM, self.variacaoTemperaturaVaporPartidaSM, self.variacaoTemperaturaMetalPartidaSM, self.variacaoTemperaturaCLESM) = self.calcVariacoes()
        # self.flag2()
        (self.TemperaturaPropMec, self.moduloElasticidade, self.coefExpansaoTerm, self.condutividadeTerm,
         self.calorEspecificoPcte) = self.getPropMec()
        (self.TemperaturaCoefPoisson, self.CoefPoisson) = self.getCoefPoisson()
        (self.TemperaturaCoefTempoRupturaFlu, self.Coef1TRP, self.Coef2TRP, self.Coef3TRP,
         self.Coef4TRP) = self.getCoefTempoRuptura(self.currentDir, self.fileNameCoefTempoRupturaRotor)
        (self.tensaoPLMrotor, self.PLMrotor) = self.getParamLarsonMiller(self.fileNameParamLarsonMillerRotor)
        (self.tensaoPMH, self.PMH) = self.getParamMansonHaferd(self.fileNameParamMansonHaferdRotor)
        (self.variacaoDeformacao, self.numeroCiclos) = self.getDeformacaoxCiclos(self.fileNameCurvaVariacaoDeformacaoNumeroCiclos)
        self.Paramslist2arrayMH('Fadiga', 'Rotor')
        (self.d1Rotor, self.r1Rotor, self.d2Rotor, self.r2Rotor, self.d3Rotor) = self.setGeometriaRotor()
        (self.d1Carcaca, self.r1Carcaca, self.d2Carcaca, self.r2Carcaca) = self.setGeometriaCarcaca()
        (self.muVapor, self.rhoVapor, self.lambdaVapor, self.cpVapor, self.niVapor, self.alphaVapor) = self.setPropTermoFisicaVaporForFluResult(self.PmediaVapor, self.TmediaVapor)
        (self.Re, self.Pr, self.Nu) = self.setParamAdimensionaisForTransCal1()
        (self.N, self.PWmax, self.omegazao, self.hCarcaca, self.Tmediacint,
         self.T2Rotor) = self.setParamsRotorCarcacaForTransCal2(self.TmediaVapor, self.Tmediacext, self.PWmedia)
        self.lambdaRotor = self.lambdaInterpolado(self.T2Rotor)
        (self.T2Rotor, self.hRotor, self.T1Rotor, self.deltaT,
         self.TmediaRotor) = self.setParamsRotorCarcacaForTransCal3()

        # if (self.PmediaVapor == 0):
            # EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Media de Vapor Vazia] (Segunda Barreira)")
            # sys.exit(1)

        self.variacaoTemperaturaMetalPartidaSM = (self.T2Rotor - 273.15) - self.temperaturaInicioTransiente
        (self.deltat, self.deltaTvapor, self.lambdaRotor, self.Biot, self.alfaRotor, self.deltaTal) = self.setParamsForFad(self.duracaoPartidaSM, self.variacaoTemperaturaVaporPartidaSM, self.T2Rotor, self.hRotor, self.r2Rotor)

        # da onde saiu o valor de deltaTvapor no Mathcad?

        self.deltaTvapor = (self.T2Rotor - 273.15) - self.temperaturaInicioTransiente

        (self.BiotVariacaoDeformacaoNominal, self.deltaTalTabela, self.deltaTalTabela) = self.getVariacaoDeformacaoNominal()
        (self.deltaTalInferior, self.deltaTalSuperior) = self.deltaTalSuperiorInferior(self.deltaTal, self.deltaTalTabela)
        (self.BiotInferior, self.BiotSuperior) = self.biotSuperiorInferior(self.Biot, self.BiotVariacaoDeformacaoNominal)
        (self.indiceDeltaTalInferior, self.indiceDeltaTalSuperior) = self.indiceDeltaTalSuperiorInferior(self.deltaTalInferior, self.deltaTalSuperior, self.deltaTalTabela)
        (self.deformacaoStarInf, self.deformacaoStarSup) = self.getDeformacaoStarInfSup(self.indiceDeltaTalInferior, self.indiceDeltaTalSuperior)

        self.deformacaoNominal = self.calcDeformacaoNominal(self.Biot)

        (self.razaoDeformacaoNominal, self.fatorK) = self.getFatorConcentracaoDeformacaoPlastica()
        self.deformacaoTotal = self.calcDeformacaoTotal()
        self.deformacaoTotalAnalisado = self.calcDeformacaoTotalAnalisado(self.deformacaoTotal)

        (self.deltaDfadiga, self.deltaDfadigaPercentual) = self.calcDeltaDfadiga()
        (self.danoDF, self.CoefA, self.CoefB, self.CoefC) = self.setTabelaCoefCurvaCLE()
        (self.limCLE, self.taxaAquecimento) = self.limCLEf(self.variacaoTemperaturaMetalPartidaSM, self.duracaoPartidaSM, self.variacaoTemperaturaCLESM, self.danoDF)
        (self.dTdtLimInfCLE, self.dTdtLimSupCLE) = self.dTdtLimSupInfCLE(self.limCLE, self.danoDF, self.variacaoTemperaturaCLESM)
        self.dfCLE = self.dfCLEf(self.limCLE, self.danoDF, self.dTdtLimInfCLE, self.dTdtLimSupCLE, self.taxaAquecimento)
        (self.deltaDfadigaCLE, self.deltaDfadigaCLEPercentual, self.nRCLE, self.NR) = self.deltaDfadigaCLEf(self.limCLE, self.taxaAquecimento, self.dfCLE, self.deltaDfadiga, self.deformacaoTotalAnalisado)

        ### Regressão linear para estimar o número de cilos até a falha em fadiga por meio da Curva de Fadiga ###

        try:
            self.putDanoFromLocalFile('CurvaFadiga_FadigaRotor', self.deltaDfadigaPercentual)
            self.putNumeroCiclosFromLocalFile('CurvaFadiga_FadigaRotor', 1)

            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('CurvaFadiga_FadigaRotor')
            self.NCRegLin, self.NC = self.getNumeroCiclosFromLocalFile('CurvaFadiga_FadigaRotor')

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
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no procedimento de cálculo da vida remanescente!' + '\n' + 'A vida remanescente em fadiga do rotor dada pela curva de fadiga não foi computada neste dia.' + '\n' + '***********************************************************'
            self.numeroCiclosCurvaFadiga_RegLin = 0

        ### Regressão linear para estimar o número de cilos até a falha em fadiga por meio da CLE ###

        try:
            self.putDanoFromLocalFile('CLE_FadigaRotor', self.deltaDfadigaCLEPercentual)  # OBS!!! -> está hardcoded
            self.putNumeroCiclosFromLocalFile('CLE_FadigaRotor', 1)  # OBS!!! -> está hardcoded

            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('CLE_FadigaRotor')
            self.NCRegLin, self.NC = self.getNumeroCiclosFromLocalFile('CLE_FadigaRotor')

            self.mean_x_RegLin = self.mean(self.NCRegLin)
            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)

            self.variance_x_RegLin = self.variance(self.NCRegLin, self.mean_x_RegLin)
            self.variance_y_RegLin = self.variance(self.danoAcumuladoRegLin, self.mean_y_RegLin)

            self.covariance_RegLin = self.covariance(self.NCRegLin, self.mean_x_RegLin, self.danoAcumuladoRegLin,
                                                     self.mean_y_RegLin)

            self.coefficients_RegLin = self.coefficients(self.mean_x_RegLin, self.mean_y_RegLin, self.variance_x_RegLin,
                                                         self.covariance_RegLin)

            self.numeroCiclos90 = self.simple_linear_regression(self.coefficients_RegLin)

            self.numeroCiclosCLE_RegLin = self.numeroCiclos90 - self.NC
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no procedimento de cálculo da vida remanescente!' + '\n' + 'A vida remanescente em fadiga do rotor pelo método da CLE não foi computada neste dia.' + '\n' + '***********************************************************'
            self.numeroCiclosCLE_RegLin = 0

        # self.flag4()
        self.output = self.outputs(self.numeroCiclosCurvaFadiga_RegLin, self.numeroCiclosCLE_RegLin, self.deltaDfadiga, self.deltaDfadigaCLE, self.indiceInicioTransiente, self.numeroCiclosFadiga)
        self.saida2 = self.saida2f(self.indiceInicioTransiente, self.numeroCiclosCurvaFadiga_RegLin, self.numeroCiclosCLE_RegLin, self.numeroCiclosFadiga, self.deltaDfadiga, self.deltaDfadigaCLE)
        print(self.saida2)
        try:
            self.writeOutfile('Rotor', 'Fadiga')
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fadiga do rotor foi enviado neste dia.' + '\n' + '***********************************************************'
            return
        # self.flag6()
        # self.flagFim()


        # Conferir as variações de temperatura, sao as maiores causas de divergencia.

    @staticmethod
    def create():
        currentDir = MecanismoDano.APP_ROOT + '/../DATA/rotor/'
        if platform.system() == "Windows":
            currentDir = MecanismoDano.APP_ROOT + '\\..\\DATA\\rotor\\'

        fileName = 'controle_fadiga.txt'

        return FadigaRotor(currentDir, fileName)


#### Remover essa estrutura após a verificação dos danos elevados ####

# def touchObjectFadRotor():
#
#     currentDir = 'C:\\SOMATURBODIAG\\rotor\\'
#     fileName = 'controle_fadiga.txt'
#
#     return FadigaRotor(currentDir, fileName)
#
# fadR = touchObjectFadRotor()
# fadR.JustDoItFad([1], 324, 10)


# print "SISTEMA:\n*** " + os.name + " / " + platform.system() + " / " + platform.release() + " ***"
# fadR = touchObjectFadRotor()
# self.JustDoItFad()
