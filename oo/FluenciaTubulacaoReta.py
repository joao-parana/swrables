# -*- coding: utf-8 -*-


import numpy as np
import os
import ErrorHandle as EH
import sys
from iapws import IAPWS97
from math import *
from scipy.integrate import quad
from scipy.interpolate import interp1d
from FluenciaTubulacao import*


class FluenciaTubulacaoReta(FluenciaTubulacao):

    def __init__(self, currentDir, fileName):
        FluenciaTubulacao.__init__(self, currentDir, fileName)


    def JustDoItTubReta(self, arrayAux2, fatigueCycles, operationTime):

        # (self.arquivoEntrada, self.arquivoSaida, self.arquivoControle) = self.setupNameFileInputParams(self.currentDir, self.fileName)
        self.tempoOperacaoBase = operationTime
        # (self.tempoOperacaoBase, self.tempo, self.Vv, self.pv, self.Tv) = self.setupInputParams(self.arquivoEntrada, self.tempo, self.Vv, self.pv, self.Tv)

        try:
            (self.tempo, self.Vv, self.pv, self.Tv) = self.setupInputParamsFromSoma(arrayAux2, self.tempo, self.Vv, self.pv, self.Tv)
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o sistema!' + '\n' + 'O dano por fluência no trecho reto da tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'
            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
                self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                self.saida2.item((2, 2))) + '\n' + '' + str(
                self.saida2.item((3, 0))) + '\t' + str(self.saida2.item((3, 1))) + '\t' + str(
                self.saida2.item((3, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Reta']['Fluencia'] = strOut

            return
        # self.flag0()


        self.Vv = self.medSmoothParams(self.Vv)
        self.pv = self.medSmoothParams(self.pv)
        self.Tv = self.medSmoothParams(self.Tv)

        errorCode = self.firstBlock('Fluencia', 'Tubulacao', 'Reta')
        if errorCode > 0:
            return

        self.fracVazao(self.Vv)
        self.indiceInicioTransiente = self.getStartIndexTrans(self.Tv, 5, 175, 50)
        self.indiceFimTransiente = self.getEndIndexTrans(self.Tv, 5, 500, 1, self.indiceInicioTransiente)
        self.instanteInicioTransiente = self.setStartInstantTrans()
        self.instanteFimTransiente = self.setEndInstantTrans()
        self.temperaturaInicioTransiente = self.setStartTempTrans(self.Tv)
        self.temperaturaFimTransiente = self.setEndTempTrans(self.Tv)
        try:
            (self.tempoFiltro1, self.VvaporFiltro1, self.PvaporFiltro1, self.TvaporFiltro1) = self.filtro1('Fluencia', self.tempo, self.Vv, self.pv,self.Tv)
            (self.tempoFiltro2, self.VvaporFiltro2, self.PvaporFiltro2, self.TvaporFiltro2) = self.filtro2('Fluencia', self.tempoFiltro1, self.VvaporFiltro1, self.PvaporFiltro1, self.TvaporFiltro1)
        except:

            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro na filtragem dos dados!' + '\n' + 'O dano por fluência na tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'
            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
                self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                self.saida2.item((2, 2))) + '\n' + '' + str(
                self.saida2.item((3, 0))) + '\t' + str(self.saida2.item((3, 1))) + '\t' + str(
                self.saida2.item((3, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Reta']['Fluencia'] = strOut

            return

            # self.flag1()
        try:

            self.VvaporSM = self.calcMediaParams(self.VvaporFiltro2, self.limiteInfVazao)
            self.PvaporSM = self.calcMediaParams(self.PvaporFiltro2, self.limiteInfPressao)
            self.TvaporSM = self.calcMediaParams(self.TvaporFiltro2, self.limiteInfTemperaturaTubulacaoValvula)
            (self.PmediaVapor, self.TmediaVapor, self.VmediaVapor) = self.redefParams(self.TvaporSM, self.PvaporSM, self.VvaporSM)
        except:

            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no tratamento dos dados!' + '\n' + 'O dano por fluência na tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'
            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')

            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
                self.saida2.item((0, 1))) + '\t' + str(
                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                self.saida2.item((2, 2))) + '\n' + '' + str(
                self.saida2.item((3, 0))) + '\t' + str(self.saida2.item((3, 1))) + '\t' + str(
                self.saida2.item((3, 2)))

            MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Reta']['Fluencia'] = strOut

            return


        errorCode = self.checkParamsForFlu('Fluencia', 'Tubulacao', 'Reta')
        if errorCode > 0:
            return

        # self.flag5()

        # self.block('Fluencia', 'Tubulacao') Já estou fazendo essa barreira em checkParamsForFlu

        # self.flag2()
        (self.TemperaturaPropMec, self.moduloElasticidade, self.coefExpansaoTerm, self.condutividadeTerm,
        self.calorEspecificoPcte) = self.getPropMec()
        (self.TemperaturaCoefPoisson, self.CoefPoisson) = self.getCoefPoisson()
        (self.TemperaturaCoefTempoRupturaFlu, self.Coef1TRP, self.Coef2TRP, self.Coef3TRP, self.Coef4TRP) = self.getCoefTempoRuptura(self.currentDir, self.fileNameCoefTempoRupturaTubulacao)
        (self.tensaoPLMtub, self.PLMtub) = self.getParamLarsonMiller(self.fileNameParamLarsonMillerTubulacao)
        (self.inputPMG, self.PMG) = self.getParamMonkmanGrant(self.fileNameParamMonkmanGrantTubulacao)
        self.Paramslist2arrayMG('Tubulacao')

        self.tempoAvaliacao = self.getTempoAvaliacao()

        if (self.PmediaVapor == 0):
            EH.ErrorHandle.handler("Nenhum dano por fluência detectado!]")
            sys.exit(1)

        (self.Dint, self.Rint, self.Dext, self.Rext, self.rc, self.t, self.f1, self.f2) = self.setGeometriaTubulacao()
        (self.muVapor, self.rhoVapor, self.lambdaVapor, self.cpVapor, self.niVapor,
        self.alphaVapor) = self.setPropTermoFisicaVaporForFluResult(self.PmediaVapor, self.Celsius2Kelvin(self.TmediaVapor))
        (self.Tint, self.Text) = self.setParamAdimensionaisForFluTubulacao(self.VvaporSM, self.PmediaVapor, self.TvaporSM, self.hext, self.Rint, self.Rext, self.Ltubo, 'Tubulacao')
        (self.C1, self.C2) = self.getTwallCoef(self.Tint, self.Text, self.Rint, self.Rext)
        self.Twallmedia = self.calcTwallMedia(self.Rint, self.Rext, self.C1, self.C2)
        self.tensaoTangencialMax = self.tensaoTangecialTubulacao(self.PmediaVapor, self.Rint, self.Rext, self.Rint, 'Reta')
        self.tensaoAxialMax = self.tensaoAxialTubulacao(self.PmediaVapor, self.Rint, self.Rext, self.Rint, 'Reta', self.f1)
        self.tensaoRadialMax = self.tensaoRadialTubulacao(self.PmediaVapor, self.Rint, self.Rext, self.Rint, 'Reta', self.f1)
        self.tensaoEquivalenteMax = self.tensaoEquivalenteTubulacao(self.tensaoTangencialMax, self.tensaoAxialMax, self.tensaoRadialMax)
        self.tRKR = self.geTtRKR(self.tensaoEquivalenteMax, self.Twallmedia)
        self.PLMtr = self.getPLM(self.tensaoEquivalenteMax, self.tensaoPLMtub, self.PLMtub)
        self.tRLM = self.getTrLM(self.PLMtr, self.Twallmedia)
        self.vidaLM = self.vidaRemanescente(self.tRLM, self.tempoAvaliacao, self.tempoOperacaoBase)
        self.vidaKR = self.vidaRemanescente(self.tRKR, self.tempoAvaliacao, self.tempoOperacaoBase)
        self.deltaDLM = self.deltaD(self.tRLM, self.tempoAvaliacao)
        self.deltaDKR = self.deltaD(self.tRKR, self.tempoAvaliacao)

        ### Regressão linear para estimar a vida remanescente em fluência por Larson-Miller ###

        try:

            self.putDanoFromLocalFile('LM_FluenciaTubulacaoReta', self.deltaDLM)  # OBS!!! -> está hardcoded
            self.putTempoAvaliacaoFromLocalFile('LM_FluenciaTubulacaoReta', self.tempoAvaliacao)  # OBS!!! -> está hardcoded

            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('LM_FluenciaTubulacaoReta')
            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('LM_FluenciaTubulacaoReta')

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
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no procedimento de cálculo da vida remanescente!' + '\n' + 'A vida remanescente em fluência do trecho reto da tubulação pelo método de Larson-Miller não foi computada neste dia.' + '\n' + '***********************************************************'
            self.vidaLM_RegLin = 0

        ### Regressão linear para estimar a vida remanescente em fluência por Kachanov-Rabotnov ###

        try:
            self.putDanoFromLocalFile('KR_FluenciaTubulacaoReta', self.deltaDKR)  # OBS!!! -> está hardcoded
            self.putTempoAvaliacaoFromLocalFile('KR_FluenciaTubulacaoReta', self.tempoAvaliacao)  # OBS!!! -> está hardcoded

            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('KR_FluenciaTubulacaoReta')
            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('KR_FluenciaTubulacaoReta')

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
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no procedimento de cálculo da vida remanescente!' + '\n' + 'A vida remanescente em fluência do trecho reto da tubulação pelo método de Kachanov-Rabotnov-Penny não foi computada neste dia.' + '\n' + '***********************************************************'
            self.vidaKR_RegLin = 0



        self.Resultados = self.resultTubulacao(self.vidaLM_RegLin, self.deltaDLM, self.vidaKR_RegLin, self.deltaDKR)
        # self.flag4()
        self.saida2 = self.saida2Function('Tubulacao')
        try:
            self.writeOutfile('Tubulacao', 'Fluencia', 'Reta')
        except:
            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fluência do trecho reto da tubulação foi enviado neste dia.' + '\n' + '***********************************************************'
            return
            # self.flag6()
        # self.flagFim()

    @staticmethod
    def create():
        # currentDir = 'C:\\SOMATURBODIAG\\tubulacaoreta\\'
        currentDir = MecanismoDano.APP_ROOT + '/../DATA/tubulacaoreta/'
        if platform.system() == "Windows":
            currentDir = MecanismoDano.APP_ROOT + '\\..\\DATA\\tubulacaoreta\\'

        fileName = 'controle_fluencia.txt'

        return FluenciaTubulacaoReta(currentDir, fileName)

# def touchObjectFadRotor():
#         #
#     currentDir = 'C:\\SOMATURBODIAG\\tubulacaoreta\\'
#     fileName = 'controle_fluencia.txt'
#         #
#     return FluenciaTubulacaoReta(currentDir, fileName)
#         #
# fluTR = touchObjectFadRotor()
# fluTR.JustDoItTubReta([1], 112000, 10)

# fluTR = FluenciaTubulacaoReta.touchObjectFluTubReta()
# arrayAux2 = ['180.0\t0.0625\t0.5469\t169.7195', '185.0\t0.1031\t0.5469\t169.5219', '190.0\t0.1313\t0.5469\t169.3299', u'195.0\t0.1344\t0.5469\t169.1466', u'200.0\t0.1281\t0.5469\t168.9461', u'205.0\t0.1125\t0.5469\t168.7542', u'210.0\t0.1031\t0.5469\t168.568', u'215.0\t0.1063\t0.5469\t168.3846', u'220.0\t0.1125\t0.5469\t168.2242', u'225.0\t0.1031\t0.5469\t168.0523', u'230.0\t0.0813\t0.5469\t167.8891', u'235.0\t0.0719\t0.5469\t167.7372', u'240.0\t0.0813\t0.5469\t167.551', u'245.0\t0.0906\t0.5469\t167.3734', u'250.0\t0.0563\t0.5469\t167.1872', u'255.0\t0.0313\t0.5469\t167.001', u'260.0\t0.0594\t0.5469\t166.8091', u'265.0\t0.0875\t0.5469\t166.6344', u'270.0\t0.0656\t0.5469\t166.4367', u'275.0\t0.0844\t0.5469\t166.2419', u'280.0\t0.1156\t0.5469\t166.0414', u'285.0\t0.1219\t0.5469\t165.818', u'290.0\t0.1\t0.5469\t165.6146', u'295.0\t0.1219\t0.5469\t165.4169', u'300.0\t0.0938\t0.5469\t165.2279', u'305.0\t0.1094\t0.5469\t165.0445', u'310.0\t0.0688\t0.5469\t164.8526', u'315.0\t0.0719\t0.5469\t164.6464', u'320.0\t0.0844\t0.5469\t164.4315', u'325.0\t0.05\t0.5469\t164.2396', u'330.0\t0.0438\t0.5469\t164.0562', u'335.0\t0.0406\t0.5469\t163.8758', u'340.0\t0.0938\t0.5469\t163.701', u'345.0\t0.0813\t0.5469\t163.5263', u'350.0\t0.0688\t0.5469\t163.363', u'355.0\t0.0688\t0.5469\t163.1912', u'360.0\t0.0563\t0.5469\t163.0021', u'365.0\t0.0406\t0.5469\t162.8216', u'370.0\t0.0188\t0.5469\t162.644', u'375.0\t0.0469\t0.5469\t162.4693', u'380.0\t0.05\t0.5469\t162.2802', u'385.0\t0.0563\t0.5469\t162.0797', u'390.0\t0.0313\t0.5469\t161.8792', u'395.0\t0.0219\t0.5469\t161.6701', u'400.0\t0.0156\t0.5469\t161.4724', u'405.0\t0.0219\t0.5469\t161.2805', u'410.0\t0.0438\t0.5469\t161.0971', u'415.0\t0.0531\t0.5469\t160.9195', u'420.0\t0.0469\t0.5469\t160.7362', u'425.0\t0.0594\t0.5469\t160.5385', u'430.0\t0.0531\t0.5469\t160.3065', u'435.0\t0.0781\t0.5469\t160.0945', u'440.0\t0.0688\t0.5469\t159.9026', u'445.0\t0.075\t0.5469\t159.7078', u'450.0\t0.0469\t0.5469\t159.513', u'455.0\t0.0469\t0.5469\t159.3182', u'460.0\t0.0406\t0.5469\t159.132', u'465.0\t0.0313\t0.5469\t158.9688', u'470.0\t0.025\t0.5469\t158.7797', u'475.0\t0.0125\t0.5469\t158.6107', u'480.0\t0.0313\t0.5469\t158.4331', u'485.0\t0.0875\t0.5469\t158.2669', u'490.0\t0.0844\t0.5469\t158.0922', u'495.0\t0.0969\t0.5469\t157.906', u'500.0\t0.1125\t0.5469\t157.7255', u'505.0\t0.0969\t0.5469\t157.5365', u'510.0\t0.1\t0.5469\t157.3417', u'515.0\t0.1063\t0.5469\t157.1526', u'520.0\t0.1031\t0.5469\t156.9607', u'525.0\t0.0594\t0.5469\t156.7602', u'530.0\t0.0656\t0.5469\t156.5654', u'535.0\t0.1\t0.5469\t156.3878', u'540.0\t0.0938\t0.5469\t156.1958', u'545.0\t0.05\t0.5469\t156.0068', u'550.0\t0.0906\t0.5469\t155.8177', u'555.0\t0.1125\t0.5469\t155.6315', u'560.0\t0.125\t0.5469\t155.4424', u'565.0\t0.1219\t0.5469\t155.2649', u'570.0\t0.0719\t0.5469\t155.1016', u'575.0\t0.0344\t0.5469\t154.924', u'580.0\t0.025\t0.5469\t154.7349', u'585.0\t0.0656\t0.5469\t154.5544', u'590.0\t0.0563\t0.5469\t154.374', u'595.0\t0.0625\t0.5469\t154.1734', u'600.0\t0.0531\t0.5469\t153.9758', u'605.0\t0.05\t0.5469\t153.7896', u'610.0\t0.0531\t0.5469\t153.6034', u'615.0\t0.0531\t0.5469\t153.4172', u'620.0\t0.0531\t0.5469\t153.2253', u'625.0\t0.0969\t0.5469\t153.0333', u'630.0\t0.1219\t0.5469\t152.8443', u'635.0\t0.0813\t0.5469\t152.6638', u'640.0\t0.0656\t0.5469\t152.4776', u'645.0\t0.0688\t0.5469\t152.3057', u'650.0\t0.05\t0.5469\t152.1367', u'655.0\t0.0281\t0.5469\t151.9534', u'660.0\t0.0156\t0.5469\t151.7786', u'665.0\t0.0281\t0.5469\t151.5867', u'670.0\t0.05\t0.5469\t151.412', u'675.0\t0.0438\t0.5469\t151.2401', u'680.0\t0.0344\t0.5469\t151.0539', u'685.0\t0.0438\t0.5469\t150.8734', u'690.0\t0.05\t0.5469\t150.7073', u'695.0\t0.0281\t0.5469\t150.5412', u'700.0\t0.0188\t0.5469\t150.3693', u'705.0\t0.0344\t0.5469\t150.2031', u'710.0\t0.0531\t0.5469\t150.0456', u'715.0\t0.0906\t0.5469\t149.8794', u'720.0\t0.075\t0.5469\t149.7018', u'725.0\t0.0719\t0.5469\t149.5328', u'730.0\t0.0625\t0.5469\t149.3523', u'735.0\t0.0656\t0.5469\t149.1719', u'740.0\t0.0625\t0.5469\t148.9714', u'745.0\t0.0344\t0.5469\t148.7966', u'750.0\t0.0438\t0.5469\t148.6104', u'755.0\t0.0594\t0.5469\t148.4185', u'760.0\t0.0688\t0.5469\t148.2466', u'765.0\t0.0625\t0.5469\t148.0576', u'770.0\t0.0875\t0.5469\t147.8771', u'775.0\t0.0563\t0.5469\t147.7138', u'780.0\t0.0406\t0.5469\t147.5419', u'785.0\t0.0125\t0.5469\t147.3701', u'790.0\t0.0063\t0.5469\t147.1953', u'795.0\t0.0219\t0.5469\t147.0292', u'800.0\t0.0594\t0.5469\t146.863', u'805.0\t0.075\t0.5469\t146.6826', u'810.0\t0.0625\t0.5469\t146.5107', u'815.0\t0.1125\t0.5469\t146.3445', u'820.0\t0.1344\t0.5469\t146.1727', u'825.0\t0.1313\t0.5469\t145.9979', u'830.0\t0.1125\t0.5469\t145.8346', u'835.0\t0.075\t0.5469\t145.6456', u'840.0\t0.0594\t0.5469\t145.4937', u'845.0\t0.05\t0.5469\t145.3076', u'850.0\t0.0406\t0.5469\t145.1357', u'855.0\t0.0281\t0.5469\t144.9495', u'860.0\t0.0313\t0.5469\t144.7833', u'865.0\t0.0125\t0.5469\t144.6344', u'870.0\t0.0406\t0.5469\t144.4482', u'875.0\t0.0688\t0.5469\t144.2935', u'880.0\t0.1\t0.5469\t144.1216', u'885.0\t0.1188\t0.5469\t143.9555', u'890.0\t0.1281\t0.5469\t143.775', u'895.0\t0.1469\t0.5469\t143.6003', u'900.0\t0.15\t0.5469\t143.4169', u'905.0\t0.1531\t0.5469\t143.2565', u'910.0\t0.1344\t0.5469\t143.0818', u'915.0\t0.1344\t0.5469\t142.9156', u'920.0\t0.1281\t0.5469\t142.7409', u'925.0\t0.1063\t0.5469\t142.5633', u'930.0\t0.0844\t0.5469\t142.3742', u'935.0\t0.0719\t0.5469\t142.2253', u'940.0\t0.0906\t0.5469\t142.0706', u'945.0\t0.0969\t0.5469\t141.9188', u'950.0\t0.1188\t0.5469\t141.7813', u'955.0\t0.1188\t0.5469\t141.618', u'960.0\t0.1375\t0.5469\t141.4576', u'965.0\t0.1438\t0.5469\t141.3143', u'970.0\t0.1219\t0.5469\t141.1768', u'975.0\t0.1094\t0.5469\t141.0479', u'980.0\t0.125\t0.5469\t140.8961', u'985.0\t0.1188\t0.5469\t140.7328', u'990.0\t0.0906\t0.5469\t140.5667', u'995.0\t0.0406\t0.5469\t140.3977', u'1000.0\t0.0719\t0.5469\t140.2344', u'1005.0\t0.0563\t0.5469\t140.0596', u'1010.0\t0.0406\t0.5469\t139.8906', u'1015.0\t0.075\t0.5469\t139.7302', u'1020.0\t0.0469\t0.5469\t139.5641', u'1025.0\t0.05\t0.5469\t139.4065', u'1030.0\t0.0844\t0.5469\t139.2318', u'1035.0\t0.0875\t0.5469\t139.0542', u'1040.0\t0.075\t0.5469\t138.888', u'1045.0\t0.1031\t0.5469\t138.7133', u'1050.0\t0.0781\t0.5469\t138.5586', u'1055.0\t0.0563\t0.5469\t138.3953', u'1060.0\t0.1188\t0.5469\t138.2148', u'1065.0\t0.1656\t0.5469\t138.0229', u'1070.0\t0.1344\t0.5469\t137.8826', u'1075.0\t0.1125\t0.5469\t137.7336', u'1080.0\t0.0938\t0.5469\t137.5703', u'1085.0\t0.1188\t0.5469\t137.3612', u'1090.0\t0.1281\t0.5469\t137.1721', u'1095.0\t0.125\t0.5469\t136.9888', u'1100.0\t0.1438\t0.5469\t136.8198', u'1105.0\t0.125\t0.5469\t136.6594', u'1110.0\t0.1094\t0.5469\t136.5133', u'1115.0\t0.1219\t0.5469\t136.3357', u'1120.0\t0.1188\t0.5469\t136.1552', u'1125.0\t0.1344\t0.5469\t136.012', u'1130.0\t0.1469\t0.5469\t135.8344', u'1135.0\t0.1531\t0.5469\t135.6654', u'1140.0\t0.1719\t0.5469\t135.5135', u'1145.0\t0.1625\t0.5469\t135.3846', u'1150.0\t0.1438\t0.5469\t135.25', u'1155.0\t0.1563\t0.5469\t135.101', u'1160.0\t0.1594\t0.5469\t134.9378', u'1165.0\t0.1625\t0.5469\t134.7859', u'1170.0\t0.1531\t0.5469\t134.6284', u'1175.0\t0.1594\t0.5469\t134.4909', u'1180.0\t0.175\t0.5469\t134.3219', u'1185.0\t0.1656\t0.5469\t134.1872', u'1190.0\t0.15\t0.5469\t134.0383', u'1195.0\t0.1438\t0.5469\t133.875', u'1200.0\t0.175\t0.5469\t133.7175', u'1205.0\t0.1781\t0.5469\t133.5542', u'1210.0\t0.1813\t0.5469\t133.4023', u'1215.0\t0.175\t0.5469\t133.262', u'1220.0\t0.1563\t0.5469\t133.1388', u'1225.0\t0.1563\t0.5469\t132.9956', u'1230.0\t0.1719\t0.5469\t132.8438', u'1235.0\t0.1594\t0.5469\t132.6919', u'1240.0\t0.1625\t0.5469\t132.5831', u'1245.0\t0.1563\t0.5469\t132.4456', u'1250.0\t0.1594\t0.5469\t132.3281', u'1255.0\t0.1688\t0.5469\t132.1648', u'1260.0\t0.175\t0.5469\t132.0102', u'1265.0\t0.1781\t0.5469\t131.9042', u'1270.0\t0.1844\t0.5469\t131.7753', u'1275.0\t0.1813\t0.5469\t131.6406', u'1280.0\t0.1813\t0.5469\t131.4802', u'1285.0\t0.1688\t0.5469\t131.3227', u'1290.0\t0.1594\t0.5469\t131.2024', u'1295.0\t0.1688\t0.5469\t131.0505', u'1300.0\t0.175\t0.5469\t130.8872', u'1305.0\t0.1625\t0.5469\t130.7383', u'1310.0\t0.1688\t0.5469\t130.5893', u'1315.0\t0.1688\t0.5469\t130.4375', u'1320.0\t0.1281\t0.5469\t130.2742', u'1325.0\t0.1281\t0.5469\t130.1195', u'1330.0\t0.1344\t0.5469\t129.9706', u'1335.0\t0.1375\t0.5469\t129.8388', u'1340.0\t0.1563\t0.5469\t129.707', u'1345.0\t0.1594\t0.5469\t129.5667', u'1350.0\t0.125\t0.5469\t129.4063', u'1355.0\t0.1313\t0.5469\t129.2659', u'1360.0\t0.1469\t0.5469\t129.1255', u'1365.0\t0.1156\t0.5469\t128.9852', u'1370.0\t0.1094\t0.5469\t128.8734', u'1375.0\t0.0844\t0.5469\t128.7188', u'1380.0\t0.1125\t0.5469\t128.5555', u'1385.0\t0.1094\t0.5469\t128.4552', u'1390.0\t0.0719\t0.5469\t128.3206', u'1395.0\t0.0906\t0.5469\t128.1773', u'1400.0\t0.0969\t0.5469\t128.0341', u'1405.0\t0.1031\t0.5469\t127.8766', u'1410.0\t0.1063\t0.5469\t127.7276', u'1415.0\t0.1375\t0.5469\t127.5872', u'1420.0\t0.1313\t0.5469\t127.4526', u'1425.0\t0.1406\t0.5469\t127.3438', u'1430.0\t0.1156\t0.5469\t127.2034', u'1435.0\t0.125\t0.5469\t127.0487', u'']
# self.JustDoItTubReta(arrayAux2)
