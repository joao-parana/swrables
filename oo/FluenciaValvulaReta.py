# -*- coding: utf-8 -*-

import numpy as np
import os
import ErrorHandle as EH
import sys
from iapws import IAPWS97
from math import *
from scipy.integrate import quad
from scipy.interpolate import interp1d
from FluenciaValvula import*

class FluenciaValvulaReta(FluenciaValvula):

    def __init__(self, currentDir, fileName):
        FluenciaValvula.__init__(self, currentDir, fileName)

    def JustDoItValvReta(self, creepData, fatigueCycles, operationTime):
        # (self.arquivoEntrada, self.arquivoSaida, self.arquivoControle) = self.setupNameFileInputParams(self.currentDir, self.fileName)
        self.tempoOperacaoBase = operationTime
        # self.setupInputParams() ...

        try:
            (self.tempo, self.Vv, self.pv, self.Tv, self.Tmint, self.Tmext) = self.setupInputParamsFromSoma(creepData, self.tempo, self.Vv, self.pv, self.Tv, self.Tmint, self.Tmext)
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o sistema!' + '\n' + 'O dano por fluência no trecho reto da válvula não foi avaliado neste dia.' + '\n' + '***********************************************************'

            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2))) + '\n' + '' + str(self.saida2.item((3, 0))) + '\t' + str(self.saida2.item((3, 1))) + '\t' + str(self.saida2.item((3, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Reta']['Fluencia'] = strOut

            return
        #(self.tempoOperacaoBase, self.tempo, self.Vv, self.pv, self.Tv, self.Tmint, self.Tmext) = self.setupInputParamsFromSoma(arrayAux2, self.tempo, self.Vv, self.pv, self.Tv, self.Tmint, self.Tmext)
        # self.flag0()
        self.Vv = self.medSmoothParams(self.Vv)
        self.pv = self.medSmoothParams(self.pv)
        self.Tv = self.medSmoothParams(self.Tv)
        self.Tmint = self.medSmoothParams(self.Tmint)
        self.Tmext = self.medSmoothParams(self.Tmext)

        errorCode = self.firstBlock('Fluencia', 'Valvula', 'Reta')
        if errorCode > 0:
            return


        self.indiceInicioTransiente = self.getStartIndexTrans(self.Tv, 5, 175, 50)
        self.indiceFimTransiente = self.getEndIndexTrans(self.Tv, 5, 500, 1, self.indiceInicioTransiente)
        self.instanteInicioTransiente = self.setStartInstantTrans()
        self.instanteFimTransiente = self.setEndInstantTrans()
        self.temperaturaInicioTransiente = self.setStartTempTrans(self.Tv)
        self.temperaturaFimTransiente = self.setEndTempTrans(self.Tv)


        try:
            (self.tempoFiltro1, self.VvaporFiltro1, self.PvaporFiltro1, self.TvaporFiltro1, self.TmetalintFiltro1,
             self.TmetalextFiltro1) = self.filtro1('Fluencia', self.tempo, self.Vv, self.pv, self.Tv, self.Tmint,
                                                   self.Tmext)

            (self.tempoFiltro2, self.VvaporFiltro2, self.PvaporFiltro2, self.TvaporFiltro2, self.TmetalintFiltro2,
             self.TmetalextFiltro2) = self.filtro2('Fluencia', self.tempoFiltro1, self.VvaporFiltro1,
                                                   self.PvaporFiltro1, self.TvaporFiltro1, self.TmetalintFiltro1,
                                                   self.TmetalextFiltro1)
        except:

            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro na filtragem dos dados!' + '\n' + 'O dano por fluência na válvula não foi avaliado neste dia.' + '\n' + '***********************************************************'
            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
                self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                self.saida2.item((2, 2))) + '\n' + '' + str(
                self.saida2.item((3, 0))) + '\t' + str(self.saida2.item((3, 1))) + '\t' + str(
                self.saida2.item((3, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Reta']['Fluencia'] = strOut

            return
        # self.flag1()

        try:

            self.VvaporSM = self.calcMediaParams(self.VvaporFiltro2, self.limiteInfVazao)
            self.PvaporSM = self.calcMediaParams(self.PvaporFiltro2, self.limiteInfPressao)
            self.TvaporSM = self.calcMediaParams(self.TvaporFiltro2, self.limiteInfTemperaturaTubulacaoValvula)
            self.TmetalintSM = self.calcMediaParams(self.TmetalintFiltro2, self.limiteInfTemperaturaTubulacaoValvula)
            self.TmetalextSM = self.calcMediaParams(self.TmetalextFiltro2, self.limiteInfTemperaturaTubulacaoValvula)

        except:


            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no tratamento dos dados!' + '\n' + 'O dano por fluência na válvula não foi avaliado neste dia.' + '\n' + '***********************************************************'
            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
                self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                self.saida2.item((2, 2))) + '\n' + '' + str(
                self.saida2.item((3, 0))) + '\t' + str(self.saida2.item((3, 1))) + '\t' + str(
                self.saida2.item((3, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Reta']['Fluencia'] = strOut

            return


        errorCode = self.checkParamsForFlu('Fluencia', 'Valvula', 'Reta')
        if errorCode > 0:
            return

        # self.flag5()

        (self.PmediaVapor, self.TmediaVapor , self.VmediaVapor, self.TmetalIntMedia,
         self.TmetalExtMedia) = self.redefParams(self.TvaporSM, self.PvaporSM, self.VvaporSM, self.TmetalintSM,
                                                   self.TmetalextSM)

        # self.block('Fluencia', 'Valvula') Já estou fazendo essa barreira em checkParamsForFlu

        # self.flag2()
        (self.TemperaturaPropMec, self.moduloElasticidade, self.coefExpansaoTerm, self.condutividadeTerm,
         self.calorEspecificoPcte) = self.getPropMec()
        (self.TemperaturaCoefPoisson, self.CoefPoisson) = self.getCoefPoisson()
        (self.TemperaturaCoefTempoRupturaFlu, self.Coef1TRP, self.Coef2TRP, self.Coef3TRP,
         self.Coef4TRP) = self.getCoefTempoRuptura(self.currentDir, self.fileNameCoefTempoRupturaTubulacao)
        (self.tensaoPLMvalv, self.PLMvalv) = self.getParamLarsonMiller(self.fileNameParamLarsonMillerTubulacao)
        (self.inputPMG, self.PMG) = self.getParamMonkmanGrant(self.fileNameParamMonkmanGrantTubulacao)
        self.Paramslist2arrayMG('Valvula')
        (self.Dint, self.Rint, self.Dext, self.Rext, self.t, self.f1, self.f2) = self.setGeometriaValvula()
        self.tempoAvaliacao = self.getTempoAvaliacao()

        if (self.PmediaVapor == 0):
            EH.ErrorHandle.handler("ERROR: [Nenhum dano por fluência detectado!]")
            sys.exit(1)

        (self.muVapor, self.rhoVapor, self.lambdaVapor, self.cpVapor, self.niVapor,
         self.alphaVapor) = self.setPropTermoFisicaVaporForFluResult(self.PmediaVapor, self.TmediaVapor)
        (self.Tint, self.Text) = self.setParamAdimensionaisForFluTubulacao(self.VvaporSM, self.PmediaVapor,
                                                                              self.TvaporSM, self.hext, self.Rint,
                                                                              self.Rext, self.Ltubo, 'Valvula')
        (self.C1, self.C2) = self.getTwallCoef(self.Tint, self.Text, self.Rint, self.Rext)
        self.Twallmedia = self.calcTwallMedia(self.Rint, self.Rext, self.C1, self.C2)
        self.tensaoTangencialMax = self.tensaoTangecialTubulacao(self.PmediaVapor, self.Rint, self.Rext,
                                                                   self.Rint, 'Reta')
        self.tensaoAxialMax = self.tensaoAxialTubulacao(self.PmediaVapor, self.Rint, self.Rext, self.Rint, 'Reta',
                                                          self.f1)
        self.tensaoRadialMax = self.tensaoRadialTubulacao(self.PmediaVapor, self.Rint, self.Rext, self.Rint,
                                                            'Reta', self.f1)
        self.tensaoEquivalenteMax = self.tensaoEquivalenteTubulacao(self.tensaoTangencialMax, self.tensaoAxialMax,
                                                                      self.tensaoRadialMax)
        self.tRKR = self.geTtRKR(self.tensaoEquivalenteMax, self.Twallmedia)
        self.PLMtr = self.getPLM(self.tensaoEquivalenteMax, self.tensaoPLMvalv, self.PLMvalv)
        self.tRLM = self.getTrLM(self.PLMtr, self.Twallmedia)
        self.vidaLM = self.vidaRemanescente(self.tRLM, self.tempoAvaliacao, self.tempoOperacaoBase)
        self.vidaKR = self.vidaRemanescente(self.tRKR, self.tempoAvaliacao, self.tempoOperacaoBase)
        self.deltaDLM = self.deltaD(self.tRLM, self.tempoAvaliacao)
        self.deltaDKR = self.deltaD(self.tRKR, self.tempoAvaliacao)

        ### Regressão linear para estimar a vida remanescente em fluência por Larson-Miller ###

        try:
            self.putDanoFromLocalFile('LM_FluenciaValvulaReta', self.deltaDLM)  # OBS!!! -> está hardcoded
            self.putTempoAvaliacaoFromLocalFile('LM_FluenciaValvulaReta', self.tempoAvaliacao)  # OBS!!! -> está hardcoded

            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('LM_FluenciaValvulaReta')
            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('LM_FluenciaValvulaReta')

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
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no procedimento de cálculo da vida remanescente!' + '\n' + 'A vida remanescente em fluência do trecho reto da válvula pelo método de Larson-Miller não foi computada neste dia.' + '\n' + '***********************************************************'
            self.vidaKR_RegLin = 0

        ### Regressão linear para estimar a vida remanescente em fluência por Kachanov-Rabotnov ###

        try:

            self.putDanoFromLocalFile('KR_FluenciaValvulaReta', self.deltaDKR)  # OBS!!! -> está hardcoded
            self.putTempoAvaliacaoFromLocalFile('KR_FluenciaValvulaReta', self.tempoAvaliacao)  # OBS!!! -> está hardcoded

            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('KR_FluenciaValvulaReta')
            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('KR_FluenciaValvulaReta')

            self.mean_x_RegLin = self.mean(self.tempoOperacaoRegLin)
            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)

            self.variance_x_RegLin = self.variance(self.tempoOperacaoRegLin, self.mean_x_RegLin)
            self.variance_y_RegLin = self.variance(self.danoAcumuladoRegLin, self.mean_y_RegLin)

            self.covariance_RegLin = self.covariance(self.tempoOperacaoRegLin, self.mean_x_RegLin, self.danoAcumuladoRegLin,
                                                     self.mean_y_RegLin)

            self.coefficients_RegLin = self.coefficients(self.mean_x_RegLin, self.mean_y_RegLin, self.variance_x_RegLin,
                                                         self.covariance_RegLin)

            self.tempoOperacao90 = self.simple_linear_regression(self.coefficients_RegLin)

            self.vidaKR_RegLin = self.tempoOperacao90 - self.tempoOp
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no procedimento de cálculo da vida remanescente!' + '\n' + 'A vida remanescente em fluência do trecho reto da válvula pelo método de Kachanov-Rabotnov-Penny não foi computada neste dia.' + '\n' + '***********************************************************'
            self.vidaKR_RegLin = 0


        self.Resultados = self.resultTubulacao(self.vidaLM_RegLin, self.deltaDLM, self.vidaKR_RegLin, self.deltaDKR)
        # self.flag4()
        self.saida2 = self.saida2Function('Valvula')
        try:
            self.writeOutfile('Valvula', 'Fluencia', 'Reta')
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fluência do trecho reto da válvula foi enviado neste dia.' + '\n' + '***********************************************************'
            return
        # self.flag6()
        # self.flagFim()


    @staticmethod
    def create():
        # currentDir = 'C:\\Users\\victorv\\Desktop\\Desenv\\SOMA-Turbodiag\\DATA\\valvulareta\\'
        currentDir = MecanismoDano.APP_ROOT + '/../DATA/valvulareta/' # o comando os.getcwd está incluindo o diretorio oo no caminho do arquivo erroneamente!!!!!
        if platform.system() == "Windows":
            currentDir = MecanismoDano.APP_ROOT + '\\..\\DATA\\valvulareta\\'

        fileName = 'controle_fluencia.txt'

        return FluenciaValvulaReta(currentDir, fileName)


#fluVR = FluenciaValvulaReta.touchObjectFluValvReta()
#self.JustDoItValvReta(arrayAux2)
