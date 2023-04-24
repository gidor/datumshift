# -*- coding: UTF-8 -*-
#!/usr/bin/python
__doc__ = \
    """
import muodulo di lettura di file GRIGLIATI IGMI
porting delle funzionalità da vb
"""
__version__ = "0.0"
__author__ = "gd"
# Attribute VB_Name = "http_gr1"
# Option Explicit
# -------------------------------------------------
# VARIABILI INTRODOTTE PER LE FUNZIONALITA DI ACCESSO VIA HTTP AI GRIGLIATI
# Private http_Conn As MSXML2.XMLHTTP40
# Private http_Conn As MSXML2.XMLHTTP40

import numpy as np
import math
import os
from typing import Union, IO, Any
# DICHIARATE PER COMPILAZIONE SONO GLOBALI?


# Dim Fi_SO_sist, La_SO_sist As Double
Fi_SO_sist = float(0.0)
La_SO_sist = float(0.0)
# Dim Fi_SO_geoid, La_SO_geoid As Double
Fi_SO_geoid = float(0.0)
La_SO_geoid = float(0.0)

# Public Fi_ED50_Roma40(153, 109), La_ED50_Roma40(153, 109), Fi_WGS84_Roma40(153, 109), La_WGS84_Roma40(153, 109), N(381, 406) As Double
# Public Fi_ED50_Roma40_Foglio(6, 6), La_ED50_Roma40_Foglio(6, 6), Fi_WGS84_Roma40_Foglio(6, 6), La_WGS84_Roma40_Foglio(6, 6), N_Foglio(10, 14) As Double
# Public Fi_SIST_0, La_SIST_0, Fi_GEOID_0, La_GEOID_0 As Double

Fi_ED50_Roma40 = np.zeros((153, 109), np.float64)
La_ED50_Roma40 = np.zeros((153, 109), np.float64)
Fi_WGS84_Roma40 = np.zeros((153, 109), np.float64)
La_WGS84_Roma40 = np.zeros((153, 109), np.float64)
N = np.zeros((381, 406), np.float64)


Fi_SIST_0 = 0.0
La_SIST_0 = 0.0
Fi_GEOID_0 = 0.0
La_GEOID_0 = 0.0


RespC = float(0.0)  # As Long


class GrFile (object):
    """Classe di gestione del file gr1/gr2"""
    __Fname__: str = ""
    __FileObj__: IO[Any] = None
    __buffer__ = ""
    __Fi_ED50_Roma40_Foglio__: np.ndarray = np.zeros((6, 6), np.float64)
    __La_ED50_Roma40_Foglio__: np.ndarray = np.zeros((6, 6), np.float64)
    __Fi_WGS84_Roma40_Foglio__: np.ndarray = np.zeros((6, 6), np.float64)
    __La_WGS84_Roma40_Foglio__: np.ndarray = np.zeros((6, 6), np.float64)
    __N_Foglio__: np.ndarray = np.zeros((10, 14), np.float64)
    __Fi_SIST_0__: float = float(0.0)
    __La_SIST_0__: float = float(0.0)
    __epocageoide__: str = ""
    __epocagrid_WGS84_Roma40__: str = ""
    __tipogrid__: str = ""
    __epocagrid_ED50_Roma40__ = ""
    __Fi_GEOID_0__: float = 0.0
    __La_GEOID_0__: float = 0.0

    def __init__(self, path: str):
        self.__Fname__ = path
        self.__FileObj__ = open(self.__Fname__, "r")
        self._load()
        self._Close()

    def _gets(self):
        self.__buffer__: str = self.__FileObj__.readline().strip()
        return self.__buffer__

    def _getf(self) -> float:
        return float(self._gets())

    # carica il file
    def _load(self):
        result = False
        # ~ Fi_SO_sist = float(35.)
        # ~ La_SO_sist = float(5.95233333333)
        # ~ Fi_SO_geoid = float(35.333333334)
        # ~ La_SO_geoid = float(6.)
        self.__tipogrid__ = self._gets()
        self.__epocagrid_ED50_Roma40__ = self._gets()
        for I in range(0, 6):
            for J in range(0, 6):
                self.__Fi_ED50_Roma40_Foglio__[I][J] = self._getf()
        for I in range(0, 6):
            for J in range(0, 6):
                self.__La_ED50_Roma40_Foglio__[I][J] = self._getf()
        self.__epocagrid_WGS84_Roma40__ = self._gets()
        for I in range(0, 6):
            for J in range(0, 6):
                self.__Fi_WGS84_Roma40_Foglio__[I][J] = self._getf()
        for I in range(0, 6):
            for J in range(0, 6):
                self.__La_WGS84_Roma40_Foglio__[I][J] = self._getf()
        self.__Fi_SIST_0__ = self._getf()
        self.__La_SIST_0__ = self._getf()
        self.__epocageoide__ = self._gets()
        for I in range(0, 10):
            for J in range(0, 14):
                self.__N_Foglio__[I][J] = self._getf()
        self.__Fi_GEOID_0__ = self._getf()
        self.__La_GEOID_0__ = self._getf()

    # Chiude il file
    def _Close(self):
        self.__FileObj__.close()
        self.__FileObj__ = None

    @property
    def Fi_ED50_Roma40(self):
        return self.__Fi_ED50_Roma40_Foglio__

    @property
    def La_ED50_Roma40(self):
        return self.__La_ED50_Roma40_Foglio__

    @property
    def Fi_WGS84_Roma40(self):
        return self.__Fi_WGS84_Roma40_Foglio__

    @property
    def La_WGS84_Roma40(self) -> np.ndarray:
        return self.__La_WGS84_Roma40_Foglio__

    @property
    def N_Foglio(self) -> np.ndarray:
        return self.__N_Foglio__

    @property
    def Fi_SIST_NE(self) -> float:
        # PASSO DELLE GRIGLIE FI =
        # le 4 griglie sistemi sono 6X6 in Roma40 sessadecimali con passo 5' * 7'30"
        return self.__Fi_SIST_0__ + (5. * 5./60.)

    @property
    def La_SIST_NE(self) -> float:
        return self.__La_SIST_0__ + (5. * 7.5/60.)

    @property
    def Fi_SIST_SO(self) -> float:
        return self.__Fi_SIST_0__

    @property
    def La_SIST_SO(self):
        return self.__La_SIST_0__

    def __str__(self):
        return "Grigliato\t%s\tSO <Fi,La>\t<\t%f,\t%f\t>\tNE <Fi,La>\t<\t%f,\t%f\t> " % (self.__Fname__, self.Fi_SIST_SO, self.La_SIST_SO, self.Fi_SIST_NE, self.La_SIST_NE)

    @property
    def epocageoide(self) -> str:
        return self.__epocageoide__

    @property
    def epocagrid_WGS84_Roma40(self) -> str:
        return self.__epocagrid_WGS84_Roma40__

    @property
    def tipogrid(self) -> str:
        return self.__tipogrid__

    @property
    def epocagrid_ED50_Roma40(self) -> str:
        return self.__epocagrid_ED50_Roma40__

    @property
    def Fi_GEOID_0(self) -> float:
        return self.__Fi_GEOID_0__

    @property
    def La_GEOID_0(self) -> float:
        return self.__La_GEOID_0__


# costanti per griglie sistemi
sisED50_Roma40: str = "ED50_Roma40"
sisWGS84_Roma40: str = "WGS84_Roma40"
# costanti per datum
ED50: str = "ED50"
WGS84: str = "WGS84"
ROMA40: str = "Roma40"


def sec_to_prime(s: float) -> float:
    return s/60.0


def sec_to_deg(s: float) -> float:
    return s/3600.0


def prime_to_sec(p: float) -> float:
    return p*60.0


def prime_to_deg(p: float) -> float:
    return p/60.0


