#!/usr/bin/python
# -*- coding: UTF-8 -*-
__doc__ = \
    """
muodulo di definizione del contesto di conversione geodetica e di conversioni geodetiche
porting fdelle da vb
"""
__version__ = "0.0"
__author__ = "gd"
# Attribute VB_Name = "http_gr1"
from pyproj import Proj
import ConfigParser
import os
import sys
import imp
import cs2gb
from typing  import List

def main_is_frozen():
    return (hasattr(sys, "frozen") or  # new py2exe
            hasattr(sys, "importers")  # old py2exe
            or imp.is_frozen("__main__"))  # tools/freeze


def get_main_dir():
    if main_is_frozen():
        # print 'Running from path', os.path.dirname(sys.executable)
        return os.path.dirname(sys.executable)
    # ~ return os.path.dirname(sys.argv[0])
    return os.path.abspath(os.path.dirname(__file__) + os.path.sep + '..')

# find path to where we are running
# ~ path_to_script=get_main_dir()

# OPTIONAL:
# add the sibling 'lib' dir to our module search path
# ~ lib_path = os.path.join(get_main_dir(), os.path.pardir, 'lib')
#~ sys.path.insert(0, lib_path)

# OPTIONAL:
# use info to find relative data files in 'data' subdir
# ~ datafile1 = os.path.join(get_main_dir(), 'data', 'file1')


CurrentConversionContext = None

CurrentConversion = None


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class ConversionContext(Singleton):
    __config__ = None
    __confdefaults__ = None
    __IGMIGrid__ = None
    Wgs84Proj = None
    GB1Proj = None
    CatProj = None

    def __init__(self):
        self.__IGMIGrid__ = None
        self.Wgs84Proj = None
        self.GB1Proj = None
        self.CatProj = None
        self.__confdefaults__ = dict()
        for key, val in os.environ.items():
            self.__confdefaults__[key] = val
        #~ self.__confdefaults__.update(os.environ)
        # ~ AppPath='f:\\progetti\\pysetl\\src'
        # ~ AppPath=os.path.dirname(sys.executable)
        AppPath = get_main_dir()
        # ~ AppPath=os.path.abspath(os.path.dirname( __file__) + os.path.sep+ '..' )
        self.__confdefaults__['apppath'] = AppPath
        self.__config__ = ConfigParser.ConfigParser(self.__confdefaults__)
        # print os.path.dirname( __file__)
        # ~ print os.path.abspath(AppPath + os.path.sep+ 'pysetl.cfg')
        self.__config__.read([
                             os.path.abspath(
                                 AppPath + os.path.sep + 'pysetl.cfg'), os.path.expanduser('~/.pysetl.cfg')
                             ])

    @property
    def config(self):
        return self.__config__

    @property
    def Grigliato(self):
        if self.__IGMIGrid__ == None:
            # ~ gridpath=self.__config__.get( "IGMI", "gridpath",vars=self.__confdefaults__)
            # ,vars=self.__confdefaults__)
            gridpath = self.__config__.get("IGMI", "gridpath")
            from Grigliato import Grigliato
            self.__IGMIGrid__ = gr = Grigliato(gridpath)
            return self.__IGMIGrid__
        else:
            return self.__IGMIGrid__

    def initWgs84Proj(self):
        if self.Wgs84Proj == None:

            # <32632>
            proj = 'utm'
            zone = 32
            ellps = 'WGS84'
            datum = 'WGS84'
            units = 'm'
            # +no_defs  <>
            projstr = '+proj=utm +zone=32 +ellps=WGS84 +datum=WGS84 +units=m +no_defs'
            # ~ self.Wgs84Proj=Proj(proj=proj, zone=zone, ellps=ellps, datum=datum, units=units)#, no_defs=True )
            # ~ self.Wgs84Proj=Proj(init='epsg:32632')
            self.Wgs84Proj = Proj(projstr)
            return self.Wgs84Proj
        else:
            return self.Wgs84Proj

    def initGB1Proj(self):
        if self.GB1Proj == None:
            # Monte Mario / Italy zone 1
            # +proj=tmerc +lat_0=0 +lon_0=21.45233333333333 +k=0.999600 +x_0=1500000 +y_0=0 +ellps=intl +pm=rome +units=m +no_defs
            # <26591> +proj=tmerc +lat_0=0 +lon_0=21.45233333333333 +k=0.999600 +x_0=1500000 +y_0=0 +ellps=intl +pm=rome +units=m +no_defs  no_defs <>
            # ~ projstr=' +proj=tmerc +lat_0=0 +lon_0=21.45233333333333 +k=0.999600 +x_0=1500000 +y_0=0 +ellps=intl +pm=rome +units=m +no_defs'

            projstr = '+proj=tmerc +lat_0=0 +lon_0=9 +k=0.9996 +x_0=1500000 +y_0=0 +ellps=intl +units=m +no_defs'

            # <3003> +proj=tmerc +lat_0=0 +lon_0=9 +k=0.9996 +x_0=1500000 +y_0=0 +ellps=intl +units=m +no_defs  <>
            proj = 'tmerc'
            lat_0 = 0
            lon_0 = 21.45233333333333
            k = 0.999600
            x_0 = float(1500000)
            y_0 = float(0)
            ellps = 'intl'
            pm = 'rome'
            units = 'm'
            # no_defs  <>
            # ~ self.GB1Proj=Proj(proj=proj, lat_0=lat_0, lon_0=lon_0, k=k, x_0=x_0, y_0=y_0, ellps=ellps, pm=pm ,units=units)#, no_defs=True )
            # ~ self.GB1Proj=Proj(init='epsg:26592')
            self.GB1Proj = Proj(projstr)
            # ~ self.GB1Proj=Proj(init='epsg:3003')
            return self.GB1Proj
        else:
            return self.GB1Proj

    def initCatProj(self, convpar):
        # <2066>
        proj = 'cass'
        # ~ lat_0=cs2gb.geo_to_gradi(convpar.lat_g, convpar.lat_p,convpar.lat_s)
        # ~ lon_0=cs2gb.geo_to_gradi(convpar.long_g,convpar.long_p,convpar.long_s)
        lat_0, lon_0 = convpar.LatLon()

        x_0 = convpar.x_0
        y_0 = convpar.y_0
        # bessel bessel
        a = 6377397.155
        rf = 299.1528128
        # Bessel 1841
        # no_defs  <>
        self.CatProj = Proj(proj=proj, lat_0=lat_0,
                            lon_0=lon_0, x_0=x_0, y_0=y_0, a=a, rf=rf)
        self.Catparam = convpar


