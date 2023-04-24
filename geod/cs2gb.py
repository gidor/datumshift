#!/usr/bin/python
# -*- coding: UTF-8 -*-
#include "export.h"
#
import math
from pyproj import Proj

def geo_to_radianti(gr, pr,sec):
    """
       Funzione Di conversione gradi radianti
    """
    prf = pr / 60.0
    sec = sec / 3600.0
    rad = math.radians((math.fabs(gr) + math.fabs(prf) + math.fabs(sec)))# * (math.pi / 180)
    if (gr < 0.0 or pr < 0.0 or sec < 0.0) :
        rad = -rad
    return rad

def geo_to_gradi(gr, pr,sec):
    """
       Funzione Di conversione gradi primi secondi in gradi
    """
    prf = pr / 60.0
    sec = sec / 3600.0
    grad = (math.fabs(gr) + math.fabs(prf) + math.fabs(sec))
    if (gr < 0.0 or pr < 0 or sec < 0.0) :
        grad = (-1) * grad
    return grad
def RadToDeg(rad):
    return rad *(180 / math.pi)
def DegToRad(d):
    return math.radians(d) # * (math.pi / 180)

def DegToGps (grad):        
    if  grad<0 :
        s=-1
    else:
        s=1
    grad=s*grad
    g=s*math.floor(grad)
    prf = math.fabs(grad - g) * 60.0
    pr=math.floor(prf)
    sf=math.fabs(prf - pr) * 60.0
    return s*g,pr,sf



class  ConvPar():
    desc=""
    Nome=""
    Codicecatastale=""
    lat_0=0.0 #latitudine centro d'emanazione
    lon_0=0.0 #loomgitudine centro d'emanazione
    x_0=0.0  #falsa origine x
    y_0=0.0  # falsa origine y        
    Zona='N'
        #~ def __init__(self, desc, Nome,lat_g,lat_p,lat_s,long_g,long_p,long_s, x_0=0,y_0=0):
    def __init__(self, desc, Nome,lat_0,lon_0, x_0=0.0, y_0=0.0):
        self.desc=desc
        self.Nome=Nome
        self.lat_0=lat_0
        self.lon_0=lon_0
        self.x_0=x_0
        self.y_0=y_0
        self.Zona='N'
    def LatLon(self):
        return self.lat_0, self.lon_0
    def RadLatLon(self):
        return math.radians(self.lat_0), math.radians(self.lon_0)
            
    def __str__(self):
        s=str (id(self ))
        s+='\n descr ' + self.desc
        s+='\n nome  '+ self.Nome
        s+='\n deg lat  '+ str (self.lat_g)
        s+='\n prim lat '+ str (self.lat_p)
        s+='\n second lat '+ str (self.lat_s)
        s+='\n deg lon '+ str (self.long_g)
        s+='\n prim lon '+ str (self.long_p)
        s+='\n second lon '+ str (self.long_s)
        s+='\n x_0 '+ str (self.x_0)
        s+='\n y_0 '+ str (self.y_0)
        s+='\n zona '+ self.Zona
        return s
    




class GeoAngle():
    def __init__(self):
        self.rad=0 #math.NaN

    def fromDeg(self,     d):
        self.rad= math.radians(d) # * (math.pi / 180)

    def fromRad(self,     r):
        self.rad=r

    def fromGps(self ,gr, pr, sec):
        prf = pr / 60.0
        #print "pr=%f prf=%f" %(pr, prf)
        sec = sec / 3600.0
        self.rad = math.radians((math.fabs(gr) + math.fabs(prf) + math.fabs(sec)) )#* (math.pi / 180.0)
        if (gr < 0.0 or pr < 0.0 or sec < 0.0) :
            self.rad = -self.rad

    def asRad (self):
        return self.rad

    def asDeg(self):
        #~ return math.degrees(self.rad) # *180 / math.pi
        return self.rad *(180 / math.pi)

    def asGps (self):
        grad=self.asDeg()
        if  grad<0 :
            s=-1
        else:
            s=1
        grad=s*grad
        g=math.floor(grad)
        prf = math.fabs(grad - g) * 60.0
        pr=math.floor(prf)
        sf=math.fabs(prf - pr) * 60.0
        return s*g,pr,sf


def ang_gps(g, p,s):
    print (g, p,s)
    o=GeoAngle()
    o.fromGps(g, p,s)
    return o

def ang_rad(r):
    o=GeoAngle()
    o.fromRad(r)
    return o


