# ==========
# Grigliato2NTv2.py
# ==========
##
# A simple converter from IGMI's gr1 and gr2 grid shift format
# see http://www.igmi.org/prodotti/ to the Canadian NTv2 format
# that is handled by a large number of applications including
# proj.4
##
# Specifications:
# ---------------
# Canadian original spec:
# http://www.geod.nrcan.gc.ca/pdf/ntv2_guide_e.pdf
# Australian spec:
# http://www.sli.unimelb.edu.au/gda94/ and in particular
# http://www.geom.unimelb.edu.au/gda94/SoftDoc.pdf
# German spec:  (most precise, but in German)
# http://crs.bkg.bund.de/crseu/crs/descrtrans/BeTA/BETA2007dokumentation.pdf
# contains proj.4 use examples
# project page:
# http://crs.bkg.bund.de/crseu/crs/descrtrans/BeTA/de_dhdn2etrs_beta.php
# Additional Insight:
# http://www.stjohnspointl.co.uk/gis/france.htm
##
# Additional official adoptions (beyond who specified):
# -----------------------------
# * New Zealand NTv2 page:
# http://www.linz.govt.nz/core/surveysystem/geodeticinfo/conversions/datums/distortiongrid/index.html
# * France adopts NTv2:
# http://admin.geocatalogue.fr/geocatadmin/static/documents/ANNEXE_Technique_Geoportail.pdf
# http://www.certu.fr/download.php?file_url=IMG/pdf/signature37.pdf
# search for "NTv2", already included in trunk of proj.4:
# http://cia.vc/stats/author/didier/.message/0]
##
# NTv2 support by various software:
# ---------------------------------
# * proj.4 and all the lots of applications that include it:
# GRASS, Quantum GIS, PostGIS, Mapserver, OGR etc.
# * Oracle Spatial
# http://download-uk.oracle.com/docs/cd/B19306_01/appdev.102/b14255/sdo_cs_ref.htm#CHDDIAGG
# * ESRI ArcGIS
# http://www.esricanada.com/EN_support/628.asp
# http://support.esri.com/index.cfm?fa=knowledgebase.techarticles.articleShow&d=22610
# * ESRI ArcIMS
# http://edndoc.esri.com/arcims/9.2/elements/dattrans.htm
# ad es. 1313 NAD_1927_To_NAD_1983_NTv2_Canada
# * Intergraph GeoMedia
# http://srmwww.gov.bc.ca/gis/GeoMedia/NTv2.html
# * PCI
# http://www.pcigeomatics.com/services/support_center/faqs/geo_data_v10.html#NTV2
# * MapInfo
# http://reference.mapinfo.com/software/mapinfo_pro/english/9.0.2/MIPro_902_RN.pdf
# * FME
# http://www.safe.com/aboutus/news/2007/104/index.htm
##
# ==============================================================
# copyright: Comune di Grosseto
# license:   GPL any version
# author:    Bud P. Bruegger <[EMAIL PROTECTED]>
__version__ = "v0.4, 11/2/2008"
# ==============================================================

import math
import os.path
from struct import pack
from types import StringType
from Grigliato import Grigliato


# -- file and grid naming ------------------
def deriveNames(inFName, sigmaSecs):
    ascExt = "asc"
    binExt = "gsb"  # Grid Shift Binary
    # --
    subGridName, ext = os.path.splitext(os.path.basename(inFName))
    subGridName = "%s_%s" % ("IGMI", subGridName)
    pathWOext = os.path.splitext(inFName)[0]
    outAscName = "%s.%s" % (pathWOext, ascExt)
    outBinName = "%s.%s" % (pathWOext, binExt)
    return subGridName, outAscName, outBinName

# -- write out files -------------------


class HeaderEl(object):
    def __init__(self, label, binFormat, ascFormat, gsaFormat):
        self.label = label
        self.ascFormat = ascFormat
        self.gsaFormat = gsaFormat
        self.binFormat = "%s%s" % (endianity, binFormat)
        #headerDict[label] = self

    def binRep(self, valDict):
        # it seems that in a new version, all strings
        # need to be blank- not null-padded!
        labelStr = labelAscFormat % self.label
        #labelStr = pack(labelBinFormat, self.label)
        val = valDict[self.label]
        if type(val) == StringType:
            valStr = self.ascFormat % val
        else:
            valStr = pack(self.binFormat, val)
        return "%s%s" % (labelStr, valStr)

    def ascRep(self, valDict):
        # ~ labelStr = labelAscFormat % self.label
        labelStr = self.label
        valStr = self.ascFormat % valDict[self.label]
        format = self.gsaFormat
        # ~ return "%s%s\n" % (labelStr, valStr)
        return format % (labelStr, valDict[self.label])


# -- endianity and node format ------------------
endianity = '<'  # little endian
nodeBinFormat = "%sffff" % endianity
nodeAscFormat = '%10.6f%10.6f%10.6f%10.6f\n'
labelAscFormat = "%-8s"
labelBinFormat = "%s8s" % endianity


