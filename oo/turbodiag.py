#!/usr/local/soma/miniconda/bin/python
# -*- coding: utf-8 -*-

# O SOMA-Turbodiag usa a distribuicao do Python 2.7 do Anaconda

import os
import platform
import numpy as np
import requests
import sys
import json
from FluenciaValvulaReta import*
from FluenciaValvulaCurva import*
from FluenciaTubulacaoReta import*
from FluenciaTubulacaoCurva import*
from FluenciaRotor import *
from FadigaValvulaReta import *
from FadigaTubulacaoReta import *
from FadigaRotor import *
from MecanismoDano import*


class TurboDiag:

    def __init__(self):
        self.SOMA_CONTEXT_PATH='http://localhost:1443/mxml'
        print "Objeto TurboDiag criado"

    def sendtoSoma(self):
        # FLUENCIA e FADIGA
        print "\n\n* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
        print "Enviando dano no ROTOR"
        # calcFlu = MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR]['normal']['Fluencia']
        # calcFad = MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR]['normal']['Fadiga']
        # TODO: Confirmar com o Diogo o que ele esta esperando la para e colocar um "if" para proteger o caso quando calcFlu e calcFad forem
        # print (str(MecanismoDano.INITIAL_TIMESTAMP) + ' - creepResult: \n' + calcFlu + ', fatResult: \n' + calcFad)

        # r2 = requests.post(self.SOMA_CONTEXT_PATH + "/rlife", data={'op': 'putCalculationData',
        #                          'seg': 470, 'initTime':  MecanismoDano.INITIAL_TIMESTAMP,
        #                          'creepResult': calcFlu, 'fatResult': calcFad})
        #
        #
        # dict = json.loads(r2.text)
        # print (dict['operation'] == 'getNextProcessingWindow', dict['successful'])


        ########################## Rotor #####################################

        # if (dict['successful']):
        #     print dict
        # else:
        #     print "Erro na gravação dos dados no SOMA"
        #     print dict['error']
        #
        # print "Rotor"


        xxx = MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR]['normal']
        # TODO: Verificar
        if 'Fluencia' in xxx:
            calcFlu = MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR]['normal']['Fluencia']
        else:
            calcFlu = None

        xxx = MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR]['normal']

        # TODO: Verificar

        if 'Fadiga' in xxx:
            calcFad = MecanismoDano.SAIDA_CALCULO[MecanismoDano.ROTOR]['normal']['Fadiga']
        else:
            calcFad = None


        r2 = requests.post(self.SOMA_CONTEXT_PATH + "/rlife",
                           data={'op': 'putCalculationData', 'seg': 470, 'initTime': MecanismoDano.INITIAL_TIMESTAMP,
                                 'creepResult': calcFlu, 'fatResult': calcFad})

        dict = json.loads(r2.text)


        ################################### Rotor ######################################


        if (dict['successful']):
            print dict
        else:
            print "Erro na gravação dos dados no SOMA"
            print dict['error']

        print "Tubulacao Reta"

        print "\n\n* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
        print "Enviando dano na TUBULACAO RETA"

        xxx = MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Reta']
        # TODO: Verificar
        if 'Fluencia' in xxx:
            calcFlu = MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Reta']['Fluencia']
        else:
            calcFlu = None

        xxx = MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Reta']
        # TODO: Verificar
        if 'Fadiga' in xxx:
            calcFad = MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Reta']['Fadiga']
        else:
            calcFad = None

        r2 = requests.post(self.SOMA_CONTEXT_PATH + "/rlife", data={'op': 'putCalculationData', 'seg': 482, 'initTime':  MecanismoDano.INITIAL_TIMESTAMP, 'creepResult':  calcFlu, 'fatResult': calcFad})
        dict = json.loads(r2.text)
        # print (dict['operation'] == 'getNextProcessingWindow', dict['successful'])
        print(r2.text[:308] + '...')


        if (dict['successful']):
            print dict
        else:
            print "Erro na gravação dos dados no SOMA"
            print dict['error']

        print "Tubulacao Curva"

        print "\n\n* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
        print "Enviando dano na TUBULACAO CURVA"

        xxx = MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Curva']
        # TODO: Verificar
        if 'Fluencia' in xxx:
            calcFlu = MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Curva']['Fluencia']
        else:
            calcFlu = None


        xxx = MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Curva']
        # TODO: Verificar
        if 'Fadiga' in xxx:
            calcFad = MecanismoDano.SAIDA_CALCULO[MecanismoDano.TUBULACAO]['Curva']['Fadiga']
        else:
            calcFad = None

        r2 = requests.post(self.SOMA_CONTEXT_PATH + "/rlife", data={'op': 'putCalculationData', 'seg': 483, 'initTime':  MecanismoDano.INITIAL_TIMESTAMP, 'creepResult':  calcFlu, 'fatResult': calcFad})
        dict = json.loads(r2.text)
        # print (dict['operation'] == 'getNextProcessingWindow', dict['successful'])
        if (dict['successful']):
            print dict
        else:
            print "Erro na gravação dos dados no SOMA"
            print dict['error']

        print "Valvula Reta"

        print "\n\n* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
        print "Enviando dano na VALVULA RETA"


        xxx = MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Reta']
        # TODO: Verificar
        if 'Fluencia' in xxx:
            calcFlu = MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Reta']['Fluencia']
        else:
            calcFlu = None

        xxx = MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Reta']
        # TODO: Verificar
        if 'Fadiga' in xxx:
            calcFad = MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Reta']['Fadiga']
        else:
            calcFad = None

        r2 = requests.post(self.SOMA_CONTEXT_PATH + "/rlife", data={'op': 'putCalculationData', 'seg': 452, 'initTime':  MecanismoDano.INITIAL_TIMESTAMP, 'creepResult':  calcFlu, 'fatResult': calcFad})
        dict = json.loads(r2.text)
        # print (dict['operation'] == 'getNextProcessingWindow', dict['successful'])
        if (dict['successful']):
            print dict
        else:
            print "Erro na gravação dos dados no SOMA"
            print dict['error']

        print "Valvula Curva"

        print "\n\n* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
        print "Enviando dano na VALVULA CURVA"

        xxx = MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Curva']
        # TODO: Verificar
        if 'Fluencia' in xxx:
            calcFlu = MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Curva']['Fluencia']
        else:
            calcFlu = None


        xxx = MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Curva']
        # TODO: Verificar
        if 'Fadiga' in xxx:
            calcFad = MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Curva']['Fadiga']
        else:
            calcFad = None

        r2 = requests.post(self.SOMA_CONTEXT_PATH + "/rlife", data={'op': 'putCalculationData', 'seg': 486, 'initTime':  MecanismoDano.INITIAL_TIMESTAMP, 'creepResult':  calcFlu, 'fatResult': calcFad})
        dict = json.loads(r2.text)
        # print (dict['operation'] == 'getNextProcessingWindow', dict['successful'])
        if (dict['successful']):
            print dict
        else:
            print "Erro na gravação dos dados no SOMA"
            print dict['error']

        # print(r2.text[:308] + '...')

    def calculate(self, segment, creepOnly, creepIndex, dadosRecuperados, fatigueCycles, operationTime):
        print "DEBUG: dadosRecuperados = " + str(len(dadosRecuperados)) + \
              ", fatigueCycles = " + str(fatigueCycles) + \
              ", operationTime = " + str(operationTime) + \
              ", creepOnly = " + str(creepOnly) + \
              ", creepIndex = " + str(creepIndex)
        fatigueData = []
        creepData = []
        for line in dadosRecuperados.split('\n'):
            # print line
            fatigueData.append(line)

        print len(fatigueData)

        if creepOnly:
            # Veio só Fluencia
            creepData = fatigueData  # Este array contém apenas dados da Fluência
            fatigueData = []
        else:
            # Particiono os dados horizontalmente
            creepData = fatigueData[creepIndex:] # Este array contém apenas dados da Fluência

        print "Tamanho dos Arrays de entrada"
        print "Fluência = " + str(len(creepData)) + ", Fadiga = " + str(len(fatigueData))

        if segment == 'valve':
            # Calcula a Fluencia (creep) - 24 horas
            fluVR = FluenciaValvulaReta.create()
            fluVR.JustDoItValvReta(creepData, fatigueCycles, operationTime)
            # TODO: deve retornar o texto do arquivo de saida
            if creepOnly:
                # Veio só Fluencia (creep)
                print ". "
            else:
                # Veio Fluencia (creep) e Fadiga (fatigue)
                # Calcula a Fadiga (fatigue) - 48 horas
                fadVR = FadigaValvulaReta.create()
                fadVR.JustDoItFadValvReta(fatigueData, fatigueCycles, operationTime)
                # TODO: deve retornar o texto do arquivo de saida

            fluVC = FluenciaValvulaCurva.create()
            fluVC.JustDoItValvCurva(creepData, fatigueCycles, operationTime)
            # TODO: deve retornar o texto do arquivo de saida

        elif segment == 'pipe':
            # print 'Estou fazendo um teste com FadigaValvula'
            fluTR = FluenciaTubulacaoReta.create()
            fluTR.JustDoItTubReta(creepData, fatigueCycles, operationTime)
            print fluTR.Resultados
            # TODO: deve retornar o texto do arquivo de saida
            if creepOnly:
                # Veio só Fluencia (creep)
                print ". "
            else:
                # Veio Fluencia (creep) e Fadiga (fatigue)
                # Calcula a Fadiga (fatigue) - 48 horas
                fadTR = FadigaTubulacaoReta.create()
                fadTR.JustDoItFadTubReta(fatigueData, fatigueCycles, operationTime)
                # TODO: deve retornar o texto do arquivo de saida

            fluTC = FluenciaTubulacaoCurva.create()
            fluTC.JustDoItTubCurva(creepData, fatigueCycles, operationTime)
            # TODO: deve retornar o texto do arquivo de saida


        elif segment == 'firstStage':
             fluR = FluenciaRotor.create()
             fluR.JustDoItFlu(creepData, fatigueCycles, operationTime)
             # TODO: deve retornar o texto do arquivo de saida
             print fluR.Resultados
             if creepOnly:
                 # Veio só Fluencia (creep)
                 print ". "
             else:
                 # Veio Fluencia (creep) e Fadiga (fatigue)
                 # Calcula a Fadiga (fatigue) - 48 horas
                 fadR = FadigaRotor.create()
                 fadR.JustDoItFad(fatigueData, fatigueCycles, operationTime)
                 # TODO: deve retornar o texto do arquivo de saida

        print '***'
        print MecanismoDano.SAIDA_CALCULO
        print '***'

    def doNextProcessingWindow(self, dict, stage = "PRODUCTION"):
        print '\nDEBUG: OK na recuperação da NextProcessingWindow'
        windowList = dict['windowList']
        for x in range(0, 3):
            segment = dict['windowList'][x]['residualLifeSegment']
            initialTimeStamp = dict['windowList'][x]['initialTimeStamp']
            MecanismoDano.TIMESTAMP_OF_DATA[x] = initialTimeStamp
            print "\n\n**** DEBUG: Vou processar " + segment + " comecando em " + str(initialTimeStamp)
            MecanismoDano.INITIAL_TIMESTAMP = dict['windowList'][x]['initialTimeStamp']
            creepOnly = dict['windowList'][x]['creepOnly']
            creepIndex = dict['windowList'][x]['creepIndex']
            dadosRecuperados = dict['windowList'][x]['data']
            datFileName = segment + '_' + str(x) + '.dat'
            print('Salvando arquivo ' + datFileName)
            text_file = open(datFileName, "w")
            text_file.write(dadosRecuperados)
            text_file.close()
            fatigueCycles = dict['windowList'][x]['fatigueCycles']
            operationTime = dict['windowList'][x]['operationTime']
            # if (segment == 'valve') :
            #     r = MecanismoDano.getFatigueFromSoma( 486, initTime=1363046400000)
            #     lineNumber = 1
            #     for line in r.iter_lines():
            #         if lineNumber > 1 :
            #             dadosRecuperados = dadosRecuperados + line + "\n"
            #
            #         lineNumber = lineNumber + 1
            #
            #     print(dadosRecuperados)
            #     creepOnly = False
            #     creepIndex = 0
            #     ret = self.calculate(segment, creepOnly, creepIndex, dadosRecuperados, fatigueCycles, operationTime)

            ret = self.calculate(segment, creepOnly, creepIndex, dadosRecuperados, fatigueCycles, operationTime)

        if (stage == "PRODUCTION"):
            self.sendtoSoma()

    def main(self):

        print "SISTEMA:\n*** " + os.name + " / " + platform.system() + " / " + platform.release() + " ***"
        matriz = np.matrix('')
        print matriz
        print "cwd = " + os.getcwd()
        serviceURI = self.SOMA_CONTEXT_PATH + "/rlife"
        dataToService = {'op': 'getNextProcessingWindow'}
        r = requests.post( serviceURI, data = dataToService )

        print "Status Code do HTTP = " + str(r.status_code) + r.reason
        print('\nDEBUG: '+ r.text[:78] + '...\n')

        datFileName = 'problem.json'
        print('Salvando arquivo ' + datFileName)
        text_file = open(datFileName, "w")
        text_file.write(r.text)
        text_file.close()

        dict = json.loads(r.text)
        # print (dict['operation'] == 'getNextProcessingWindow', dict['successful'])
        if (dict['operation'] == 'getNextProcessingWindow' and dict['successful']):
            self.doNextProcessingWindow(dict)
            print MecanismoDano.TIMESTAMP_OF_DATA
        else:
            print "Erro na obtenção dos dados do SOMA"
            sys.exit(1)
        #
        sys.exit(0)


