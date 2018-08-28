# -*- coding: utf-8 -*-

import ErrorHandle as EH
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import platform
import requests
import sys

from iapws import IAPWS97
from math import *
from numpy.linalg import inv
from scipy import optimize
from scipy.integrate import odeint
from scipy.integrate import quad
from scipy.interpolate import interp1d
from scipy.misc import derivative
from scipy.optimize import fsolve


print "SISTEMA:\n*** " + os.name + " / " + platform.system() + " / " + platform.release() + " ***"
matriz = np.matrix('')
print matriz
print "cwd = " + os.getcwd()
serviceURI = "http://10.0.2.140:1443/mxml/rlife"
dataToService = {'op': 'getNextProcessingWindow'}

LOCAL_TEST = True
if  LOCAL_TEST :
    # serviceURI = "http://localhost:8193/first-iteraction.json"
    serviceURI = "http://localhost:8193/problem.json"
    dataToService = {}
    try:
        r = requests.get(serviceURI)
    except:
        print "\n****\nErro ao recuperar os dados do servidor local. Verifique se /turbodiag-server.py está executando\n****"
        exit(1)
else:
    r = requests.post( serviceURI, data = dataToService )

print("Status Code do HTTP = " + str(r.status_code) + ", MSG = " + r.reason)
print('\n'+ r.text[:228] + '...\n')

# print("Saida formatada com 4 espaços de indentação")
# print json.dumps(r.text, indent = 4, sort_keys = True)
# print ('\n')

# dict = json.loads(r.text)
# print (dict['operation'] == 'getNextProcessingWindow', dict['successful'])
# if (dict['operation'] == 'getNextProcessingWindow' and dict['successful']) :
#     print '\nOK na recuperação da NextProcessingWindow'
#     windowList = dict['windowList']
#     for x in range(0, 3):
#         print "Vou processar " + dict['windowList'][x]['residualLifeSegment']
#         dadosRecuperados = dict['windowList'][x]['data']
#         fatigueCycles = dict['windowList'][x]['fatigueCycles']
#         operationTime = dict['windowList'][x]['operationTime']
#         print "(len(data), fatigueCycles, operationTime)"
#         print (len(dadosRecuperados), fatigueCycles, operationTime)

from turbodiag import TurboDiag
from MecanismoDano import *

turbodiag = TurboDiag()

dict = json.loads(r.text)
# print (dict['operation'] == 'getNextProcessingWindow', dict['successful'])
if (dict['operation'] == 'getNextProcessingWindow' and dict['successful']):
    turbodiag.doNextProcessingWindow(dict, stage = "TEST")
    print MecanismoDano.TIMESTAMP_OF_DATA
else:
    if LOCAL_TEST:
        print "Erro na estrutura dos dados de teste obtidos localmente"
    else:
        print "Erro na estrutura dos dados obtidos do SOMA"

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