class Grigliato (object):
    """Classe di gestione del grigliato per l'italia intera"""
    # __Fi_SO_sist__=float(0.0)
    # __La_SO_sist__=float(0.0)
    # Dim Fi_SO_geoid, La_SO_geoid As Double
    # __Fi_SO_geoid__=float(0.0)
    # __La_SO_geoid__=float(0.0)
    # Public Fi_ED50_Roma40(153, 109), La_ED50_Roma40(153, 109), Fi_WGS84_Roma40(153, 109), La_WGS84_Roma40(153, 109), N(381, 406) As Double
    # Public Fi_ED50_Roma40_Foglio(6, 6), La_ED50_Roma40_Foglio(6, 6), Fi_WGS84_Roma40_Foglio(6, 6), La_WGS84_Roma40_Foglio(6, 6), N_Foglio(10, 14) As Double
    # Public Fi_SIST_0, La_SIST_0, Fi_GEOID_0, La_GEOID_0 As Double
    #__Fi_ED50_Roma40__=np.zeros((153,109), np.float64)
    #__La_ED50_Roma40__=np.zeros((153,109), np.float64)
    #__Fi_WGS84_Roma40__=np.zeros((153,109), np.float64)
    #__La_WGS84_Roma40__=np.zeros((153,109), np.float64)

    def __init__(self, path:str):
        """
per come sono messi i dati, prima i valori di un singolo foglio sono
caricate nelle variabili temporanee di foglio,
poi vengono ricaricati in quelle generali
GRIGLIA SISTEMI     Sud  35°                  Nord    47°.666666666667
                    Ovest  5°.95233333333     Est     19°.452333333333
le 4 griglie sistemi sono in Roma40 sessadecimali con passo 5' * 7'30"
GRIGLIA GEOIDE      Sud  35° .33334           Nord    47°.26666
                    Ovest  6°                 Est     18°.99987
la griglia geoide è in WGS84 sessadecimali con passo 2' * 2'
ATTENZIONE a come sono disposte le griglie, che sono diverse:
quella sistemi ha il primo nodo in basso a sx, quella geoide in alto a sx
"""
        self.__Fi_SO_sist__ = float(35.)
        self.__La_SO_sist__ = float(5.95233333333)
        # ~ self.__La_SO_sist__ = float(5.9333333333333333333333)
        self.__Fi_SO_geoid__ = float(35.333333334)
        self.__La_SO_geoid__ = float(6.)
        self.__Fi_ED50_Roma40__ = np.zeros((153, 109), np.float64)
        self.__La_ED50_Roma40__ = np.zeros((153, 109), np.float64)
        self.__Fi_WGS84_Roma40__ = np.zeros((153, 109), np.float64)
        self.__La_WGS84_Roma40__ = np.zeros((153, 109), np.float64)
        # inizializzo gli array ad un valore di default
        val = 0.00000
        self.__Fi_ED50_Roma40__.fill(val)
        self.__La_ED50_Roma40__.fill(val)
        self.__Fi_WGS84_Roma40__.fill(val)
        self.__La_WGS84_Roma40__.fill(val)

        self.__FiIncPrim__ = 5.0  # cell spacing is 5 minutes
        self.__LaIncPrim__ = 7.5  # cell spacing is 7'30"

        self.__FiIncSecs__ = self.__FiIncPrim__ * 60.0  # cell spacing is 5 minutes
        self.__LaIncSecs__ = self.__LaIncPrim__ * 60.0  # cell spacing is 7'30"

        self.__FiIncDeg__ = self.__FiIncPrim__ / 60.  # cell spacing is 5 minutes
        self.__LaIncDeg__ = self.__LaIncPrim__ / 60.  # cell spacing is 7'30"

        self.__Fi_SO_VAL__ = float(0.0)
        self.__La_SO_VAL__ = float(0.0)
        self.__Fi_NE_VAL__ = float(0.0)
        self.__La_NE_VAL__ = float(0.0)
        self.__epocagrid_WGS84_Roma40__ = "222"
        self.__epocagrid_ED50_Roma40__ = "222"
        self.__N__ = np.zeros((381, 406), np.float64)
        self.path = path
        list = os.listdir(path)
        for fname in list:
            if fname.endswith('gr1') or fname.endswith('gr2'):
                self._add_gr(self.path+os.sep+fname)

    def Cella(self, i: int, j: int, From: str, To: str):
        """
Restitusce i valori di shift sigmafi e sigmalambda per una cella di
un grigliato sistemi        """
        if From == ED50 and To == WGS84:
            sFi = (-self.__Fi_ED50_Roma40__[i][j]) + \
                (self.__Fi_WGS84_Roma40__[i][j])
            sLa = (-self.__La_ED50_Roma40__[i][j]) + \
                (self.__Fi_WGS84_Roma40__[i][j])
        elif From == ED50 and To == ROMA40:
            sFi = -1.*self.__Fi_ED50_Roma40__[i][j]
            sLa = -1.*self.__La_ED50_Roma40__[i][j]
            pass
        elif From == ROMA40 and To == WGS84:
            sFi = self.__Fi_WGS84_Roma40__[i][j]
            sLa = self.__La_WGS84_Roma40__[i][j]
        elif From == ROMA40 and To == ED50:
            sFi = self.__Fi_ED50_Roma40__[i][j]
            sLa = self.__La_ED50_Roma40__[i][j]
        elif From == WGS84 and To == ROMA40:
            sFi = -1*self.__Fi_WGS84_Roma40__[i][j]
            sLa = -1.*self.__La_WGS84_Roma40__[i][j]
        elif From == WGS84 and To == ED50:
            sFi = (self.__Fi_ED50_Roma40__[i][j]) + \
                (-self.__Fi_WGS84_Roma40__[i][j])
            sLa = (self.__La_ED50_Roma40__[i][j]) + \
                (-self.__Fi_WGS84_Roma40__[i][j])

        return sFi, sLa

    def interpola_shift(self, FiP: float, LaP: float, From: str, To: str) -> tuple[float, float]:
        """ restitusce i valori di shift interpolati (bileneare) da un grigliato
per un punto P di coordinate FiP LaP espressi in gradi sessagesimali.
Il Grigliato è identificato da identificato sist"""
        r, c = self.row_col_for_fi_la(FiP, LaP)
        FiA, LaA = self.fi_lambda_for_row_col(r, c)
        # I valori di shift della 4 celle contigue a P
        sFiA, sLaA = self.Cella(r, c, From, To)
        sFiB, sLaB = self.Cella(r+1, c, From, To)
        sFiC, sLaC = self.Cella(r, c+1, From, To)
        sFiD, sLaD = self.Cella(r+1, c+1, From, To)
        # pesi relativi alla posizione
        X = abs(FiP-FiA)/self.__FiIncDeg__
        Y = abs(LaP-LaA)/self.__LaIncDeg__
        # ~ X=(FiP-FiA)/self.__FiIncSecs__
        # ~ Y=(LaP-LaA)/self.__LaIncSecs__
        # parametri
        # Formula alternativa
        ###a0=f00 (A)
        ###a1=f10-f00 (B-A)
        ###a2=f01-f00 (C-A)
        ###a3=f00-f10-f01+f11 (A-B-C+D)
        a0Fi = sFiA
        a0La = sLaA
        a1Fi = sFiB-sFiA
        a1La = sLaB-sLaA
        a2Fi = sFiC-sFiA
        a2La = sLaC-sLaA
        a3Fi = sFiA-sFiB-sFiC+sFiD
        a3La = sLaA-sLaB-sLaC+sLaD
        ########################################

        # ~ a0Fi=sFiA
        # ~ a0La=sLaA
        # ~ a1Fi=sFiB-sFiA
        # ~ a1La=sLaB-sLaA
        # ~ a2Fi=sFiD-sFiA
        # ~ a2La=sLaD-sLaA
        # ~ a3Fi=sFiA+sFiC-sFiB-sFiD
        # ~ a3La=sLaA+sLaC-sLaB-sLaD
        # caloclo dello shift interpolato
        sFiP = a0Fi+(a1Fi*X)+(a2Fi*Y)+(a3Fi*X*Y)
        sLaP = a0La+(a1La*X)+(a2La*Y)+(a3La*X*Y)
        return sFiP, sLaP

    def get_shift_secs(self, FiP: float, LaP: float, From: str, To: str) -> tuple[float, float]:
        """Reperisce le informazioni di shift a partire da Fi Lambda espressi in secondi"""
        return self.get_shift(self.sec_to_deg(FiP), self.sec_to_deg(LaP), From, To)

    def get_shift(self, FiP: float, LaP: float, From: str, To: str) -> tuple[float, float]:
        """Reperisce le informazioni di shift a partire da Fi Lambda espressi in gradi"""
        sFiP1 = float(0.0)
        sLaP1 = float(0.0)
        if From != ROMA40:
            for i in range(1, 5, 1):
                sFiP2, sLaP2 = self.interpola_shift(
                    FiP+sec_to_deg(sFiP1), LaP+sec_to_deg(sLaP1), From, To)
                DF = sFiP1-sFiP2
                DL = sLaP1-sLaP2
                sFiP1, sLaP1 = sFiP2, sLaP2
        else:
            sFiP2, sLaP2 = self.interpola_shift(FiP, LaP, From, To)
        return sFiP2, sLaP2

    def fi_lambda_for_row_col(self, i: int, j: int) -> tuple[float, float]:
        """restitisce le coordinate fi lambda di una cella  di riga i e colonna j"""
        Fi = self.__Fi_SO_sist__ + (i*self.__FiIncDeg__)
        La = self.__La_SO_sist__ + (j*self.__LaIncDeg__)
        return Fi, La

    def row_col_for_fi_la(self, Fi: float, La: float) -> tuple[int, int]:
        """restitisce riga e colonna per un punto di coordinate fi lambda """
        iS = int(math.floor(
            (float(Fi) - self.__Fi_SO_sist__ + 0.00000001) / self.__FiIncDeg__))
        jS = int(math.floor(
            (float(La) - self.__La_SO_sist__ + 0.00000001) / self.__LaIncDeg__))

        return iS, jS

    def _add_gr(self, path: str):
        """Aggiunge un gr1/2 al grigliato"""
        gr = GrFile(path)
        self.__epocagrid_ED50_Roma40__ = gr.epocagrid_ED50_Roma40
        self.__epocagrid_WGS84_Roma40__ = gr.epocagrid_WGS84_Roma40
        # print gr
        # stesso ciclo della sub originale
        # spostamento in quelle generali unitarie per tutta l'Italia
        # Dim i0_S, j0_S  As Long
        # xxxi=gr.Fi_SIST_SO
        # ~ i0_S = math.floor((gr.Fi_SIST_SO - self.__Fi_SO_sist__ + 0.00000001) * 60 / 5)
        # ~ j0_S = math.floor((gr.La_SIST_SO - self.__La_SO_sist__ + 0.00000001) * 60 / 7.5)
        i0_S, j0_S = self.row_col_for_fi_la(gr.Fi_SIST_SO, gr.La_SIST_SO)
        # ~ print "%s FI<%f> La<%f> R<%d> C<%d> " %(gr.__Fname__ ,gr.Fi_SIST_SO,gr.La_SIST_SO,i0_S ,j0_S)
        for I in range(0, 6):
            for J in range(0, 6):
                # HIC SUNT LEONES
                self.__Fi_ED50_Roma40__[
                    i0_S + I][j0_S + J] = gr.Fi_ED50_Roma40[I][J]
                self.__La_ED50_Roma40__[
                    i0_S + I][j0_S + J] = gr.La_ED50_Roma40[I][J]
                self.__Fi_WGS84_Roma40__[
                    i0_S + I][j0_S + J] = gr.Fi_WGS84_Roma40[I][J]
                self.__La_WGS84_Roma40__[
                    i0_S + I][j0_S + J] = gr.La_WGS84_Roma40[I][J]
        #   Dim i0_G, j0_G  As Long
        i0_G = math.floor(
            (gr.Fi_GEOID_0 - self.__Fi_SO_geoid__ + 0.00000001) * 60 / 2)
        j0_G = math.floor(
            (gr.La_GEOID_0 - self.__La_SO_geoid__ + 0.00000001) * 60 / 2)
        for I in range(0, 10):
            for J in range(0, 14):
                self.__N__[i0_G + I][j0_G + J] = gr.N_Foglio[9 - I][J]
        if self.__Fi_SO_VAL__ == 0.0 or self.__Fi_SO_VAL__ > gr.Fi_SIST_SO:
            self.__Fi_SO_VAL__ = gr.Fi_SIST_SO
        if self.__La_SO_VAL__ == 0.0 or self.__La_SO_VAL__ > gr.La_SIST_SO:
            self.__La_SO_VAL__ = gr.La_SIST_SO

        if self.__Fi_NE_VAL__ == 0.0 or self.__Fi_NE_VAL__ < gr.Fi_SIST_NE:
            self.__Fi_NE_VAL__ = gr.Fi_SIST_NE
        if self.__La_NE_VAL__ == 0.0 or self.__La_NE_VAL__ < gr.La_SIST_NE:
            self.__La_NE_VAL__ = gr.La_SIST_NE

    @staticmethod
    def sec_to_prime(s: float) -> float:
        return s/60.0

    @staticmethod
    def sec_to_deg(s: float) -> float:
        return s/3600.0

    @staticmethod
    def prime_to_sec(p: float) -> float:
        return p*60.0

    @staticmethod
    def prime_to_deg(p: float) -> float:
        return p/60.0

    @staticmethod
    def deg_to_prime(g: float) -> float:
        return g*60.0

    @staticmethod
    def deg_to_sec(g: float) -> float:
        return g*3600.0

    @property
    def ED50(self) -> str:
        return ED50

    @property
    def WGS84(self) -> str:
        return WGS84

    @property
    def Roma40(self) -> str:
        return ROMA40

    @property
    def epocagrid_ED50_Roma40(self):
        return self.__epocagrid_ED50_Roma40__

    @property
    def epocagrid_WGS84_Roma40(self):
        return self.__epocagrid_WGS84_Roma40__

    @property
    def Fi_ED50_Roma40(self):
        return self.__Fi_ED50_Roma40__

    @property
    def La_ED50_Roma40(self):
        return self.__La_ED50_Roma40__

    @property
    def Fi_WGS84_Roma40(self):
        return self.__Fi_WGS84_Roma40__

    @property
    def La_WGS84_Roma40(self):
        return self.__La_WGS84_Roma40__

    @property
    def N(self):
        return self.__N__

    @property
    def Fi_SO_VAL(self):
        return self.__Fi_SO_VAL__

    @property
    def La_SO_VAL(self):
        return self.__La_SO_VAL__

    @property
    def Fi_NE_VAL(self):
        return self.__Fi_NE_VAL__

    @property
    def La_NE_VAL(self):
        return self.__La_NE_VAL__