def nome_mappa(nome):
    #~ G465A0001A0
    # ~ nome='G465A0001A0'
    com = nome[0:4]
    sez = nome[4:5]
    fog = nome[5:9]
    svil = nome[9:11]
    return com, sez, fog, svil


def get_parameter(mappa):
    com, sez, fog, svil = nome_mappa(mappa)
    global CurrentConversionContext
    if CurrentConversionContext == None:
        CurrentConversionContext = ConversionContext()
    conf = CurrentConversionContext.config

    lat_0 = None
    lon_0 = None
    x_0 = None
    y_0 = None
    descr = ""
    comune = ""
    codicecatastale = ""

    try:
        # cerco per com + sez + fog + svil
        sec = com + sez + fog + svil
        # ~ lat_0=conf.get( com + sez + fog + svil, "lat_0")
        # ~ lon_0=conf.get( com + sez + fog + svil, "lon_0")
        # ~ x_0  =conf.get( com + sez + fog + svil, "x_0")
        # ~ y_0  =conf.get( com + sez + fog + svil, "y_0")
        lat_0 = conf.get(sec, "lat_0")
        lon_0 = conf.get(sec, "lon_0")
        x_0 = conf.get(sec, "x_0")
        y_0 = conf.get(sec, "y_0")
        print("sezione <%s> lat_0:%s, lon_0:%s, x_0:%s, y_0:%s " %
              (sec, lat_0, lon_0, x_0, y_0))
        try:
            descr = conf.get(sec, "descr")
            comune = conf.get(sec, "comune")
            codicecatastale = conf.get(sec, "codicecatastale")
        except:
            pass
    except ConfigParser.NoSectionError:
        try:
            # cerco per com + sez + fog
            sec = com + sez + fog
            lat_0 = conf.get(sec, "lat_0")
            lon_0 = conf.get(sec, "lon_0")
            x_0 = conf.get(sec, "x_0")
            y_0 = conf.get(sec, "y_0")
            print("sezione <%s> lat_0:%s, lon_0:%s, x_0:%s, y_0:%s " %
                  (sec, lat_0, lon_0, x_0, y_0))
            try:
                descr = conf.get(sec, "descr")
                comune = conf.get(sec, "comune")
                codicecatastale = conf.get(sec, "codicecatastale")
            except:
                pass
        except ConfigParser.NoSectionError:
            try:
                # cerco per com + sez
                sec = com + sez
                lat_0 = conf.get(sec, "lat_0")
                lon_0 = conf.get(sec, "lon_0")
                x_0 = conf.get(sec, "x_0")
                y_0 = conf.get(sec, "y_0")
                print("sezione <%s> lat_0:%s, lon_0:%s, x_0:%s, y_0:%s " %
                      (sec, lat_0, lon_0, x_0, y_0))
                try:
                    comune = conf.get(sec, "comune")
                    codicecatastale = conf.get(sec, "codicecatastale")
                    descr = conf.get(sec, "descr")
                except:
                    pass
            except ConfigParser.NoSectionError:
                try:
                    # cerco per com
                    sec = com
                    lat_0 = conf.get(sec, "lat_0")
                    lon_0 = conf.get(sec, "lon_0")
                    x_0 = conf.get(sec, "x_0")
                    y_0 = conf.get(sec, "y_0")
                    print("sezione <%s> lat_0:%s, lon_0:%s, x_0:%s, y_0:%s " %
                          (sec, lat_0, lon_0, x_0, y_0))
                    try:
                        comune = conf.get(sec, "comune")
                        codicecatastale = conf.get(sec, "codicecatastale")
                        descr = conf.get(sec, "descr")
                    except:
                        pass
                except:
                    pass
    if lat_0 == None:
        return None
    else:
        return cs2gb.ConvPar(comune, descr, float(lat_0), float(lon_0), float(x_0), float(y_0))
        # ~ d0,p0,s0 =cs2gb.DegToGps (float(lat_0))
        # ~ d1,p1,s1 =cs2gb.DegToGps (float(lon_0))
        # ~ print comune
        # ~ print descr
        # ~ print d0,p0,s0
        # ~ print "lat_0" + lat_0
        # ~ print d1,p1,s1
        # ~ print "lon_0" + lon_0


