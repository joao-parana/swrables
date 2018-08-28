# -*- coding: utf-8 -*-

import platform

class ErrorHandle():
    @staticmethod
    def handler(msg):
        print msg
        #return True

    @staticmethod
    def getPlataform():
        return platform.system()