def do_test(c1, LatRm, LongRm, c2, latverto, lonverto, gr):
    SLatW, SLongW = gr.get_shift(LatRm, LongRm, gr.Roma40, gr.WGS84)

    LatW = LatRm + gr.sec_to_deg(SLatW)
    LongW = LongRm + gr.sec_to_deg(SLongW)
    vertodeltaFI = (latverto-LatRm)*3600.0
    vertodeltaLA = (lonverto-LongRm)*3600.0
    deltaFI = (LatW - latverto)*3600.0
    deltaLA = (LongW - lonverto)*3600.0

    print("___________________________________________________")
    print("%d Input %f %f" % (c1, LatRm, LongRm))
    print("scarto in secondi Fi<%f>  Lambda <%f>" % (deltaFI,   deltaLA))
    print("paramtre GRID Fi<%f>  Lambda <%f>" % (SLatW, SLongW))
    print("paramtre Verto Fi<%f>  Lambda <%f>" %
          (vertodeltaFI,   vertodeltaLA))
    print("===================================================")


def test(grid):
    do_test(136016,	46.33333333,	7.952333333, 136016,
           46.334031322,    7.951942411, grid)
    do_test(136017,	46.33333333,	8.077333333, 136017,
           46.334030983,    8.076950619, grid)

    #~ do_test(136016,  46.33333333,7.933333333,136016,46.334031378,7.932941101,grid)

    #~ do_test(136017,	46.33333333,8.058333333, 136017,46.334031034,8.057949371 ,grid)
    #~ do_test(137016,	46.41666667,7.933333333, 137016,46.417367791,7.932941088 ,grid)
    #~ do_test(137017,	46.41666667,8.058333333, 137017,46.417367493,8.057949363 ,grid)

    #~ do_test(109012, 44.083333, 7.452333,	109012,44.083967919, 7.451911000 ,grid)
    #~ do_test(109013, 44.083333, 7.577333,	109013,44.083967531, 7.576918978 ,grid)
    #~ do_test(109014, 44.083333, 7.702333,	109014,44.083967619, 7.701926211 ,grid)
    #~ do_test(109015, 44.083333, 7.827333,	109015,44.083968164, 7.826933225 ,grid)
    #~ do_test(109016, 44.083333, 7.952333,	109016,44.083967814, 7.951940586 ,grid)
    #~ do_test(109017, 44.083333, 8.077333,	109017,44.083967308, 8.076947783 ,grid)
    #~ do_test(109018, 44.083333, 8.202333,	109018,44.083967072, 8.201954956 ,grid)
    # ~ print"###################################################################"

    do_test(1, 45.07044834, 7.686152184, 1, 45.071112089, 7.685736261, grid)
    do_test(2, 45.36187452, 7.768697395, 2, 45.362545321, 7.768286494, grid)
    do_test(3, 44.91636897, 7.489495721, 3, 44.917027456, 7.489067924, grid)
    do_test(4, 45.31485555, 7.305264601, 4, 45.315524766, 7.304828627, grid)
    do_test(5, 45.31098157, 7.258883484, 5, 45.311650613, 7.258444833, grid)
    do_test(6, 45.43315695, 7.94906053, 6, 45.433830714, 7.948662020, grid)
    do_test(7, 45.38298891, 7.711682128, 7, 45.383660019, 7.711268612, grid)
    do_test(8, 45.43290414, 7.739681444, 8, 45.433576650, 7.739270474, grid)
    do_test(9, 45.11835412, 7.397114101, 9, 45.119019143, 7.396681651, grid)
    do_test(10, 45.11417091, 7.412839497, 10, 45.114835920, 7.412407805, grid)
    do_test(11, 45.42575886, 7.578755284, 11, 45.426430600, 7.578336099, grid)
    do_test(12, 45.09584053, 7.526500154, 12, 45.096505344, 7.526075642, grid)
    do_test(13, 45.03694603, 7.867907494, 13, 45.037609869, 7.867502283, grid)
    do_test(14, 45.48914664, 7.804579706, 14, 45.489821046, 7.804173481, grid)
    do_test(15, 44.84158423, 7.226533242, 15, 44.842240515, 7.226095434, grid)
    do_test(16, 45.04316602, 7.903120501, 16, 45.043830382, 7.902717468, grid)
    do_test(17, 45.07990252, 7.393895928, 17, 45.080566556, 7.393463197, grid)
    do_test(18, 45.42398803, 7.995045022, 18, 45.424661791, 7.994649018, grid)
    do_test(19, 45.38485553, 7.756562208, 19, 45.385526869, 7.756151131, grid)
    do_test(20, 45.27565601, 7.521552824, 20, 45.276324539, 7.521128003, grid)
    do_test(21, 45.06818985, 7.817569418, 21, 45.068854152, 7.817161127, grid)
    do_test(22, 45.41032882, 7.745247199, 22, 45.411000756, 7.744836037, grid)
    do_test(23, 45.38298891, 7.711682128, 23, 45.383660019, 7.711268612, grid)
    do_test(24, 45.30146078, 7.218541092, 24, 45.302129507, 7.218100115, grid)
    do_test(25, 45.46029996, 7.858815733, 25, 45.460973895, 7.858412060, grid)
    do_test(26, 45.29025241, 7.629337218, 26, 45.290921239, 7.628918064, grid)
    do_test(27, 45.07958393, 6.697103872, 27, 45.080247403, 6.696639027, grid)
    do_test(28, 45.0604229, 6.68459631, 28, 45.061085905, 6.684131007, grid)
    do_test(29, 45.07142677, 6.722200802, 29, 45.072089945, 6.721737269, grid)
    do_test(30, 45.11264616, 6.745737044, 30, 45.113310325, 6.745274319, grid)
    do_test(31, 45.32612976, 7.870944131, 31, 45.326800166, 7.870538722, grid)
    do_test(32, 45.02126443, 7.57832419, 32, 45.021926822, 7.577902821, grid)
    do_test(33, 44.80012373, 7.287434127, 33, 44.800778811, 7.286998651, grid)
    do_test(34, 44.80807248, 7.115932517, 34, 44.808728004, 7.115491209, grid)
    do_test(35, 45.47326167, 7.941734425, 35, 45.473936564, 7.941336176, grid)
    do_test(36, 45.14974722, 7.659111428, 36, 45.150413090, 7.658693868, grid)
    do_test(37, 45.41797167, 7.641496072, 37, 45.418643414, 7.641079779, grid)
    do_test(38, 45.48914664, 7.804579706, 38, 45.489821046, 7.804173481, grid)
    do_test(39, 45.48914664, 7.804579706, 39, 45.489821046, 7.804173481, grid)
    do_test(40, 45.35965384, 7.987671681, 40, 45.360325899, 7.987274452, grid)
    do_test(41, 45.12251073, 7.243588403, 41, 45.123175008, 7.243148733, grid)
    do_test(42, 45.26767691, 7.765715306, 42, 45.268345447, 7.765302802, grid)
    do_test(43, 45.17685106, 7.844045319, 43, 45.177518066, 7.843637599, grid)
    do_test(44, 44.82684471, 7.304102616, 44, 44.827500497, 7.303667387, grid)
    do_test(45, 45.48914664, 7.804579706, 45, 45.489821046, 7.804173481, grid)
    do_test(46, 45.49405534, 7.778176606, 46, 45.494729730, 7.777769070, grid)
    do_test(47, 45.52278252, 7.642142266, 47, 45.523456993, 7.641728305, grid)
    do_test(50, 45.01973746, 7.467866002, 50, 45.020399783, 7.467437097, grid)
    do_test(53, 45.14433198, 7.198142517, 53, 45.144996578, 7.197700638, grid)
    do_test(54, 44.87300937, 7.412768434, 54, 44.873666376, 7.412336862, grid)
    do_test(55, 45.47326167, 7.941734425, 55, 45.473936564, 7.941336176, grid)
    do_test(56, 45.32869833, 7.655690804, 56, 45.329368015, 7.655273416, grid)
    do_test(57, 45.13650388, 7.149380889, 57, 45.137168059, 7.148936769, grid)
    do_test(58, 45.14068148, 7.117030154, 58, 45.141345619, 7.116584465, grid)
    do_test(59, 45.0669538, 7.437257973, 59, 45.067617663, 7.436827320, grid)
    do_test(60, 45.24458661, 7.51826253, 60, 45.245254528, 7.517837189, grid)
    do_test(61, 45.23419734, 7.507578039, 61, 45.234865070, 7.507152120, grid)
    do_test(62, 45.30762805, 7.892228568, 62, 45.308298194, 7.891824430, grid)
    do_test(63, 44.97179927, 7.779679103, 63, 44.972460342, 7.779268450, grid)
    do_test(64, 45.52474111, 7.512380519, 64, 45.525415125, 7.511960241, grid)
    do_test(65, 45.52474111, 7.512380519, 65, 45.525415125, 7.511960241, grid)
    do_test(66, 44.79976916, 7.325399802, 66, 44.800424195, 7.324965564, grid)
    do_test(67, 44.80760547, 7.301115888, 67, 44.808260740, 7.300680775, grid)
    do_test(68, 45.33212641, 7.883598109, 68, 45.332797044, 7.883193669, grid)
    do_test(69, 45.30762805, 7.892228568, 69, 45.308298194, 7.891824430, grid)
    do_test(70, 44.9586183, 7.601050812, 70, 44.959278380, 7.600630051, grid)
    do_test(71, 45.39186582, 7.648780061, 71, 45.392536970, 7.648363585, grid)
    do_test(72, 44.93845156, 7.332772659, 72, 44.939110784, 7.332337555, grid)
    do_test(73, 45.34339337, 7.379942568, 73, 45.344063259, 7.379511159, grid)
    do_test(74, 45.08337515, 7.331158365, 74, 45.084038906, 7.330722613, grid)
    do_test(75, 45.40050809, 7.966389016, 75, 45.401181057, 7.965991037, grid)
    do_test(76, 45.39125384, 7.959764467, 76, 45.391926529, 7.959365996, grid)
    do_test(77, 45.48914664, 7.804579706, 77, 45.489821046, 7.804173481, grid)
    do_test(78, 44.90637702, 7.675654212, 78, 44.907035198, 7.675237391, grid)
    do_test(79, 44.84548745, 7.717770461, 79, 44.846143589, 7.717356417, grid)
    do_test(80, 45.13046132, 7.937923921, 80, 45.131128222, 7.937522899, grid)
    do_test(81, 45.48914664, 7.804579706, 81, 45.489821046, 7.804173481, grid)
    do_test(82, 45.17681329, 7.648063285, 82, 45.177479794, 7.647645007, grid)
    do_test(83, 45.1063597, 7.481780036, 83, 45.107024754, 7.481352321, grid)
    do_test(84, 45.16083973, 7.885364451, 84, 45.161506791, 7.884959682, grid)
    do_test(85, 44.89877499, 7.566689981, 85, 44.899432848, 7.566266962, grid)
    do_test(86, 45.43290414, 7.739681444, 86, 45.433576650, 7.739270474, grid)
    do_test(87, 45.38298891, 7.711682128, 87, 45.383660019, 7.711268612, grid)
    do_test(88, 45.38298891, 7.711682128, 88, 45.383660019, 7.711268612, grid)
    do_test(89, 45.38298891, 7.711682128, 89, 45.383660019, 7.711268612, grid)
    do_test(90, 45.43955443, 7.663973611, 90, 45.440226801, 7.663558907, grid)
    do_test(91, 45.43955443, 7.663973611, 91, 45.440226801, 7.663558907, grid)
    do_test(92, 45.43955443, 7.663973611, 92, 45.440226801, 7.663558907, grid)
    do_test(93, 45.11526661, 7.812375574, 93, 45.115932050, 7.811966602, grid)
    do_test(94, 45.14910341, 8.036321956, 94, 45.149771144, 8.035926282, grid)
    do_test(95, 44.78411115, 7.373101917, 95, 44.784765623, 7.372669684, grid)
    do_test(96, 44.85994889, 7.503767271, 96, 44.860605344, 7.503340395, grid)
    do_test(97, 45.31207542, 7.390599846, 97, 45.312744654, 7.390168602, grid)
    do_test(98, 45.42730414, 7.201061998, 98, 45.427976002, 7.200620403, grid)
    do_test(99, 44.93463527, 6.817729437, 99, 44.935294684, 6.817272107, grid)
    do_test(100, 44.95391696, 6.795274323, 100, 44.954576909, 6.794815631, grid)
    do_test(101, 44.9966032, 6.795241772, 101, 44.997264231, 6.794782633, grid)
    do_test(102, 44.97995211, 6.801882223, 102, 44.980612703, 6.801423596, grid)
    do_test(103, 44.96848868, 6.801611094, 103, 44.969148983, 6.801152574, grid)
    do_test(104, 44.98185982, 6.811992322, 104, 44.982520435, 6.811534190, grid)
    do_test(105, 44.91986777, 6.825952881, 105, 44.920526797, 6.825496138, grid)
    do_test(106, 45.3627433, 7.343315806, 106, 45.363413614, 7.342882592, grid)
    do_test(107, 45.14769543, 7.169127157, 107, 45.148359982, 7.168683873, grid)
    do_test(108, 45.48914664, 7.804579706, 108, 45.489821046, 7.804173481, grid)
    do_test(109, 45.01241604, 7.826551092, 109, 45.013078771, 7.826143347, grid)
    do_test(110, 45.41797167, 7.641496072, 110, 45.418643414, 7.641079779, grid)
    do_test(111, 45.1192559, 6.983351295, 111, 45.119919461, 6.982899744, grid)
    do_test(112, 45.10027258, 7.328905926, 112, 45.100936756, 7.328470088, grid)
    do_test(113, 45.189665, 7.889828371, 113, 45.190332669, 7.889423709, grid)
    do_test(114, 45.32755889, 7.760338274, 114, 45.328228799, 7.759926267, grid)
    do_test(115, 45.43955443, 7.663973611, 115, 45.440226801, 7.663558907, grid)
    do_test(116, 45.09483745, 7.925526622, 116, 45.095503477, 7.925125043, grid)
    do_test(117, 45.23514437, 7.602615223, 117, 45.235812057, 7.602194343, grid)
    do_test(118, 44.93229318, 6.728282685, 118, 44.932952716, 6.727820751, grid)
    do_test(119, 45.30017108, 7.462238886, 119, 45.300840122, 7.461811374, grid)
    do_test(120, 45.05064159, 7.304476339, 120, 45.051304221, 7.304039578, grid)
    do_test(121, 45.0855028, 7.575713026, 121, 45.086167385, 7.575292172, grid)
    do_test(122, 45.43955443, 7.663973611, 122, 45.440226801, 7.663558907, grid)
    do_test(123, 45.43817159, 7.797480834, 123, 45.438844529, 7.797073091, grid)
    do_test(124, 45.11512155, 7.310991499, 124, 45.115786009, 7.310554873, grid)
    do_test(125, 45.1316643, 7.277948983, 125, 45.132329004, 7.277510849, grid)
    do_test(126, 45.13510605, 7.294708564, 126, 45.135770935, 7.294271195, grid)
    do_test(127, 45.31222525, 7.534041692, 127, 45.312894504, 7.533618000, grid)
    do_test(128, 45.38762524, 7.994240826, 128, 45.388298047, 7.993844302, grid)
    do_test(129, 45.36027835, 7.815840381, 129, 45.360949284, 7.815431960, grid)
    do_test(130, 45.33583525, 7.795958321, 130, 45.336505474, 7.795548330, grid)
    do_test(131, 44.98300539, 7.376260356, 131, 44.983666180, 7.375826965, grid)
    do_test(132, 44.94950584, 7.375357323, 132, 44.950165475, 7.374923983, grid)
    do_test(133, 45.39186582, 7.648780061, 133, 45.392536970, 7.648363585, grid)
    do_test(134, 45.39186582, 7.648780061, 134, 45.392536970, 7.648363585, grid)
    do_test(135, 45.39186582, 7.648780061, 135, 45.392536970, 7.648363585, grid)
    do_test(136, 45.13554424, 7.574113733, 136, 45.136209962, 7.573692222, grid)
    do_test(137, 45.09493848, 6.916953339, 137, 45.095601597, 6.916498997, grid)
    do_test(138, 45.33167775, 7.690877269, 138, 45.332347549, 7.690461669, grid)
    do_test(139, 45.03425727, 7.05272283, 139, 45.034918665, 7.052275702, grid)
    do_test(140, 45.02469192, 7.087338632, 140, 45.025353074, 7.086893222, grid)
    do_test(141, 45.20450253, 6.982780956, 141, 45.205168231, 6.982328489, grid)
    do_test(142, 45.21592195, 7.521425846, 142, 45.216589324, 7.521000686, grid)
    do_test(143, 45.48914664, 7.804579706, 143, 45.489821046, 7.804173481, grid)
    do_test(144, 45.27407544, 7.823596164, 144, 45.274744279, 7.823186708, grid)
    do_test(145, 45.34710694, 7.585230771, 145, 45.347776930, 7.584810217, grid)
    do_test(146, 45.43475665, 7.605680025, 146, 45.435428700, 7.605262365, grid)
    do_test(147, 45.28014356, 7.663282751, 147, 45.280812193, 7.662865186, grid)
    do_test(148, 44.93415038, 7.348070769, 148, 44.934809472, 7.347636328, grid)
    do_test(149, 44.83638462, 7.374986371, 149, 44.837040496, 7.374553529, grid)
    do_test(150, 45.09668166, 7.842712276, 150, 45.097346909, 7.842305384, grid)
    do_test(151, 45.09668166, 7.842712276, 151, 45.097346909, 7.842305384, grid)
    do_test(152, 45.12999134, 7.852671349, 152, 45.130657420, 7.852264720, grid)
    do_test(153, 45.26291593, 7.468990473, 153, 45.263584245, 7.468562751, grid)
    do_test(154, 45.14132339, 7.015971942, 154, 45.141987448, 7.015521591, grid)
    do_test(155, 45.04142836, 7.352319764, 155, 45.042090942, 7.351885135, grid)
    do_test(156, 45.16013889, 7.498671348, 156, 45.160805188, 7.498244794, grid)
    do_test(157, 45.12357455, 8.021991214, 157, 45.124241637, 8.021594769, grid)
    do_test(158, 45.36753169, 7.259066894, 158, 45.368202095, 7.258628639, grid)
    do_test(159, 45.36725528, 7.305923669, 159, 45.367925693, 7.305488277, grid)
    do_test(160, 45.36406202, 7.222510806, 160, 45.364732328, 7.222070298, grid)
    do_test(161, 45.25794532, 7.55792586, 161, 45.258613467, 7.557502690, grid)
    do_test(162, 45.06253775, 7.578348916, 162, 45.063201566, 7.577928015, grid)
    do_test(164, 44.94001841, 7.218149816, 164, 44.940677510, 7.217710683, grid)
    do_test(166, 45.38298891, 7.711682128, 166, 45.383660019, 7.711268612, grid)
    do_test(167, 45.46697918, 7.874425325, 167, 45.467653417, 7.874022766, grid)
    do_test(168, 45.18203598, 7.523291184, 168, 45.182702713, 7.522866153, grid)
    do_test(169, 44.95581805, 7.665185256, 169, 44.956477982, 7.664767855, grid)
    do_test(170, 45.26955557, 7.480402762, 170, 45.270224006, 7.479975729, grid)
    do_test(171, 45.15221307, 7.988924904, 171, 45.152880702, 7.988526678, grid)
    do_test(172, 45.13027847, 7.987245791, 172, 45.130945610, 7.986847537, grid)
    do_test(173, 45.18434774, 7.713883071, 173, 45.185014358, 7.713468024, grid)
    do_test(174, 45.22744732, 7.293269391, 174, 45.228114465, 7.292832154, grid)
    do_test(175, 45.48914664, 7.804579706, 175, 45.489821046, 7.804173481, grid)
    do_test(176, 45.31765971, 7.606967816, 176, 45.318329097, 7.606547866, grid)
    do_test(177, 45.41672808, 7.460422001, 177, 45.417399452, 7.459996662, grid)
    do_test(178, 45.23504301, 7.739190186, 178, 45.235710763, 7.738776201, grid)
    do_test(179, 44.84134164, 7.635546613, 179, 44.841997433, 7.635127688, grid)
    do_test(180, 45.43817087, 7.79748085, 180, 45.438843809, 7.797073107, grid)
    do_test(181, 45.38298891, 7.711682128, 181, 45.383660019, 7.711268612, grid)
    do_test(182, 45.49405534, 7.778176606, 182, 45.494729730, 7.777769070, grid)
    do_test(183, 44.80795584, 7.245997808, 183, 44.808611174, 7.245560917, grid)
    do_test(184, 44.81881031, 7.258043949, 184, 44.819465928, 7.257607345, grid)
    do_test(185, 44.77317612, 7.220014176, 185, 44.773830528, 7.219576722, grid)
    do_test(186, 44.80228019, 7.250284146, 186, 44.802935366, 7.249847444, grid)
    do_test(187, 45.31728413, 7.767335296, 187, 45.317953823, 7.766923524, grid)
    do_test(188, 44.85122823, 7.398956419, 188, 44.851884528, 7.398524401, grid)
    do_test(190, 45.05704518, 7.87449283, 190, 45.057709676, 7.874088058, grid)
    do_test(191, 45.061013, 7.879180567, 191, 45.061677659, 7.878776095, grid)
    do_test(192, 44.95062448, 7.035558031, 192, 44.951283823, 7.035111479, grid)
    do_test(193, 45.25902329, 7.542201455, 193, 45.259691471, 7.541777481, grid)
    do_test(194, 45.11722097, 7.115461774, 194, 45.117884521, 7.115016276, grid)
    do_test(195, 45.30359419, 7.939264157, 195, 45.304264606, 7.938863328, grid)
    do_test(196, 45.11905819, 7.069609908, 196, 45.119721636, 7.069162279, grid)
    do_test(197, 45.35577418, 7.883429224, 197, 45.356445428, 7.883025170, grid)
    do_test(198, 45.49405534, 7.778176606, 198, 45.494729730, 7.777769070, grid)
    do_test(199, 45.29135617, 7.395880656, 199, 45.292024980, 7.395449438, grid)
    do_test(200, 45.04545606, 7.921057955, 200, 45.046120664, 7.920656036, grid)
    do_test(201, 45.14422044, 7.063331498, 201, 45.144884506, 7.062883252, grid)
    do_test(202, 45.30092293, 7.440659484, 202, 45.301591980, 7.440230839, grid)
    do_test(203, 44.99952587, 7.684932614, 203, 45.000187311, 7.684516238, grid)
    do_test(204, 45.0182169, 7.7367231, 204, 45.018879158, 7.736309793, grid)
    #~ do_test(205,45.06510499,7.848402249,205,45.065769467,7.847995861,grid)
    #~ do_test(206,45.34070495,7.84383221,206,45.341375524,7.843425138,grid)
    #~ do_test(207,45.48914664,7.804579706,207,45.489821046,7.804173481,grid)
    #~ do_test(208,45.48914664,7.804579706,208,45.489821046,7.804173481,grid)
    #~ do_test(210,45.03807049,7.946338348,210,45.038735116,7.945937954,grid)
    #~ do_test(211,44.9955608,7.646293006,211,44.996222172,7.645874720,grid)
    #~ do_test(212,45.4761217,7.300120292,212,45.476794578,7.299685803,grid)
    #~ do_test(213,45.24319058,7.57337138,213,45.243858427,7.572948962,grid)
    #~ do_test(214,45.48914664,7.804579706,214,45.489821046,7.804173481,grid)
    #~ do_test(215,44.93391181,7.543725105,215,44.934570969,7.543300780,grid)
    #~ do_test(216,45.1886061,7.015510384,216,45.189271350,7.015059526,grid)
    #~ do_test(217,45.34065519,7.693366846,217,45.341325208,7.692951535,grid)
    #~ do_test(218,45.0066814,7.537670848,218,45.007343285,7.537246603,grid)
    #~ do_test(219,45.33104247,7.859879947,219,45.331712909,7.859473825,grid)
    #~ do_test(220,44.84795241,7.344101785,220,44.848608752,7.343667725,grid)
    #~ do_test(221,44.86911248,7.607690615,221,44.869769269,7.607270005,grid)
    #~ do_test(222,45.03660552,6.831314801,222,45.037267454,6.830857034,grid)
    #~ do_test(223,45.04160285,6.754535969,223,45.042265148,6.754074323,grid)
    #~ do_test(224,45.04381623,6.788465584,224,45.044478478,6.788005605,grid)
    #~ do_test(225,45.03660552,6.831314801,225,45.037267454,6.830857034,grid)
    #~ do_test(226,45.34903386,7.743062517,226,45.349704241,7.742649987,grid)
    #~ do_test(227,45.45675873,7.978890978,227,45.457433370,7.978494644,grid)
    #~ do_test(228,44.82987497,7.589782729,228,44.830530328,7.589361120,grid)
    #~ do_test(229,45.40973419,7.787390864,229,45.410406301,7.786981954,grid)
    #~ do_test(230,45.43817087,7.79748085,230,45.438843809,7.797073107,grid)
    #~ do_test(231,45.06828544,7.83514592,231,45.068949879,7.834738704,grid)
    #~ do_test(232,45.43580356,7.855941661,232,45.436476773,7.855537287,grid)
    #~ do_test(233,45.43290414,7.739681444,233,45.433576650,7.739270474,grid)
    #~ do_test(234,45.01603624,7.750177403,234,45.016698527,7.749764923,grid)
    #~ do_test(235,45.40934147,7.825536009,235,45.410013742,7.825129141,grid)
    #~ do_test(236,44.95633359,7.196117268,236,44.956993119,7.195677154,grid)
    #~ do_test(237,44.97930316,7.163242458,237,44.979963285,7.162800777,grid)
    #~ do_test(238,44.93653633,7.117890856,238,44.937195266,7.117448082,grid)
    #~ do_test(239,44.94173479,7.117818047,239,44.942393863,7.117375187,grid)
    #~ do_test(240,44.94340575,7.126671413,240,44.944064872,7.126228858,grid)
    #~ do_test(241,44.95113396,7.142121197,241,44.951793299,7.141679106,grid)
    #~ do_test(242,44.93653633,7.117890856,242,44.937195266,7.117448082,grid)
    #~ do_test(243,44.94340575,7.126671413,243,44.944064872,7.126228858,grid)
    #~ do_test(244,44.94173479,7.117818047,244,44.942393863,7.117375187,grid)
    #~ do_test(245,44.94689124,7.102293535,245,44.947550437,7.101850009,grid)
    #~ do_test(246,44.95062448,7.035558031,246,44.951283823,7.035111479,grid)
    #~ do_test(247,44.94173479,7.117818047,247,44.942393863,7.117375187,grid)
    #~ do_test(248,44.9318691,7.125303039,248,44.932527916,7.124860613,grid)
    #~ do_test(249,44.94857183,7.09420273,249,44.949231064,7.093758872,grid)
    #~ do_test(250,44.93075875,7.156078843,250,44.931417548,7.155637568,grid)
    #~ do_test(251,44.94340575,7.126671413,251,44.944064872,7.126228858,grid)
    #~ do_test(252,44.94173479,7.117818047,252,44.942393863,7.117375187,grid)
    #~ do_test(253,44.94173479,7.117818047,253,44.942393863,7.117375187,grid)
    #~ do_test(254,44.93653633,7.117890856,254,44.937195266,7.117448082,grid)
    #~ do_test(255,44.9318691,7.125303039,255,44.932527916,7.124860613,grid)
    #~ do_test(256,44.94340575,7.126671413,256,44.944064872,7.126228858,grid)
    #~ do_test(257,45.3711494,7.654838588,257,45.371820077,7.654421986,grid)
    #~ do_test(258,45.28732163,7.406073872,258,45.287990369,7.405643154,grid)
    #~ do_test(259,45.09922663,7.548546998,259,45.099891524,7.548124049,grid)
    #~ do_test(260,44.94688617,7.221584438,260,44.947545473,7.221145349,grid)
    #~ do_test(261,44.88862524,7.32755498,261,44.889282888,7.327119988,grid)
    #~ do_test(262,44.88596784,7.307999921,262,44.886625404,7.307564309,grid)
    #~ do_test(263,45.04378991,7.776993559,263,45.044453233,7.776582791,grid)
    #~ do_test(264,44.93410424,7.612584584,264,44.934763409,7.612164293,grid)
    #~ do_test(265,44.98999243,7.463400495,265,44.990653693,7.462971233,grid)
    #~ do_test(266,44.91978213,7.425695839,266,44.920440739,7.425264649,grid)
    #~ do_test(267,45.45052979,8.001787414,267,45.451204380,8.001392298,grid)
    #~ do_test(268,44.91964446,7.844565528,268,44.920304350,7.844158870,grid)
    #~ do_test(269,44.95415216,7.179221664,269,44.954811613,7.178780936,grid)
    #~ do_test(270,45.42575886,7.578755284,270,45.426430600,7.578336099,grid)
    #~ do_test(271,44.88740037,7.265628076,271,44.888057972,7.265191067,grid)
    #~ do_test(272,44.99612588,6.921033276,272,44.996786561,6.920580468,grid)
    #~ do_test(273,44.88783033,7.050668259,273,44.888488054,7.050223423,grid)
    #~ do_test(274,44.92628512,7.047023004,274,44.926943833,7.046577421,grid)
    #~ do_test(275,44.85981482,7.90163435,275,44.860473071,7.901231330,grid)
    #~ do_test(276,44.91028133,7.196398839,276,44.910939568,7.195959294,grid)
    #~ do_test(277,44.86650957,7.268330445,277,44.867166554,7.267893719,grid)
    #~ do_test(278,44.8608096,7.242129186,278,44.861466428,7.241691675,grid)
    #~ do_test(279,45.39186582,7.648780061,279,45.392536970,7.648363585,grid)
    #~ do_test(280,45.39186582,7.648780061,280,45.392536970,7.648363585,grid)
    #~ do_test(281,45.42234265,7.770013171,281,45.423015016,7.769603597,grid)
    #~ do_test(282,45.48914664,7.804579706,282,45.489821046,7.804173481,grid)
    #~ do_test(283,45.48914664,7.804579706,283,45.489821046,7.804173481,grid)
    #~ do_test(284,45.05385787,7.424443271,284,45.054521220,7.424012012,grid)
    #~ do_test(285,45.44695555,7.49114417,285,45.447627643,7.490721090,grid)
    #~ do_test(286,45.11831884,7.891785499,286,45.118985041,7.891381550,grid)
    #~ do_test(287,45.03086336,7.522542909,287,45.031526076,7.522117810,grid)
    #~ do_test(288,44.98598009,7.86947553,288,44.986642390,7.869070351,grid)
    #~ do_test(289,45.33534583,7.62554931,289,45.336015618,7.625130515,grid)
    #~ do_test(290,45.33773064,7.619263487,290,45.338400474,7.618844429,grid)
    #~ do_test(291,45.33251219,7.724727461,291,45.333182097,7.724313629,grid)
    #~ do_test(292,45.25018669,7.71600864,292,45.250854702,7.715593399,grid)
    #~ do_test(293,45.06908466,7.510877787,293,45.069748693,7.510452097,grid)
    #~ do_test(294,45.19774498,7.574575513,294,45.198411984,7.574153478,grid)
    #~ do_test(295,45.30872447,7.575610601,295,45.309393640,7.575188974,grid)
    #~ do_test(296,44.92436355,7.331741174,296,44.925022316,7.331306099,grid)
    #~ do_test(297,45.38973885,7.870081926,297,45.390410899,7.869677568,grid)
    #~ do_test(298,45.52474111,7.870081926,298,45.525416985,7.869680274,grid)
    #~ do_test(299,45.52345193,7.482106252,299,45.524125812,7.481684448,grid)
    #~ do_test(300,45.24605273,7.967248016,300,45.246722125,7.966848472,grid)
    #~ do_test(301,44.7917881,7.197666185,301,44.792443042,7.197227839,grid)
    #~ do_test(302,45.01181244,7.108111206,302,45.012473320,7.107666850,grid)
    #~ do_test(303,45.068613,7.46456944,303,45.069277008,7.464140392,grid)
    #~ do_test(304,45.10587807,7.403724303,304,45.106542827,7.403292130,grid)
    #~ do_test(305,45.49405534,7.778176606,305,45.494729730,7.777769070,grid)
    #~ do_test(306,45.07173673,6.884646474,306,45.072399376,6.884190871,grid)
    #~ do_test(307,45.3711494,7.654838588,307,45.371820077,7.654421986,grid)
    #~ do_test(308,45.45736458,7.850656677,308,45.458038374,7.850252430,grid)
    #~ do_test(309,45.45332459,7.844003132,309,45.453998223,7.843598380,grid)
    #~ do_test(310,44.95062448,7.035558031,310,44.951283823,7.035111479,grid)
    #~ do_test(311,45.45332459,7.844003132,311,45.453998223,7.843598380,grid)
    #~ do_test(312,45.22190333,7.782907196,312,45.222570934,7.782495558,grid)
    #~ do_test(313,45.24768698,7.610742085,313,45.248354906,7.610321532,grid)
    #~ do_test(314,45.39186582,7.648780061,314,45.392536970,7.648363585,grid)
    #~ do_test(315,45.13407047,7.217855419,315,45.134734906,7.217414520,grid)
    #~ do_test(316,45.22459049,7.657778122,316,45.225257948,7.657360067,grid)
    #~ do_test(317,45.02845467,7.453309337,317,45.029117291,7.452879445,grid)
    #~ do_test(318,44.89934895,7.239408021,318,44.900006895,7.238970035,grid)
    #~ do_test(319,44.88577065,7.254750903,319,44.886428203,7.254313555,grid)
    #~ do_test(320,45.14134041,7.535023409,320,45.142006268,7.534599261,grid)
    #~ do_test(321,45.33583525,7.795958321,321,45.336505474,7.795548330,grid)
    #~ do_test(322,45.12793633,7.179345526,322,45.128600422,7.178902884,grid)
    #~ do_test(323,45.3117928,7.809450831,323,45.312462493,7.809041194,grid)
    #~ do_test(324,45.40934147,7.825536009,324,45.410013742,7.825129141,grid)
    #~ do_test(325,45.21835916,7.632402487,325,45.219026508,7.631983202,grid)
    #~ do_test(326,45.10200834,7.766673284,326,45.102673248,7.766261803,grid)
    #~ do_test(327,44.90645447,7.313769079,327,44.907112663,7.313333490,grid)
    #~ do_test(328,45.35022863,7.672849144,328,45.350898845,7.672433007,grid)
    #~ do_test(329,45.15294524,7.864289225,329,45.153611934,7.863883118,grid)
    #~ do_test(330,45.15407473,7.932498043,330,45.154742081,7.932096501,grid)
    #~ do_test(331,44.86527733,7.301632312,331,44.865934265,7.301196666,grid)
    #~ do_test(332,45.09845978,7.356614834,332,45.099124075,7.356180341,grid)
    #~ do_test(333,45.10647997,7.27341643,333,45.107143998,7.272978142,grid)
    #~ do_test(334,45.01241604,7.826551092,334,45.013078771,7.826143347,grid)
    #~ do_test(335,44.94263504,6.915030307,335,44.943294420,6.914577917,grid)
    #~ do_test(336,45.02620566,6.857055286,336,45.026867261,6.856598907,grid)
    #~ do_test(337,44.89544331,7.486290819,337,44.896101043,7.485862842,grid)
    #~ do_test(338,45.3852478,7.841293077,338,45.385919535,7.840886724,grid)
    #~ do_test(339,45.09298832,7.880276901,339,45.093653859,7.879872448,grid)
    #~ do_test(340,44.94677592,6.852370262,340,44.947435556,6.851914586,grid)
    #~ do_test(341,44.94677592,6.852370262,341,44.947435556,6.851914586,grid)
    #~ do_test(342,45.40460413,7.993605555,342,45.405277362,7.993209191,grid)
    #~ do_test(343,45.48914664,7.804579706,343,45.489821046,7.804173481,grid)
    #~ do_test(344,45.48914664,7.804579706,344,45.489821046,7.804173481,grid)
    #~ do_test(345,45.23319606,7.853649946,345,45.233864242,7.853242400,grid)
    #~ do_test(346,45.13610502,7.771891714,346,45.136770756,7.771480213,grid)
    #~ do_test(347,45.39651495,7.530631694,347,45.397185977,7.530209453,grid)
    #~ do_test(348,45.42234265,7.770013171,348,45.423015016,7.769603597,grid)
    #~ do_test(349,45.38298891,7.711682128,349,45.383660019,7.711268612,grid)
    #~ do_test(350,45.38381411,7.880861377,350,45.384486076,7.880457630,grid)
    #~ do_test(351,45.13625086,7.045474483,351,45.136914756,7.045025533,grid)
    #~ do_test(352,45.48914664,7.804579706,352,45.489821046,7.804173481,grid)
    #~ do_test(353,45.18903444,7.966691122,353,45.189702732,7.966291606,grid)
    #~ do_test(354,45.40241026,7.763418289,354,45.403082076,7.763007940,grid)
    #~ do_test(355,44.82080044,7.22724684,355,44.821456144,7.226809242,grid)
    #~ do_test(356,45.03623252,7.41752398,356,45.036895246,7.417092403,grid)
    #~ do_test(357,45.49405534,7.778176606,357,45.494729730,7.777769070,grid)
    #~ do_test(358,45.52278252,7.642142266,358,45.523456993,7.641728305,grid)
    #~ do_test(359,45.26997095,7.430832809,359,45.270639377,7.430403183,grid)
    #~ do_test(360,45.52278252,7.642142266,360,45.523456993,7.641728305,grid)
    #~ do_test(361,45.52278252,7.642142266,361,45.523456993,7.641728305,grid)
    #~ do_test(362,44.98821701,7.741493437,362,44.988878334,7.741080383,grid)
    #~ do_test(363,45.0478463,7.027480726,363,45.048508060,7.027032208,grid)
    #~ do_test(364,45.23116501,7.196149565,364,45.231831852,7.195707311,grid)
    #~ do_test(366,45.49405534,7.778176606,366,45.494729730,7.777769070,grid)
    #~ do_test(367,45.49405534,7.778176606,367,45.494729730,7.777769070,grid)
    #~ do_test(368,45.49405534,7.778176606,368,45.494729730,7.777769070,grid)
    #~ do_test(369,45.13512308,7.485388653,369,45.135788801,7.484961227,grid)
    #~ do_test(370,45.07551974,7.339854557,370,45.076183309,7.339419246,grid)
    #~ do_test(371,45.22416944,7.495928638,371,45.224836987,7.495502062,grid)
    #~ do_test(372,45.3711494,7.654838588,372,45.371820077,7.654421986,grid)
    #~ do_test(373,45.30653392,7.748390282,373,45.307203307,7.747977380,grid)
    #~ do_test(374,45.20946531,7.500531707,374,45.210132574,7.500105355,grid)
    #~ do_test(375,45.20972401,7.491279101,375,45.210391284,7.490852220,grid)
    #~ do_test(376,45.27845223,7.618294467,376,45.279120802,7.617874618,grid)
    #~ do_test(377,45.1544662,7.012045464,377,45.155130585,7.011594768,grid)
    #~ do_test(378,45.13404212,7.629823404,378,45.134707680,7.629404588,grid)
    #~ do_test(379,45.18903444,7.966691122,379,45.189702732,7.966291606,grid)
    #~ do_test(380,45.1460153,8.091536981,380,45.146683121,8.091144280,grid)
    #~ do_test(381,45.38692617,7.953403281,381,45.387598709,7.953004391,grid)
    #~ do_test(382,45.40855773,7.934434802,382,45.409230702,7.934034951,grid)
    #~ do_test(383,45.40973419,7.787390864,383,45.410406301,7.786981954,grid)
    #~ do_test(384,45.38298891,7.711682128,384,45.383660019,7.711268612,grid)
    #~ do_test(385,45.43290414,7.739681444,385,45.433576650,7.739270474,grid)
    #~ do_test(386,44.84304445,7.495966886,386,44.843700297,7.495539545,grid)
    #~ do_test(387,44.78195582,7.50666299,387,44.782609845,7.506236988,grid)
    #~ do_test(388,45.24183905,7.554228287,388,45.242506887,7.553804859,grid)
    #~ do_test(389,45.1177663,7.386318971,389,45.118431248,7.385885987,grid)
    #~ do_test(390,45.04442032,7.467870574,390,45.045083494,7.467441718,grid)
    #~ do_test(391,45.3111119,7.978896916,391,45.311782757,7.978498654,grid)
    #~ do_test(392,45.10745619,7.225673216,392,45.108119979,7.225232814,grid)
    #~ do_test(393,44.80712742,7.155176384,393,44.807782853,7.154736448,grid)
    #~ do_test(394,44.92605752,7.249934953,394,44.926716254,7.249497056,grid)
    #~ do_test(395,44.92299469,7.741554463,395,44.923653806,7.741141500,grid)
    #~ do_test(396,44.94802481,7.633255109,396,44.948684482,7.632835997,grid)
    #~ do_test(397,44.86501944,7.568711377,397,44.865676064,7.568288475,grid)
    #~ do_test(398,45.30359419,7.939264157,398,45.304264606,7.938863328,grid)
    #~ do_test(399,45.43290414,7.739681444,399,45.433576650,7.739270474,grid)
    #~ do_test(400,45.23547857,7.3705906,400,45.236146153,7.370157428,grid)
    #~ do_test(401,45.21498303,7.378004684,401,45.215650189,7.377571763,grid)
    #~ do_test(402,45.20111247,7.776583076,402,45.201779637,7.776171272,grid)
    #~ do_test(403,44.95446692,7.51216295,403,44.955126849,7.511736737,grid)