def initGB():
    global CurrentConversionContext
    if CurrentConversionContext == None:
        CurrentConversionContext = ConversionContext()
    CurrentConversionContext.initGB1Proj()


def initWGS():
    global CurrentConversionContext
    if CurrentConversionContext == None:
        CurrentConversionContext = ConversionContext()
    CurrentConversionContext.initWgs84Proj()


def set_parameter(parameters):
    global CurrentConversionContext
    if CurrentConversionContext == None:
        CurrentConversionContext = ConversionContext()
    CurrentConversionContext.initCatProj(parameters)


def grigliato():
    global CurrentConversionContext
    if CurrentConversionContext == None:
        CurrentConversionContext = ConversionContext()
    return CurrentConversionContext.Grigliato


def cs2wgs(point: tuple[float, float])->tuple[float, float]:
    x = point[0]
    y = point[1]
    global CurrentConversionContext
    if CurrentConversionContext == None:
        print("NO CurrentConversionContext")
        CurrentConversionContext = ConversionContext()

    gr = CurrentConversionContext.Grigliato
    convpar = CurrentConversionContext.Catparam

    LongGe, LatGe = CurrentConversionContext.CatProj(x, y, inverse=True)

    ### conversione in radianti
    LatRm, LongRm = cs2gb.Geomova02ToRoma40(
        cs2gb.DegToRad(LatGe), cs2gb.DegToRad(LongGe),  convpar)

    # Lat Lon in gradi
    # longitudine definita rispetto a Monte Mario sommo la longitudine di MM  in Roma40
    LatRm = cs2gb.RadToDeg(LatRm)
    LongRm = cs2gb.RadToDeg(LongRm) + 12.45233333333333333333

    xgb, ygb = CurrentConversionContext.GB1Proj(LongRm, LatRm)

    SLatW, SLongW = gr.get_shift(LatRm, LongRm, gr.Roma40, gr.WGS84)

    LatW = LatRm + gr.sec_to_deg(SLatW)
    LongW = LongRm + gr.sec_to_deg(SLongW)

    xwgs, ywgs = CurrentConversionContext.Wgs84Proj(LongW, LatW, inverse=False)
    return (xwgs, ywgs)


