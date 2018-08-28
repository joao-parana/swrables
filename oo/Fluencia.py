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

class Fluencia(MecanismoDano):
    def __init__(self, currentDir, fileName):  # currentDir deve terminar com '\'
        MecanismoDano.__init__(self, currentDir, fileName)

        #if (EH.ErrorHandle.getPlataform() == 'Windows'):
            #currentDirAux = 'C:\\SOMATURBODIAG\\rotor\\'
            #currentDir = os.getcwd() + '/../DATA/rotor/'
            #if platform.system() == "Windows":
            #    currentDir = '..\\rotor\\'

            #self.currentDir = currentDirAux
        #else:

        """
        # self.FILE_SEPARATOR = '/'
        # if platform.system() == "Windows":
        #    self.FILE_SEPARATOR = '\\'
        """







    def getFromSoma(self, op, seg, initTime=1363046400000, host="localhost"):

        r = requests.post("http://" + host + ":1443/mxml/rlife", data={'op': op, 'seg': seg, 'initTime': initTime})

        return r




    def calcMediaParams(self, lista, limInfMedia):


        Npontos = 0
        vaux = 0

        for i in range(len(lista)):
            if lista[i] > limInfMedia:
                Npontos = Npontos + 1
                vaux = vaux + lista[i]

        if Npontos == 0:
            return Npontos

        else:
            return round((vaux / float(Npontos)), 4)


    def Paramslist2arrayMG(self, Equipamento):

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
        self.inputPMG = np.asarray(self.inputPMG)
        self.PMG = np.asarray(self.PMG)

        if Equipamento == 'Tubulacao':

            self.tensaoPLMtub = np.asarray(self.tensaoPLMtub)
            self.PLMtub = np.asarray(self.PLMtub)

        elif Equipamento == 'Valvula':

            self.tensaoPLMvalv = np.asarray(self.tensaoPLMvalv)
            self.PLMvalv = np.asarray(self.PLMvalv)

        else:
            return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Equipamento inexistente! Digite o tipo de equipamento: Rotor, Tubulacao ou Valvula]")




    def Einterpolado(self, T):

        cModuloElasticidade = interp1d(self.TemperaturaPropMec, self.moduloElasticidade)


        if T >= self.TemperaturaPropMec[-1]:
            moduloElasticidade = cModuloElasticidade(self.TemperaturaPropMec[-1])

        elif T <= self.TemperaturaPropMec[0]:
            moduloElasticidade = cModuloElasticidade(self.TemperaturaPropMec[0])

        else:
            moduloElasticidade = cModuloElasticidade(T)

        return float(moduloElasticidade)






    def cPinterpolado(self, T):

        cCalorEspecificoPcte = interp1d(self.TemperaturaPropMec, self.calorEspecificoPcte)

        if T >= self.TemperaturaPropMec[-1]:
            cP = cCalorEspecificoPcte(self.TemperaturaPropMec[-1])

        elif T <= self.TemperaturaPropMec[0]:
            cP = cCalorEspecificoPcte(self.TemperaturaPropMec[0])

        else:
            cP = cCalorEspecificoPcte(T)

        return cP

    def niInterpolado(self, T):

        cCoeficientePoisson = interp1d(self.TemperaturaCoefPoisson, self.CoefPoisson)

        if T >= self.TemperaturaCoefPoisson[-1]:
            ni = cCoeficientePoisson(self.TemperaturaCoefPoisson[-1])

        elif T <= self.TemperaturaCoefPoisson[0]:
            ni = cCoeficientePoisson(self.TemperaturaCoefPoisson[0])

        else:
            ni = cCoeficientePoisson(T)

        return ni



    ### OBS: Nesse ponto do código, tem-se como objetivo extrapolar as curvas de parâmetro de Larson-Miller e de Manson-Haferd para se obter valores desses parâmetros que estão abaixo do nível de tensão mínimo típico encontrado nessas curvas.
    ###      Para isso, tomou-se a derivada no ponto de tensão mínimo obtendo-se, assim, os coeficientes angulares das retas utilizadas para a extrapolação m_ELM e m_EMH respectivamente. Essa metodologia de obtenção dos ditos coeficiente foi implementada e obtida no Mathcad devido a maior simplicidade com a operação de diferenciação.
    ###      Os coeficientes lineares beta_ELM e beta_EMH foram obtidos facilmente a partir do conhecimento das coordenadas (sigma_ELM, PLM_E) e (s

    def PLMcor(self, sigma, tensaoPLM, PLM):

        self.sigmaELM = tensaoPLM[0]
        self.PLM_E = PLM[0]
        self.mELM = -15.26637  # [1/MPa]
        self.betaELM = self.PLM_E - self.mELM * self.sigmaELM
        PLMAux = []

        for i in range(len(PLM)):

            PLMAux.append(PLM[i]*1000.)

        cPLM = interp1d(tensaoPLM, PLMAux)

        if sigma >= tensaoPLM[-1]:

            return cPLM(tensaoPLM[-1])

        elif sigma <= tensaoPLM[0]:

            return self.mELM * sigma + self.betaELM

        else:
            return cPLM(sigma)

    def PMHcor(self, sigma):

        self.sigmaEMH = self.tensaoPMH[0]
        self.PMH_E = self.PMH[0]
        self.mEMH = -2.20924 * (10 ** -5)  # [1/MPa]
        self.betaEMH = self.PMH_E - self.mEMH * self.sigmaEMH
        PMHAux = []

        for i in range(len(self.PMH)):
            PMHAux.append(self.PMH[i] / 100.)

        cPMH = interp1d(self.tensaoPMH, PMHAux)

        if sigma >= self.tensaoPMH[-1]:

            return cPMH(self.tensaoPMH[-1])

        elif sigma <= self.tensaoPMH[0]:

            return (self.mEMH * sigma + self.betaEMH)/100.

        else:
            return cPMH(sigma)



    def flag3(self):  # leitura das propriedades dos materiais OK!

        if self.saida2.item(0) == 0:

            with open(self.arquivoControle, "w") as file:
                file.write('3\n5')
        else:

            with open(self.arquivoControle, "w") as file:
                file.write('5\n5')




    def getTempoAvaliacao(self):

        return (len(self.tempoFiltro2) * 5 / 60.)





















    def tensaoRadialRotor(self, r):

        return (self.bar2Pa(self.PmediaVapor)) / ((r / self.r1Rotor) ** 2) * (
            ((self.r2Rotor ** 2 / self.r1Rotor ** 2) - (r ** 2 / self.r1Rotor ** 2)) / (
            (self.r2Rotor ** 2 / self.r1Rotor ** 2) - 1)) - (
                   self.bar2Pa(self.PmediaVapor)) + self.rho * (self.r2Rotor ** 2) * (self.omegazao ** 2) * (1 / 8.) * (
        (3 - 2 * self.ni) / (1 - self.ni)) * (
             1 - (r ** 2) / (self.r2Rotor ** 2)) * (1 - self.r1Rotor ** 2 / r ** 2) + (
                  -self.beta * self.E * self.deltaT / 2 * (
                  1 - self.ni)) * (
                      (
                      log(
                          self.r2Rotor / r) / log(
                          self.r2Rotor / self.r1Rotor)) - (
                      (
                      self.r2Rotor / r) ** 2 - 1) / (
                          (
                          self.r2Rotor / self.r1Rotor) ** 2 - 1))

    def tensaoTangencialRotor(self, r):

        return (-self.bar2Pa(self.PmediaVapor) / (r / self.r1Rotor) ** 2) * (
        (((self.r2Rotor ** 2) / (self.r1Rotor ** 2)) + ((r ** 2) / (self.r1Rotor ** 2))) / (
        (self.r2Rotor ** 2) / (self.r1Rotor ** 2) - 1)) - self.bar2Pa(self.PmediaVapor) + self.rho * (self.r2Rotor ** 2) * (self.omegazao ** 2) * (
        (1 / 8.) * ((3 - 2 * self.ni) / (1 - self.ni)) * (
        1 + ((self.r1Rotor ** 2) / (self.r2Rotor ** 2)) + ((self.r1Rotor ** 2) / (r ** 2))) - (
        (1 / 8.) * ((1 + 2 * self.ni) / (1 - self.ni)) * ((r ** 2) / (self.r2Rotor ** 2)))) + (-self.beta * self.E * self.deltaT / (
        2 * (1 - self.ni))) * (((log(self.r2Rotor / r) - 1) / log(self.r2Rotor / self.r1Rotor)) + (
        ((self.r2Rotor / r) ** 2 + 1) / ((self.r2Rotor / self.r1Rotor) ** 2 - 1)))

    def tensaoAxialRotor(self, r):

        integrand = lambda r: (self.ni * (self.tensaoTangencialRotor(r) - self.tensaoRadialRotor(r)) - self.beta * self.E * self.deltaT) * r
        I, err = quad(integrand, self.r1Rotor, self.r2Rotor)

        return (-self.bar2Pa(self.PmediaVapor) / (self.r2Rotor ** 2 / self.r1Rotor ** 2 - 1)) + self.ni * (
        self.tensaoRadialRotor(r) + self.tensaoTangencialRotor(r)) - self.beta * self.E * self.deltaT + (-2 / (self.r2Rotor ** 2 - self.r1Rotor ** 2)) * I

    def tensaoEquivalenteRotor(self, r):

        return (1 / 2 ** .5) * ((self.tensaoRadialRotor(r) - self.tensaoTangencialRotor(r)) ** 2 + (
        self.tensaoRadialRotor(r) - self.tensaoAxialRotor(r)) ** 2 + (self.tensaoTangencialRotor(r) - self.tensaoAxialRotor(r)) ** 2) ** .5

    def getPLM(self, tensaoEquivalente, tensaoPLM, PLM):

        self.sigmaELM = tensaoPLM[0]
        self.PLM_E = PLM[0]
        self.mELM = -1.52*10**-5 # [1/MPa]
        self.betaELM = self.PLM_E*10**3 - self.mELM * self.sigmaELM*10**6
        PLMAux = []

        for i in range(len(PLM)):
            PLMAux.append(PLM[i] * 1000.)

        cPLM = interp1d(tensaoPLM, PLMAux)


        if self.Pa2MPa(tensaoEquivalente) >= tensaoPLM[-1]:

            return cPLM(tensaoPLM[-1])

        elif self.Pa2MPa(tensaoEquivalente) <= tensaoPLM[0]:

            return self.mELM * tensaoEquivalente + self.betaELM

        else:
            return cPLM(self.Pa2MPa(tensaoEquivalente))

        # if self.Pa2MPa(tensaoEquivalente) >= self.sigmaELM:
        #
        #     return cPLM(self.Pa2MPa(tensaoEquivalente))
        # else:
        #     return self.mELM * tensaoEquivalente + self.betaELM








    def getPMH(self, tensaoEquivalente):

        PMH = self.PMHcor(self.Pa2MPa(tensaoEquivalente))

        return PMH

    def Aextrapolado(self, T):

        cCoeficienteA = interp1d(self.TemperaturaCoefTempoRupturaFlu, self.Coef1TRP)

        if T >= self.TemperaturaCoefTempoRupturaFlu[-1]:
            return cCoeficienteA(self.TemperaturaCoefTempoRupturaFlu[-1])

        elif T <= self.TemperaturaCoefTempoRupturaFlu[0]:
            return cCoeficienteA(self.TemperaturaCoefTempoRupturaFlu[0])

        else:
            return cCoeficienteA(T)

    def Bextrapolado(self, T):

        cCoeficienteB = interp1d(self.TemperaturaCoefTempoRupturaFlu, self.Coef2TRP)

        if T >= self.TemperaturaCoefTempoRupturaFlu[-1]:
            return cCoeficienteB(self.TemperaturaCoefTempoRupturaFlu[-1])

        elif T <= self.TemperaturaCoefTempoRupturaFlu[0]:
            return cCoeficienteB(self.TemperaturaCoefTempoRupturaFlu[0])

        else:
            return cCoeficienteB(T)

    def Cextrapolado(self, T):

        cCoeficienteC = interp1d(self.TemperaturaCoefTempoRupturaFlu, self.Coef3TRP)

        if T >= self.TemperaturaCoefTempoRupturaFlu[-1]:
            return cCoeficienteC(self.TemperaturaCoefTempoRupturaFlu[-1])

        elif T <= self.TemperaturaCoefTempoRupturaFlu[0]:
            return cCoeficienteC(self.TemperaturaCoefTempoRupturaFlu[0])

        else:
            return cCoeficienteC(T)

    def Dextrapolado(self, T):

        cCoeficienteD = interp1d(self.TemperaturaCoefTempoRupturaFlu, self.Coef4TRP)

        if T >= self.TemperaturaCoefTempoRupturaFlu[-1]:
            return cCoeficienteD(self.TemperaturaCoefTempoRupturaFlu[-1])

        elif T <= self.TemperaturaCoefTempoRupturaFlu[0]:
            return cCoeficienteD(self.TemperaturaCoefTempoRupturaFlu[0])

        else:
            return cCoeficienteD(T)

    def geTtR(self, tensaoEquivalente, T):

        A = self.Aextrapolado(T)
        B = self.Bextrapolado(T)
        C = self.Cextrapolado(T)
        D = -self.Dextrapolado(T)
        E = (1 - (self.Pa2MPa(tensaoEquivalente) / self.Aextrapolado(T)) ** (1 + self.Bextrapolado(T)))
        F = self.Cextrapolado(T)
        G = (self.Pa2MPa(tensaoEquivalente)) ** (-self.Dextrapolado(T))
        tR = (1 - (self.Pa2MPa(tensaoEquivalente) / self.Aextrapolado(T)) ** (1 + self.Bextrapolado(T))) * self.Cextrapolado(T) * (self.Pa2MPa(tensaoEquivalente)) ** (-self.Dextrapolado(T))

        return tR

    def getTrLM(self, PLM, Trotor):

        expoenteLM = PLM / Trotor - 20

        tRLM = 10 ** (PLM / Trotor - 20)

        return tRLM

    def getTrMH(self):

        tR1MH = 10 ** (self.PMHR1 * (self.T1Rotor - 370) + 17.145)
        tR2MH = 10 ** (self.PMHR2 * (self.T2Rotor - 370) + 17.145)

        return (tR1MH, tR2MH)

    def getTrPenny(self):

        if self.T1Rotor < (450 + 273.15):

            tRPenny = self.tR2

        else:

            tRPenny = min(self.tR1, self.tR2)

        return tRPenny

    def tRLMfinal(self):

        tRLM = min(self.tR1LM, self.tR2LM)

        return tRLM

    def tRMHfinal(self):

        tRMH = min(self.tR1MH, self.tR2MH)

        if tRMH == 0:
            tRMH = max(self.tR1MH, self.tR2MH)

        return tRMH

    def vidaRemanescente(self, tR, tempoAvaliacao, tempoOperacaoBase):

        return (str(tR - (tempoAvaliacao + tempoOperacaoBase)))

    def vidasRemanescentesFunction(self, tRLM, tRMH, tRPenny):

        # VidasRemanescentes = np.matrix('' + self.vidaRemanescente(tRLM, self.tempoAvaliacao, self.tempoOperacaoBase ) + ';' + self.vidaRemanescente(tRMH, self.tempoAvaliacao, self.tempoOperacaoBase ) + ';' + self.vidaRemanescente(tRPenny, self.tempoAvaliacao, self.tempoOperacaoBase ) + '')
        VidasRemanescentes = np.matrix('' + str(self.vidaLM_RegLin) + ';' + str(self.vidaMH_RegLin) + ';' + str(self.vidaPenny_RegLin) + '')

        return VidasRemanescentes

    def deltaD(self, tR, tempoAvaliacao):

        return (str((tempoAvaliacao / tR)*100))

    def deltaDfluenciaFunction(self, tRLM, tRMH, tRPenny):

        deltaDfluencia = [ self.deltaD(tRLM, self.tempoAvaliacao) , self.deltaD(tRMH, self.tempoAvaliacao) , self.deltaD(tRPenny, self.tempoAvaliacao) ]


        return deltaDfluencia

    def result(self):

        Resultados = [
            [str(self.VidasRemanescentes.item(0)), str(self.deltaDfluencia[0]), str(self.tRLM),
             str(self.T1Rotor - 273.15),
             str(self.hCarcaca)],
            [str(self.VidasRemanescentes.item(1)), str(self.deltaDfluencia[1]), str(self.tRMH),
             str(self.T2Rotor - 273.15),
             str(self.Pa2MPa(self.tensaoEquivalenteR1Rotor))],
            [str(self.VidasRemanescentes.item(2)), str(self.deltaDfluencia[2]), str(self.tRPenny), str(self.hRotor),
             str(self.Pa2MPa(self.tensaoEquivalenteR2Rotor))]]

        return Resultados

    def resultTubulacao(self, vidaLM, deltaDLM, vidaKR, deltaDKR):

        Resultados = [  [vidaLM, deltaDLM ] , [vidaKR, deltaDKR] ]

        return Resultados



    def saida2Function(self, Equipamento):

        if Equipamento == 'Rotor':

            saida2 = [['50', str(self.tempoAvaliacao), '0'], ['0', '10', '30'],
                    ['1', self.Resultados[0][0], self.Resultados[0][1]],
                    ['2', self.Resultados[1][0], self.Resultados[1][1]],
                    ['3', self.Resultados[2][0], self.Resultados[2][1]]]

            return saida2

        elif Equipamento == 'Tubulacao':

            saida2 = [['50', str(self.tempoAvaliacao), '0'], ['0', '10', '30'],
                    ['1', self.Resultados[0][0], self.Resultados[0][1]],
                    ['3', self.Resultados[1][0], self.Resultados[1][1]]]

            return saida2

        elif Equipamento == 'Valvula':

            saida2 = [['50', str(self.tempoAvaliacao), '0'], ['0', '10', '30'],
                    ['1', self.Resultados[0][0], self.Resultados[0][1]],
                    ['3', self.Resultados[1][0], self.Resultados[1][1]]]

            return saida2

        else:

            return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Equipamento inexistente! Digite o tipo de equipamento: Rotor, Tubulacao ou Valvula]")











    def fracVazao(self, lista):

        for i in range (len(lista)):

            lista[i] = (lista[i]) / 2.


    def getParamMonkmanGrant(self, fileNameParamMonkmanGrant):  ## Reescrever essa função!!!!!!

        arrayAux7 = []
        listaAux7 = []
        inputPMG = []
        PMG = []
        inputPMGfloat = []
        PMGfloat = []

        with open(self.currentDir + fileNameParamMonkmanGrant,
                  "rb") as ins:  ### Abre o arquivo controle_fluencia.txt
            for line in ins:
                arrayAux7.append(line)

        for i in range(len(arrayAux7)):
            listaAux7.append(arrayAux7[i].strip('\r\n'))

        for i in range(len(listaAux7)):
            inputPMG.append(listaAux7[i].split('\t')[0])

        for i in range(len(listaAux7)):
            PMG.append(listaAux7[i].split('\t')[1])

        # Transformando as string em números:

        for i in range(len(inputPMG)):
            inputPMGfloat.append(float(inputPMG[i]))

        for i in range(len(PMG)):
            PMGfloat.append(float(PMG[i]))

        return (inputPMGfloat, PMGfloat)



    def setParamAdimensionaisForFluTubulacao(self, VvaporSM, PmediaVapor, TvaporSM, hext, Rint, Rext, L, Equipamento):

        iterMax = 6
        i = 0
        Tavaliacao = self.Celsius2Kelvin(TvaporSM)
        Tavaliacao2 = self.Celsius2Kelvin(TvaporSM)

        while i <= iterMax:

            a = self.tolh2kgs(VvaporSM)
            b = self.muPT(self.bar2MPa(PmediaVapor), (Tavaliacao ))
            c = self.mm2m(Rint)

            Re = (4 * self.tolh2kgs(VvaporSM)) / (pi * 2 * self.mm2m(Rint) * self.muPT(self.bar2MPa(PmediaVapor), (Tavaliacao)))

            Pr = self.niPT(self.bar2MPa(PmediaVapor), Tavaliacao) / self.alfaPT(self.bar2MPa(PmediaVapor), Tavaliacao)

            fricFactor = 1 / ((.79 * log(Re) - 1.64) ** 2)

            if Equipamento == 'Tubulacao':

                Nu = (fricFactor / 8.) * Pr * (Re - 1000) / (
                1 + 12.7 * ((fricFactor / 8.) ** .5) * (-1 + Pr ** (2 / 3.)))

            elif Equipamento == 'Valvula':

                Nu = .046 * (Re**.85) * (Pr**.43)

            else:
                return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Equipamento inexistente! Digite o tipo de equipamento: Tubulacao ou Valvula]")


            hint = Nu * self.kPT(self.bar2MPa(PmediaVapor), (Tavaliacao)) / (2 * self.mm2m(Rint))

            RtconvVapor = 1 / (hint * 2 * pi * self.mm2m(Rint) * L)

            Rtcond = (1 / (2 * pi * self.lambdaInterpolado(Tavaliacao2) * L)) * log(self.mm2m(Rext) / self.mm2m(Rint))

            RtconvAr = 1 / (hext * 2 * pi * self.mm2m(Rext) * L)

            Qtotal = (Tavaliacao - self.Celsius2Kelvin(self.Tar)) / (RtconvVapor + Rtcond + RtconvAr)

            Text = self.Celsius2Kelvin(self.Tar) + Qtotal * RtconvAr

            Tint = Text + Qtotal * Rtcond

            Tavaliacao = (Tint + self.Celsius2Kelvin(TvaporSM)) / 2.

            Tavaliacao2 = (Tint + Text) / 2.

            i = i + 1

        return (Tint, Text)

    def getTwallCoef(self, Tint, Text, Rint, Rext):

        C1 = (Tint - Text) / log(self.mm2m(Rint)/self.mm2m(Rext))
        C2 = Tint - C1*log(self.mm2m(Rint))

        return (C1, C2)

    def calcTwallMedia(self, Rint, Rext, C1, C2):

        integrand = lambda r: 2*r*( C1*log(r) + C2 )
        I, err = quad(integrand, self.mm2m(Rint), self.mm2m(Rext))
        TwallMedia = ( 1 / (self.mm2m(Rext)**2 - self.mm2m(Rint)**2))*I

        return TwallMedia

    def tensaoTangecialTubulacao(self, P, Rint, Rext, r, type):

        if type == 'Reta':

            return (self.bar2Pa(P) * ( (self.mm2m(Rext)/self.mm2m(r))**2 + 1 )) / ((self.mm2m(Rext)/self.mm2m(Rint))**2 - 1)

        elif type == 'Curva':

            return ((self.bar2Pa(P) * ((self.mm2m(Rext) / self.mm2m(r)) ** 2 + 1)) / ((self.mm2m(Rext) / self.mm2m(Rint)) ** 2 - 1)) * self.f1

        else:
            return EH.ErrorHandle.handler("ERROR: [Ocorreu o erro : Geometria inexistente! Digite o tipo de geometria: Reta ou Curva]")

    def tensaoAxialTubulacao(self,  P, Rint, Rext, r, type, f1):

        if type == 'Reta':

            return self.tensaoTangecialTubulacao(P, Rint, Rext, r, 'Reta') / 2.

        elif type == 'Curva':

            return (self.tensaoTangecialTubulacao(P, Rint, Rext, r, 'Reta') / 2.)*f1

        else:
            return EH.ErrorHandle.handler(
                "ERROR: [Ocorreu o erro : Geometria inexistente! Digite o tipo de geometria: Reta ou Curva]")

    def tensaoRadialTubulacao(self, P, Rint, Rext, r, type, f1):

        if type == 'Reta':

            return (-self.bar2Pa(P) * ((self.mm2m(Rext) / self.mm2m(r)) ** 2 - 1)) / (((self.mm2m(Rext) / self.mm2m(Rint)) ** 2) - 1)

        elif type == 'Curva':
            return ((-self.bar2Pa(P) * ((self.mm2m(Rext) / self.mm2m(r)) ** 2 - 1)) / (((self.mm2m(Rext) / self.mm2m(Rint)) ** 2) - 1))*f1

        else:
            return EH.ErrorHandle.handler(
                "ERROR: [Ocorreu o erro : Geometria inexistente! Digite o tipo de geometria: Reta ou Curva]")

    def tensaoEquivalenteTubulacao(self, tensaoTangencial, tensaoAxial, tensaoRadial):

        return (1 / (2)**.5 ) * ( (tensaoTangencial - tensaoAxial)**2 + (tensaoTangencial - tensaoRadial)**2 + (tensaoAxial - tensaoRadial)**2)**.5



    def geTtRKR(self, tensaoEquivalente, T):

        A = self.Aextrapolado(T)
        B = self.Bextrapolado(T)
        C = self.Cextrapolado(T)
        D = self.Dextrapolado(T)

        tRKR = (1 - (self.Pa2MPa(tensaoEquivalente) / self.Aextrapolado(T)) ** (1 + self.Bextrapolado(T))) * self.Cextrapolado(T) * (self.Pa2MPa(tensaoEquivalente)) ** (-self.Dextrapolado(T))


        return tRKR