def node_bin_rep(nodeVals:list[float])-> bytes:
    return pack(nodeBinFormat, *nodeVals)


def node_asc_rep(nodeVals:float)-> str:
    return nodeAscFormat % nodeVals


def nm_gr(inDir:dir, tgr:str)-> tuple[str,str,str]:
    ascExt = "_t.asc"
    binExt = "_t.gsb"  # Grid Shift Binary
    #subGridName = "IGMI"+tgr
    subGridName = tgr
    outAscName = inDir+os.sep+subGridName + ascExt
    outBinName = inDir+os.sep+subGridName + binExt
    return subGridName, outAscName, outBinName


def grigliato_to_ntv2(inDir:str, gr: Grigliato):
    # ~ from Grigliato import Grigliato
    # ~ gr=Grigliato(inDir)
    # minimumu grid cel SO
    LatS = gr.Fi_SO_VAL
    LongW = gr.La_SO_VAL
    # ~ import cs2gb
    # ~ g,p,s=cs2gb.DegToGps(LatS)
    # ~ g1,p1,s1=cs2gb.DegToGps(LongW)
    # ~ print "Lat/Lon Minimum grid cel SW %.0f %.0f'%.8f\" %.0f %.0f'%.8f\" " %(g,p,s,g1,p1,s1)

    LatSSecs = LatS * 3600
    LongWSecs = LongW * 3600

    # maximus grid cel NE
    LatN = gr.Fi_NE_VAL
    LongE = gr.La_NE_VAL
    # ~ g,p,s=cs2gb.DegToGps(LatN)
    # ~ g1,p1,s1=cs2gb.DegToGps(LongE)
    # ~ print "Lat/Lon maximus grid cel NE %.0f %.0f'%.8f\" %.0f %.0f'%.8f\" " %(g,p,s,g1,p1,s1)

    LatNSecs = LatN * 3600
    LongESecs = LongE * 3600

    # Lat cell spacing is originaly 5' minutes
    LatIncSecs:float  = 5.0 * 60.0
    # ~ LatIncSecs = 2.5 * 60
    # Long cell spacing is originaly 7'30"
    LongIncSecs:float = 7.5 * 60.0
    # ~ LongIncSecs = 2.5 * 60

    # Grird_Point_per_Row
    # ~ GrirdPointRow =int(math.floor(1+(abs(LongESecs-LongWSecs)/LongIncSecs)))
    GrirdPointRow:int = int(math.floor(1+(abs(LongESecs-LongWSecs)/LongIncSecs)))
    print("GrirdPointRow %d" % GrirdPointRow)
    # Grird_Point_per_Column
    # ~ GrirdPointCol = int(math.floor(1+(abs(LatNSecs-LatSSecs)/LatIncSecs)))
    GrirdPointCol = int(math.floor(1+(abs(LatNSecs-LatSSecs)/LatIncSecs)))
    print("GrirdPointCol %d" % GrirdPointCol)

    noNodes = GrirdPointRow * GrirdPointCol
    print("calcolate  %d celle" % noNodes)

    print("LatSSecs  %f" % LatSSecs)
    print("LatNSecs  %f" % LatNSecs)
    print("LongWSecs %f" % LongWSecs)
    print("LongESecs %f" % LongESecs)

    # Correct longESecs with resampling grid size
    E = LongWSecs + ((GrirdPointRow - 1) * LongIncSecs)
    N = LatSSecs + ((GrirdPointCol - 1) * LatIncSecs)
    LongESecs = E
    LatNSecs = N
    print("LatSSecs  %f" % LatSSecs)
    print("LatNSecs  %f" % LatNSecs)
    print("LongWSecs %f" % LongWSecs)
    print("LongESecs %f" % LongESecs)

    gridVersion = gr.epocagrid_WGS84_Roma40.strip().strip('"')

    # create precision column from constant set above
    # IGMI orderes nodes from lower left to upper right
    # NTv2 wants them from lower right to upper left
    # rows thus need to be inverted:

    subGridName, outAscName,  outBinName = nm_gr(inDir, "R40WGS")

    # -- assign header values -------------------------
    hdVals = {}
    hdVals['NUM_OREC'] = 11  # seems required for NTv2 files
    hdVals['NUM_SREC'] = 11  # seems required for NTv2 files
    hdVals['NUM_FILE'] = 1
    hdVals['GS_TYPE'] = 'SECONDS'
    hdVals['VERSION'] = 'NTv2.0'
    hdVals['SYSTEM_F'] = 'Roma40'
    hdVals['SYSTEM_T'] = 'WGS84'
    hdVals['MAJOR_F'] = 6378388.000  # Hayford international
    hdVals['MINOR_F'] = 6356911.946  # from paper by Di Filippo
    hdVals['MAJOR_T'] = 6378137.000  # WGS84
    hdVals['MINOR_T'] = 6356752.314  # from paper by Di Filippo
    # --
    hdVals['SUB_NAME'] = subGridName
    hdVals['PARENT'] = 'NONE'
    hdVals['CREATED'] = '02-01-01'  # gridVersion
    hdVals['UPDATED'] = '02-01-01'  # gridVersion
    hdVals['S_LAT'] = LatSSecs
    hdVals['N_LAT'] = LatNSecs
    # all positive "positive E longitudes" need to be converted
    # to negative "positive W" longitudes
    hdVals['E_LONG'] = -LongESecs
    hdVals['W_LONG'] = -LongWSecs
    hdVals['LAT_INC'] = LatIncSecs
    hdVals['LONG_INC'] = LongIncSecs
    hdVals['GS_COUNT'] = noNodes
    # --
    hdVals['END'] = '0.33E+33'  # footer (not really a header element ;-)
    # --    return hdVals, shiftLines
    #########################################
    # Directly from
    # "GDAit Software Architecture Manual"
    # http://www.geom.unimelb.edu.au/gda94/SoftDoc.pdf
    # Appendix C. NTv2 Grid Shift File, pages 25-30
    hdList = [
        # == Grid Shift File Overview Information
        #   Table C.2
        HeaderEl('NUM_OREC', 'q', '%3d', '%-8s%3d\n'),
        HeaderEl('NUM_SREC', 'q', '%3d', '%-8s%3d\n'),
        HeaderEl('NUM_FILE', 'q', '%3d', '%-8s%3d\n'),
        HeaderEl('GS_TYPE', '8s', '%-8s', '%-8s%-8s\n'),
        HeaderEl('VERSION', '8s', '%-8s', '%-8s%-8s\n'),
        HeaderEl('SYSTEM_F', '8s', '%-8s', '%-8s%-8s\n'),
        HeaderEl('SYSTEM_T', '8s', '%-8s', '%-8s%-8s\n'),
        HeaderEl('MAJOR_F', 'd', '%12.3f', '%-8s%12.3f\n'),
        HeaderEl('MINOR_F', 'd', '%12.3f', '%-8s%12.3f\n'),
        HeaderEl('MAJOR_T', 'd', '%12.3f', '%-8s%12.3f\n'),
        HeaderEl('MINOR_T', 'd', '%12.3f', '%-8s%12.3f\n'),
        # == Sub Grid Overview Information
        #   Table C.3
        HeaderEl('SUB_NAME', '8s', '%-8s', '%-8s%-8s\n'),
        HeaderEl('PARENT', '8s', '%-8s', '%-8s%-8s\n'),
        HeaderEl('CREATED', '8s', '%-8s', '%-8s%-8s\n'),
        HeaderEl('UPDATED', '8s', '%-8s', '%-8s%-8s\n'),
        HeaderEl('S_LAT', 'd', '%15.6f', '%-8s%15.6f\n'),
        HeaderEl('N_LAT', 'd', '%15.6f', '%-8s%15.6f\n'),
        HeaderEl('E_LONG', 'd', '%15.6f', '%-8s%15.6f\n'),
        HeaderEl('W_LONG', 'd', '%15.6f', '%-8s%15.6f\n'),
        HeaderEl('LAT_INC', 'd', '%15.6f', '%-8s%15.6f\n'),
        HeaderEl('LONG_INC', 'd', '%15.6f', '%-8s%15.6f\n'),
        HeaderEl('GS_COUNT', 'q', '%6d', '%-8s%6d\n')]
    footerEl = HeaderEl('END', '8s', '%-8s', '%-8s%-8s\n')

    # -- write out files -------
    outAsc = open(outAscName, 'wt')
    outBin = open(outBinName, 'wb')
    for hd in hdList:
        # print hd.ascRep(hdVals),
        outAsc.write(hd.ascRep(hdVals))
        outBin.write(hd.binRep(hdVals))

    LAT = LatSSecs  # latitudine della cella
    N_LAT = LatNSecs  # latitudine della cella + nord
    W_LONG = LongWSecs  # longiutudine della cella + west
    c = 0
    r = 0
    co = 0

    while LAT < N_LAT+1:
        LONG = LongESecs
        while LONG > W_LONG-1:
            sf, sl = gr.get_shift_secs(LAT, LONG, gr.Roma40, gr.WGS84)
            # negative long corrects for "positive east system"
            node = (sf, -sl, 0.0, 0.0)
            outAsc.write(node_asc_rep(node))
            outBin.write(node_bin_rep(node))
            LONG -= LongIncSecs
            c += 1
            co += 1
        LAT += LatIncSecs
        r += 1
        col = co
        co = 0
    print("scritte %d colonne" % col)
    print("scritte %d celle" % c)
    print("scritte %d righe " % r)
    outAsc.write(footerEl.ascRep(hdVals))
    outBin.write(footerEl.binRep(hdVals))

    outAsc.close()
    del outAsc
    outBin.close()
    del outBin


# ================================================================
if __name__ == '__main__':
    gdir = 'd:\progetti\pysetl\grigliati_1'
    #gdir ='h:\pysetl\grigliati_1'
    grigliato_to_ntv2(gdir)