def debug_conv(point: tuple[float,float])->tuple[float,float]:
    x = point[0]
    y = point[1]

    global CurrentConversionContext
    if CurrentConversionContext == None:
        print("NO CurrentConversionContext")
        CurrentConversionContext = ConversionContext()

    gr = CurrentConversionContext.Grigliato
    convpar = CurrentConversionContext.Catparam

    LongGe, LatGe = CurrentConversionContext.CatProj(x, y, inverse=True)

    ### conversione in radianti
    LatRm, LongRm = cs2gb.Geomova02ToRoma40(
        cs2gb.DegToRad(LatGe), cs2gb.DegToRad(LongGe),  convpar)

    xgb1, ygb1 = cs2gb.LatLong2ToBoaga(LatRm, LongRm, 1, 1, convpar)
    LongRm1, LatRm1 = CurrentConversionContext.GB1Proj(
        xgb1, ygb1, inverse=True)

    # Lat Lon in gradi
    # longitudine definita rispetto a Monte Mario sommo la longitudine di MM  in Roma40
    LatRm = cs2gb.RadToDeg(LatRm)
    LongRm = cs2gb.RadToDeg(LongRm) + 12.45233333333333333333

    xgb, ygb = CurrentConversionContext.GB1Proj(LongRm, LatRm)

    SLatW, SLongW = gr.get_shift(LatRm, LongRm, gr.Roma40, gr.WGS84)

    LatW = LatRm + gr.sec_to_deg(SLatW)
    LongW = LongRm + gr.sec_to_deg(SLongW)

    xwgs, ywgs = CurrentConversionContext.Wgs84Proj(LongW, LatW, inverse=False)
    print("____________________________________")
    print("Wgs84Proj:" + CurrentConversionContext.Wgs84Proj.srs)
    print("CatProj  :" + CurrentConversionContext.CatProj.srs)
    print("GB1Proj  :" + CurrentConversionContext.GB1Proj.srs)
    print("==================================")

    print("%s %s" % (convpar.desc, convpar.Nome))
    print("Lat/Lon Genova04 %.8f %.8f " % (LatGe, LongGe))
    g, p, s = cs2gb.DegToGps(LatGe)
    g1, p1, s1 = cs2gb.DegToGps(LongGe)
    print("Lat/Lon Genova04 %.0f %.0f'%.8f'' %.0f %.0f'%.8f\" " %
          (g, p, s, g1, p1, s1))

    print("Lat/Lon Roma40   %.8f %.8f " % (LatRm, LongRm))
    print("Lat/Lon Roma401  %.8f %.8f " % (LatRm1, LongRm1))
    g, p, s = cs2gb.DegToGps(LatRm1)
    g1, p1, s1 = cs2gb.DegToGps(LongRm1)
    print("Lat/Lon Roma40 %.0f° %.0f'%.8f\" %.0f° %.0f'%.8f\" " %
          (g, p, s, g1, p1, s1))

    print("X/Y GB           %.8f %.8f " % (xgb, ygb))
    print("X/Y GB1          %.8f %.8f " % (xgb1, ygb1))
    print("Lat/Lon WGS84    %.8f %.8f " % (LatW, LongW))
    print("X/Y WGS84UTM32N  %.8f %.8f " % (xwgs, ywgs))
    print("==================================")
    return (xwgs, ywgs)


def cs_to_gb(point:tuple[float,float])->tuple[float,float]:
    x = point[0]
    y = point[1]

    global CurrentConversionContext
    if CurrentConversionContext == None:
        print("NO CurrentConversionContext")
        CurrentConversionContext = ConversionContext()

    gr = CurrentConversionContext.Grigliato
    convpar = CurrentConversionContext.Catparam

    LongGe, LatGe = CurrentConversionContext.CatProj(x, y, inverse=True)

    ### conversione in radianti
    LatRm, LongRm = cs2gb.Geomova02ToRoma40(
        cs2gb.DegToRad(LatGe), cs2gb.DegToRad(LongGe),  convpar)
    # Lat Lon in gradi
    # longitudine definita rispetto a Monte Mario sommo la longitudine di MM rispetto a genova
    LatRm = cs2gb.RadToDeg(LatRm)
    LongRm = cs2gb.RadToDeg(LongRm) + 12.45233333333333333333

    xgb, ygb = CurrentConversionContext.GB1Proj(LongRm, LatRm)

    return (xgb, ygb)