def esamina(rt, ct):
    print("riga(i):<%i>\tcol(j):<%i>\tdeltaFi:<%f>\tdeltaLA<%f>" %
          (rt, ct, gr.Fi_WGS84_Roma40[rt][ct], gr.La_WGS84_Roma40[rt][ct]))
    ft, lt = gr.fi_lambda_for_row_col(rt, ct)
    print("riga(i):<%i>\tcol(j):<%i>\tFi:<%f>\tLA<%f>" % (rt, ct, ft, lt))
    rt, ct = gr.row_col_for_fi_la(ft, lt)
    print("riga(i):<%i>\tcol(j):<%i>\tFi:<%f>\tLA<%f>" % (rt, ct, ft, lt))

    print("___________________________________________________")


if __name__ == "__main__":

    gdir = 'F:\progetti\pysetl\grigliati_1'
    #gdir ='h:\pysetl\grigliati_1'
    # ~ grfile= GrFile(gdir+os.sep+'019.gr1')
    gr = Grigliato(gdir)
    test(gr)
    # (print gr.Fi_ED50_Roma40)

    # ~ (print  "caricato FI SO %f LA SO %f FI NE %f LA NE %f " %(gr.Fi_SO_VAL,gr.La_SO_VAL,gr.Fi_NE_VAL,gr.La_NE_VAL))

    # ~ Is,Js = gr.row_col_for_fi_la(gr.Fi_SO_VAL,gr.La_SO_VAL)
    # ~ Ie,Je = gr.row_col_for_fi_la(gr.Fi_NE_VAL,gr.La_NE_VAL)
    # ~ (print "da riga %i col %i" %(Is,Js))
    # ~ (print "fino a riga %i col %i" %(Ie,Je))
    # ~ (print "riga(i):<%i>\tcol(j):<%i>\tdeltaFi:<%f>\tdeltaLA<%f>" %(Is,Js,gr.Fi_WGS84_Roma40[Is][Js],gr.La_WGS84_Roma40[Is][Js]))
    # ~ (print "riga(i):<%i>\tcol(j):<%i>\tdeltaFi:<%f>\tdeltaLA<%f>" %(Ie,Je,gr.Fi_WGS84_Roma40[Ie][Je],gr.La_WGS84_Roma40[Ie][Je]))

    esamina(136, 16)
    esamina(136, 17)
    # ~ rt=136
    # ~ ct=16
    # ~ (print "riga(i):<%i>\tcol(j):<%i>\tdeltaFi:<%f>\tdeltaLA<%f>" %(rt,ct,gr.Fi_WGS84_Roma40[rt][ct],gr.La_WGS84_Roma40[rt][ct]))
    # ~ ft,lt= gr.fi_lambda_for_row_col(rt,ct)
    # ~ (print "riga(i):<%i>\tcol(j):<%i>\tFi:<%f>\tLA<%f>" %(rt,ct,ft,lt))
    # ~ rt,ct=gr.row_col_for_fi_la(ft,lt)
    # ~ (print "riga(i):<%i>\tcol(j):<%i>\tFi:<%f>\tLA<%f>" %(rt,ct,ft,lt))

    # ~ f=gr.Fi_SO_VAL

    # ~ while f <= gr.Fi_NE_VAL+0.01:
    # ~ l=gr.La_SO_VAL
    # ~ while l <= gr.La_NE_VAL+0.01:
    # ~ #sf,sl=gr.get_shift(f,l, Roma40, WGS84)
    # ~ i,j=gr.row_col_for_fi_la(f,l)
    # ~ sf,sl=gr.get_shift(f,l, WGS84, Roma40)
    # ~ print "rigacol:<%03.0d%03.0d>\tFi:<%f>\tLa:<%f>\tdeltaFi:<%f>\tdeltaLA<%f>" %(i,j,f,l,sf,sl)
    # ~ l+=gr.__LaIncDeg__
    # ~ f+=gr.__FiIncDeg__

    # for i in range (gr.Fi_SO_VAL,,Ie+1):
    #    for j in range (Js,Je+1):
    #        print "riga(i):<%i>\tcol(j):<%i>\tdeltaFi:<%f>\tdeltaLA<%f>" %(i,j,gr.Fi_WGS84_Roma40[i][j],gr.La_WGS84_Roma40[i][j])