"""
Public int trasfCoord(double *BOAGAN     ,
                      double *BOAGAE     ,
                      double CATASTALEX  ,
                      double CATASTALEY  ,
                      int    em          ,
                      int    FUSO        )
"""
#~ {
    #~ double LATORIGINE,LONGORIGINE,LATCATASTALE,LONGCATASTALE;
    #~ double LATMONTEMARIO,LONGMONTEMARIO,LATINTERNATIONAL,LONGINTERNATIONAL;
    #~ double C,S,T,T2,LG,GF,SF,PF,PL,GL,SL;
    #~ double DF0,DF1,DF2,DL0,DL1,DL2,DF,DL,FM;

def cassini_to_geonova02 (
        CATASTALEX  ,
        CATASTALEY  ,
        #em          ,
        #FUSO        ,
        ConvPar):

    ################################################################################
    ### DATI RELATIVI ALL'ELLISSOIDE INTERNAZIONALE.
    ################################################################################
    #FO=1500000,2520000
    #LO=-0.0602545835,0.0444651716
    ################################################################################
    ### Coordinate Geografiche di Monte Mario riferite all'Elissoide di Bessel
    ### orientato a Genova o Castanea delle Furie
    ################################################################################
    FR=0.7317021345,0.667845259
    LR=0.0616253021,-0.0535521556
    ################################################################################
    ################################################################################
    #KA = -0.0000000536614     #KB = 0.0000147717    #KC = -0.0000132161    #KD = -1.30566E-11    #KE = -0.0000264868    #KF = 0.00000481892    #KG = -0.000023873
    #KH = 0.00000000973    #KI = 0.00000668    #KL = -0.000106903    #KM = -0.0000726875    #KN = 0.000041306
    #KO = -0.000155367    #KP = -0.00000804748    #KQ = -0.00014923
    A6 =0.0
    B6 =0.0
    B8 =0.0
    SAB=0.0
    ENB=0.0
    ERB=0.0
    EN =0.0
    ER =0.0
    SA =0.0
    S2 =0.0
    C2 =0.0
    #A1 = 6365107.438    #A2 = 16100.592    #A4 = 16.9694    #A61 = 0.0223;
    ################################################################################
    #FUSO = FUSO - 1
    if (ConvPar.Zona=='N'):
        z=0
    else:
        z=1
    LATMONTEMARIO  = FR[z];
    LONGMONTEMARIO = LR[z];
    ################################################################################
    #~ LATORIGINE  = geo_to_radianti(ConvPar.lat_g  ,ConvPar.lat_p  ,ConvPar.lat_s  )
    #~ LONGORIGINE = geo_to_radianti(ConvPar.long_g ,ConvPar.long_p ,ConvPar.long_s )
    LATORIGINE , LONGORIGINE=ConvPar.RadLatLon()
    ################################################################################
    ### Conversione da coordinate piane a geografiche
    ################################################################################
    SAB = 6377397.15
    ENB = 0.006674372
    ERB = 0.006719218

    S  = math.sin(LATORIGINE)
    C  = math.cos(LATORIGINE)
    T  = math.tan(LATORIGINE)

    Q  = math.sqrt(1 - ENB * S * S)
    NF = SAB / Q
    RO = (SAB * (1 - ENB)) / ( Q * Q * Q)
    S2 = S * C
    C2 = C * C - S * S
    A6 = CATASTALEX / NF
    LATORIGINE = LATORIGINE + (CATASTALEX / RO) * (1.0 - 0.5 * ERB * A6 * (3.0 * S2 + A6 * C2));

    S  = math.sin(LATORIGINE)
    C  = math.cos(LATORIGINE)
    T  = math.tan(LATORIGINE)

    Q  = math.sqrt(1.0 - ENB * S * S)
    NF = SAB / Q
    RO = (SAB * (1 - ENB)) / (Q * Q * Q)

    B6 = CATASTALEY * CATASTALEY / NF
    B8 = (1.0 + 3.0 * T) / (12.0 * NF * NF)
    LATCATASTALE = LATORIGINE - B6 * T / (2.0 * RO) * (1 - B8 * CATASTALEY * CATASTALEY)
    LONGCATASTALE = LONGORIGINE + CATASTALEY / (NF * C) * (1.0 - T * T * B6 / (3.0 * NF))
    return LATCATASTALE, LONGCATASTALE


