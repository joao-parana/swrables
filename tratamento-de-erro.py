oo/FadigaRotor.py:        try:
oo/FadigaRotor.py-            (self.tempo, self.pv, self.Tv, self.Tic, self.Wturb) = self.setupInputParamsFromSoma(arrayAux2, self.tempo,
oo/FadigaRotor.py-                                                                                                 self.pv, self.Tv,
oo/FadigaRotor.py-                                                                                                 self.Tic, self.Wturb)
oo/FadigaRotor.py-        except:
oo/FadigaRotor.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o sistema!' + '\n' + 'O dano por fadiga no rotor não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FadigaRotor.py-            self.saida2 = np.matrix('40 0 0; 0 20 30; 4 0 0; 5 0 0')
oo/FadigaRotor.py-
oo/FadigaRotor.py-            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
oo/FadigaRotor.py-                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
oo/FadigaRotor.py-                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
--
oo/FadigaRotor.py:        try:
oo/FadigaRotor.py-            (self.tempoFiltro1, self.PvaporFiltro1, self.TvaporFiltro1, self.TmetalFiltro1,
oo/FadigaRotor.py-             self.PotenciaFiltro1) = self.filtro1('Fadiga', self.tempo, self.pv, self.Tv, self.Tic, self.Wturb)
oo/FadigaRotor.py-            (self.tempoFiltro2, self.PvaporFiltro2, self.TvaporFiltro2, self.TmetalFiltro2,
oo/FadigaRotor.py-             self.PotenciaFiltro2) = self.filtro2('Fadiga', self.tempoFiltro1, self.PvaporFiltro1, self.TvaporFiltro1,
oo/FadigaRotor.py-                                                  self.TmetalFiltro1, self.PotenciaFiltro1)
oo/FadigaRotor.py-        except:
oo/FadigaRotor.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro na filtragem dos dados!' + '\n' + 'O dano por fadiga no rotor não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FadigaRotor.py-            self.saida2 = np.matrix('40 0 0; 0 20 30; 4 0 0; 5 0 0')
oo/FadigaRotor.py-
oo/FadigaRotor.py-            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
--
oo/FadigaRotor.py:        try:
oo/FadigaRotor.py-
oo/FadigaRotor.py-            (self.PvaporSM, self.TvaporSM, self.TmediacextSM, self.PWmediaSM) = self.lastValue()
oo/FadigaRotor.py-        except:
oo/FadigaRotor.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no tratamento dos dados!' + '\n' + 'O dano por fadiga no rotor não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FadigaRotor.py-            self.saida2 = np.matrix('40 0 0; 0 20 30; 4 0 0; 5 0 0')
oo/FadigaRotor.py-
oo/FadigaRotor.py-            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
oo/FadigaRotor.py-                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
oo/FadigaRotor.py-                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
oo/FadigaRotor.py-                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
--
oo/FadigaRotor.py:        try:
oo/FadigaRotor.py-            self.putDanoFromLocalFile('CurvaFadiga_FadigaRotor', self.deltaDfadigaPercentual)
oo/FadigaRotor.py-            self.putNumeroCiclosFromLocalFile('CurvaFadiga_FadigaRotor', 1)
oo/FadigaRotor.py-
oo/FadigaRotor.py-            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('CurvaFadiga_FadigaRotor')
oo/FadigaRotor.py-            self.NCRegLin, self.NC = self.getNumeroCiclosFromLocalFile('CurvaFadiga_FadigaRotor')
oo/FadigaRotor.py-
oo/FadigaRotor.py-            self.mean_x_RegLin = self.mean(self.NCRegLin)
oo/FadigaRotor.py-            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)
oo/FadigaRotor.py-
oo/FadigaRotor.py-            self.variance_x_RegLin = self.variance(self.NCRegLin, self.mean_x_RegLin)
--
oo/FadigaRotor.py:        try:
oo/FadigaRotor.py-            self.putDanoFromLocalFile('CLE_FadigaRotor', self.deltaDfadigaCLEPercentual)  # OBS!!! -> está hardcoded
oo/FadigaRotor.py-            self.putNumeroCiclosFromLocalFile('CLE_FadigaRotor', 1)  # OBS!!! -> está hardcoded
oo/FadigaRotor.py-
oo/FadigaRotor.py-            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('CLE_FadigaRotor')
oo/FadigaRotor.py-            self.NCRegLin, self.NC = self.getNumeroCiclosFromLocalFile('CLE_FadigaRotor')
oo/FadigaRotor.py-
oo/FadigaRotor.py-            self.mean_x_RegLin = self.mean(self.NCRegLin)
oo/FadigaRotor.py-            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)
oo/FadigaRotor.py-
oo/FadigaRotor.py-            self.variance_x_RegLin = self.variance(self.NCRegLin, self.mean_x_RegLin)
--
oo/FadigaRotor.py:        try:
oo/FadigaRotor.py-            self.writeOutfile('Rotor', 'Fadiga')
oo/FadigaRotor.py-        except:
oo/FadigaRotor.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fadiga do rotor foi enviado neste dia.' + '\n' + '***********************************************************'
oo/FadigaRotor.py-            return
oo/FadigaRotor.py-        # self.flag6()
oo/FadigaRotor.py-        # self.flagFim()
oo/FadigaRotor.py-
oo/FadigaRotor.py-
oo/FadigaRotor.py-        # Conferir as variações de temperatura, sao as maiores causas de divergencia.
oo/FadigaRotor.py-
--
oo/FadigaTubulacaoReta.py:        try:
oo/FadigaTubulacaoReta.py-            (self.tempo, self.Vv, self.pv, self.Tv) = self.setupInputParamsFromSoma(arrayAux2, self.tempo, self.Vv,
oo/FadigaTubulacaoReta.py-                                                                                    self.pv, self.Tv)
oo/FadigaTubulacaoReta.py-        except:
oo/FadigaTubulacaoReta.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o sistema!' + '\n' + 'O dano por fadiga na tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-            self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
oo/FadigaTubulacaoReta.py-                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
--
oo/FadigaTubulacaoReta.py:        try:
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-            (self.tVazao, self.matVazaoMod, self.tTemperatura, self.matTemperaturaMod, self.tPressao,
oo/FadigaTubulacaoReta.py-             self.matPressaoMod, self.nmaxElem, self.tmin) = self.matMods(self.indiceInicioVazao,
oo/FadigaTubulacaoReta.py-                                                                              self.indiceInicioTemperatura,
oo/FadigaTubulacaoReta.py-                                                                              self.indiceInicioPressao)
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-            # Os matMods nao apresentam grandes discrepancia, pois os indices de inicio de transiente estão razoavelmente compativeis
oo/FadigaTubulacaoReta.py-            # contudo ha uma discrepancia nao identificada nos valores das grandezas medidas: vazao, pressao e temperatura.
oo/FadigaTubulacaoReta.py-
--
oo/FadigaTubulacaoReta.py:        try:
oo/FadigaTubulacaoReta.py-            (self.tempoFiltro1, self.VvaporFiltro1, self.PvaporFiltro1, self.TvaporFiltro1) = self.filtro1('Fadiga',
oo/FadigaTubulacaoReta.py-                                                                                                           self.tempo,
oo/FadigaTubulacaoReta.py-                                                                                                           self.Vv,
oo/FadigaTubulacaoReta.py-                                                                                                           self.pv,
oo/FadigaTubulacaoReta.py-                                                                                                           self.Tv)
oo/FadigaTubulacaoReta.py-        except:
oo/FadigaTubulacaoReta.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro na filtragem dos dados!' + '\n' + 'O dano por fadiga na tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-            self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')
--
oo/FadigaTubulacaoReta.py:        try:
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-            (self.duracaoPartidaSM, self.variacaoTemperaturaVaporSM) = self.calcVariacoesTubValv()
oo/FadigaTubulacaoReta.py-        except:
oo/FadigaTubulacaoReta.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no tratamento dos dados!' + '\n' + 'O dano por fadiga na tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FadigaTubulacaoReta.py-            self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
oo/FadigaTubulacaoReta.py-                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
oo/FadigaTubulacaoReta.py-                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
oo/FadigaTubulacaoReta.py-                self.saida2.item((2, 0))) + '\t' + str(
--
oo/FadigaTubulacaoReta.py:        try:
oo/FadigaTubulacaoReta.py-            self.putDanoFromLocalFile('CurvaFadiga_FadigaTubulacaoReta', self.danoFadiga * 100)  # OBS!!! -> está hardcoded
oo/FadigaTubulacaoReta.py-            self.putNumeroCiclosFromLocalFile('CurvaFadiga_FadigaTubulacaoReta', 1)  # OBS!!! -> está hardcoded
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('CurvaFadiga_FadigaTubulacaoReta')
oo/FadigaTubulacaoReta.py-            self.NCRegLin, self.NC = self.getNumeroCiclosFromLocalFile('CurvaFadiga_FadigaTubulacaoReta')
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-            self.mean_x_RegLin = self.mean(self.NCRegLin)
oo/FadigaTubulacaoReta.py-            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-            self.variance_x_RegLin = self.variance(self.NCRegLin, self.mean_x_RegLin)
--
oo/FadigaTubulacaoReta.py:        try:
oo/FadigaTubulacaoReta.py-            self.putDanoFromLocalFile('CurvaFadiga_FadigaTubulacaoCurva',
oo/FadigaTubulacaoReta.py-                                      self.danoFadigaCurva * 100)  # OBS!!! -> está hardcoded
oo/FadigaTubulacaoReta.py-            self.putNumeroCiclosFromLocalFile('CurvaFadiga_FadigaTubulacaoCurva', 1)  # OBS!!! -> está hardcoded
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-            self.danoAcumuladoRegLinCurva = self.getDanoFromLocalFile('CurvaFadiga_FadigaTubulacaoCurva')
oo/FadigaTubulacaoReta.py-            self.NCRegLinCurva, self.NCcurva = self.getNumeroCiclosFromLocalFile('CurvaFadiga_FadigaTubulacaoCurva')
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-            self.mean_x_RegLinCurva = self.mean(self.NCRegLinCurva)
oo/FadigaTubulacaoReta.py-            self.mean_y_RegLinCurva = self.mean(self.danoAcumuladoRegLinCurva)
oo/FadigaTubulacaoReta.py-
--
oo/FadigaTubulacaoReta.py:        try:
oo/FadigaTubulacaoReta.py-            self.writeOutfile('Tubulacao', 'Fadiga', 'Reta')
oo/FadigaTubulacaoReta.py-        except:
oo/FadigaTubulacaoReta.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fadiga do trecho reto da tubulação foi enviado neste dia.' + '\n' + '***********************************************************'
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py:        try:
oo/FadigaTubulacaoReta.py-            self.writeOutfile('Tubulacao', 'Fadiga', 'Curva')
oo/FadigaTubulacaoReta.py-        except:
oo/FadigaTubulacaoReta.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fadiga do trecho curvo da tubulação foi enviado neste dia.' + '\n' + '***********************************************************'
oo/FadigaTubulacaoReta.py-            return
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-        # self.flag5Tubulacao()
oo/FadigaTubulacaoReta.py-
oo/FadigaTubulacaoReta.py-        # self.flagFimTubulacao()
oo/FadigaTubulacaoReta.py-
--
oo/FadigaValvulaReta.py:        try:
oo/FadigaValvulaReta.py-            (self.tempo, self.Vv, self.pv, self.Tv, self.Tmint, self.Tmext) = self.setupInputParamsFromSoma(arrayAux2, self.tempo, self.Vv, self.pv, self.Tv, self.Tmint, self.Tmext)
oo/FadigaValvulaReta.py-        except:
oo/FadigaValvulaReta.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o sistema!' + '\n' + 'O dano por fadiga na tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-            self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
oo/FadigaValvulaReta.py-                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
oo/FadigaValvulaReta.py-                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
oo/FadigaValvulaReta.py-                self.saida2.item((2, 0))) + '\t' + str(
--
oo/FadigaValvulaReta.py:        try:
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-            (self.tVazao, self.matVazaoMod, self.tTemperatura, self.matTemperaturaMod, self.tPressao,
oo/FadigaValvulaReta.py-             self.matPressaoMod, self.nmaxElem, self.tmin) = self.matMods(self.indiceInicioVazao,
oo/FadigaValvulaReta.py-                                                                              self.indiceInicioTemperatura,
oo/FadigaValvulaReta.py-                                                                              self.indiceInicioPressao)
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-            self.matPressaoModModificado = self.modifica(len(self.matPressaoMod[0]), self.tmin, self.matPressaoMod)
oo/FadigaValvulaReta.py-            self.matVazaoModModificado = self.modifica(len(self.matVazaoMod[0]), self.tmin,
oo/FadigaValvulaReta.py-                                                         self.matVazaoMod)
oo/FadigaValvulaReta.py-            self.matTemperaturaModModificado = self.modifica(len(self.matTemperaturaMod[0]), self.tmin,
--
oo/FadigaValvulaReta.py:        try:
oo/FadigaValvulaReta.py-            (self.tempoFiltro1, self.VvaporFiltro1, self.PvaporFiltro1, self.TvaporFiltro1) = self.filtro1('Fadiga',
oo/FadigaValvulaReta.py-                                                                                                           self.tempo,
oo/FadigaValvulaReta.py-                                                                                                           self.Vv,
oo/FadigaValvulaReta.py-                                                                                                           self.pv,
oo/FadigaValvulaReta.py-                                                                                                           self.Tv)
oo/FadigaValvulaReta.py-        except:
oo/FadigaValvulaReta.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro na filtragem dos dados!' + '\n' + 'O dano por fadiga na válvula não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-            self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')
--
oo/FadigaValvulaReta.py:        try:
oo/FadigaValvulaReta.py-            (self.duracaoPartidaSM, self.variacaoTemperaturaVaporSM) = self.calcVariacoesTubValv()
oo/FadigaValvulaReta.py-        except:
oo/FadigaValvulaReta.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no tratamento dos dados!' + '\n' + 'O dano por fadiga na válvula não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-            self.saida2 = np.matrix('40 0 0; 0 20 30; 6 0 0')
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
oo/FadigaValvulaReta.py-                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
oo/FadigaValvulaReta.py-                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
--
oo/FadigaValvulaReta.py:        try:
oo/FadigaValvulaReta.py-            self.putDanoFromLocalFile('CurvaFadiga_FadigaValvulaReta', self.danoFadiga*100)  # OBS!!! -> está hardcoded
oo/FadigaValvulaReta.py-            self.putNumeroCiclosFromLocalFile('CurvaFadiga_FadigaValvulaReta', 1)  # OBS!!! -> está hardcoded
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('CurvaFadiga_FadigaValvulaReta')
oo/FadigaValvulaReta.py-            self.NCRegLin, self.NC = self.getNumeroCiclosFromLocalFile('CurvaFadiga_FadigaValvulaReta')
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-            self.mean_x_RegLin = self.mean(self.NCRegLin)
oo/FadigaValvulaReta.py-            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-            self.variance_x_RegLin = self.variance(self.NCRegLin, self.mean_x_RegLin)
--
oo/FadigaValvulaReta.py:        try:
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-            self.putDanoFromLocalFile('CurvaFadiga_FadigaValvulaCurva', self.danoFadigaCurva * 100)  # OBS!!! -> está hardcoded
oo/FadigaValvulaReta.py-            self.putNumeroCiclosFromLocalFile('CurvaFadiga_FadigaValvulaCurva', 1)  # OBS!!! -> está hardcoded
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-            self.danoAcumuladoRegLinCurva = self.getDanoFromLocalFile('CurvaFadiga_FadigaValvulaCurva')
oo/FadigaValvulaReta.py-            self.NCRegLinCurva, self.NCcurva = self.getNumeroCiclosFromLocalFile('CurvaFadiga_FadigaValvulaCurva')
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-            self.mean_x_RegLinCurva = self.mean(self.NCRegLinCurva)
oo/FadigaValvulaReta.py-            self.mean_y_RegLinCurva = self.mean(self.danoAcumuladoRegLinCurva)
oo/FadigaValvulaReta.py-
--
oo/FadigaValvulaReta.py:        try:
oo/FadigaValvulaReta.py-            self.writeOutfile('Valvula', 'Fadiga', 'Reta')
oo/FadigaValvulaReta.py-        except:
oo/FadigaValvulaReta.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fadiga do trecho reto da válvula foi enviado neste dia.' + '\n' + '***********************************************************'
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py:        try:
oo/FadigaValvulaReta.py-            self.writeOutfile('Valvula', 'Fadiga', 'Curva')
oo/FadigaValvulaReta.py-        except:
oo/FadigaValvulaReta.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fadiga do trecho curvo da válvula foi enviado neste dia.' + '\n' + '***********************************************************'
oo/FadigaValvulaReta.py-            return
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-        # self.flag5Tubulacao()
oo/FadigaValvulaReta.py-
oo/FadigaValvulaReta.py-        # self.flagFimTubulacao()
oo/FadigaValvulaReta.py-
--
oo/FatigueTest.py:    try:
oo/FatigueTest.py-        r = requests.get(serviceURI)
oo/FatigueTest.py-    except:
oo/FatigueTest.py-        print "\n****\nErro ao recuperar os dados do servidor local. Verifique se /turbodiag-server.py está executando\n****"
oo/FatigueTest.py-        exit(1)
oo/FatigueTest.py-else:
oo/FatigueTest.py-    r = requests.post( serviceURI, data = dataToService )
oo/FatigueTest.py-
oo/FatigueTest.py-print("Status Code do HTTP = " + str(r.status_code) + ", MSG = " + r.reason)
oo/FatigueTest.py-print('\n'+ r.text[:228] + '...\n')
oo/FatigueTest.py-
--
oo/FluenciaRotor.py:        try:
oo/FluenciaRotor.py-            (self.tempo, self.pv, self.Tv, self.Tic, self.Wturb) = self.setupInputParamsFromSoma(arrayAux2, self.tempo, self.pv, self.Tv, self.Tic, self.Wturb)
oo/FluenciaRotor.py-        except:
oo/FluenciaRotor.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o sistema!' + '\n' + 'O dano por fluência no rotor não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FluenciaRotor.py-            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 2 0 0; 3 0 0')
oo/FluenciaRotor.py-
oo/FluenciaRotor.py-            strOut = str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
oo/FluenciaRotor.py-                self.saida2.item((0, 2))) + '\n' + str(self.saida2.item((1, 0))) + '\t' + str(
oo/FluenciaRotor.py-                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
oo/FluenciaRotor.py-                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
oo/FluenciaRotor.py-                self.saida2.item((2, 2))) + '\n' + '' + str(self.saida2.item((3, 0))) + '\t' + str(
--
oo/FluenciaRotor.py:        try:
oo/FluenciaRotor.py-            (self.tempoFiltro1, self.PvaporFiltro1, self.TvaporFiltro1, self.TmetalFiltro1, self.PotenciaFiltro1) = self.filtro1('Fluencia', self.tempo, self.pv, self.Tv, self.Tic, self.Wturb)
oo/FluenciaRotor.py-            (self.tempoFiltro2, self.PvaporFiltro2, self.TvaporFiltro2, self.TmetalFiltro2, self.PotenciaFiltro2) = self.filtro2('Fluencia', self.tempoFiltro1, self.PvaporFiltro1, self.TvaporFiltro1, self.TmetalFiltro1, self.PotenciaFiltro1)
oo/FluenciaRotor.py-        except:
oo/FluenciaRotor.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro na filtragem dos dados!' + '\n' + 'O dano por fluência no rotor não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FluenciaRotor.py-            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 2 0 0; 3 0 0')
oo/FluenciaRotor.py-
oo/FluenciaRotor.py-            strOut = str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(
oo/FluenciaRotor.py-                self.saida2.item((0, 2))) + '\n' + str(self.saida2.item((1, 0))) + '\t' + str(
oo/FluenciaRotor.py-                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
oo/FluenciaRotor.py-                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
--
oo/FluenciaRotor.py:        try:
oo/FluenciaRotor.py-
oo/FluenciaRotor.py-            self.PvaporSM = self.calcMediaParams(self.PvaporFiltro2, self.limiteInfPressaoRotor)
oo/FluenciaRotor.py-            self.TvaporSM = self.calcMediaParams(self.TvaporFiltro2, self.limiteInfTemperaturaRotor)
oo/FluenciaRotor.py-            self.TmediacextSM = self.calcMediaParams(self.TmetalFiltro2, self.limiteInfTemperaturaRotor)
oo/FluenciaRotor.py-            self.PWmediaSM = self.calcMediaParams(self.PotenciaFiltro2, self.limiteInfPotencia)
oo/FluenciaRotor.py-
oo/FluenciaRotor.py-        except:
oo/FluenciaRotor.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no tratamento dos dados!' + '\n' + 'O dano por fluência no rotor não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FluenciaRotor.py-            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 2 0 0; 3 0 0')
oo/FluenciaRotor.py-
--
oo/FluenciaRotor.py:        try:
oo/FluenciaRotor.py-            self.putDanoFromLocalFile('LM_FluenciaRotor', self.deltaDfluencia[0])  # OBS!!! -> está hardcoded
oo/FluenciaRotor.py-            self.putTempoAvaliacaoFromLocalFile('LM_FluenciaRotor',
oo/FluenciaRotor.py-                                                self.tempoAvaliacao)  # OBS!!! -> está hardcoded
oo/FluenciaRotor.py-
oo/FluenciaRotor.py-            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('LM_FluenciaRotor')
oo/FluenciaRotor.py-            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('LM_FluenciaRotor')
oo/FluenciaRotor.py-
oo/FluenciaRotor.py-            self.mean_x_RegLin = self.mean(self.tempoOperacaoRegLin)
oo/FluenciaRotor.py-            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)
oo/FluenciaRotor.py-
--
oo/FluenciaRotor.py:        try:
oo/FluenciaRotor.py-            self.putDanoFromLocalFile('Penny_FluenciaRotor', self.deltaDfluencia[2])  # OBS!!! -> está hardcoded
oo/FluenciaRotor.py-            self.putTempoAvaliacaoFromLocalFile('Penny_FluenciaRotor',
oo/FluenciaRotor.py-                                                self.tempoAvaliacao)  # OBS!!! -> está hardcoded
oo/FluenciaRotor.py-
oo/FluenciaRotor.py-            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('Penny_FluenciaRotor')
oo/FluenciaRotor.py-            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('Penny_FluenciaRotor')
oo/FluenciaRotor.py-
oo/FluenciaRotor.py-            self.mean_x_RegLin = self.mean(self.tempoOperacaoRegLin)
oo/FluenciaRotor.py-            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)
oo/FluenciaRotor.py-
--
oo/FluenciaRotor.py:        try:
oo/FluenciaRotor.py-            self.putDanoFromLocalFile('MH_FluenciaRotor', self.deltaDfluencia[1])  # OBS!!! -> está hardcoded
oo/FluenciaRotor.py-            self.putTempoAvaliacaoFromLocalFile('MH_FluenciaRotor',
oo/FluenciaRotor.py-                                                self.tempoAvaliacao)  # OBS!!! -> está hardcoded
oo/FluenciaRotor.py-
oo/FluenciaRotor.py-            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('MH_FluenciaRotor')
oo/FluenciaRotor.py-            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('MH_FluenciaRotor')
oo/FluenciaRotor.py-
oo/FluenciaRotor.py-            self.mean_x_RegLin = self.mean(self.tempoOperacaoRegLin)
oo/FluenciaRotor.py-            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)
oo/FluenciaRotor.py-
--
oo/FluenciaRotor.py:        try:
oo/FluenciaRotor.py-            self.writeOutfile('Rotor', 'Fluencia')
oo/FluenciaRotor.py-        except:
oo/FluenciaRotor.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fluência do rotor foi enviado neste dia.' + '\n' + '***********************************************************'
oo/FluenciaRotor.py-            return
oo/FluenciaRotor.py-
oo/FluenciaRotor.py-        # self.flag6()
oo/FluenciaRotor.py-        # self.flagFim()
oo/FluenciaRotor.py-
oo/FluenciaRotor.py-   
oo/FluenciaRotor.py-    @staticmethod
--
oo/FluenciaTubulacaoCurva.py:        try:
oo/FluenciaTubulacaoCurva.py-            (self.tempo, self.Vv, self.pv, self.Tv) = self.setupInputParamsFromSoma(creepData, self.tempo, self.Vv, self.pv, self.Tv)
oo/FluenciaTubulacaoCurva.py-        except:
oo/FluenciaTubulacaoCurva.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o sistema!' + '\n' + 'O dano por fluência no trecho curvo da tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FluenciaTubulacaoCurva.py-            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')
oo/FluenciaTubulacaoCurva.py-
oo/FluenciaTubulacaoCurva.py-            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
oo/FluenciaTubulacaoCurva.py-                self.saida2.item((0, 1))) + '\t' + str(
oo/FluenciaTubulacaoCurva.py-                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
oo/FluenciaTubulacaoCurva.py-                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
oo/FluenciaTubulacaoCurva.py-                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
--
oo/FluenciaTubulacaoCurva.py:        try:
oo/FluenciaTubulacaoCurva.py-            (self.tempoFiltro1, self.VvaporFiltro1, self.PvaporFiltro1, self.TvaporFiltro1) = self.filtro1('Fluencia', self.tempo, self.Vv, self.pv,self.Tv)
oo/FluenciaTubulacaoCurva.py-            (self.tempoFiltro2, self.VvaporFiltro2, self.PvaporFiltro2, self.TvaporFiltro2) = self.filtro2('Fluencia', self.tempoFiltro1, self.VvaporFiltro1, self.PvaporFiltro1, self.TvaporFiltro1)
oo/FluenciaTubulacaoCurva.py-        except:
oo/FluenciaTubulacaoCurva.py-
oo/FluenciaTubulacaoCurva.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro na filtragem dos dados!' + '\n' + 'O dano por fluência na tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FluenciaTubulacaoCurva.py-            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')
oo/FluenciaTubulacaoCurva.py-
oo/FluenciaTubulacaoCurva.py-            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
oo/FluenciaTubulacaoCurva.py-                self.saida2.item((0, 1))) + '\t' + str(
oo/FluenciaTubulacaoCurva.py-                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
--
oo/FluenciaTubulacaoCurva.py:        try:
oo/FluenciaTubulacaoCurva.py-
oo/FluenciaTubulacaoCurva.py-            self.VvaporSM = self.calcMediaParams(self.VvaporFiltro2, self.limiteInfVazao)
oo/FluenciaTubulacaoCurva.py-            self.PvaporSM = self.calcMediaParams(self.PvaporFiltro2, self.limiteInfPressao)
oo/FluenciaTubulacaoCurva.py-            self.TvaporSM = self.calcMediaParams(self.TvaporFiltro2, self.limiteInfTemperaturaTubulacaoValvula)
oo/FluenciaTubulacaoCurva.py-            (self.PmediaVapor, self.TmediaVapor, self.VmediaVapor) = self.redefParams(self.TvaporSM, self.PvaporSM,
oo/FluenciaTubulacaoCurva.py-                                                                                      self.VvaporSM)
oo/FluenciaTubulacaoCurva.py-        except:
oo/FluenciaTubulacaoCurva.py-
oo/FluenciaTubulacaoCurva.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no tratamento dos dados!' + '\n' + 'O dano por fluência na tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FluenciaTubulacaoCurva.py-            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')
--
oo/FluenciaTubulacaoCurva.py:        try:
oo/FluenciaTubulacaoCurva.py-            self.putDanoFromLocalFile('LM_FluenciaTubulacaoCurva', self.deltaDLM)  # OBS!!! -> está hardcoded
oo/FluenciaTubulacaoCurva.py-            self.putTempoAvaliacaoFromLocalFile('LM_FluenciaTubulacaoCurva', self.tempoAvaliacao)  # OBS!!! -> está hardcoded
oo/FluenciaTubulacaoCurva.py-
oo/FluenciaTubulacaoCurva.py-            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('LM_FluenciaTubulacaoCurva')
oo/FluenciaTubulacaoCurva.py-            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('LM_FluenciaTubulacaoCurva')
oo/FluenciaTubulacaoCurva.py-
oo/FluenciaTubulacaoCurva.py-            self.mean_x_RegLin = self.mean(self.tempoOperacaoRegLin)
oo/FluenciaTubulacaoCurva.py-            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)
oo/FluenciaTubulacaoCurva.py-
oo/FluenciaTubulacaoCurva.py-            self.variance_x_RegLin = self.variance(self.tempoOperacaoRegLin, self.mean_x_RegLin)
--
oo/FluenciaTubulacaoCurva.py:        try:
oo/FluenciaTubulacaoCurva.py-
oo/FluenciaTubulacaoCurva.py-            self.putDanoFromLocalFile('KR_FluenciaTubulacaoCurva', self.deltaDKR)  # OBS!!! -> está hardcoded
oo/FluenciaTubulacaoCurva.py-            self.putTempoAvaliacaoFromLocalFile('KR_FluenciaTubulacaoCurva', self.tempoAvaliacao)  # OBS!!! -> está hardcoded
oo/FluenciaTubulacaoCurva.py-
oo/FluenciaTubulacaoCurva.py-            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('KR_FluenciaTubulacaoCurva')
oo/FluenciaTubulacaoCurva.py-            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('KR_FluenciaTubulacaoCurva')
oo/FluenciaTubulacaoCurva.py-
oo/FluenciaTubulacaoCurva.py-            self.mean_x_RegLin = self.mean(self.tempoOperacaoRegLin)
oo/FluenciaTubulacaoCurva.py-            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)
oo/FluenciaTubulacaoCurva.py-
--
oo/FluenciaTubulacaoCurva.py:        try:
oo/FluenciaTubulacaoCurva.py-            self.writeOutfile('Tubulacao', 'Fluencia', 'Curva')
oo/FluenciaTubulacaoCurva.py-        except:
oo/FluenciaTubulacaoCurva.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fluência do trecho curvo da tubulação foi enviado neste dia.' + '\n' + '***********************************************************'
oo/FluenciaTubulacaoCurva.py-            return
oo/FluenciaTubulacaoCurva.py-        # self.flag6()
oo/FluenciaTubulacaoCurva.py-        # self.flagFim()
oo/FluenciaTubulacaoCurva.py-    
oo/FluenciaTubulacaoCurva.py-    @staticmethod
oo/FluenciaTubulacaoCurva.py-    def create():
oo/FluenciaTubulacaoCurva.py-        # currentDir = 'C:\\SOMATURBODIAG\\tubulacaocurva\\'
--
oo/FluenciaTubulacaoReta.py:        try:
oo/FluenciaTubulacaoReta.py-            (self.tempo, self.Vv, self.pv, self.Tv) = self.setupInputParamsFromSoma(arrayAux2, self.tempo, self.Vv, self.pv, self.Tv)
oo/FluenciaTubulacaoReta.py-        except:
oo/FluenciaTubulacaoReta.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o sistema!' + '\n' + 'O dano por fluência no trecho reto da tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FluenciaTubulacaoReta.py-            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')
oo/FluenciaTubulacaoReta.py-
oo/FluenciaTubulacaoReta.py-            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
oo/FluenciaTubulacaoReta.py-                self.saida2.item((0, 1))) + '\t' + str(
oo/FluenciaTubulacaoReta.py-                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
oo/FluenciaTubulacaoReta.py-                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
oo/FluenciaTubulacaoReta.py-                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
--
oo/FluenciaTubulacaoReta.py:        try:
oo/FluenciaTubulacaoReta.py-            (self.tempoFiltro1, self.VvaporFiltro1, self.PvaporFiltro1, self.TvaporFiltro1) = self.filtro1('Fluencia', self.tempo, self.Vv, self.pv,self.Tv)
oo/FluenciaTubulacaoReta.py-            (self.tempoFiltro2, self.VvaporFiltro2, self.PvaporFiltro2, self.TvaporFiltro2) = self.filtro2('Fluencia', self.tempoFiltro1, self.VvaporFiltro1, self.PvaporFiltro1, self.TvaporFiltro1)
oo/FluenciaTubulacaoReta.py-        except:
oo/FluenciaTubulacaoReta.py-
oo/FluenciaTubulacaoReta.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro na filtragem dos dados!' + '\n' + 'O dano por fluência na tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FluenciaTubulacaoReta.py-            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')
oo/FluenciaTubulacaoReta.py-
oo/FluenciaTubulacaoReta.py-            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
oo/FluenciaTubulacaoReta.py-                self.saida2.item((0, 1))) + '\t' + str(
oo/FluenciaTubulacaoReta.py-                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
--
oo/FluenciaTubulacaoReta.py:        try:
oo/FluenciaTubulacaoReta.py-
oo/FluenciaTubulacaoReta.py-            self.VvaporSM = self.calcMediaParams(self.VvaporFiltro2, self.limiteInfVazao)
oo/FluenciaTubulacaoReta.py-            self.PvaporSM = self.calcMediaParams(self.PvaporFiltro2, self.limiteInfPressao)
oo/FluenciaTubulacaoReta.py-            self.TvaporSM = self.calcMediaParams(self.TvaporFiltro2, self.limiteInfTemperaturaTubulacaoValvula)
oo/FluenciaTubulacaoReta.py-            (self.PmediaVapor, self.TmediaVapor, self.VmediaVapor) = self.redefParams(self.TvaporSM, self.PvaporSM, self.VvaporSM)
oo/FluenciaTubulacaoReta.py-        except:
oo/FluenciaTubulacaoReta.py-
oo/FluenciaTubulacaoReta.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no tratamento dos dados!' + '\n' + 'O dano por fluência na tubulação não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FluenciaTubulacaoReta.py-            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')
oo/FluenciaTubulacaoReta.py-
--
oo/FluenciaTubulacaoReta.py:        try:
oo/FluenciaTubulacaoReta.py-
oo/FluenciaTubulacaoReta.py-            self.putDanoFromLocalFile('LM_FluenciaTubulacaoReta', self.deltaDLM)  # OBS!!! -> está hardcoded
oo/FluenciaTubulacaoReta.py-            self.putTempoAvaliacaoFromLocalFile('LM_FluenciaTubulacaoReta', self.tempoAvaliacao)  # OBS!!! -> está hardcoded
oo/FluenciaTubulacaoReta.py-
oo/FluenciaTubulacaoReta.py-            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('LM_FluenciaTubulacaoReta')
oo/FluenciaTubulacaoReta.py-            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('LM_FluenciaTubulacaoReta')
oo/FluenciaTubulacaoReta.py-
oo/FluenciaTubulacaoReta.py-            self.mean_x_RegLin = self.mean(self.tempoOperacaoRegLin)
oo/FluenciaTubulacaoReta.py-            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)
oo/FluenciaTubulacaoReta.py-
--
oo/FluenciaTubulacaoReta.py:        try:
oo/FluenciaTubulacaoReta.py-            self.putDanoFromLocalFile('KR_FluenciaTubulacaoReta', self.deltaDKR)  # OBS!!! -> está hardcoded
oo/FluenciaTubulacaoReta.py-            self.putTempoAvaliacaoFromLocalFile('KR_FluenciaTubulacaoReta', self.tempoAvaliacao)  # OBS!!! -> está hardcoded
oo/FluenciaTubulacaoReta.py-
oo/FluenciaTubulacaoReta.py-            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('KR_FluenciaTubulacaoReta')
oo/FluenciaTubulacaoReta.py-            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('KR_FluenciaTubulacaoReta')
oo/FluenciaTubulacaoReta.py-
oo/FluenciaTubulacaoReta.py-            self.mean_x_RegLin = self.mean(self.tempoOperacaoRegLin)
oo/FluenciaTubulacaoReta.py-            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)
oo/FluenciaTubulacaoReta.py-
oo/FluenciaTubulacaoReta.py-            self.variance_x_RegLin = self.variance(self.tempoOperacaoRegLin, self.mean_x_RegLin)
--
oo/FluenciaTubulacaoReta.py:        try:
oo/FluenciaTubulacaoReta.py-            self.writeOutfile('Tubulacao', 'Fluencia', 'Reta')
oo/FluenciaTubulacaoReta.py-        except:
oo/FluenciaTubulacaoReta.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fluência do trecho reto da tubulação foi enviado neste dia.' + '\n' + '***********************************************************'
oo/FluenciaTubulacaoReta.py-            return
oo/FluenciaTubulacaoReta.py-            # self.flag6()
oo/FluenciaTubulacaoReta.py-        # self.flagFim()
oo/FluenciaTubulacaoReta.py-
oo/FluenciaTubulacaoReta.py-    @staticmethod
oo/FluenciaTubulacaoReta.py-    def create():
oo/FluenciaTubulacaoReta.py-        # currentDir = 'C:\\SOMATURBODIAG\\tubulacaoreta\\'
--
oo/FluenciaValvulaCurva.py:        try:
oo/FluenciaValvulaCurva.py-            (self.tempo, self.Vv, self.pv, self.Tv, self.Tmint, self.Tmext) = self.setupInputParamsFromSoma(creepData, self.tempo, self.Vv, self.pv, self.Tv, self.Tmint, self.Tmext)
oo/FluenciaValvulaCurva.py-        except:
oo/FluenciaValvulaCurva.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o sistema!' + '\n' + 'O dano por fluência no trecho curvo da válvula não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FluenciaValvulaCurva.py-            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')
oo/FluenciaValvulaCurva.py-
oo/FluenciaValvulaCurva.py-            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(
oo/FluenciaValvulaCurva.py-                self.saida2.item((0, 1))) + '\t' + str(
oo/FluenciaValvulaCurva.py-                self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(
oo/FluenciaValvulaCurva.py-                self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(
oo/FluenciaValvulaCurva.py-                self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(
--
oo/FluenciaValvulaCurva.py:        try:
oo/FluenciaValvulaCurva.py-            (self.tempoFiltro1, self.VvaporFiltro1, self.PvaporFiltro1, self.TvaporFiltro1, self.TmetalintFiltro1,
oo/FluenciaValvulaCurva.py-             self.TmetalextFiltro1) = self.filtro1('Fluencia', self.tempo, self.Vv, self.pv, self.Tv, self.Tmint,
oo/FluenciaValvulaCurva.py-                                                   self.Tmext)
oo/FluenciaValvulaCurva.py-
oo/FluenciaValvulaCurva.py-            (self.tempoFiltro2, self.VvaporFiltro2, self.PvaporFiltro2, self.TvaporFiltro2, self.TmetalintFiltro2,
oo/FluenciaValvulaCurva.py-             self.TmetalextFiltro2) = self.filtro2('Fluencia', self.tempoFiltro1, self.VvaporFiltro1,
oo/FluenciaValvulaCurva.py-                                                   self.PvaporFiltro1, self.TvaporFiltro1, self.TmetalintFiltro1,
oo/FluenciaValvulaCurva.py-                                                   self.TmetalextFiltro1)
oo/FluenciaValvulaCurva.py-        except:
oo/FluenciaValvulaCurva.py-
--
oo/FluenciaValvulaCurva.py:        try:
oo/FluenciaValvulaCurva.py-
oo/FluenciaValvulaCurva.py-            self.VvaporSM = self.calcMediaParams(self.VvaporFiltro2, self.limiteInfVazao)
oo/FluenciaValvulaCurva.py-            self.PvaporSM = self.calcMediaParams(self.PvaporFiltro2, self.limiteInfPressao)
oo/FluenciaValvulaCurva.py-            self.TvaporSM = self.calcMediaParams(self.TvaporFiltro2, self.limiteInfTemperaturaTubulacaoValvula)
oo/FluenciaValvulaCurva.py-            self.TmetalintSM = self.calcMediaParams(self.TmetalintFiltro2, self.limiteInfTemperaturaTubulacaoValvula)
oo/FluenciaValvulaCurva.py-            self.TmetalextSM = self.calcMediaParams(self.TmetalextFiltro2, self.limiteInfTemperaturaTubulacaoValvula)
oo/FluenciaValvulaCurva.py-
oo/FluenciaValvulaCurva.py-        except:
oo/FluenciaValvulaCurva.py-
oo/FluenciaValvulaCurva.py-
--
oo/FluenciaValvulaCurva.py:        try:
oo/FluenciaValvulaCurva.py-            self.putDanoFromLocalFile('LM_FluenciaValvulaCurva', self.deltaDLM)  # OBS!!! -> está hardcoded
oo/FluenciaValvulaCurva.py-            self.putTempoAvaliacaoFromLocalFile('LM_FluenciaValvulaCurva', self.tempoAvaliacao)  # OBS!!! -> está hardcoded
oo/FluenciaValvulaCurva.py-
oo/FluenciaValvulaCurva.py-            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('LM_FluenciaValvulaCurva')
oo/FluenciaValvulaCurva.py-            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('LM_FluenciaValvulaCurva')
oo/FluenciaValvulaCurva.py-
oo/FluenciaValvulaCurva.py-            self.mean_x_RegLin = self.mean(self.tempoOperacaoRegLin)
oo/FluenciaValvulaCurva.py-            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)
oo/FluenciaValvulaCurva.py-
oo/FluenciaValvulaCurva.py-            self.variance_x_RegLin = self.variance(self.tempoOperacaoRegLin, self.mean_x_RegLin)
--
oo/FluenciaValvulaCurva.py:        try:
oo/FluenciaValvulaCurva.py-
oo/FluenciaValvulaCurva.py-            self.putDanoFromLocalFile('KR_FluenciaValvulaCurva', self.deltaDKR)  # OBS!!! -> está hardcoded
oo/FluenciaValvulaCurva.py-            self.putTempoAvaliacaoFromLocalFile('KR_FluenciaValvulaCurva', self.tempoAvaliacao)  # OBS!!! -> está hardcoded
oo/FluenciaValvulaCurva.py-
oo/FluenciaValvulaCurva.py-            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('KR_FluenciaValvulaCurva')
oo/FluenciaValvulaCurva.py-            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('KR_FluenciaValvulaCurva')
oo/FluenciaValvulaCurva.py-
oo/FluenciaValvulaCurva.py-            self.mean_x_RegLin = self.mean(self.tempoOperacaoRegLin)
oo/FluenciaValvulaCurva.py-            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)
oo/FluenciaValvulaCurva.py-
--
oo/FluenciaValvulaCurva.py:        try:
oo/FluenciaValvulaCurva.py-            self.writeOutfile('Valvula', 'Fluencia', 'Curva')
oo/FluenciaValvulaCurva.py-        except:
oo/FluenciaValvulaCurva.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fluência do trecho curvo da válvula foi enviado neste dia.' + '\n' + '***********************************************************'
oo/FluenciaValvulaCurva.py-            return
oo/FluenciaValvulaCurva.py-
oo/FluenciaValvulaCurva.py-        # self.flag6()
oo/FluenciaValvulaCurva.py-        # self.flagFim()
oo/FluenciaValvulaCurva.py-
oo/FluenciaValvulaCurva.py-    
oo/FluenciaValvulaCurva.py-    @staticmethod
--
oo/FluenciaValvulaReta.py:        try:
oo/FluenciaValvulaReta.py-            (self.tempo, self.Vv, self.pv, self.Tv, self.Tmint, self.Tmext) = self.setupInputParamsFromSoma(creepData, self.tempo, self.Vv, self.pv, self.Tv, self.Tmint, self.Tmext)
oo/FluenciaValvulaReta.py-        except:
oo/FluenciaValvulaReta.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o sistema!' + '\n' + 'O dano por fluência no trecho reto da válvula não foi avaliado neste dia.' + '\n' + '***********************************************************'
oo/FluenciaValvulaReta.py-
oo/FluenciaValvulaReta.py-            self.saida2 = np.matrix('50 0 0; 0 10 30; 1 0 0; 3 0 0')
oo/FluenciaValvulaReta.py-
oo/FluenciaValvulaReta.py-            strOut = '' + str(self.saida2.item((0, 0))) + '\t' + str(self.saida2.item((0, 1))) + '\t' + str(self.saida2.item((0, 2))) + '\n' + '' + str(self.saida2.item((1, 0))) + '\t' + str(self.saida2.item((1, 1))) + '\t' + str(self.saida2.item((1, 2))) + '\n' + '' + str(self.saida2.item((2, 0))) + '\t' + str(self.saida2.item((2, 1))) + '\t' + str(self.saida2.item((2, 2))) + '\n' + '' + str(self.saida2.item((3, 0))) + '\t' + str(self.saida2.item((3, 1))) + '\t' + str(self.saida2.item((3, 2)))
oo/FluenciaValvulaReta.py-
oo/FluenciaValvulaReta.py-            MecanismoDano.SAIDA_CALCULO[MecanismoDano.VALVULA]['Reta']['Fluencia'] = strOut
oo/FluenciaValvulaReta.py-
--
oo/FluenciaValvulaReta.py:        try:
oo/FluenciaValvulaReta.py-            (self.tempoFiltro1, self.VvaporFiltro1, self.PvaporFiltro1, self.TvaporFiltro1, self.TmetalintFiltro1,
oo/FluenciaValvulaReta.py-             self.TmetalextFiltro1) = self.filtro1('Fluencia', self.tempo, self.Vv, self.pv, self.Tv, self.Tmint,
oo/FluenciaValvulaReta.py-                                                   self.Tmext)
oo/FluenciaValvulaReta.py-
oo/FluenciaValvulaReta.py-            (self.tempoFiltro2, self.VvaporFiltro2, self.PvaporFiltro2, self.TvaporFiltro2, self.TmetalintFiltro2,
oo/FluenciaValvulaReta.py-             self.TmetalextFiltro2) = self.filtro2('Fluencia', self.tempoFiltro1, self.VvaporFiltro1,
oo/FluenciaValvulaReta.py-                                                   self.PvaporFiltro1, self.TvaporFiltro1, self.TmetalintFiltro1,
oo/FluenciaValvulaReta.py-                                                   self.TmetalextFiltro1)
oo/FluenciaValvulaReta.py-        except:
oo/FluenciaValvulaReta.py-
--
oo/FluenciaValvulaReta.py:        try:
oo/FluenciaValvulaReta.py-
oo/FluenciaValvulaReta.py-            self.VvaporSM = self.calcMediaParams(self.VvaporFiltro2, self.limiteInfVazao)
oo/FluenciaValvulaReta.py-            self.PvaporSM = self.calcMediaParams(self.PvaporFiltro2, self.limiteInfPressao)
oo/FluenciaValvulaReta.py-            self.TvaporSM = self.calcMediaParams(self.TvaporFiltro2, self.limiteInfTemperaturaTubulacaoValvula)
oo/FluenciaValvulaReta.py-            self.TmetalintSM = self.calcMediaParams(self.TmetalintFiltro2, self.limiteInfTemperaturaTubulacaoValvula)
oo/FluenciaValvulaReta.py-            self.TmetalextSM = self.calcMediaParams(self.TmetalextFiltro2, self.limiteInfTemperaturaTubulacaoValvula)
oo/FluenciaValvulaReta.py-
oo/FluenciaValvulaReta.py-        except:
oo/FluenciaValvulaReta.py-
oo/FluenciaValvulaReta.py-
--
oo/FluenciaValvulaReta.py:        try:
oo/FluenciaValvulaReta.py-            self.putDanoFromLocalFile('LM_FluenciaValvulaReta', self.deltaDLM)  # OBS!!! -> está hardcoded
oo/FluenciaValvulaReta.py-            self.putTempoAvaliacaoFromLocalFile('LM_FluenciaValvulaReta', self.tempoAvaliacao)  # OBS!!! -> está hardcoded
oo/FluenciaValvulaReta.py-
oo/FluenciaValvulaReta.py-            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('LM_FluenciaValvulaReta')
oo/FluenciaValvulaReta.py-            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('LM_FluenciaValvulaReta')
oo/FluenciaValvulaReta.py-
oo/FluenciaValvulaReta.py-            self.mean_x_RegLin = self.mean(self.tempoOperacaoRegLin)
oo/FluenciaValvulaReta.py-            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)
oo/FluenciaValvulaReta.py-
oo/FluenciaValvulaReta.py-            self.variance_x_RegLin = self.variance(self.tempoOperacaoRegLin, self.mean_x_RegLin)
--
oo/FluenciaValvulaReta.py:        try:
oo/FluenciaValvulaReta.py-
oo/FluenciaValvulaReta.py-            self.putDanoFromLocalFile('KR_FluenciaValvulaReta', self.deltaDKR)  # OBS!!! -> está hardcoded
oo/FluenciaValvulaReta.py-            self.putTempoAvaliacaoFromLocalFile('KR_FluenciaValvulaReta', self.tempoAvaliacao)  # OBS!!! -> está hardcoded
oo/FluenciaValvulaReta.py-
oo/FluenciaValvulaReta.py-            self.danoAcumuladoRegLin = self.getDanoFromLocalFile('KR_FluenciaValvulaReta')
oo/FluenciaValvulaReta.py-            self.tempoOperacaoRegLin, self.tempoOp = self.getTempoAvalicaoFromLocalFile('KR_FluenciaValvulaReta')
oo/FluenciaValvulaReta.py-
oo/FluenciaValvulaReta.py-            self.mean_x_RegLin = self.mean(self.tempoOperacaoRegLin)
oo/FluenciaValvulaReta.py-            self.mean_y_RegLin = self.mean(self.danoAcumuladoRegLin)
oo/FluenciaValvulaReta.py-
--
oo/FluenciaValvulaReta.py:        try:
oo/FluenciaValvulaReta.py-            self.writeOutfile('Valvula', 'Fluencia', 'Reta')
oo/FluenciaValvulaReta.py-        except:
oo/FluenciaValvulaReta.py-            print '***********************************************************' + '\n' + 'WARNING: Ocorreu um erro no envio de dados para o SOMA!' + '\n' + 'Nenhum dado de fluência do trecho reto da válvula foi enviado neste dia.' + '\n' + '***********************************************************'
oo/FluenciaValvulaReta.py-            return
oo/FluenciaValvulaReta.py-        # self.flag6()
oo/FluenciaValvulaReta.py-        # self.flagFim()
oo/FluenciaValvulaReta.py-
oo/FluenciaValvulaReta.py-
oo/FluenciaValvulaReta.py-    @staticmethod
oo/FluenciaValvulaReta.py-    def create():
--
oo/turbodiag-server.py:        try:
oo/turbodiag-server.py-            # Always read in binary mode. Opening files in text mode may cause
oo/turbodiag-server.py-            # newline translations, making the actual size of the content
oo/turbodiag-server.py-            # transmitted *less* than the content-length!
oo/turbodiag-server.py-            f = open(path, 'rb')
oo/turbodiag-server.py-        except IOError:
oo/turbodiag-server.py-            self.send_error(404, "File not found")
oo/turbodiag-server.py-            return None
oo/turbodiag-server.py-
oo/turbodiag-server.py-        if self.range_from is None:
oo/turbodiag-server.py-            self.send_response(200)
--
oo/turbodiag-server.py:        try:
oo/turbodiag-server.py-            list = os.listdir(path)
oo/turbodiag-server.py-        except os.error:
oo/turbodiag-server.py-            self.send_error(404, "No permission to list directory")
oo/turbodiag-server.py-            return None
oo/turbodiag-server.py-        list.sort(key=lambda a: a.lower())
oo/turbodiag-server.py-        f = StringIO()
oo/turbodiag-server.py-        displaypath = cgi.escape(unquote(self.path))
oo/turbodiag-server.py-
oo/turbodiag-server.py-        f.write('<!doctype html>\n')
oo/turbodiag-server.py-        f.write('<html class="no-js" lang="">\n')
--
oo/turbodiag-server.py:        try:
oo/turbodiag-server.py-            httpd = ThreadingHTTPServer(("", port), Handler)
oo/turbodiag-server.py-            return httpd
oo/turbodiag-server.py-        except socket.error as e:
oo/turbodiag-server.py-            if e.errno == errno.EADDRINUSE:
oo/turbodiag-server.py-                next_attempts -= 1
oo/turbodiag-server.py-                port += 1
oo/turbodiag-server.py-            else:
oo/turbodiag-server.py-                raise
oo/turbodiag-server.py-
oo/turbodiag-server.py-def main(args=None):