if __name__ == '__main__':
    #
    # Aqui começa a execução do programa
    #
    turbodiag = TurboDiag()
    RET = turbodiag.main()
    print "RET = %s" % RET


# Diretórios:
# IN  C:\SOMATURBODIAG\rotor\in \
# OUT C:\SOMATURBODIAG\rotor\out\
# REL C:\SOMATURBODIAG\rotor\out\
#
# Exemplo de saida do método getNextProcessingWindow
# {
#   "operation": "getNextProcessingWindow",
#   "windowList": [
#     {
#       "creepIndex": 0,
#       "residualLifeSegment": "pipe",
#       "data": "180.0\t0.0625\t0.5469\t169.7195\n185.0\t0.1031\t0.5469\t169.5219\n190.0\t0.1313\t0.5469\t169.3299\n195.0\t0.1344\t0.5469\t169.1466\n200.0\t0.1281\t0.5469\t168.9461\n",
#       "creepOnly": true,
#       "initialTimeStamp": 1362960000000,
#       "endTimeStamp": 1363046400000,
#       "dataHeader": "Timestamp\thistorical_U07_I731FY3002_avg\thistorical_U07_I731PT3015_avg\thistorical_U07_I731TT3019_avg\n",
#       "fatigueCycles": 320,
#       "operationTime": 112000
#     },
#     {
#       "creepIndex": 0,
#       "residualLifeSegment": "valve",
#       "data": "180.0\t0.0625\t0.5469\t169.7195\t214.5719\t201.8313\n185.0\t0.1031\t0.5469\t169.5219\t214.2813\t201.5656\n",
#       "creepOnly": true,
#       "initialTimeStamp": 1362960000000,
#       "endTimeStamp": 1363046400000,
#       "dataHeader": "Timestamp\thistorical_U07_I731FY3002_avg\thistorical_U07_I731PT3015_avg\thistorical_U07_I731TT3019_avg\thistorical_U07_I730TE4002_avg\thistorical_U07_I730TE4004_avg\n",
#       "fatigueCycles": 320,
#       "operationTime": 112000
#     },
#     {
#       "creepIndex": 0,
#       "residualLifeSegment": "firstStage",
#       "data": "1265.0\t0.0\t131.9042\t306.956\t0.7031\n1270.0\t0.0\t131.7753\t306.8414\t0.7055\n",
#       "creepOnly": true,
#       "initialTimeStamp": 1362960000000,
#       "endTimeStamp": 1363046400000,
#       "dataHeader": "Timestamp\thistorical_U07_I732PT3001_avg\thistorical_U07_I731TT3019_avg\thistorical_U07_I730TT3012_avg\thistorical_U07_I760ET1002_avg\n",
#       "fatigueCycles": 320,
#       "operationTime": 112000
#     }
#   ],
#   "successful": true
# }