def Geomova02ToRoma40 (
        LATCATASTALE ,
        LONGCATASTALE,  #em          ,#FUSO        ,
        ConvPar):
    ################################################################################
    ### DATI RELATIVI ALL'ELLISSOIDE INTERNAZIONALE.
    ################################################################################
    #FO=1500000,2520000
    #LO=-0.0602545835,0.0444651716
    ################################################################################
    ### Coordinate Geografiche di Monte Mario riferite all'Elissoide di Bessel
    ### orientato a Genova o Castanea delle Furie
    ################################################################################
    FR=0.7317021345,0.667845259
    LR=0.0616253021,-0.0535521556
    ###
    KA = -0.0000000536614
    KB = 0.0000147717
    KC = -0.0000132161
    KD = -1.30566E-11
    KE = -0.0000264868
    KF = 0.00000481892
    KG = -0.000023873
    KH = 0.00000000973
    KI = 0.00000668
    KL = -0.000106903
    KM = -0.0000726875
    KN = 0.000041306
    KO = -0.000155367
    KP = -0.00000804748
    KQ = -0.00014923
    A6 =0.0
    B6 =0.0
    B8 =0.0
    SAB=0.0
    ENB=0.0
    ERB=0.0
    EN =0.0
    ER =0.0
    SA =0.0
    S2 =0.0
    C2 =0.0
    #~ A1 = 6365107.438
    #~ A2 = 16100.592
    #~ A4 = 16.9694
    #~ A61 = 0.0223;
    ###
    #FUSO = FUSO - 1
    if (ConvPar.Zona=='N'):
        z=0
    else:
        z=1
    ################################################################################
    LATMONTEMARIO  = FR[z]
    LONGMONTEMARIO = LR[z]

    ################################################################################
    ### Cambiamento di ellissoide
    ################################################################################
    DF0 = 0.000005386
    DL0 = 0.0
    DF  = (LATCATASTALE - LATMONTEMARIO)
    DL  = (LONGCATASTALE - LONGMONTEMARIO)
    FM  = (LATCATASTALE + LATMONTEMARIO) / 2.0
    DF1 = DF0 + (KA * DF) + (KB * DL) + (KC * DF * DL) + (KD * DL * DL)
    DL1 = DL0 + (KE * DF) + (KF * DL) + (KG * DF * DF) + (KH * DF * DL) + (KI * DL * DL)
    DF2 = (KL * DF) + (KM * DF * (math.sin(FM) * math.sin(FM))) + (KN * DL * DL)
    DL2 = (KO * DL) + (KP * DL) / (math.cos(FM)) + (KQ * DF * DL);

    LATINTERNATIONAL  = LATCATASTALE  + DF1 + DF2;
    LONGINTERNATIONAL = LONGCATASTALE - LONGMONTEMARIO + DL1 + DL2;
    return LATINTERNATIONAL  ,LONGINTERNATIONAL


def LatLong2ToBoaga (
        LATINTERNATIONAL ,
        LONGINTERNATIONAL,
        em          ,
        FUSO        ,
        ConvPar):
    A1 = 6365107.438
    A2 = 16100.592
    A4 = 16.9694
    A61 = 0.0223

    ################################################################################
    ### DATI RELATIVI ALL'ELLISSOIDE INTERNAZIONALE.
    ################################################################################
    FO=1500000,2520000
    LO=-0.0602545835,0.0444651716
    ################################################################################
    ### Coordinate Geografiche di Monte Mario riferite all'Elissoide di Bessel
    ### orientato a Genova o Castanea delle Furie
    ################################################################################
    #FR=0.7317021345,0.667845259
    #LR=0.0616253021,-0.0535521556

    FUSO = FUSO - 1

    ################################################################################
    ### Trasformazione da coordinate geografiche int a piane
    ################################################################################
    SA = 6375836.645
    EN = 0.006722670022
    ER = 0.006768170197

    S = math.sin(LATINTERNATIONAL)
    C = math.cos(LATINTERNATIONAL)
    T = math.tan(LATINTERNATIONAL)

    Q  = math.sqrt(1 - EN * S * S)
    NF = SA / Q
    RO = (SA * (1 - EN)) / (Q * Q * Q)

    ETA = ER * (C * C)
    DL  = LONGINTERNATIONAL - LO[FUSO]
    DL2 = DL * DL
    B   = A1 * LATINTERNATIONAL - 2 * A2 * S * C + A4 * math.sin(4 * LATINTERNATIONAL) - A61 * math.sin(6 * LATINTERNATIONAL)
    CX1 = NF * S * C * DL2 / 2
    CX2 = NF * S * C * C * C * (5 - T * T + 9 * ETA + 4 * ETA * ETA) * DL2 * DL2 / 24

    BOAGAN = B + CX1 + CX2

    CY1 = NF * C * DL
    CY2 = NF * C * C * C * (1 - T * T + ETA) * DL2 * DL / 6
    CY5 = NF * DL * DL * DL * DL * DL * C * C * C * C * C * (5 - 18 * T * T + T * T * T * T + 14 * ETA - 58 * T * T * ETA) / 120

    BOAGAE = FO[FUSO] + CY1 + CY2 + CY5

    return BOAGAE, BOAGAN ;
######################################################################################
######################################################################################
######################################################################################


######################################################################################
######################################################################################


