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

SOMA_CONTEXT_PATH='http://localhost:1443/mxml'
print "SISTEMA:\n*** " + os.name + " / " + platform.system() + " / " + platform.release() + " ***"
matriz = np.matrix('')
print matriz
print "cwd = " + os.getcwd()
serviceURI = SOMA_CONTEXT_PATH + "/rlife"
dataToService = {'op': 'getNextProcessingWindow'}

LOCAL_TEST = True
if  LOCAL_TEST :
    # serviceURI = "http://localhost:8193/first-iteraction.json"
    serviceURI = "http://localhost:8193/problem.json"
    dataToService = {}
    r = requests.get( serviceURI )
else:
    r = requests.post( serviceURI, data = dataToService )

print(r.status_code)
print(r.reason)
print("Status Code do HTTP = " + str(r.status_code), r.reason)
print('\n'+ r.text[:228] + '...\n')

print("Saida formatada com 4 espaços de indentação")
print json.dumps(r.text, indent = 4, sort_keys = True)
print ('\n')

dict = json.loads(r.text)
print (dict['operation'] == 'getNextProcessingWindow', dict['successful'])
if (dict['operation'] == 'getNextProcessingWindow' and dict['successful']) :
    print '\nOK na recuperação da NextProcessingWindow'
    windowList = dict['windowList']

    print "Status Code do HTTP = " + str(r.status_code) + r.reason
    print('\nDEBUG: '+ r.text[:78] + '...\n')
    # Condicao de parada: {"operation":"getNextProcessingWindow","windowList":[{},{},{}],"successful":true}
    windowList = dict['windowList']
    w1 = dict['windowList'][0] 
    w2 = dict['windowList'][1] 
    w3 = dict['windowList'][2]
    print(str(w1) == "{}")
    print(str(w2) == "{}")
    print(str(w3) == "{}")
    print(str(w1))
    print(str(w2))
    print(str(w3))

    if (str(w1) == "{}" and str(w2) == "{}" and str(w3) == "{}") :
        print("Nada mais a processar")
        sys.exit(127)
    
    sys.exit(0)

    for x in range(0, 3):
        print "Vou processar " + dict['windowList'][x]['residualLifeSegment']
        dadosRecuperados = dict['windowList'][x]['data']
        fatigueCycles = dict['windowList'][x]['fatigueCycles']
        operationTime = dict['windowList'][x]['operationTime']
        print "(len(data), fatigueCycles, operationTime)"
        print (len(dadosRecuperados), fatigueCycles, operationTime)


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
