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

from Fluencia import*

class FluenciaRotor(Fluencia):

    def __init__(self, currentDir, fileName):
        Fluencia.__init__(self, currentDir, fileName)

    def JustDoItFlu(self, arrayAux2, fatigueCycles, operationTime):

        # currentDir = 'C:\\SOMATURBODIAG\\rotor\\'
        currentDir = os.getcwd() + '/../DATA/rotor/'
        if platform.system() == "Windows":
            currentDir = os.getcwd() + '\\DATA\\rotor\\'

        fileName = 'controle_fluencia.txt'
        # fluR = FluenciaRotor(currentDir, fileName)

        # (self.arquivoEntrada, self.arquivoSaida, self.arquivoControle) = self.setupNameFileInputParams(self.currentDir, self.fileName)
        self.tempoOperacaoBase = operationTime

        try:
            (self.tempo, self.pv, self.Tv, self.Tic, self.Wturb) = self.setupInputParamsFromSoma(arrayAux2, self.tempo, self.pv, self.Tv, self.Tic, self.Wturb)
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o sistema!' + '\n' + 'O dano por fluência no rotor não foi avaliado neste dia.' + '\n' + '***********************************************************'
            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 2 0 0; 3 0 0')

            strOut = str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                self.saida2.item((2, 2))) + '\n' + '' + str(self.saida2.item((3, 0))) + '\t' + str(
                self.saida2.item((3, 1))) + '\t' + str(self.saida2.item((3, 2))) + '\n' + '' + str(
                self.saida2.item((4, 0))) + '\t' + str(self.saida2.item((4, 1))) + '\t' + str(
                self.saida2.item((4, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR]['normal']['Fluencia'] = strOut
            return


        # self.flag0()
        self.pv = self.medSmoothParams(self.pv)
        self.Tv = self.medSmoothParams(self.Tv)
        self.Tic = self.medSmoothParams(self.Tic)
        self.Wturb = self.medSmoothParams(self.Wturb)

        errorCode1 = self.firstBlock('Fluencia', 'Rotor')
        if errorCode1 > 0:
            return
        ### OBS: Para a grandeza de tempo, que já vem tratada do SOMA, a janela foi adotada como 1 para que os valores não fossem alterados

        self.indiceInicioTransiente = self.getStartIndexTrans(self.Tic, 5, 175, 50)
        self.indiceFimTransiente = self.getEndIndexTrans(self.Tic, 5, 505, 1, self.indiceInicioTransiente)
        self.instanteInicioTransiente = self.setStartInstantTrans()
        self.instanteFimTransiente = self.setEndInstantTrans()
        self.temperaturaInicioTransiente = self.setStartTempTrans(self.Tic)
        self.temperaturaFimTransiente = self.setEndTempTrans(self.Tic)
        try:
            (self.tempoFiltro1, self.PvaporFiltro1, self.TvaporFiltro1, self.TmetalFiltro1, self.PotenciaFiltro1) = self.filtro1('Fluencia', self.tempo, self.pv, self.Tv, self.Tic, self.Wturb)
            (self.tempoFiltro2, self.PvaporFiltro2, self.TvaporFiltro2, self.TmetalFiltro2, self.PotenciaFiltro2) = self.filtro2('Fluencia', self.tempoFiltro1, self.PvaporFiltro1, self.TvaporFiltro1, self.TmetalFiltro1, self.PotenciaFiltro1)
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro na filtragem dos dados!' + '\n' + 'O dano por fluência no rotor não foi avaliado neste dia.' + '\n' + '***********************************************************'
            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 2 0 0; 3 0 0')

            strOut = str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                self.saida2.item((2, 2))) + '\n' + '' + str(self.saida2.item((3, 0))) + '\t' + str(
                self.saida2.item((3, 1))) + '\t' + str(self.saida2.item((3, 2))) + '\n' + '' + str(
                self.saida2.item((4, 0))) + '\t' + str(self.saida2.item((4, 1))) + '\t' + str(
                self.saida2.item((4, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR]['normal']['Fluencia'] = strOut
            return
        # self.flag1()

        try:

            self.PvaporSM = self.calcMediaParams(self.PvaporFiltro2, self.limiteInfPressaoRotor)
            self.TvaporSM = self.calcMediaParams(self.TvaporFiltro2, self.limiteInfTemperaturaRotor)
            self.TmediacextSM = self.calcMediaParams(self.TmetalFiltro2, self.limiteInfTemperaturaRotor)
            self.PWmediaSM = self.calcMediaParams(self.PotenciaFiltro2, self.limiteInfPotencia)

        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no tratamento dos dados!' + '\n' + 'O dano por fluência no rotor não foi avaliado neste dia.' + '\n' + '***********************************************************'
            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 2 0 0; 3 0 0')

            strOut = str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                self.saida2.item((2, 2))) + '\n' + '' + str(self.saida2.item((3, 0))) + '\t' + str(
                self.saida2.item((3, 1))) + '\t' + str(self.saida2.item((3, 2))) + '\n' + '' + str(
                self.saida2.item((4, 0))) + '\t' + str(self.saida2.item((4, 1))) + '\t' + str(
                self.saida2.item((4, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR]['normal']['Fluencia'] = strOut
            return


        errorCode2 = self.checkParamsForFlu('Fluencia', 'Rotor')
        if errorCode2 > 0:
            return

        # self.flag5()

        (self.PmediaVapor, self.TmediaVapor, self.Tmediacext, self.PWmedia) = self.redefParams(self.PvaporSM, self.TvaporSM, self.TmediacextSM, self.PWmediaSM)

        # self.block('Fluencia', 'Rotor') Já estou fazendo essa barreira em checkParamsForFlu

        # self.flag2()
        (self.TemperaturaPropMec, self.moduloElasticidade, self.coefExpansaoTerm, self.condutividadeTerm, self.calorEspecificoPcte) = self.getPropMec()
        (self.TemperaturaCoefPoisson, self.CoefPoisson) = self.getCoefPoisson()
        (self.TemperaturaCoefTempoRupturaFlu, self.Coef1TRP, self.Coef2TRP, self.Coef3TRP, self.Coef4TRP) = self.getCoefTempoRuptura(self.currentDir, self.fileNameCoefTempoRupturaRotor)
        (self.tensaoPLMrotor, self.PLMrotor) = self.getParamLarsonMiller(self.fileNameParamLarsonMillerRotor)
        (self.tensaoPMH, self.PMH) = self.getParamMansonHaferd(self.fileNameParamMansonHaferdRotor)
        self.Paramslist2arrayMH('Fluencia', 'Rotor')
        (self.d1Rotor, self.r1Rotor, self.d2Rotor, self.r2Rotor, self.d3Rotor) = self.setGeometriaRotor()
        (self.d1Carcaca, self.r1Carcaca, self.d2Carcaca, self.r2Carcaca) = self.setGeometriaCarcaca()
        self.tempoAvaliacao = self.getTempoAvaliacao()

        if (self.PmediaVapor == 0):
            EH.ErrorHandle.handler("ERROR: [Nenhum dano por fluência detectado!]")
            sys.exit(1)

        (self.muVapor, self.rhoVapor, self.lambdaVapor, self.cpVapor, self.niVapor, self.alphaVapor) = self.setPropTermoFisicaVaporForFluResult(self.PmediaVapor, self.TmediaVapor)
        (self.Re, self.Pr, self.Nu) = self.setParamAdimensionaisForTransCal1()
        (self.N, self.PWmax, self.omegazao, self.hCarcaca, self.Tmediacint, self.T2Rotor) = self.setParamsRotorCarcacaForTransCal2(self.TmediaVapor, self.Tmediacext, self.PWmedia)
        self.lambdaRotor = self.lambdaInterpolado(self.T2Rotor)
        (self.T2Rotor, self.hRotor, self.T1Rotor, self.deltaT, self.TmediaRotor) = self.setParamsRotorCarcacaForTransCal3()
        self.E = self.Einterpolado(self.T2Rotor) * 10 ** 6
        self.beta = self.betaInterpolado(self.T2Rotor)
        self.ni = self.niInterpolado(self.T2Rotor)
        self.PmediaVaporPa = self.bar2Pa(self.PmediaVapor)
        self.tensaoRadialR1Rotor = self.tensaoRadialRotor(self.r1Rotor)
        self.tensaoRadialR2Rotor = self.tensaoRadialRotor(self.r2Rotor)
        self.tensaoTangencialR1Rotor = self.tensaoTangencialRotor(self.r1Rotor)
        self.tensaoTangencialR2Rotor = self.tensaoTangencialRotor(self.r2Rotor)
        self.tensaoAxialR1Rotor = self.tensaoAxialRotor(self.r1Rotor)
        self.tensaoAxialR2Rotor = self.tensaoAxialRotor(self.r2Rotor)
        self.tensaoEquivalenteR1Rotor = self.tensaoEquivalenteRotor(self.r1Rotor)
        self.tensaoEquivalenteR2Rotor = self.tensaoEquivalenteRotor(self.r2Rotor)
        self.PLMR1 = self.getPLM(self.tensaoEquivalenteR1Rotor, self.tensaoPLMrotor, self.PLMrotor)
        self.PLMR2 = self.getPLM(self.tensaoEquivalenteR2Rotor, self.tensaoPLMrotor, self.PLMrotor)
        self.PMHR1 = self.getPMH(self.tensaoEquivalenteR1Rotor)
        self.PMHR2 = self.getPMH(self.tensaoEquivalenteR2Rotor)
        self.tR1 = self.geTtR(self.tensaoEquivalenteR1Rotor, self.T1Rotor)
        self.tR2 = self.geTtR(self.tensaoEquivalenteR2Rotor, self.T2Rotor)
        self.tR1LM = self.getTrLM(self.PLMR1, self.T1Rotor)
        self.tR2LM = self.getTrLM(self.PLMR2, self.T2Rotor)
        (self.tR1MH, self.tR2MH) = self.getTrMH()
        self.tRPenny = self.getTrPenny()
        self.tRLM = self.tRLMfinal()
        self.tRMH = self.tRMHfinal()
        self.deltaDfluencia = self.deltaDfluenciaFunction(self.tRLM, self.tRMH, self.tRPenny)

        ### Regressão linear para estimar a vida remanescente em fluência por Larson-Miller ###

        try:
            self.putDanoFromLocalFile('LM_FluenciaRotor', self.deltaDfluencia[0])  # OBS!!! -> está hardcoded
            self.putTempoAvaliacaoFromLocalFile('LM_FluenciaRotor',
                                                self.tempoAvaliacao)  # OBS!!! -> está hardcoded

            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('LM_FluenciaRotor')
            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('LM_FluenciaRotor')

            self.mean_x_RegLin = self.mean(self.tempoOperacaoRegLin)
            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)

            self.variance_x_RegLin = self.variance(self.tempoOperacaoRegLin, self.mean_x_RegLin)
            self.variance_y_RegLin = self.variance(self.danoAcumuladoRegLin, self.mean_y_RegLin)

            self.covariance_RegLin = self.covariance(self.tempoOperacaoRegLin, self.mean_x_RegLin, self.danoAcumuladoRegLin,
                                                     self.mean_y_RegLin)

            self.coefficients_RegLin = self.coefficients(self.mean_x_RegLin, self.mean_y_RegLin, self.variance_x_RegLin,
                                                         self.covariance_RegLin)

            self.tempoOperacao90 = self.simple_linear_regression(self.coefficients_RegLin)

            self.vidaLM_RegLin = self.tempoOperacao90 - self.tempoOp

        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no procedimento de cálculo da vida remanescente!' + '\n' + 'A vida remanescente em fluência do rotor pelo método de Larson-Miller não foi computada neste dia.' + '\n' + '***********************************************************'
            self.vidaLM_RegLin = 0




        ### Regressão linear para estimar a vida remanescente em fluência por Kachanov-Rabotnov-Penny ###

        try:
            self.putDanoFromLocalFile('Penny_FluenciaRotor', self.deltaDfluencia[2])  # OBS!!! -> está hardcoded
            self.putTempoAvaliacaoFromLocalFile('Penny_FluenciaRotor',
                                                self.tempoAvaliacao)  # OBS!!! -> está hardcoded

            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('Penny_FluenciaRotor')
            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('Penny_FluenciaRotor')

            self.mean_x_RegLin = self.mean(self.tempoOperacaoRegLin)
            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)

            self.variance_x_RegLin = self.variance(self.tempoOperacaoRegLin, self.mean_x_RegLin)
            self.variance_y_RegLin = self.variance(self.danoAcumuladoRegLin, self.mean_y_RegLin)

            self.covariance_RegLin = self.covariance(self.tempoOperacaoRegLin, self.mean_x_RegLin, self.danoAcumuladoRegLin,
                                                     self.mean_y_RegLin)

            self.coefficients_RegLin = self.coefficients(self.mean_x_RegLin, self.mean_y_RegLin, self.variance_x_RegLin,
                                                         self.covariance_RegLin)

            self.tempoOperacao90 = self.simple_linear_regression(self.coefficients_RegLin)

            self.vidaPenny_RegLin = self.tempoOperacao90 - self.tempoOp
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no procedimento de cálculo da vida remanescente!' + '\n' + 'A vida remanescente em fluência do rotor pelo método de Kachanov-Rabotnov-Penny não foi computada neste dia.' + '\n' + '***********************************************************'
            self.vidaPenny_RegLin = 0

        ### Regressão linear para estimar a vida remanescente em fluência por Manson-Haferd ###

        try:
            self.putDanoFromLocalFile('MH_FluenciaRotor', self.deltaDfluencia[1])  # OBS!!! -> está hardcoded
            self.putTempoAvaliacaoFromLocalFile('MH_FluenciaRotor',
                                                self.tempoAvaliacao)  # OBS!!! -> está hardcoded

            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('MH_FluenciaRotor')
            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('MH_FluenciaRotor')

            self.mean_x_RegLin = self.mean(self.tempoOperacaoRegLin)
            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)

            self.variance_x_RegLin = self.variance(self.tempoOperacaoRegLin, self.mean_x_RegLin)
            self.variance_y_RegLin = self.variance(self.danoAcumuladoRegLin, self.mean_y_RegLin)

            self.covariance_RegLin = self.covariance(self.tempoOperacaoRegLin, self.mean_x_RegLin, self.danoAcumuladoRegLin,
                                                     self.mean_y_RegLin)

            self.coefficients_RegLin = self.coefficients(self.mean_x_RegLin, self.mean_y_RegLin, self.variance_x_RegLin,
                                                         self.covariance_RegLin)

            self.tempoOperacao90 = self.simple_linear_regression(self.coefficients_RegLin)

            self.vidaMH_RegLin = self.tempoOperacao90 - self.tempoOp
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no procedimento de cálculo da vida remanescente!' + '\n' + 'A vida remanescente em fluência do rotor pelo método de Manson-Haferd não foi computada neste dia.' + '\n' + '***********************************************************'
            self.vidaMH_RegLin = 0

        self.VidasRemanescentes = self.vidasRemanescentesFunction(self.tRLM, self.tRMH, self.tRPenny)
        self.Resultados = self.result()
        # self.flag4()
        self.saida2 = self.saida2Function('Rotor')
        try:
            self.writeOutfile('Rotor', 'Fluencia')
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fluência do rotor foi enviado neste dia.' + '\n' + '***********************************************************'
            return

        # self.flag6()
        # self.flagFim()

   
    @staticmethod
    def create():
        currentDir = MecanismoDano.APP_ROOT + '/../DATA/rotor/'
        if platform.system() == "Windows":
            currentDir = MecanismoDano.APP_ROOT + '\\..\\DATA\\rotor\\'
    
        fileName = 'controle_fluencia.txt'
    
        return FluenciaRotor(currentDir, fileName)

    # print(self.arquivoEntrada)
    # print(self.arquivoControle)


# print "SISTEMA:\n*** " + os.name + " / " + platform.system() + " / " + platform.release() + " ***"

# fluR = touchObjectFluRotor()

# self.JustDoItFlu()