def cs_test( point, parameters):
    x=point[0]
    y=point[1]
    convpar=parameters
    ###<2066> 
    proj='cass' 
    ###lat_0 = geo_to_gradi(convpar.lat_g, convpar.lat_p,convpar.lat_s)
    ###lon_0 = geo_to_gradi(convpar.long_g,convpar.long_p,convpar.long_s)
    lat_0,lon_0 = convpar.LatLon()
    x_0=convpar.x_0
    y_0=convpar.y_0
    #bessel bessel 
    a=6377397.155    
    rf=299.1528128   
    ###Bessel 1841    
    ###no_defs  <>
    CatProj=Proj(proj=proj, lat_0=lat_0 ,lon_0=lon_0 ,x_0=x_0 ,y_0=y_0 ,a=a ,rf=rf )
    print "=================================="
    print "%s %s" % (convpar.desc, convpar.Nome)
    LongGe,LatGe=CatProj(x,y, inverse=True)
    print "%.8f %.8f " %(LatGe, LongGe)
    LatGe1, LongGe1=cassini_to_geonova02 (x,y, convpar)
    #~ la=GeoAngle()
    #~ la.fromRad(LatGe1)
    #~ lo=GeoAngle()
    #~ lo.fromRad(LongGe1)
    #~ print "%.8f %.8f " %(LatGe1, LongGe1)
    print "%.8f %.8f " %(RadToDeg(LatGe1), RadToDeg(LongGe1))
    print "%.8f %.8f " %(lat_0, lon_0)
    print "=================================="
    ###<32632> 
    proj='utm' 
    zone=32 
    ellps='WGS84' 
    datum='WGS84' 
    units='m' 
    ##+no_defs  <>
    Wgs84Proj=Proj(proj=proj, zone=zone, ellps=ellps, datum=datum, units=units, no_defs=True )
    xwgs,ywgs=Wgs84Proj(LongGe,LatGe)
    print "%.8f %.8f " %(xwgs,ywgs)
    print "=================================="
    
    






if __name__ == "__main__":
    A1JKB=ConvPar("ABBADIA ALPINA (PINEROLO)","Abbadia campanile",geo_to_gradi(44,53,10.072171),geo_to_gradi(-1,36,51.320861))
    A1AC=ConvPar("AGLIE'","Agliè",geo_to_gradi(45,21,43.568556),geo_to_gradi(-1,9,12.498892))
    A1AD=ConvPar("AIRASCA","Airasca campanile",    geo_to_gradi(44,54,59.527348),geo_to_gradi(-1,25,57.822861))
    A1AEA=ConvPar("ALA DI STURA","Campanile Ala di Stura",geo_to_gradi(45,18,54.287619),geo_to_gradi(-1,37,1.14614))
    A1AF=ConvPar("ALBIANO D'IVREA","Albiano",geo_to_gradi(45,26,0.217155),geo_to_gradi(0,58,23.0757))
    #~ Catx=0.0
    #~ Caty=0.0
    #~ ang=ang_gps(44, 53, 10.072171)
    #~ print ang.asRad()
    #~ print ang.asDeg()
    #~ print ang.asGps()

    #~ ang=ang_gps(-1,36,51.320861)
    #~ print ang.asRad()
    #~ print ang.asDeg()
    #~ print ang.asGps()
    point=(0.0,0,0)
    cs_test( point, A1JKB)
    cs_test( point, A1AC)
    cs_test( point, A1AD)
    cs_test( point, A1AEA)
    cs_test( point, A1AF)
    


    #~ par=A1JKB
    #~ Bo_x , Bo_y =CassiniToBoaga ( Catx, Caty,1 , 1,par)
    #~ print Bo_x ,Bo_y

    #~ Ge_Lat, Ge_Long=cassini_to_geonova02 ( Catx, Caty, par)
    #~ print "Georafice catastali Genova 02"
    #~ print """LAT %f° %f' %f" """ % ang_rad(Ge_Lat).asGps()# ,ang_rad(Ge_Long).asGps() )
    #~ print """LONG %f° %f' %f" """ % ang_rad(Ge_Long).asGps()# ,ang_rad(Ge_Long).asGps() )


    #~ print Ge_Lat ,Ge_Long
    #~ Rm_Lat, Rm_Long=Geomova02ToRoma40 (Ge_Lat, Ge_Long,par)
    #~ print "Georafice Roma40"
    #~ print """LAT %f° %f' %f" """ % ang_rad(Rm_Lat).asGps()# ,ang_rad(Ge_Long).asGps() )
    #~ print """LONG %f° %f' %f" """ % ang_rad(Rm_Long).asGps()# ,ang_rad(Ge_Long).asGps() )

    #~ print Rm_Lat ,Rm_Long
    #~ Bo_x , Bo_y =LatLong2ToBoaga (Rm_Lat, Rm_Long,1, 1,par)
    #~ print Bo_x ,Bo_y



