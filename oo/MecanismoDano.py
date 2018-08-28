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
import requests
from MecanismoDano import*

class MecanismoDano:

    # currentDir = 'C:\\SOMATURBODIAG\\tubulacaoreta\\'
    APP_ROOT = os.getcwd()

    INITIAL_TIMESTAMP = 0
    SAIDA_CALCULO = {}
    ROTOR = 'Rotor'
    TUBULACAO = 'Tubulacao'
    VALVULA = 'Valvula'

    SAIDA_CALCULO[ROTOR] = {}
    SAIDA_CALCULO[TUBULACAO] = {}
    SAIDA_CALCULO[VALVULA] = {}

    SAIDA_CALCULO[TUBULACAO]['Reta'] = {}
    SAIDA_CALCULO[TUBULACAO]['Curva'] = {}
    SAIDA_CALCULO[VALVULA]['Reta'] = {}
    SAIDA_CALCULO[VALVULA]['Curva'] = {}
    SAIDA_CALCULO[ROTOR]['normal'] = {}
    # SAIDA_CALCULO[ROTOR]['normal']['Fadiga'] = {}
    # SAIDA_CALCULO[ROTOR]['normal']['Fluencia'] = {}

    # Essa diferença que está causando o dicionário vazio na Fadiga do Rotor

    TIMESTAMP_OF_DATA = {}
    TIMESTAMP_OF_DATA[0] = 0
    TIMESTAMP_OF_DATA[1] = 0
    TIMESTAMP_OF_DATA[2] = 0

    def __init__(self, currentDir, fileName):
        self.FILE_SEPARATOR = '/'
        if platform.system() == "Windows":
            self.FILE_SEPARATOR = '\\'


        self.currentDir = currentDir
        self.fileName = fileName

        self.fileNamePropMec = 'Propriedades_Mecanicas.txt'
        self.fileNameCoefPoisson = 'Coeficiente_Poisson.txt'
        self.arquivoEntrada = ''
        self.arquivoControle = ''
        self.arquivoSaida = ''
        self.tempoOperacaoBase = ''
        self.tempo = []
        self.pv = []
        self.Tv = []
        self.saida2 = np.matrix('')
        self.width = 5
        self.threshold1 = 175
        self.threshold2 = 50
        self.threshold3 = 500
        self.threshold4 = 1
        self.indiceInicioTransiente = 0
        self.indiceFimTransiente = 0
        self.instanteInicioTransiente = 0
        self.instanteFimTransiente = 0
        self.temperaturaInicioTransiente = 0
        self.temperaturaFimTransiente = 0
        self.tempoFiltro1 = []
        self.TvaporFiltro1 = []
        self.PvaporFiltro1 = []
        self.limiteInfFiltro2Rotor = 500
        self.limiteInfFiltro2 = 520
        self.limiteSupFiltro2rotor = 650
        self.tempoFiltro2 = []
        self.TvaporFiltro2 = []
        self.PvaporFiltro2 = []
        self.limiteInfPressao = 140
        self.limiteInfPressaoRotor = 60 # alterado de acordo com a recomendação da usina
        self.limiteInfTemperaturaRotor = 500
        self.PvaporSM = 0
        self.TvaporSM = 0
        self.TemperaturaPropMec = []
        self.moduloElasticidade = []
        self.coefExpansaoTerm = []
        self.condutividadeTerm = []
        self.calorEspecificoPcte = []
        self.TemperaturaCoefPoisson = []
        self.CoefPoisson = []
        self.TemperaturaCoefTempoRupturaFlu = []
        self.Coef1TRP = []
        self.Coef2TRP = []
        self.Coef3TRP = []
        self.Coef4TRP = []
        self.rho = 7820  # [kg/m³]
        self.tensaoPMH = []
        self.PMH = []
        self.tempoAvaliacao = 0
        self.PmediaVapor = 0
        self.TmediaVapor = 0
        self.E = 0
        self.beta = 0
        self.ni = 0
        self.muVapor = 0
        self.rhoVapor = 0
        self.lambdaVapor = 0
        self.cPvapor = 0
        self.niVapor = 0
        self.aplhaVapor = 0
        self.Re = 0
        self.Nu = 0
        self.Pr = 0
        self.deltaT = 0
        self.PLMR1 = 0
        self.PLMR2 = 0
        self.PMHR1 = 0
        self.PMHR2 = 0
        self.tR1 = 0
        self.tR2 = 0
        self.tR1LM = 0
        self.tR2LM = 0
        self.tR1MH = 0
        self.tR2MH = 0
        self.tRPenny = 0
        self.tRLM = 0
        self.tRMH = 0
        self.VidasRemanescentes = np.matrix('')
        self.deltaDfluencia = np.matrix('')
        self.Resultados = []

        #### Veio da FluenciaTubulacao ####

        self.Vv = []
        self.VvaporFiltro1 = []
        self.VvaporFiltro2 = []
        self.limiteSupFiltro2tubulacao = 600
        self.limiteInfTemperaturaTubulacaoValvula = 500
        self.limiteInfVazao = 100
        self.VvaporSM = 0
        self.VmediaVapor = 0
        self.fileNameCoefTempoRupturaTubulacao = 'Coeficientes_Tempo_Ruptura_Fluencia_Tubulacao.txt'
        self.fileNameParamLarsonMillerTubulacao = 'Parametro_Larson_Miller_Tubulacao.txt'
        self.fileNameParamMonkmanGrantTubulacao = 'Curva_Monkman_Grant_Tubulacao.txt'
        self.inputPMG = []
        self.PMG = []
        self.Dint = 0
        self.Rint = 0
        self.Dext = 0
        self.Rext = 0
        self.rc = 0
        self.t = 0
        self.f1 = 0
        self.f2 = 0
        self.hext = 16.5  # [W/m²K]
        self.Tar = 34
        self.Ltubo = 1  # [m]
        self.Tint = 0
        self.Text = 0
        self.C1 = 0
        self.C2 = 0
        self.Twallmedia = 0
        self.tensaoTangecialTubulacaoReta1 = 0
        self.tensaoTangencialMax = 0
        self.tensaoAxialMax = 0
        self.tensaoRadialMax = 0
        self.tensaoEquivalenteMax = 0
        self.tRKR = 0
        self.tRLM = 0
        self.vidaLM = ''
        self.vidaKR = ''
        self.deltaDLM = ''
        self.deltaDKR = ''
        self.tensaoPLMtub = []
        self.PLMtub = []
        self.PLMtr = 0

        ### Veio de FluenciaRotor ###

        self.fileNameCoefTempoRupturaRotor = 'Coeficientes_Tempo_Ruptura_Fluencia.txt'
        self.fileNameParamLarsonMillerRotor = 'Parametro_Larson_Miller_Rotor.txt'
        self.fileNameParamMansonHaferdRotor = 'Parametro_Manson_Haferd.txt'
        self.Tic = []
        self.Wturb = []
        self.TmetalFiltro1 = []
        self.PotenciaFiltro1 = []
        self.TmetalFiltro2 = []
        self.PotenciaFiltro2 = []
        self.limiteInfPotencia = 100
        self.limiteSupFiltro2rotor = 650
        self.TmediacextSM = 0
        self.PWmediaSM = 0
        self.lambdaCarcaca = 30  # [W/m.K]
        self.d1Rotor = 0
        self.r1Rotor = 0
        self.d2Rotor = 0
        self.r2Rotor = 0
        self.d3Rotor = 0
        self.Tmediacext = 0
        self.PWmedia = 0
        self.N = 0
        self.PWmax = 0
        self.omegazao = 0
        self.hCarcaca = 0
        self.Tmediacint = 0
        self.lambdaRotor = 0
        self.hRotor = 0
        self.T1Rotor = 0
        self.T2Rotor = 0
        self.TmediaRotor = 0
        self.tensaoRadialR1Rotor = 0
        self.tensaoRadialR2Rotor = 0
        self.tensaoTangencialR1Rotor = 0
        self.tensaoTangencialR2Rotor = 0
        self.tensaoAxialR1Rotor = 0
        self.tensaoAxialR2Rotor = 0
        self.tensaoEquivalenteR1Rotor = 0
        self.tensaoEquivalenteR2Rotor = 0
        self.tensaoPLMrotor = []
        self.PLMrotor = []

        ###### Teste Regressão Linear ######

        self.danoAcumuladoRegLin = []
        self.NCRegLin = []
        self.tempoOperacaoRegLin = []
        self.mean_x_RegLin = 0
        self.mean_y_RegLin = 0
        self.variance_x_RegLin = 0
        self.variance_y_RegLin = 0
        self.covariance_x_RegLin = 0
        self.covariance_y_RegLin = 0
        self.a_coef_RegLin = 0
        self.b_coef_RegLin = 0
        self.coefficients_RegLin = []
        self.tempoOperacao90 = 0
        self.numeroCiclos90 = 0
        self.tempoOp = 0
        self.NC = 1
        self.vidaLM_RegLin = 0
        self.vidaPenny_RegLin = 0
        self.vidaMH_RegLin = 0
        self.vidaKR_RegLin = 0
        self.numeroCiclosCurvaFadiga_RegLin = 0
        self.deltaDfadigaCLEPercentual = 0
        self.numeroCiclosCLE_RegLin = 0
        self.danoAcumuladoRegLinCurva = 0
        self.NCRegLinCurva = 0
        self.NCcurva = 0
        self.mean_x_RegLinCurva = 0
        self.mean_y_RegLinCurva = 0
        self.variance_x_RegLinCurva = 0
        self.variance_y_RegLinCurva = 0
        self.covariance_RegLinCurva = 0
        self.coefficients_RegLinCurva = 0
        self.numeroCiclos90Curva = 0
        self.numeroCiclosCurvaFadiga_RegLinCurva = 0





        #### Metodos vindo de Fluencia.py ###

    # def setupInputParamsFromSoma(self, arquivoEntrada, *args):

    def Pa2MPa(self, Tensao):

        return Tensao * 10 ** -6





    def bar2Pa(self, Pbar):

        return Pbar * .1 * 10 ** 6

    def mm2m(self, L):

        return L/1000.

    def tolh2kgs(self, V):

        return V*.278

    def s2hr(self, time):

        return time/3600.

    def setupInputParamsFromSoma(self, arrayAux2, *args):

        listaAux2 = []
        tempo = []
        Vv = []
        pv = []
        Tv = []
        Tic = []
        Wturb = []
        Tmint = []
        Tmext = []

        if len(args) == 5:


            # for line in arquivoEntrada.iter_lines():
            #    arrayAux2.append(line)

            for i in range(len(arrayAux2)):
                listaAux2.append(arrayAux2[i].strip('\r\n'))

            # tempoOperacaoBase = float(listaAux2[0])  # [hr]        ### Retira o tempo de operação contido no arquivo corrente
            # tempoOperacaoBase será passado pelo SOMA de outra forma

            del listaAux2[
                0:1]  ### Apaga as duas primeiras linhas do arquivo corrente que contém o tempo de operação e os labels dos parâmetros

            len(listaAux2)

            for i in range(len(listaAux2) - 1):
                tempo.append(float(listaAux2[i].split('\t')[0]))

            for i in range(len(listaAux2) - 1):
                pv.append(float(listaAux2[i].split('\t')[1]))

            for i in range(len(listaAux2) - 1):
                Tv.append(float(listaAux2[i].split('\t')[2]))  ### Retira os parâmetros contidos no arquivo corrente e armazena-os em listas

            for i in range(len(listaAux2) - 1):
                Tic.append(float(listaAux2[i].split('\t')[3]))

            for i in range(len(listaAux2) - 1):
                Wturb.append(float(listaAux2[i].split('\t')[4]))

            return (tempo, pv, Tv, Tic, Wturb)

        elif len(args) == 6:

            # with open(arquivoEntrada, "rb") as ins:  ### Abre o arquivo de entrada contido no arquivo controle_fluencia.txt
            #    for line in ins:
            #        arrayAux2.append(line)

            for i in range(len(arrayAux2)):
                listaAux2.append(arrayAux2[i].strip('\r\n'))

            # tempoOperacaoBase = float(listaAux2[0])  # [hr]        ### Retira o tempo de operação contido no arquivo corrente
            # tempoOperacaoBase será passado pelo SOMA de outra forma

            del listaAux2[
                0:1]  ### Apaga as duas primeiras linhas do arquivo corrente que contém o tempo de operação e os labels dos parâmetros

            len(listaAux2)

            for i in range(len(listaAux2) - 1):
                tempo.append(listaAux2[i].split('\t')[0])

            for i in range(len(listaAux2) - 1):
                Vv.append(listaAux2[i].split('\t')[1])

            for i in range(len(listaAux2) - 1):
                pv.append(listaAux2[i].split('\t')[2])

            for i in range(len(listaAux2) - 1):
                Tv.append(listaAux2[i].split('\t')[3])  ### Retira os parâmetros contidos no arquivo corrente e armazena-os em listas

            for i in range(len(listaAux2) - 1):
                Tmint.append(listaAux2[i].split('\t')[4])

            for i in range(len(listaAux2) - 1):
                Tmext.append(listaAux2[i].split('\t')[5])

            return (tempo, Vv, pv, Tv, Tmint, Tmext)

        elif len(args) == 4:

            # with open(arquivoEntrada, "rb") as ins:  ### Abre o arquivo de entrada contido no arquivo controle_fluencia.txt
            #    for line in ins:
            #        arrayAux2.append(line)

            for i in range(len(arrayAux2)):
                listaAux2.append(arrayAux2[i].strip('\r\n'))

            #tempoOperacaoBase = float(listaAux2[0])  # [hr]        ### Retira o tempo de operação contido no arquivo corrente
            # tempoOperacaoBase será passado pelo SOMA de outra forma


            # del listaAux2[0:1]  ### Apaga as duas primeiras linhas do arquivo corrente que contém o tempo de operação e os labels dos parâmetros

            print len(listaAux2)

            for i in range(len(listaAux2) - 1):
                tempo.append(int(round(float(listaAux2[i].split('\t')[0]))))

            for i in range(len(listaAux2) - 1):
                Vv.append(round(float(listaAux2[i].split('\t')[1]), 3))

            for i in range(len(listaAux2) - 1):
                pv.append(round(float(listaAux2[i].split('\t')[2]), 3))

            for i in range(len(listaAux2) - 1):
                Tv.append(round(float(listaAux2[i].split('\t')[3]), 3))  ### Retira os parâmetros contidos no arquivo corrente e armazena-os em listas

            return (tempo, Vv, pv, Tv)

        else:
            return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Número de listas incompatível!]")


    def flag2(self):

        if len(self.saida2) == 1:
            with open(self.arquivoControle, "w") as file:
                file.write('2\n5')
        else:
            with open(self.arquivoControle, "w") as file:
                file.write('5\n5')

    def getPropMec(self):

        listaAux3 = []
        arrayAux3 = []
        TemperaturaPropMec = []
        moduloElasticidade = []
        coefExpansaoTerm = []
        condutividadeTerm = []
        calorEspecificoPcte = []
        TemperaturaPropMecFloat = []
        moduloElasticidadeFloat = []
        coefExpansaoTermFloat = []
        condutividadeTermFloat = []
        calorEspecificoPcteFloat = []

        with open(self.currentDir + self.fileNamePropMec, "rb") as ins:  ### Abre o arquivo controle_fluencia.txt
            for line in ins:
                arrayAux3.append(line)

        for i in range(len(arrayAux3)):
            listaAux3.append(arrayAux3[i].strip('\r\n'))

        for i in range(len(listaAux3)):
            TemperaturaPropMec.append(listaAux3[i].split(' ')[0])

        for i in range(len(listaAux3)):
            moduloElasticidade.append(listaAux3[i].split(' ')[1])

        for i in range(len(listaAux3)):
            coefExpansaoTerm.append(listaAux3[i].split(' ')[2])

        for i in range(len(listaAux3)):
            condutividadeTerm.append(listaAux3[i].split(' ')[3])

        for i in range(len(listaAux3)):
            calorEspecificoPcte.append(listaAux3[i].split(' ')[4])

        for i in range(len(TemperaturaPropMec)):
            TemperaturaPropMecFloat.append(float(TemperaturaPropMec[i]))

        for i in range(len(TemperaturaPropMecFloat)):  # Convertendo a temperatura de °C para Kelvin:
            TemperaturaPropMecFloat[i] = TemperaturaPropMecFloat[i] + 273.15

        for i in range(len(moduloElasticidade)):  # Unidade: MPa
            moduloElasticidadeFloat.append(float(moduloElasticidade[i]))

        for i in range(len(coefExpansaoTerm)):  # Unidade: 1/K
            coefExpansaoTermFloat.append(float(coefExpansaoTerm[i]))

        for i in range(len(condutividadeTerm)):  # Unidade: W/m.K
            condutividadeTermFloat.append(float(condutividadeTerm[i]))

        for i in range(len(calorEspecificoPcte)):  # Unidade: J/kg.K
            calorEspecificoPcteFloat.append(float(calorEspecificoPcte[i]))

        return (TemperaturaPropMecFloat, moduloElasticidadeFloat, coefExpansaoTermFloat, condutividadeTermFloat,
                calorEspecificoPcteFloat)

    def getCoefPoisson(self):

        listaAux4 = []
        arrayAux4 = []
        TemperaturaCoefPoisson = []
        CoefPoisson = []
        TemperaturaCoefPoissonFloat = []
        CoefPoissonFloat = []

        with open(self.currentDir + self.fileNameCoefPoisson, "rb") as ins:  ### Abre o arquivo controle_fluencia.txt
            for line in ins:
                arrayAux4.append(line)

        for i in range(len(arrayAux4)):
            listaAux4.append(arrayAux4[i].strip('\r\n'))

        for i in range(len(listaAux4)):
            TemperaturaCoefPoisson.append(listaAux4[i].split('\t')[0])

        for i in range(len(listaAux4)):
            CoefPoisson.append(listaAux4[i].split('\t')[1])

        for i in range(len(TemperaturaCoefPoisson)):
            TemperaturaCoefPoissonFloat.append(float(TemperaturaCoefPoisson[i]))

        for i in range(len(TemperaturaCoefPoissonFloat)):  # Convertendo a temperatura de °C para Kelvin:
            TemperaturaCoefPoissonFloat[i] = TemperaturaCoefPoissonFloat[i] + 273.15

        for i in range(len(CoefPoisson)):
            CoefPoissonFloat.append(float(CoefPoisson[i]))

        return (TemperaturaCoefPoissonFloat, CoefPoissonFloat)


    def setGeometriaValvula(self):

        Dint = 660
        Rint = 330
        Dext = 880
        Rext = 440
        t = (Dext - Dint) / 2.
        f1 = 1.5
        f2 = 1.5

        return (Dint, Rint, Dext, Rext, t, f1, f2)

    def muPT(self, p, Temp):

        steam = IAPWS97(P=p, T=Temp)

        return steam.mu

    def bar2MPa(self, Pbar):

        return Pbar * .1

    def niPT(self, p, Temp):

        steam = IAPWS97(P=p, T=Temp)

        return steam.nu

    def kPT(self, p, Temp):

        steam = IAPWS97(P=p, T=Temp)

        return steam.k

    def alfaPT(self, p, Temp):

        steam = IAPWS97(P=p, T=Temp)

        return steam.alfa

    def Celsius2Kelvin(self, TCelsius):

        return TCelsius + 273.15

    def getCoefTempoRuptura(self,currentDir, fileNameCoefTempoRuptura):

        arrayAux5 = []
        listaAux5 = []
        TemperaturaCoefTempoRupturaFlu = []
        Coef1TRP = []
        Coef2TRP = []
        Coef3TRP = []
        Coef4TRP = []
        TemperaturaCoefTempoRupturaFluFloat = []
        Coef1TRPfloat = []
        Coef2TRPfloat = []
        Coef3TRPfloat = []
        Coef4TRPfloat = []

        with open(currentDir + fileNameCoefTempoRuptura,
                  "rb") as ins:  ### Abre o arquivo controle_fluencia.txt
            for line in ins:
                arrayAux5.append(line)

        for i in range(len(arrayAux5)):
            listaAux5.append(arrayAux5[i].strip('\r\n'))

        for i in range(len(listaAux5)):
            TemperaturaCoefTempoRupturaFlu.append(listaAux5[i].split('\t')[0])

        for i in range(len(listaAux5)):
            Coef1TRP.append(listaAux5[i].split('\t')[1])

        for i in range(len(listaAux5)):
            Coef2TRP.append(listaAux5[i].split('\t')[2])

        for i in range(len(listaAux5)):
            Coef3TRP.append(listaAux5[i].split('\t')[3])

        for i in range(len(listaAux5)):
            Coef4TRP.append(listaAux5[i].split('\t')[4])

        for i in range(len(TemperaturaCoefTempoRupturaFlu)):
            TemperaturaCoefTempoRupturaFluFloat.append(float(TemperaturaCoefTempoRupturaFlu[i]))

        for i in range(len(TemperaturaCoefTempoRupturaFluFloat)):  # Convertendo a temperatura de °C para Kelvin:
            TemperaturaCoefTempoRupturaFluFloat[i] = TemperaturaCoefTempoRupturaFluFloat[i] + 273.15

        for i in range(len(Coef1TRP)):
            Coef1TRPfloat.append(float(Coef1TRP[i]))

        for i in range(len(Coef2TRP)):
            Coef2TRPfloat.append(float(Coef2TRP[i]))

        for i in range(len(Coef3TRP)):
            Coef3TRPfloat.append(float(Coef3TRP[i]))

        for i in range(len(Coef4TRP)):
            Coef4TRPfloat.append(float(Coef4TRP[i]))

        return (TemperaturaCoefTempoRupturaFluFloat, Coef1TRPfloat, Coef2TRPfloat, Coef3TRPfloat, Coef4TRPfloat)

    def getParamLarsonMiller(self, fileNameParamLarsonMiller):

        arrayAux6 = []
        listaAux6 = []
        tensaoPLM = []
        PLM = []
        tensaoPLMfloat = []
        PLMfloat = []

        with open(self.currentDir + fileNameParamLarsonMiller,
                  "rb") as ins:  ### Abre o arquivo controle_fluencia.txt
            for line in ins:
                arrayAux6.append(line)

        for i in range(len(arrayAux6)):
            listaAux6.append(arrayAux6[i].strip('\r\n'))

        for i in range(len(listaAux6)):
            tensaoPLM.append(listaAux6[i].split('\t')[0])

        for i in range(len(listaAux6)):
            PLM.append(listaAux6[i].split('\t')[1])

        for i in range(len(tensaoPLM)):
            tensaoPLMfloat.append(float(tensaoPLM[i]))

        for i in range(len(PLM)):
            PLMfloat.append(float(PLM[i]))

        return (tensaoPLMfloat, PLMfloat)

    def setGeometriaCarcaca(self):

        d1Carcaca = 1.11  # [m]
        r1Carcaca = 0.5 * d1Carcaca
        d2Carcaca = 1.520  # [m]
        r2Carcaca = 0.5 * d2Carcaca

        return (d1Carcaca, r1Carcaca, d2Carcaca, r2Carcaca)

    def setParamAdimensionaisForTransCal1(self):

        omegazao = 2 * pi * 3600 / 60.
        Re = self.r2Rotor * omegazao * self.d2Rotor / self.niVapor
        Pr = self.niVapor / self.alphaVapor
        Nu = 0.038 * (((Re / 2.) * (((self.r1Carcaca - self.r2Rotor) / self.r2Rotor) ** .5)) ** .8) * (Pr ** .33)

        return (Re, Pr, Nu)

    def setParamsRotorCarcacaForTransCal2(self, TmediaVapor, Tmediacext, PWmedia):

        N = 3600
        PWmax = 360  # [MW]
        omegazao = 2 * pi * N / 60.  # [1/s]
        hCarcaca = 360 + 6540 * (PWmedia / PWmax) ** .8  # [W/m².K]
        Tmediacint = (hCarcaca * self.d1Carcaca * TmediaVapor + (
            2 * self.lambdaCarcaca / (log(self.d2Carcaca / self.d1Carcaca))) * Tmediacext) / (
                         hCarcaca * self.d1Carcaca + (2 * self.lambdaCarcaca / (log(self.d2Carcaca / self.d1Carcaca))))
        T2Rotor = Tmediacint

        return (N, PWmax, omegazao, hCarcaca, Tmediacint, T2Rotor)

    def lambdaInterpolado(self, T):


        cCondutividadeTerm = interp1d(self.TemperaturaPropMec, self.condutividadeTerm)


        if T >= self.TemperaturaPropMec[-1]:
            condTerm = cCondutividadeTerm(self.TemperaturaPropMec[-1])

        elif T <= self.TemperaturaPropMec[0]:
            condTerm = cCondutividadeTerm(self.TemperaturaPropMec[0])

        else:
            condTerm = cCondutividadeTerm(T)

        return float(condTerm)

        return cCondutividadeTerm(T)

    def setPropTermoFisicaVaporForFluResult(self, P, T): # P[bar] ; T[ºC]

        muVapor = self.muPT(self.bar2MPa(P), T)  # [Pa.s]
        rhoVapor = self.rhoPT(self.bar2MPa(P), T)  # [kg/m³]
        lambdaVapor = self.kPT(self.bar2MPa(P), T)  # [W/m.K]
        cpVapor = self.cpPT(self.bar2MPa(P), T) * 1000   # Multiplaca?o por 1000 para converter [kJ/kg.K] para [m?/K.s?], pois a tabela de vapor IAWPS97 trabalha com a primeira unidade e o c?igo Mathcad com a ?ltima.
        niVapor = muVapor / rhoVapor
        alphaVapor = lambdaVapor / (rhoVapor * cpVapor)

        return (muVapor, rhoVapor, lambdaVapor, cpVapor, niVapor, alphaVapor)

    def setGeometriaRotor(self):

        d1Rotor = 0.096  # [m]
        r1Rotor = 0.5 * d1Rotor  # raio do furo no eixo do rotor AP, isto é, a distância entre a linha de centro do eixo do rotor e a superfície do furo.
        d2Rotor = 0.730  # [m]
        r2Rotor = 0.5 * d2Rotor  # raio da base da palheta do rotor AP, isto é, a distância entre a linha de centro do eixo do rotor e a superfície de fixação da palheta.
        d3Rotor = 0.942  # [m]

        return (d1Rotor, r1Rotor, d2Rotor, r2Rotor, d3Rotor)


    def getParamMansonHaferd(self, fileNameParamMansonHaferd):

        arrayAux7 = []
        listaAux7 = []
        tensaoPMH = []
        PMH = []
        tensaoPMHfloat = []
        PMHfloat = []

        with open(self.currentDir + fileNameParamMansonHaferd,
                  "rb") as ins:  ### Abre o arquivo controle_fluencia.txt
            for line in ins:
                arrayAux7.append(line)

        for i in range(len(arrayAux7)):
            listaAux7.append(arrayAux7[i].strip('\r\n'))

        for i in range(len(listaAux7)):
            tensaoPMH.append(listaAux7[i].split('\t')[0])

        for i in range(len(listaAux7)):
            PMH.append(listaAux7[i].split('\t')[1])

        for i in range(len(tensaoPMH)):
            tensaoPMHfloat.append(float(tensaoPMH[i]))

        for i in range(len(PMH)):
            PMHfloat.append(float(PMH[i]))

        return (tensaoPMHfloat, PMHfloat)

    def setParamsRotorCarcacaForTransCal3(self):

        T2Rotor = self.Tmediacint
        hRotor = self.lambdaVapor * self.Nu / self.d2Rotor
        T1Rotor = (T2Rotor - (hRotor / (2 * self.lambdaRotor)) * self.d2Rotor * (self.TmediaVapor - T2Rotor) * log(
            self.d2Rotor / self.d1Rotor))
        deltaT = T2Rotor - T1Rotor
        TmediaRotor = 0.5 * (T2Rotor + T1Rotor)

        return (T2Rotor, hRotor, T1Rotor, deltaT, TmediaRotor)

    def flag4(self): # cálculo do dano e do tempo de ruptura por fluência OK!

        if self.saida2.item(0) == 0:

            with open(self.arquivoControle, "w") as file:

                file.write('4\n5')
        else:

            with open(self.arquivoControle, "w") as file:

                file.write('5\n5')

    def writeOutfile(self, Equipamento, mecanismoDano , geometria = 'normal'):

        strOut = ''

        if mecanismoDano == 'Fluencia':

            if Equipamento == 'Rotor':

                strOut = '' + str(self.saida2[0][0]) + '\t' + str(self.saida2[0][1]) + '\t' + str(
                        self.saida2[0][2]) + '\n' + str(
                        self.saida2[1][0]) + '\t' + str(self.saida2[1][1]) + '\t' + str(
                        self.saida2[1][2]) + '\n' + str(
                        self.saida2[2][0]) + '\t' + str(self.saida2[2][1]) + '\t' + str(
                        self.saida2[2][2]) + '\n' + str(
                        self.saida2[3][0]) + '\t' + str(self.saida2[3][1]) + '\t' + str(
                        self.saida2[3][2]) + '\n' + str(
                        self.saida2[4][0]) + '\t' + str(self.saida2[4][1]) + '\t' + str(self.saida2[4][2])

                MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR][geometria]['Fluencia'] = strOut

                # with open(self.arquivoSaida, "w") as file:
                    # file.write(strOut)

                return

            elif Equipamento == 'Tubulacao':

                if geometria == 'Reta':

                    strOut = '' + str(self.saida2[0][0]) + '\t' + str(self.saida2[0][1]) + '\t' + str(
                            self.saida2[0][2]) + '\n' + '' + str(
                            self.saida2[1][0]) + '\t' + str(self.saida2[1][1]) + '\t' + str(
                            self.saida2[1][2]) + '\n' + '' + str(
                            self.saida2[2][0]) + '\t' + str(self.saida2[2][1]) + '\t' + str(
                            self.saida2[2][2]) + '\n' + '' + str(
                            self.saida2[3][0]) + '\t' + str(self.saida2[3][1]) + '\t' + str(self.saida2[3][2])

                    MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO][geometria]['Fluencia'] = strOut

                    # with open(self.arquivoSaida, "w") as file:
                        # file.write(strOut)

                    return

                if geometria == 'Curva':

                    strOut = '' + str(self.saida2[0][0]) + '\t' + str(self.saida2[0][1]) + '\t' + str(
                            self.saida2[0][2]) + '\n' + '' + str(
                            self.saida2[1][0]) + '\t' + str(self.saida2[1][1]) + '\t' + str(
                            self.saida2[1][2]) + '\n' + '' + str(
                            self.saida2[2][0]) + '\t' + str(self.saida2[2][1]) + '\t' + str(
                            self.saida2[2][2]) + '\n' + '' + str(
                            self.saida2[3][0]) + '\t' + str(self.saida2[3][1]) + '\t' + str(self.saida2[3][2])

                    MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO][geometria]['Fluencia'] = strOut

                    # with open(self.arquivoSaida, "w") as file:
                        # file.write(strOut)

                    return

            elif Equipamento == 'Valvula':

                if geometria == 'Reta':

                    strOut = '' + str(self.saida2[0][0]) + '\t' + str(self.saida2[0][1]) + '\t' + str(
                            self.saida2[0][2]) + '\n' + '' + str(
                            self.saida2[1][0]) + '\t' + str(self.saida2[1][1]) + '\t' + str(
                            self.saida2[1][2]) + '\n' + '' + str(
                            self.saida2[2][0]) + '\t' + str(self.saida2[2][1]) + '\t' + str(
                            self.saida2[2][2]) + '\n' + '' + str(
                            self.saida2[3][0]) + '\t' + str(self.saida2[3][1]) + '\t' + str(self.saida2[3][2])

                    MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA][geometria]['Fluencia'] = strOut

                    # with open(self.arquivoSaida, "w") as file:
                        # file.write(strOut)

                    return

                if geometria == 'Curva':

                    strOut = '' + str(self.saida2[0][0]) + '\t' + str(self.saida2[0][1]) + '\t' + str(
                            self.saida2[0][2]) + '\n' + '' + str(
                            self.saida2[1][0]) + '\t' + str(self.saida2[1][1]) + '\t' + str(
                            self.saida2[1][2]) + '\n' + '' + str(
                            self.saida2[2][0]) + '\t' + str(self.saida2[2][1]) + '\t' + str(
                            self.saida2[2][2]) + '\n' + '' + str(
                            self.saida2[3][0]) + '\t' + str(self.saida2[3][1]) + '\t' + str(self.saida2[3][2])

                    MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA][geometria]['Fluencia'] = strOut

                    # with open(self.arquivoSaida, "w") as file:
                        # file.write(strOut)

                    return

                print strOut

            else:

                return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Equipamento inexistente! Digite o tipo de equipamento: Rotor, Tubulacao ou Valvula]")

        elif mecanismoDano == 'Fadiga':

            if Equipamento == 'Rotor':

                strOut = '' + str(self.saida2[0][0]) + '\t' + str(self.saida2[0][1]) + '\t' + str(
                        self.saida2[0][2]) + '\n' + '' + str(
                        self.saida2[1][0]) + '\t' + str(self.saida2[1][1]) + '\t' + str(
                        self.saida2[1][2]) + '\n' + '' + str(
                        self.saida2[2][0]) + '\t' + str(self.saida2[2][1]) + '\t' + str(
                        self.saida2[2][2]) + '\n' + '' + str(
                        self.saida2[3][0]) + '\t' + str(self.saida2[3][1]) + '\t' + str(self.saida2[3][2])

                MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR][geometria]['Fadiga'] = strOut

                # with open(self.arquivoSaida, "w") as file:
                    # file.write(strOut)

                return

            if Equipamento == 'Tubulacao':

                if (geometria == 'Reta'):
                    complemento = str(
                        self.saida2[2][0]) + '\t' + str(self.saida2[2][1]) + '\t' + str(
                        self.saida2[2][2])
                else:
                    complemento = str(
                        self.saida2[3][0]) + '\t' + str(self.saida2[3][1]) + '\t' + str(
                        self.saida2[3][2])

                strOut = '' + str(self.saida2[0][0]) + '\t' + str(self.saida2[0][1]) + '\t' + str(
                    self.saida2[0][2]) + '\n' + '' + str(
                    self.saida2[1][0]) + '\t' + str(self.saida2[1][1]) + '\t' + str(
                    self.saida2[1][2]) + '\n' + '' + complemento

                MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO][geometria]['Fadiga'] = strOut

                # with open(self.arquivoSaida, "w") as file:
                    # file.write(strOut)

                return


            if Equipamento == 'Valvula':

                if (geometria == 'Reta'):
                    complemento = str(
                        self.saida2[2][0]) + '\t' + str(self.saida2[2][1]) + '\t' + str(
                        self.saida2[2][2])
                else:

                    complemento = str(
                        self.saida2[3][0]) + '\t' + str(self.saida2[3][1]) + '\t' + str(
                        self.saida2[3][2])

                strOut = '' + str(self.saida2[0][0]) + '\t' + str(self.saida2[0][1]) + '\t' + str(
                    self.saida2[0][2]) + '\n' + '' + str(
                    self.saida2[1][0]) + '\t' + str(self.saida2[1][1]) + '\t' + str(
                    self.saida2[1][2]) + '\n' + '' + complemento

                MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA][geometria]['Fadiga'] = strOut


                # with open(self.arquivoSaida, "w") as file:
                    # file.write(strOut)

                return

            else:

                return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Equipamento inexistente! Digite o tipo de equipamento: Rotor, Tubulacao ou Valvula]")

        else:
            return EH.ErrorHandle.handler(
                "ERROR: [Ocorreu o erro : Mecanismo de dano inexistente! Digite o tipo de mecanismo de dano: Fluencia ou Fadiga]")

        print strOut

    def flag6(self):  # final do processo de cálculo OK!

        with open(self.arquivoControle, "w") as file:
            file.write('5\n5')

    def flagFim(self):

        FlagFim = self.arquivoControle + '.over'

        with open(FlagFim, "w") as file:

            file.write('1')

    def setGeometriaTubulacao(self):

        Dint = 193.
        Rint = .0965
        Dext = 290.
        Rext = .145
        rc = 305.
        t = (Dext - Dint) / 2.
        f1 = (4*rc/Dext - 1) / (4*rc/Dext - 2)
        f2 = (4 * rc / Dext + 1) / (4 * rc / Dext + 2)

        return (Dint, Rint, Dext, Rext, rc, t, f1, f2)


    def Paramslist2arrayMH(self, mecanismoDano, equipamento):



        if mecanismoDano == 'Fluencia':

            self.TemperaturaPropMec = np.asarray(self.TemperaturaPropMec)
            self.moduloElasticidade = np.asarray(self.moduloElasticidade)
            self.coefExpansaoTerm = np.asarray(self.coefExpansaoTerm)
            self.condutividadeTerm = np.asarray(self.condutividadeTerm)
            self.calorEspecificoPcte = np.asarray(self.calorEspecificoPcte)
            self.TemperaturaCoefPoisson = np.asarray(self.TemperaturaCoefPoisson)
            self.CoefPoisson = np.asarray(self.CoefPoisson)
            self.TemperaturaCoefTempoRupturaFlu = np.asarray(self.TemperaturaCoefTempoRupturaFlu)
            self.Coef1TRP = np.asarray(self.Coef1TRP)
            self.Coef2TRP = np.asarray(self.Coef2TRP)
            self.Coef3TRP = np.asarray(self.Coef3TRP)
            self.Coef4TRP = np.asarray(self.Coef4TRP)
            self.tensaoPLMrotor = np.asarray(self.tensaoPLMrotor)
            self.PLMrotor = np.asarray(self.PLMrotor)
            self.tensaoPMH = np.asarray(self.tensaoPMH)
            self.PMH = np.asarray(self.PMH)

        elif mecanismoDano == 'Fadiga':

            if equipamento == 'Rotor':
                self.TemperaturaPropMec = np.asarray(self.TemperaturaPropMec)
                self.moduloElasticidade = np.asarray(self.moduloElasticidade)
                self.coefExpansaoTerm = np.asarray(self.coefExpansaoTerm)
                self.condutividadeTerm = np.asarray(self.condutividadeTerm)
                self.calorEspecificoPcte = np.asarray(self.calorEspecificoPcte)
                self.TemperaturaCoefPoisson = np.asarray(self.TemperaturaCoefPoisson)
                self.CoefPoisson = np.asarray(self.CoefPoisson)
                self.TemperaturaCoefTempoRupturaFlu = np.asarray(self.TemperaturaCoefTempoRupturaFlu)
                self.Coef1TRP = np.asarray(self.Coef1TRP)
                self.Coef2TRP = np.asarray(self.Coef2TRP)
                self.Coef3TRP = np.asarray(self.Coef3TRP)
                self.Coef4TRP = np.asarray(self.Coef4TRP)
                self.tensaoPLMrotor = np.asarray(self.tensaoPLMrotor)
                self.PLMrotor = np.asarray(self.PLMrotor)
                self.tensaoPMH = np.asarray(self.tensaoPMH)
                self.PMH = np.asarray(self.PMH)
                self.variacaoDeformacao = np.asarray(self.variacaoDeformacao)
                self.numeroCiclos = np.asarray(self.numeroCiclos)

            elif equipamento == 'Tubulacao':
                self.TemperaturaPropMec = np.asarray(self.TemperaturaPropMec)
                self.moduloElasticidade = np.asarray(self.moduloElasticidade)
                self.coefExpansaoTerm = np.asarray(self.coefExpansaoTerm)
                self.condutividadeTerm = np.asarray(self.condutividadeTerm)
                self.calorEspecificoPcte = np.asarray(self.calorEspecificoPcte)
                self.TemperaturaCoefPoisson = np.asarray(self.TemperaturaCoefPoisson)
                self.CoefPoisson = np.asarray(self.CoefPoisson)
                self.amplitudeDeformacao = np.asarray(self.amplitudeDeformacao)
                self.amplitudeTensao = np.asarray(self.amplitudeTensao)
                self.amplitudeDeformacaoNR = np.asarray(self.amplitudeDeformacaoNR)
                self.Nf25 = np.asarray(self.Nf25)

            elif equipamento == 'Valvula':
                self.TemperaturaPropMec = np.asarray(self.TemperaturaPropMec)
                self.moduloElasticidade = np.asarray(self.moduloElasticidade)
                self.coefExpansaoTerm = np.asarray(self.coefExpansaoTerm)
                self.condutividadeTerm = np.asarray(self.condutividadeTerm)
                self.calorEspecificoPcte = np.asarray(self.calorEspecificoPcte)
                self.TemperaturaCoefPoisson = np.asarray(self.TemperaturaCoefPoisson)
                self.CoefPoisson = np.asarray(self.CoefPoisson)
                self.amplitudeDeformacao = np.asarray(self.amplitudeDeformacao)
                self.amplitudeTensao = np.asarray(self.amplitudeTensao)
                self.amplitudeDeformacaoNR = np.asarray(self.amplitudeDeformacaoNR)
                self.Nf25 = np.asarray(self.Nf25)

            else:
                return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Digite o equipamento: Rotor, Tubulacao ou Valvula!]")



        else:
            return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Digite o mecanismo de dano: Fluencia ou Fadiga!]")

    #### Fim Metodos Fluencia.py ####

    #### Método criado somente para voltar a filosofia antiga de recebimento de dados ####

    def setupNameFileInputParamsTesteFadigaRotor(self, currentDir, fileName):

        os.chdir(currentDir)  ### Muda o diretório corrente do Python para o diretório de interesse
        arrayAux1 = []
        listaAux1 = []

        with open(currentDir + fileName, "rb") as ins:  ### Abre o arquivo controle_fluencia.txt
            for line in ins:
                arrayAux1.append(line)

        listaAux1.append(arrayAux1[0].strip('\r\n'))
        arquivoEntrada = listaAux1[0].split('\t')[1]
        arquivoControle = listaAux1[0].split('\t')[5]
        arquivoSaida = listaAux1[0].split('\t')[3]

        return (arquivoEntrada, arquivoSaida, arquivoControle)

    #######################################################################################

    def setupNameFileInputParams(self, currentDir, fileName):

        # Exemplos de Diretórios:
        # IN  C:\SOMATURBODIAG\rotor\in \
        # OUT C:\SOMATURBODIAG\rotor\out\
        # REL C:\SOMATURBODIAG\rotor\out\
        # currentDir = os.getcwd() + '/../DATA/valvulareta/' # o comando os.getcwd está incluindo o diretorio oo no caminho do arquivo erroneamente!!!!!
        # if platform.system() == "Windows":
        #    currentDir = os.getcwd() + '\\..\\DATA\\valvulareta\\'

        # MAUDONET os.chdir(currentDir)  ### Muda o diretório corrente do Python para o diretório de interesse
        arrayAux1 = []
        listaAux1 = []

        with open(currentDir + fileName, "rb") as ins:  ### Abre o arquivo controle_fluencia.txt
            for line in ins:
                arrayAux1.append(line)

        listaAux1.append(arrayAux1[0].strip('\r\n'))
        # arquivoEntrada = currentDir + self.FILE_SEPARATOR + 'in' + self.FILE_SEPARATOR + listaAux1[0].split('\t')[1]
        arquivoEntrada = listaAux1[0].split('\t')[1]
        # arquivoControle = currentDir + self.FILE_SEPARATOR + 'out' + self.FILE_SEPARATOR + listaAux1[0].split('\t')[5]
        arquivoControle = listaAux1[0].split('\t')[5]
        # arquivoSaida = currentDir + self.FILE_SEPARATOR + 'out' + self.FILE_SEPARATOR + listaAux1[0].split('\t')[3]
        arquivoSaida = listaAux1[0].split('\t')[3]

        return (arquivoEntrada, arquivoSaida, arquivoControle)


    def setupInputParams(self, arquivoEntrada, *args):

        print "arquivoEntrada = " + arquivoEntrada
        arrayAux2 = []
        listaAux2 = []
        tempo = []
        Vv = []
        pv = []
        Tv = []
        Tic = []
        Wturb = []
        Tmint = []
        Tmext = []

        if len(args) == 5:

            with open(arquivoEntrada, "rb") as ins:  ### Abre o arquivo de entrada contido no arquivo controle_fluencia.txt
                for line in ins:
                    arrayAux2.append(line)

            for i in range(len(arrayAux2)):
                listaAux2.append(arrayAux2[i].strip('\r\n'))

            tempoOperacaoBase = float(listaAux2[0])  # [hr]        ### Retira o tempo de operação contido no arquivo corrente

            del listaAux2[
                0:2]  ### Apaga as duas primeiras linhas do arquivo corrente que contém o tempo de operação e os labels dos parâmetros

            len(listaAux2)

            for i in range(len(listaAux2) - 1):
                tempo.append(float(listaAux2[i].split('\t')[0]))

            for i in range(len(listaAux2) - 1):
                pv.append(float(listaAux2[i].split('\t')[1]))

            for i in range(len(listaAux2) - 1):
                Tv.append(float(listaAux2[i].split('\t')[2]))  ### Retira os parâmetros contidos no arquivo corrente e armazena-os em listas

            for i in range(len(listaAux2) - 1):
                Tic.append(float(listaAux2[i].split('\t')[3]))

            for i in range(len(listaAux2) - 1):
                Wturb.append(float(listaAux2[i].split('\t')[4]))

            return (tempoOperacaoBase, tempo, pv, Tv, Tic, Wturb)

        elif len(args) == 6:

            with open(arquivoEntrada, "rb") as ins:  ### Abre o arquivo de entrada contido no arquivo controle_fluencia.txt
                for line in ins:
                    arrayAux2.append(line)

            for i in range(len(arrayAux2)):
                listaAux2.append(arrayAux2[i].strip('\r\n'))

            tempoOperacaoBase = float(listaAux2[0])  # [hr]        ### Retira o tempo de operação contido no arquivo corrente

            del listaAux2[
                0:2]  ### Apaga as duas primeiras linhas do arquivo corrente que contém o tempo de operação e os labels dos parâmetros

            len(listaAux2)

            for i in range(len(listaAux2) - 1):
                tempo.append(listaAux2[i].split('\t')[0])

            for i in range(len(listaAux2) - 1):
                Vv.append(listaAux2[i].split('\t')[1])

            for i in range(len(listaAux2) - 1):
                pv.append(listaAux2[i].split('\t')[2])

            for i in range(len(listaAux2) - 1):
                Tv.append(listaAux2[i].split('\t')[3])  ### Retira os parâmetros contidos no arquivo corrente e armazena-os em listas

            for i in range(len(listaAux2) - 1):
                Tmint.append(listaAux2[i].split('\t')[4])

            for i in range(len(listaAux2) - 1):
                Tmext.append(listaAux2[i].split('\t')[5])

            return (tempoOperacaoBase, tempo, Vv, pv, Tv, Tmint, Tmext)

        elif len(args) == 4:

            with open(arquivoEntrada, "rb") as ins:  ### Abre o arquivo de entrada contido no arquivo controle_fluencia.txt
                for line in ins:
                    arrayAux2.append(line)

            for i in range(len(arrayAux2)):
                listaAux2.append(arrayAux2[i].strip('\r\n'))

            tempoOperacaoBase = float(listaAux2[0])  # [hr]        ### Retira o tempo de operação contido no arquivo corrente

            del listaAux2[
                0:2]  ### Apaga as duas primeiras linhas do arquivo corrente que contém o tempo de operação e os labels dos parâmetros

            len(listaAux2)

            for i in range(len(listaAux2) - 1):
                tempo.append(listaAux2[i].split('\t')[0])

            for i in range(len(listaAux2) - 1):
                Vv.append(round(float(listaAux2[i].split('\t')[1]), 3))

            for i in range(len(listaAux2) - 1):
                pv.append(round(float(listaAux2[i].split('\t')[2]), 3))

            for i in range(len(listaAux2) - 1):
                Tv.append(round(float(listaAux2[i].split('\t')[3]), 3))  ### Retira os parâmetros contidos no arquivo corrente e armazena-os em listas

            return (tempoOperacaoBase, tempo, Vv, pv, Tv)

        else:
            return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Número de listas incompatível!]")


    def flag0(self):  # leitura do arquivo contendo os dados de entrada OK!

        if len(self.Tv) >= 0:
            with open(self.arquivoControle, "w") as file:
                file.write('0\n5')

        else:
            return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Falha no check 0 de 5!]")


    def medSmoothParams(self, lista):  ### Além de suavizar os parâmetros, converte de string para float os valores armazenados



        smoothList = []
        for i in range(len(lista)):

            if i == 0:
                smoothList.append(round(float(lista[i]), 3))

            elif i == 1:
                smoothList.append(round(np.median([float(lista[i-1]) , float(lista[i]) , float(lista[i + 1])]), 3))


            elif 1 < i < len(lista) - 2:

                smoothList.append(round(np.median([float(lista[i-2]), float(lista[i - 1]), float(lista[i]), float(
                    lista[i + 1]), float(lista[i + 2])]), 3))


            elif i == (len(lista) - 2):

                smoothList.append(round(np.median([float(lista[i-1]), float(lista[i]), float(lista[i+1])]), 3))

            elif i == (len(lista) - 1):
                smoothList.append(round(float(lista[i]), 3))


        return smoothList




    def checkParamsForFlu(self, mecanismoDano, Equipamento, geometria = 'normal' ):
        # Analisa se os dados coletados produzem dano por fluência

        strOut = ''
        retCode = -1

        if mecanismoDano == 'Fluencia':

            retCode = 1

            if Equipamento == 'Rotor':

                if max(self.Tv) < 200 or max(self.pv) < 60 or self.PvaporSM < 60 or self.PWmediaSM < 100:  ### Aplica as condições para avaliar se há dano por fluência

                    self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 2 0 0; 3 0 0')

                    strOut = str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                            self.saida2.item((0, 2))) + '\n' + str(self.saida2.item((1, 0))) + '\t' + str(
                            self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                            self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                            self.saida2.item((2, 2))) + '\n' + '' + str(self.saida2.item((3, 0))) + '\t' + str(
                            self.saida2.item((3, 1))) + '\t' + str(self.saida2.item((3, 2))) + '\n' + '' + str(
                            self.saida2.item((4, 0))) + '\t' + str(self.saida2.item((4, 1))) + '\t' + str(
                            self.saida2.item((4, 2)))

                    MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR][geometria]['Fluencia'] = strOut

                    # with open(r'' + self.arquivoSaida + '', "w") as file:
                        # file.write(strOut)

                    print('WARNING: [Nao ha fluencia para ser calculada nesse arquivo!]')
                    # return 1

                else:
                    retCode = 0
                    self.saida2 = np.matrix('0')

            if Equipamento == 'Tubulacao':

                if geometria == 'Reta':

                    if max(self.Tv) < 200 or max(self.pv) < 80 or self.PvaporSM < 80 or self.VvaporSM < 100:  ### Aplica as condições para avaliar se há dano por fluência

                        self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')

                        strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
                            self.saida2.item((0, 1))) + '\t' + str(
                            self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                            self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                            self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                            self.saida2.item((2, 2))) + '\n' + '' + str(
                            self.saida2.item((3, 0))) + '\t' + str(self.saida2.item((3, 1))) + '\t' + str(
                            self.saida2.item((3, 2)))

                        MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO][geometria]['Fluencia'] = strOut

                        # with open(r'' + self.arquivoSaida + '', "w") as file:
                            # file.write(strOut)

                        print('WARNING: [Nao ha fluencia para ser calculada nesse arquivo!]')
                        # return 1

                    else:
                        retCode = 0
                        self.saida2 = np.matrix('0')


                if geometria == 'Curva':

                    if max(self.Tv) < 200 or max(self.pv) < 80 or self.PvaporSM < 80 or self.VvaporSM < 100:  ### Aplica as condições para avaliar se há dano por fluência

                        self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')

                        strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
                            self.saida2.item((0, 1))) + '\t' + str(
                            self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                            self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                            self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                            self.saida2.item((2, 2))) + '\n' + '' + str(
                            self.saida2.item((3, 0))) + '\t' + str(self.saida2.item((3, 1))) + '\t' + str(
                            self.saida2.item((3, 2)))

                        MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO][geometria]['Fluencia'] = strOut

                        # with open(r'' + self.arquivoSaida + '', "w") as file:
                            # file.write(strOut)

                        print('WARNING: [Nao ha fluencia para ser calculada nesse arquivo!]')
                        # return 1

                    else:
                        retCode = 0
                        self.saida2 = np.matrix('0')

            if Equipamento == 'Valvula':

                if geometria == 'Reta':

                    if max(self.Tv) < 200 or max(self.pv) < 80 or self.PvaporSM < 80 or self.VvaporSM < 100:  ### Aplica as condições para avaliar se há dano por fluência

                        self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')

                        strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
                            self.saida2.item((0, 1))) + '\t' + str(
                            self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                            self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                            self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                            self.saida2.item((2, 2))) + '\n' + '' + str(
                            self.saida2.item((3, 0))) + '\t' + str(self.saida2.item((3, 1))) + '\t' + str(
                            self.saida2.item((3, 2)))

                        MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA][geometria]['Fluencia'] = strOut

                        # with open(r'' + self.arquivoSaida + '', "w") as file:
                            # file.write(strOut)

                        print('WARNING: [Nao ha fluencia para ser calculada nesse arquivo!]')
                        # return 1

                    else:
                        retCode = 0
                        self.saida2 = np.matrix('0')

                if geometria == 'Curva':

                    if max(self.Tv) < 200 or max(self.pv) < 80 or self.PvaporSM < 80 or self.VvaporSM < 100:  ### Aplica as condições para avaliar se há dano por fluência

                        self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')

                        strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
                            self.saida2.item((0, 1))) + '\t' + str(
                            self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                            self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                            self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                            self.saida2.item((2, 2))) + '\n' + '' + str(
                            self.saida2.item((3, 0))) + '\t' + str(self.saida2.item((3, 1))) + '\t' + str(
                            self.saida2.item((3, 2)))

                        MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA][geometria]['Fluencia'] = strOut

                        # with open(r'' + self.arquivoSaida + '', "w") as file:
                            # file.write(strOut)

                        print('WARNING: [Nao ha fluencia para ser calculada nesse arquivo!]')
                        # return 1

                    else:
                        retCode = 0
                        self.saida2 = np.matrix('0')

                # return​ EH.ErrorHandle.handler("WARNING: [Não existe fluencia!]")

        elif mecanismoDano == 'Fadiga':

            retCode = 2

            if Equipamento == 'Rotor':

                if (max(self.Tv) < 200 or max(self.pv) < 60) or self.PvaporSM < 60 or self.PWmediaSM < 100:  ### Aplica as condições para avaliar se há dano por fluência

                    self.saida2 = np.matrix('40 0 0; 0 20 30; 4 0 0; 5 0 0')

                    strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                                self.saida2.item((2, 2))) + '\n' + '' + str(self.saida2.item((3, 0))) + '\t' + str(
                                self.saida2.item((3, 1))) + '\t' + str(self.saida2.item((3, 2)))

                    MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR][geometria]['Fadiga'] = strOut

                    # with open(r'' + self.arquivoSaida + '', "w") as file:
                        # file.write(strOut)

                    print('WARNING: [Nao ha fadiga para ser calculada nesse arquivo!]')
                    # return 2

                    # return​ EH.ErrorHandle.handler("WARNING: [Não existe fadiga!]")
                else:
                    retCode = 0
                    self.saida2 = np.matrix('0')


            elif Equipamento == 'Tubulacao':

                if geometria == 'Reta':

                    # if max(self.Tv) < 200 or max(self.pv) < 80:  ### Aplica as condições para avaliar se há dano por fluência
                    if max(self.Tv) < 200 or max(self.pv) < 80 or self.indiceFimTransiente == -1:

                        self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')

                        strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                            self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                            self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                            self.saida2.item((2, 0))) + '\t' + str(
                            self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2)))

                        MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO][geometria]['Fadiga'] = strOut

                        # with open(r'' + self.arquivoSaida + '', "w") as file:
                            # file.write(strOut)

                        # return​ EH.ErrorHandle.handler("WARNING: [Não existe fadiga!]")
                        print('WARNING: [Nao ha fadiga para ser calculada nesse arquivo!]')
                        # return 2

                    else:
                        retCode = 0
                        self.saida2 = np.matrix('0')

                if geometria == 'Curva':

                    # if max(self.Tv) < 200 or max(self.pv) < 80:  ### Aplica as condições para avaliar se há dano por fluência
                    if (max(self.Tv) < 200 or max(self.pv) < 80) or self.indiceFimTransiente == -1:
                        self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')

                        strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                            self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                            self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                            self.saida2.item((2, 0))) + '\t' + str(
                            self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2)))

                        MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO][geometria]['Fadiga'] = strOut

                        # with open(r'' + self.arquivoSaida + '', "w") as file:
                            # file.write(strOut)

                        # return​ EH.ErrorHandle.handler("WARNING: [Não existe fadiga!]")
                        print('WARNING: [Nao ha fadiga para ser calculada nesse arquivo!]')
                        # return 2

                    else:
                        retCode = 0
                        self.saida2 = np.matrix('0')


            elif Equipamento == 'Valvula':

                if geometria == 'Reta':

                    if (max(self.Tv) < 200 or max(self.pv) < 80) or self.indiceFimTransiente == -1:
                    #if max(self.Tv) < 200 or max(
                    #    self.pv) < 80:  ### Aplica as condições para avaliar se há dano por fluência

                        self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')

                        strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                        self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                        self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                        self.saida2.item((2, 0))) + '\t' + str(
                        self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2)))

                        MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA][geometria]['Fadiga'] = strOut

                        # with open(r'' + self.arquivoSaida + '', "w") as file:
                            # file.write(strOut)

                        # return​ EH.ErrorHandle.handler("WARNING: [Não existe fadiga!]")
                        print('WARNING: [Nao ha fadiga para ser calculada nesse arquivo!]')
                        # return 2

                    else:
                        retCode = 0
                        self.saida2 = np.matrix('0')

                if geometria == 'Curva':

                    if (max(self.Tv) < 200 or max(self.pv) < 80) or self.indiceFimTransiente == -1:
                    # if max(self.Tv) < 200 or max(
                    #    self.pv) < 80:  ### Aplica as condições para avaliar se há dano por fluência

                        self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')

                        strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                        self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                        self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                        self.saida2.item((2, 0))) + '\t' + str(
                        self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2)))

                        MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA][geometria]['Fadiga'] = strOut

                        # with open(r'' + self.arquivoSaida + '', "w") as file:
                            # file.write(strOut)

                        # return​ EH.ErrorHandle.handler("WARNING: [Não existe fadiga!]")
                        print('WARNING: [Nao ha fadiga para ser calculada nesse arquivo!]')
                        # return 2

                    else:
                        retCode = 0
                        self.saida2 = np.matrix('0')


            else:
                return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Digite o equipamento: Rotor, Tubulacao ou Valvula!]")

        else:
            return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Digite o mecanismo de dano: Fluencia ou Fadiga!]")

        print strOut

        return retCode



    def rhoPT(self, p, Temp):

        steam = IAPWS97(P=p, T=Temp)

        return steam.rho

    def cpPT(self, p, Temp):

        steam = IAPWS97(P=p, T=Temp)

        return steam.cp

    def alphaInterpolado(self, T):

        cCondutividadeTerm = interp1d(self.TemperaturaPropMec, self.condutividadeTerm)

        cCalorEspecificoPcte = interp1d(self.TemperaturaPropMec, self.calorEspecificoPcte)

        if T >= self.TemperaturaPropMec[-1]:
            condutividadeTerm = cCondutividadeTerm(self.TemperaturaPropMec[-1])
            calorEspecificoPcte = cCalorEspecificoPcte(self.TemperaturaPropMec[-1])

        elif T <= self.TemperaturaPropMec[0]:
            condutividadeTerm = cCondutividadeTerm(self.TemperaturaPropMec[0])
            calorEspecificoPcte = cCalorEspecificoPcte(self.TemperaturaPropMec[0])
        else:
            condutividadeTerm = cCondutividadeTerm(T)
            calorEspecificoPcte = cCalorEspecificoPcte(T)

        return float(condutividadeTerm / (self.rho * calorEspecificoPcte))

    def betaInterpolado(self, T):

        cCoefExpansaoTerm = interp1d(self.TemperaturaPropMec, self.coefExpansaoTerm)

        if T >= self.TemperaturaPropMec[-1]:
            coefExpansaoTerm = cCoefExpansaoTerm(self.TemperaturaPropMec[-1])

        elif T <= self.TemperaturaPropMec[0]:
            coefExpansaoTerm = cCoefExpansaoTerm(self.TemperaturaPropMec[0])

        else:
            coefExpansaoTerm = cCoefExpansaoTerm(T)


        return float(coefExpansaoTerm)

    def flag5(self):  ### FLAG = 5: final do processo de cálculo de média e identificação de dano por fluência OK!

        if self.saida2.item((0, 0)) >= 0 or self.saida2.item((1, 1)) >= 0:
            with open(self.arquivoControle, "w") as file:
                file.write('5\n5')

    # def getStartIndexTrans(self, lista, width, threshold1, threshold2):
    #
    #     for i in range(len(lista) - width):
    #         pos = i
    #         if lista[i] > threshold1 and abs(float(lista[i + width - 1] - lista[i])) > threshold2:
    #             break
    #
    #         if pos == (len(lista) - width - 1):
    #             pos = -1
    #
    #     if pos != -1:
    #         return pos
    #     else:
    #         return pos

    def getStartIndexTrans(self, lista, width, threshold1, threshold2):

        for i in range(len(lista) - width):

            var1 = lista[i]
            var2 = i
            var3 = i+width-1
            var4 = lista[i+width-1]
            var5 = abs(float(lista[i + width - 1] - lista[i]))

            if lista[i] > threshold1 and abs(float(lista[i + width - 1] - lista[i])) > threshold2:
                break

        pos = i

        if pos == (len(lista) - width - 1):
            pos = -1

        return pos

    def getEndIndexTrans(self, lista, width, threshold3, threshold4, indiceInicioTransiente):

        tmp = len(lista) - width
        print (tmp)
        # for i in range(len(lista) - width):
        #     pos = i
        #     if lista[i] > threshold3 and abs(lista[i + width - 1] - lista[i]) < threshold4:
        #         # pos = 0 # sugestão do Bruno para compatibilizar com MathCad
        #         break
        #
        #     elif pos == (len(lista) - width - 1):
        #         pos = -1

        for i in range(int(indiceInicioTransiente), len(lista) - width):

            a = lista[i]
            b = lista[i + width - 1]
            dif = b - a

            if lista[i] > threshold3 and abs(lista[i + width - 1] - lista[i]) < threshold4:
                # pos = 0 # sugestão do Bruno para compatibilizar com MathCad
                break

        pos = i

        if pos == (len(lista) - width - 1):
            pos = -1

        if self.indiceInicioTransiente != -1:
            indiceFimTransiente = pos
        else:
            indiceFimTransiente = -1

        return indiceFimTransiente


    def setStartInstantTrans(self):

        if self.indiceInicioTransiente != -1:
            instanteInicioTransiente = self.tempo[self.indiceInicioTransiente]
        else:
            instanteInicioTransiente = self.tempo[0]

        return instanteInicioTransiente

    def setEndInstantTrans(self):

        if self.indiceFimTransiente != -1:
            instanteFimTransiente = self.tempo[self.indiceFimTransiente]
        else:
            instanteFimTransiente = self.tempo[-1]
        t = self.tempo[len(self.tempo) - 1]

        return instanteFimTransiente

    def setStartTempTrans(self, lista):

        if self.indiceInicioTransiente != -1:
            temperaturaInicioTransiente = lista[self.indiceInicioTransiente]
        else:
            temperaturaInicioTransiente = lista[0]

        return temperaturaInicioTransiente

    def setEndTempTrans(self, lista):

        if self.indiceFimTransiente != -1:
            temperaturaFimTransiente = lista[self.indiceFimTransiente]
        else:
            temperaturaFimTransiente = lista[-1]

        return temperaturaFimTransiente


    def filtro1(self, mecanismoDano, *args): # OBS: Todas as listas devem ter o mesmo comprimento, tratar esse erro dps!!!!!!!!!!!

        listaAuxTempo = []
        listaAuxVvapor = []
        listaAuxPvapor = []
        listaAuxTvapor = []
        listaAuxTmetal = []
        listaAuxPotencia = []
        listaAuxTmetalint = []
        listaAuxTmetalext = []

        if mecanismoDano == 'Fluencia':

            if len(args) == 5:

                for i in range(len(self.Tic)):
                    if i <= self.indiceInicioTransiente or i >= self.indiceFimTransiente:
                        listaAuxTempo.append(self.tempo[i])
                        listaAuxPvapor.append(self.pv[i])
                        listaAuxTvapor.append(self.Tv[i])
                        listaAuxTmetal.append(self.Tic[i])
                        listaAuxPotencia.append(self.Wturb[i])

                return (listaAuxTempo, listaAuxPvapor, listaAuxTvapor, listaAuxTmetal, listaAuxPotencia)

            elif len(args) == 4:

                for i in range(len(self.Tv)):
                    if i <= self.indiceInicioTransiente or i >= self.indiceFimTransiente:
                        listaAuxTempo.append(self.tempo[i])
                        listaAuxVvapor.append(self.Vv[i])
                        listaAuxPvapor.append(self.pv[i])
                        listaAuxTvapor.append(self.Tv[i])


                return (listaAuxTempo, listaAuxVvapor, listaAuxPvapor, listaAuxTvapor)

            elif len(args) == 6:

                for i in range(len(self.Tv)):
                    if i <= self.indiceInicioTransiente or i >= self.indiceFimTransiente:
                        listaAuxTempo.append(self.tempo[i])
                        listaAuxVvapor.append(self.Vv[i])
                        listaAuxPvapor.append(self.pv[i])
                        listaAuxTvapor.append(self.Tv[i])
                        listaAuxTmetalint.append(self.Tmint[i])
                        listaAuxTmetalext.append(self.Tmext[i])

                return (listaAuxTempo, listaAuxVvapor, listaAuxPvapor, listaAuxTvapor, listaAuxTmetalint, listaAuxTmetalext)

            else:
                return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Número de listas incompatível com o filtro aplicado!]")

        elif mecanismoDano == 'Fadiga':

            if len(args) == 5:

                for i in range(len(self.Tic)):
                    if i >= self.indiceInicioTransiente and i <= self.indiceFimTransiente:
                        listaAuxTempo.append(self.tempo[i])
                        listaAuxPvapor.append(self.pv[i])
                        listaAuxTvapor.append(self.Tv[i])
                        listaAuxTmetal.append(self.Tic[i])
                        listaAuxPotencia.append(self.Wturb[i])

                return (listaAuxTempo, listaAuxPvapor, listaAuxTvapor, listaAuxTmetal, listaAuxPotencia)

            elif len(args) == 4:

                if self.indiceFimTransiente == -1:
                    self.indiceFimTransiente = len(self.Tv) - 1


                for i in range(len(self.Tv)):
                    if i >= self.indiceInicioTransiente and i <= self.indiceFimTransiente:
                        listaAuxTempo.append(self.tempo[i])
                        listaAuxVvapor.append(self.Vv[i])
                        listaAuxPvapor.append(self.pv[i])
                        listaAuxTvapor.append(self.Tv[i])


                return (listaAuxTempo, listaAuxVvapor, listaAuxPvapor, listaAuxTvapor)

            elif len(args) == 6:

                if self.indiceFimTransiente == -1:
                    self.indiceFimTransiente = len(self.Tv) - 1

                for i in range(len(self.Tv)):
                    if i >= self.indiceInicioTransiente and i <= self.indiceFimTransiente:
                        listaAuxTempo.append(self.tempo[i])
                        listaAuxVvapor.append(self.Vv[i])
                        listaAuxPvapor.append(self.pv[i])
                        listaAuxTvapor.append(self.Tv[i])
                        listaAuxTmetalint.append(self.Tmint[i])
                        listaAuxTmetalext.append(self.Tmext[i])

                return (listaAuxTempo, listaAuxVvapor, listaAuxPvapor, listaAuxTvapor, listaAuxTmetalint, listaAuxTmetalext)

            else:
                return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Número de listas incompatível com o filtro aplicado!]")

        else:
            return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Digite o mecanismo de dano: Fluencia ou Fadiga!]")



    def filtro2(self, mecanismoDano, *args):  # OBS: Todas as listas devem ter o mesmo comprimento, tratar esse erro dps!!!!!!!!!!!

        listaAuxTempo = []
        listaAuxVvapor = []
        listaAuxPvapor = []
        listaAuxTvapor = []
        listaAuxTvapor
        listaAuxTmetal = []
        listaAuxPotencia = []
        listaAuxTmetalint = []
        listaAuxTmetalext = []



        if mecanismoDano == 'Fluencia':

            if len(args) == 5:

                for i in range(len(self.TmetalFiltro1)):
                    if self.TmetalFiltro1[i] >= self.limiteInfFiltro2Rotor and self.TmetalFiltro1[
                        i] <= self.limiteSupFiltro2rotor:
                        listaAuxTempo.append(self.tempoFiltro1[i])
                        listaAuxPvapor.append(self.PvaporFiltro1[i])
                        listaAuxTvapor.append(self.TvaporFiltro1[i])
                        listaAuxTmetal.append(self.TmetalFiltro1[i])
                        listaAuxPotencia.append(self.PotenciaFiltro1[i])

                contTvapor = 0
                contPvapor = 0

                for i in range(len(listaAuxTvapor)):
                    if listaAuxTvapor[i] >= 550.0:
                        listaAuxTvapor[i] = 550.0
                        contTvapor = contTvapor + 1

                for i in range(len(listaAuxPvapor)):
                    if listaAuxPvapor[i] >= 150.0:
                        listaAuxPvapor[i] = 150.0
                        contPvapor = contPvapor + 1

                if contTvapor > 0:
                    print '***********************************************************' + '\n' + 'WARNING: A temperatura do vapor registrada na região do rotor excedeu os limites de operação!' + '\n' + '***********************************************************'

                if contPvapor > 0:
                    print '***********************************************************' + '\n' + 'WARNING: A pressão do vapor registrada na região do rotor excedeu os limites de operação!' + '\n' + '***********************************************************'



                return (listaAuxTempo, listaAuxPvapor, listaAuxTvapor, listaAuxTmetal, listaAuxPotencia)

            elif len(args) == 4:

                for i in range(len(self.TvaporFiltro1)):
                    if self.TvaporFiltro1[i] >= self.limiteInfFiltro2 and self.TvaporFiltro1[
                        i] <= self.limiteSupFiltro2tubulacao:
                        listaAuxTempo.append(self.tempoFiltro1[i])
                        listaAuxVvapor.append(self.VvaporFiltro1[i])
                        listaAuxPvapor.append(self.PvaporFiltro1[i])
                        listaAuxTvapor.append(self.TvaporFiltro1[i])

                contTvapor = 0
                contVvapor = 0
                contPvapor = 0

                for i in range(len(listaAuxTvapor)):
                    if listaAuxTvapor[i] >= 550.0:
                        listaAuxTvapor[i] = 550.0
                        contTvapor = contTvapor + 1

                if contTvapor > 0:
                    print '***********************************************************' + '\n' + 'WARNING: A temperatura do vapor registrada na região da tubulação da carcaça externa de alta pressão excedeu os limites de operação!' + '\n' + '***********************************************************'


                for i in range(len(listaAuxVvapor)):
                    if listaAuxVvapor[i] >= 550.0:
                        listaAuxVvapor[i] = 550.0
                        contVvapor = contVvapor + 1

                if contVvapor > 0:
                    print '***********************************************************' + '\n' + 'WARNING: A vazão do vapor registrada na região da tubulação da carcaça externa de alta pressão excedeu os limites de operação!' + '\n' + '***********************************************************'

                for i in range(len(listaAuxPvapor)):
                    if listaAuxPvapor[i] >= 200.0:
                        listaAuxPvapor[i] = 200.0
                        contPvapor = contPvapor + 1

                if contPvapor > 0:
                    print '***********************************************************' + '\n' + 'WARNING: A pressão do vapor registrada na região da tubulação da carcaça externa de alta pressão excedeu os limites de operação!' + '\n' + '***********************************************************'


                return (listaAuxTempo, listaAuxVvapor, listaAuxPvapor, listaAuxTvapor)

            elif len(args) == 6:

                for i in range(len(self.TvaporFiltro1)):
                    if self.TvaporFiltro1[i] >= self.limiteInfFiltro2 and self.TvaporFiltro1[
                        i] <= self.limiteSupFiltro2tubulacao:
                        listaAuxTempo.append(self.tempoFiltro1[i])
                        listaAuxVvapor.append(self.VvaporFiltro1[i])
                        listaAuxPvapor.append(self.PvaporFiltro1[i])
                        listaAuxTvapor.append(self.TvaporFiltro1[i])
                        listaAuxTmetalint.append(self.TmetalintFiltro1[i])
                        listaAuxTmetalext.append(self.TmetalextFiltro1[i])

                contTvapor = 0
                contVvapor = 0
                contPvapor = 0

                for i in range(len(listaAuxTvapor)):
                    if listaAuxTvapor[i] >= 550.0:
                        listaAuxTvapor[i] = 550.0
                        contTvapor = contTvapor + 1

                if contTvapor > 0:
                    print '***********************************************************' + '\n' + 'WARNING: A temperatura do vapor registrada na região da válvula de bloqueio 2 excedeu os limites de operação!' + '\n' + '***********************************************************'


                for i in range(len(listaAuxVvapor)):
                    if listaAuxVvapor[i] >= 550.0:
                        listaAuxVvapor[i] = 550.0
                        contVvapor = contVvapor + 1

                if contVvapor > 0:
                    print '***********************************************************' + '\n' + 'WARNING: A vazão do vapor registrada na região da válvula de bloqueio 2 excedeu os limites de operação!' + '\n' + '***********************************************************'

                for i in range(len(listaAuxPvapor)):
                    if listaAuxPvapor[i] >= 200.0:
                        listaAuxPvapor[i] = 200.0
                        contPvapor = contPvapor + 1

                if contPvapor > 0:
                    print '***********************************************************' + '\n' + 'WARNING: A pressão do vapor registrada na região da válvula de bloqueio 2 excedeu os limites de operação!' + '\n' + '***********************************************************'


                return (
                listaAuxTempo, listaAuxVvapor, listaAuxPvapor, listaAuxTvapor, listaAuxTmetalint, listaAuxTmetalext)

            else:
                return EH.ErrorHandle.handler(
                    "ERROR: [Ocorreu o erro : Número de listas incompatível com o filtro aplicado!]")

        elif mecanismoDano == 'Fadiga':

            if len(args) == 5:

                for i in range(len(self.TmetalFiltro1)):
                    if self.TmetalFiltro1[i] >= 175.0 and self.TmetalFiltro1[
                        i] <= 650.0:
                        listaAuxTempo.append(self.tempoFiltro1[i])
                        listaAuxPvapor.append(self.PvaporFiltro1[i])
                        listaAuxTvapor.append(self.TvaporFiltro1[i])
                        listaAuxTmetal.append(self.TmetalFiltro1[i])
                        listaAuxPotencia.append(self.PotenciaFiltro1[i])

                contTvapor = 0
                contVvapor = 0
                contPvapor = 0

                for i in range(len(listaAuxTvapor)):
                    if listaAuxTvapor[i] >= 550.0:
                        listaAuxTvapor[i] = 550.0
                        contTvapor = contTvapor + 1

                if contTvapor > 0:
                    print '***********************************************************' + '\n' + 'WARNING: A temperatura do vapor registrada na região do primeiro estágio do rotor alta pressão excedeu os limites de operação!' + '\n' + '***********************************************************'

                for i in range(len(listaAuxVvapor)):
                    if listaAuxVvapor[i] >= 550.0:
                        listaAuxVvapor[i] = 550.0
                        contVvapor = contVvapor + 1

                if contVvapor > 0:
                    print '***********************************************************' + '\n' + 'WARNING: A vazão do vapor registrada na região do primeiro estágio do rotor alta pressão excedeu os limites de operação!' + '\n' + '***********************************************************'

                for i in range(len(listaAuxPvapor)):
                    if listaAuxPvapor[i] >= 150.0:
                        listaAuxPvapor[i] = 150.0
                        contPvapor = contPvapor + 1

                if contPvapor > 0:
                    print '***********************************************************' + '\n' + 'WARNING: A pressão do vapor registrada na região do primeiro estágio do rotor alta pressão excedeu os limites de operação!' + '\n' + '***********************************************************'


                return (listaAuxTempo, listaAuxPvapor, listaAuxTvapor, listaAuxTmetal, listaAuxPotencia)

            elif len(args) == 4:

                for i in range(len(self.TvaporFiltro1)):
                    if self.TvaporFiltro1[i] >= 175.0 and self.TvaporFiltro1[
                        i] <= 650.0:
                        listaAuxTempo.append(self.tempoFiltro1[i])
                        listaAuxVvapor.append(self.VvaporFiltro1[i])
                        listaAuxPvapor.append(self.PvaporFiltro1[i])
                        listaAuxTvapor.append(self.TvaporFiltro1[i])

                contTvapor = 0
                contVvapor = 0
                contPvapor = 0

                for i in range (len(listaAuxTvapor)):
                    if listaAuxTvapor[i] >= 550.0:
                        listaAuxTvapor[i] = 550.0
                        contTvapor = contTvapor + 1

                if contTvapor > 0:
                    print '***********************************************************' + '\n' + 'WARNING: A temperatura do vapor registrada na região da tubulação da carcaça externa de alta pressão excedeu os limites de operação!' + '\n' + '***********************************************************'


                for i in range (len(listaAuxVvapor)):
                    if listaAuxVvapor[i] >= 550.0:
                        listaAuxVvapor[i] = 550.0
                        contVvapor = contVvapor + 1

                if contVvapor > 0:
                    print '***********************************************************' + '\n' + 'WARNING: A vazão do vapor registrada na região da tubulação da carcaça externa de alta pressão excedeu os limites de operação!' + '\n' + '***********************************************************'


                for i in range(len(listaAuxPvapor)):
                    if listaAuxPvapor[i] >= 200.0:
                        listaAuxPvapor[i] = 200.0
                        contPvapor = contPvapor + 1

                if contPvapor > 0:
                    print '***********************************************************' + '\n' + 'WARNING: A pressão do vapor registrada na região da tubulação da carcaça externa de alta pressão excedeu os limites de operação!' + '\n' + '***********************************************************'



                return (listaAuxTempo, listaAuxVvapor, listaAuxPvapor, listaAuxTvapor)

            elif len(args) == 6:

                for i in range(len(self.TvaporFiltro1)):
                    if self.TvaporFiltro1[i] >= 175.0 and self.TvaporFiltro1[
                        i] <= 650.0:
                        listaAuxTempo.append(self.tempoFiltro1[i])
                        listaAuxVvapor.append(self.VvaporFiltro1[i])
                        listaAuxPvapor.append(self.PvaporFiltro1[i])
                        listaAuxTvapor.append(self.TvaporFiltro1[i])
                        listaAuxTmetalint.append(self.TmetalintFiltro1[i])
                        listaAuxTmetalext.append(self.TmetalextFiltro1[i])

                contTvapor = 0
                contVvapor = 0
                contPvapor = 0

                for i in range(len(listaAuxTvapor)):
                    if listaAuxTvapor[i] >= 550.0:
                        listaAuxTvapor[i] = 550.0
                        contTvapor = contTvapor + 1

                if contTvapor > 0:
                    print '***********************************************************' + '\n' + 'WARNING: A temperatura do vapor registrada na região da válvula de bloqueio 2 excedeu os limites de operação!' + '\n' + '***********************************************************'

                for i in range(len(listaAuxVvapor)):
                    if listaAuxVvapor[i] >= 550.0:
                        listaAuxVvapor[i] = 550.0
                        contVvapor = contVvapor + 1

                if contVvapor > 0:
                    print '***********************************************************' + '\n' + 'WARNING: A vazão do vapor registrada na região da válvula de bloqueio 2 excedeu os limites de operação!' + '\n' + '***********************************************************'

                for i in range(len(listaAuxPvapor)):
                    if listaAuxPvapor[i] >= 200.0:
                        listaAuxPvapor[i] = 200.0
                        contPvapor = contPvapor + 1

                if contPvapor > 0:
                    print '***********************************************************' + '\n' + 'WARNING: A pressão do vapor registrada na região da válvula de bloqueio 2 excedeu os limites de operação!' + '\n' + '***********************************************************'



                return (
                listaAuxTempo, listaAuxVvapor, listaAuxPvapor, listaAuxTvapor, listaAuxTmetalint, listaAuxTmetalext)

            else:
                return EH.ErrorHandle.handler(
                    "ERROR: [Ocorreu o erro : Número de listas incompatível com o filtro aplicado!]")

        else:
            return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Digite o mecanismo de dano: Fluencia ou Fadiga!]")





    def flag1(self):  # aplicação do filtro aos dados de entrada OK!

        if len(self.TvaporFiltro2) > 0:
            with open(self.arquivoControle, "w") as file:
                file.write('1\n5')
        else:
            with open(self.arquivoControle, "w") as file:
                file.write('5\n5')


    def block(self, mecanismoDano, Equipamento):

        if mecanismoDano == 'Fluencia':

            if Equipamento == 'Rotor':

                if self.PvaporSM <= 80 or self.PWmediaSM < 100:
                    self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 2 0 0; 3 0 0')
                    return
                else:
                    self.saida2 = np.matrix('0')
                    return

            elif Equipamento == 'Tubulacao':

                if self.PvaporSM <= 80 or self.VvaporSM < 100:
                    self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 2 0 0; 3 0 0')
                    return
                else:
                    self.saida2 = np.matrix('0')
                    return

            elif Equipamento == 'Valvula':

                if self.PvaporSM <= 80 or self.VvaporSM < 100:
                    self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 2 0 0; 3 0 0')
                    return
                else:
                    self.saida2 = np.matrix('0')
                    return

            else:
                return EH.ErrorHandle.handler(
                    "ERROR: [Ocorreu o erro : Equipamento inexistente! Digite o tipo de equipamento: Rotor, Tubulacao ou Valvula]")

        elif mecanismoDano == 'Fadiga':

            if Equipamento == 'Rotor':

                if self.PvaporSM <= 80 or self.PWmediaSM < 100:
                    self.saida2 = np.matrix('40 0 0; 0 20 30; 4 0 0; 5 0 0')
                    return
                else:
                    self.saida2 = np.matrix('0')
                    return

            elif Equipamento == 'Tubulacao':

                if self.PvaporSM <= 80 or self.VvaporSM < 100:
                    self.saida2 = np.matrix('40 0 0; 0 20 30; 4 0 0; 5 0 0')
                    return
                else:
                    self.saida2 = np.matrix('0')
                    return

            elif Equipamento == 'Valvula':

                if self.PvaporSM <= 80 or self.VvaporSM < 100:
                    self.saida2 = np.matrix('40 0 0; 0 20 30; 4 0 0; 5 0 0')
                    return
                else:
                    self.saida2 = np.matrix('0')
                    return

            else:
                return EH.ErrorHandle.handler(
                    "ERROR: [Ocorreu o erro : Equipamento inexistente! Digite o tipo de equipamento: Rotor, Tubulacao ou Valvula]")

        else:
            return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Digite o mecanismo de dano: Fluencia ou Fadiga!]")


    def firstBlock(self, mecanismoDano, Equipamento, geometria = 'normal'):

        if mecanismoDano == 'Fluencia':

            retCode = 1

            if Equipamento == 'Rotor':

                if max(self.Tv) < 200 or max(self.pv) < 60:

                    self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 2 0 0; 3 0 0')

                    strOut = str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                        self.saida2.item((0, 2))) + '\n' + str(self.saida2.item((1, 0))) + '\t' + str(
                        self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                        self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                        self.saida2.item((2, 2))) + '\n' + '' + str(self.saida2.item((3, 0))) + '\t' + str(
                        self.saida2.item((3, 1))) + '\t' + str(self.saida2.item((3, 2))) + '\n' + '' + str(
                        self.saida2.item((4, 0))) + '\t' + str(self.saida2.item((4, 1))) + '\t' + str(
                        self.saida2.item((4, 2)))

                    MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR][geometria]['Fluencia'] = strOut

                    return 1



                else:
                    self.saida2 = np.matrix('0')
                    return 0

            elif Equipamento == 'Tubulacao':

                if geometria == 'Reta':

                    if max(self.Tv) < 200 or max(self.pv) < 80:

                        self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')

                        strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
                            self.saida2.item((0, 1))) + '\t' + str(
                            self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                            self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                            self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                            self.saida2.item((2, 2))) + '\n' + '' + str(
                            self.saida2.item((3, 0))) + '\t' + str(self.saida2.item((3, 1))) + '\t' + str(
                            self.saida2.item((3, 2)))

                        MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO][geometria]['Fluencia'] = strOut

                        return 1


                    else:

                        self.saida2 = np.matrix('0')
                        return 0

                if geometria == 'Curva':

                    if max(self.Tv) < 200 or max(self.pv) < 80:

                        self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')

                        strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
                            self.saida2.item((0, 1))) + '\t' + str(
                            self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                            self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                            self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                            self.saida2.item((2, 2))) + '\n' + '' + str(
                            self.saida2.item((3, 0))) + '\t' + str(self.saida2.item((3, 1))) + '\t' + str(
                            self.saida2.item((3, 2)))

                        MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO][geometria]['Fluencia'] = strOut

                        return 1


                    else:

                        self.saida2 = np.matrix('0')
                        return 0



            elif Equipamento == 'Valvula':

                if geometria == 'Reta':

                    if max(self.Tv) < 200 or max(self.pv) < 80:

                        self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')

                        strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
                            self.saida2.item((0, 1))) + '\t' + str(
                            self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                            self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                            self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                            self.saida2.item((2, 2))) + '\n' + '' + str(
                            self.saida2.item((3, 0))) + '\t' + str(self.saida2.item((3, 1))) + '\t' + str(
                            self.saida2.item((3, 2)))

                        MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA][geometria]['Fluencia'] = strOut

                        return 1


                    else:

                        self.saida2 = np.matrix('0')
                        return 0

                if geometria == 'Curva':

                    if max(self.Tv) < 200 or max(self.pv) < 80:

                        self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')

                        strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
                            self.saida2.item((0, 1))) + '\t' + str(
                            self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                            self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                            self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                            self.saida2.item((2, 2))) + '\n' + '' + str(
                            self.saida2.item((3, 0))) + '\t' + str(self.saida2.item((3, 1))) + '\t' + str(
                            self.saida2.item((3, 2)))

                        MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA][geometria]['Fluencia'] = strOut

                        return 1


                    else:

                        self.saida2 = np.matrix('0')
                        return 0

            else:
                return EH.ErrorHandle.handler(
                    "ERROR: [Ocorreu o erro : Equipamento inexistente! Digite o tipo de equipamento: Rotor, Tubulacao ou Valvula]")

        elif mecanismoDano == 'Fadiga':

            retCode = 2

            if Equipamento == 'Rotor':

                if (max(self.Tv) < 200 or max(self.pv) < 60):

                    self.saida2 = np.matrix('40 0 0; 0 20 30; 4 0 0; 5 0 0')

                    strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                        self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                        self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                        self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
                        self.saida2.item((2, 2))) + '\n' + '' + str(self.saida2.item((3, 0))) + '\t' + str(
                        self.saida2.item((3, 1))) + '\t' + str(self.saida2.item((3, 2)))

                    MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR][geometria]['Fadiga'] = strOut

                    return 2



                else:

                    self.saida2 = np.matrix('0')
                    return 0

            elif Equipamento == 'Tubulacao':

                if geometria == 'Reta':


                    if max(self.Tv) < 200 or max(self.pv) < 80:

                        self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')

                        strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                            self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                            self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                            self.saida2.item((2, 0))) + '\t' + str(
                            self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2)))

                        MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO][geometria]['Fadiga'] = strOut

                        return 2



                    else:

                        self.saida2 = np.matrix('0')
                        return 0

                if geometria == 'Curva':


                    if (max(self.Tv) < 200 or max(self.pv) < 80):
                        self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')

                        strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                            self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                            self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                            self.saida2.item((2, 0))) + '\t' + str(
                            self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2)))

                        MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO][geometria]['Fadiga'] = strOut

                        return 2



                    else:

                        self.saida2 = np.matrix('0')
                        return 0

            elif Equipamento == 'Valvula':

                if geometria == 'Reta':

                    if (max(self.Tv) < 200 or max(self.pv) < 80):

                        self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')

                        strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                        self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                        self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                        self.saida2.item((2, 0))) + '\t' + str(
                        self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2)))

                        MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA][geometria]['Fadiga'] = strOut

                        return 2



                    else:

                        self.saida2 = np.matrix('0')
                        return 0

                if geometria == 'Curva':

                    if max(self.Tv) < 200 or max(self.pv) < 80:

                        self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')

                        strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
                        self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
                        self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
                        self.saida2.item((2, 0))) + '\t' + str(
                        self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2)))

                        MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA][geometria]['Fadiga'] = strOut

                        return 2



                    else:

                        self.saida2 = np.matrix('0')
                        return 0




    def redefParams(self, *args):

        if len(args) == 4:

            PWmedia = self.PWmediaSM
            Pmediavapor = self.PvaporSM
            Tmediavapor = self.TvaporSM + 273.15  ### Conversão ºC para K
            Tmediacext = self.TmediacextSM + 273.15  ### Conversão ºC para K

            return (Pmediavapor, Tmediavapor, Tmediacext, PWmedia)

        elif len(args) == 3:

            Pmediavapor = self.PvaporSM
            Tmediavapor = self.TvaporSM + 273.15  ### Conversão ºC para K
            Vmediavapor = self.VvaporSM  ### Conversão ºC para K

            return (Pmediavapor, Tmediavapor, Vmediavapor)

        elif len(args) == 5:

            Pmediavapor = self.PvaporSM
            Tmediavapor = self.TvaporSM + 273.15  ### Conversão ºC para K
            Vmediavapor = self.VvaporSM  ### Conversão ºC para K
            Tmediacint = self.TmetalintSM + 273.15
            Tmediacext = self.TmetalextSM + 273.15

            return (Pmediavapor, Tmediavapor, Vmediavapor, Tmediacint, Tmediacext)

        else:

            return 'Numero de argumentos incompativel com a funcao'



    def putDanoFromLocalFile(self, seg = 486, valor = -1.0):
        with open(self.currentDir + "dano_" + str(seg) + ".txt", "r") as danoFile:
            data = danoFile.readlines()
            var1 = float(data[-1].replace('\n', ''))
            var2 = float(valor)
            var3 = var1 + var2

        with open(self.currentDir + "dano_" + str(seg) + ".txt", "a") as danoFile:
            danoFile.write(str(var3) + '\n')

    def putTempoAvaliacaoFromLocalFile(self, seg = 486, valor = -1.0):

        with open(self.currentDir + "tempoAvaliacao_" + str(seg) + ".txt", "r") as tempoAvaliacaoFile:
            data = tempoAvaliacaoFile.readlines()
            var1 = float(data[-1].replace('\n', ''))
            var2 = float(valor)
            var3 = var1 + var2

        with open(self.currentDir + "tempoAvaliacao_" + str(seg) + ".txt", "a") as tempoAvaliacaoFile:
            tempoAvaliacaoFile.write(str(var3) + '\n')

    def putNumeroCiclosFromLocalFile(self, seg = 486, valor = -1.0):

        with open(self.currentDir + "numeroCiclos_" + str(seg) + ".txt", "r") as numeroCiclosFile:
            data = numeroCiclosFile.readlines()
            var1 = float(data[-1].replace('\n', ''))
            var2 = float(valor)
            var3 = var1 + var2

        with open(self.currentDir + "numeroCiclos_" + str(seg) + ".txt", "a") as numeroCiclosFile:
            numeroCiclosFile.write(str(var3) + '\n')

    def getDanoFromLocalFile(self, seg = 486): # OBS!!! -> Preciso extrair a soma dos valores dos danos ou criar um metodo que some
        with open(self.currentDir + "dano_" + str(seg) + ".txt", "r") as danoFile:
            data = danoFile.readlines()
            for i in range(len(data)):
                data[i] = float(data[i].replace('\n', ''))
        return data

    def getTempoAvalicaoFromLocalFile(self, seg = 486): # OBS!!! -> Preciso extrair a soma dos valores dos tempos de avaliacao ou criar um metodo que some
        with open(self.currentDir + "tempoAvaliacao_" + str(seg) + ".txt", "r") as tempoAvaliacaoFile:
            data = tempoAvaliacaoFile.readlines()
            tempoOp = float(data[-1].replace('\n', ''))
            for i in range(len(data)):
                data[i] = float(data[i].replace('\n', ''))
        return data, tempoOp

    def getNumeroCiclosFromLocalFile(self, seg = 486): # OBS!!! -> Preciso extrair a soma dos valores dos tempos de avaliacao ou criar um metodo que some
        with open(self.currentDir + "numeroCiclos_" + str(seg) + ".txt", "r") as numeroCiclosFile:
            data = numeroCiclosFile.readlines()
            NC = float(data[-1].replace('\n', ''))
            for i in range(len(data)):
                data[i] = float(data[i].replace('\n', ''))
        return data, NC



    ####### Funções necessárias para a regressão linear da vida remanescente ########


    ## OBS!!! -> Criar as variáveis no construtor para cada método caso seja necessário



    def mean(self, values):
        return sum(values) / float(len(values))

    def variance(self, values, mean):
        return sum([(x - mean) ** 2 for x in values])

    def covariance(self, x, mean_x, y, mean_y):
        covar = 0.0
        for i in range(len(x)):
            covar += (x[i] - mean_x) * (y[i] - mean_y)
        return covar

    def coefficients(self, x_mean, y_mean, x_variance, covariance): #

        b1 = covariance / x_variance
        b0 = y_mean - b1 * x_mean
        return [b0, b1]

    def simple_linear_regression(self, coefficients): # Modificar essa função para atender o critério de 90% de dano

        b = coefficients[0]
        a = coefficients[1]

        tempoOperacaoDano90 = (90 - b) / a

        return tempoOperacaoDano90




    @staticmethod
    def getFatigueFromSoma(seg = 486, initTime=1363046400000):
        # http://10.0.2.140:1443/mxml/rlife&op=getFatigue&seg=486&initTime=1363046400000
        host = '10.0.2.140'
        r = requests.post("http://" + host + ":1443/mxml/rlife", data={'op': 'getFatigue', 'seg': seg, 'initTime': initTime})
        size = len(r.text)
        print("\n\nStatus Code do HTTP no getFatigueFromSoma")
        print(str(r.status_code) + " - " + str(r.reason) + " qtq de bytes = " + str(size))
        return r