def gb2wgs(point:tuple[float,float])->tuple[float,float]:
    x = point[0]
    y = point[1]
    global CurrentConversionContext
    if CurrentConversionContext == None:
        print("NO CurrentConversionContext")
        CurrentConversionContext = ConversionContext()

    gr = CurrentConversionContext.Grigliato

    # geografiche ROMA40
    LongRm, LatRm = CurrentConversionContext.GB1Proj(x, y, inverse=True)

    SLatW, SLongW = gr.get_shift(LatRm, LongRm, gr.Roma40, gr.WGS84)

    LatW = LatRm + gr.sec_to_deg(SLatW)
    LongW = LongRm + gr.sec_to_deg(SLongW)
    xwgs, ywgs = CurrentConversionContext.Wgs84Proj(LongW, LatW, inverse=False)
    return (xwgs, ywgs)


def identity(point:tuple[float,float])->tuple[float,float]:
    return point


def convert(point:tuple[float,float])->tuple[float,float]:
    global CurrentConversion
    if CurrentConversion == None:
        CurrentConversion = identity
    return CurrentConversion(point)


def SetConversion(cfg):
    global CurrentConversion
    if cfg == 'CS2GB':
        CurrentConversion = cs_to_gb
        print("CurrentConversion=cs_to_gb")

    elif cfg == 'CS2WGS':
        CurrentConversion = cs2wgs
        print("CurrentConversion=cs2wgs")
    elif cfg == 'DEBUG':
        CurrentConversion = debug_conv
        print("CurrentConversion=debug_conv")
    elif cfg == 'GB2WGS':
        CurrentConversion = gb2wgs
        print("CurrentConversion=gb2wgs")
    else:
        CurrentConversion = identity
        print("CurrentConversion=identity")


if __name__ == '__main__':
    # ~ tt=get_parameter('A525_000100')
    # ~ print (tt)
    # ~ tt=get_parameter('C133A000100C133A000100.CMF')

    # ~ print tt
    # ~ print tt.desc
    # ~ print tt.Nome
    # ~ print tt.lat_g
    # ~ print tt.lat_p
    # ~ print tt.lat_s
    # ~ print tt.long_g
    # ~ print tt.long_p
    # ~ print tt.long_s
    # ~ print tt.x_0
    # ~ print tt.y_0
    # ~ print tt.Zona

    A1JKB = cs2gb.ConvPar(
        "ABBADIA ALPINA (PINEROLO)", "Abbadia campanile", cs2gb.geo_to_gradi(
            44, 53, 10.072171), cs2gb.geo_to_gradi(-1, 36, 51.320861)
    )

    A1AS = cs2gb.ConvPar(
        "AZEGLIO", "Campanile d’Azeglio", cs2gb.geo_to_gradi(
            45, 25, 27.203086), cs2gb.geo_to_gradi(-0, 55, 37.503652)
    )
    A1AC = cs2gb.ConvPar(
        "AGLIE'", "Agliè", cs2gb.geo_to_gradi(
            45, 21, 43.568556), cs2gb.geo_to_gradi(-1, 9, 12.498892)
    )
    A1AD = cs2gb.ConvPar(
        "AIRASCA", "Airasca campanile", cs2gb.geo_to_gradi(
            44, 54, 59.527348), cs2gb.geo_to_gradi(-1, 25, 57.822861)
    )
    A1AEA = cs2gb.ConvPar(
        "ALA DI STURA", "Campanile Ala di Stura", cs2gb.geo_to_gradi(
            45, 18, 54.287619), cs2gb.geo_to_gradi(-1, 37, 1.14614)
    )
    A1AF = cs2gb.ConvPar(
        "ALBIANO D'IVREA", "Albiano", cs2gb.geo_to_gradi(
            45, 26, 0.217155), cs2gb.geo_to_gradi(0, 58, 23.0757)
    )

    point = (0.0, 0, 0)
    initGB()
    initWGS()
    SetConversion('DEBUG')

    set_parameter(A1AS)
    convert(point)
    set_parameter(A1AC)
    convert(point)
    set_parameter(A1JKB)
    convert(point)
    set_parameter(A1AD)
    convert(point)
    set_parameter(A1AEA)
    convert(point)
    set_parameter(A1AF)
    convert(point)

    gdir = 'F:\progetti\pysetl\grigliati_1'
    c = ConversionContext()
    d = ConversionContext()
    print("%d -- %d" % (id(c), id(d)))
