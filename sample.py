from  configparser                import ExtendedInterpolation
from  pathlib                     import Path
import configparser, contextlib
import os, sys, time
from osmfilter import  osm_colors          as CC
from osmfilter.osmfilter import run_filter as run_filter
#from osmfilter import osmfilter.run_filter as runfilter
#from .osmfilter import osmfilter          as osmfilter

import logging
#from L_OSM_ElementFilterList import whitefilter, blackfilter
from osmfilter.pbfreader import Node, Way, Relation


@contextlib.contextmanager
def benchmark(name):
    start = time.time()
    yield
    logger.info(CC.Green+'{} {:.2f}s'.format(name, time.time() - start)+CC.END)
    

if __name__=='__main__':

    select_all=True

    prefilter = {
        Node: {"substance"    : ["gas","cng"],
                      "pipeline"     : ["substation","marker","valve","pressure_control_station",select_all],
                      "product"      : ["gas","cng"],
                      "substation"   : ["valve","measurement", "inspection_gauge","compression","valve_group"],
                      "man_made"     : ["pipeline","pipeline_marker","pumping_station"],
                      "gas"          : ["station",select_all],
                      "content"      : ["gas","cng"],
                      "storage"      : ["gas","cng"],
                      "industrial"   : ["gas","terminal","wellsite","cng"]
                      },

        Way: {"substance"     : ["gas","cng"],
                     "man_made"      : ["gasometer","pipeline","petroleum_well","pumping_station",
                                       "pipeline_marker","pipeline_station","storage_tank","gas_cavern"],
                     "industrial"    : ["gas","terminal","cng"],
                     "gas"           : ["station"],
                     "content"       : ["gas","cng"],
                     "pipeline"      : ["substation","marker","valve","pressure_control_station",select_all],
                     "storage"       : ["gas","cng"],
                     "seamark:type"  : ["pipeline_submarine"],
                     "land_use"      : ["industrial:gas"]
                      },

        Relation: {"substance"    : ["gas","cng"],
                      "man_made"     : ["gasometer","pipeline","petroleum_well","pumping_station",
                                       "pipeline_marker","pipeline_station","storage_tank","gas_cavern"],
                      "industrial"   : ["gas","terminal","cng"],
                      "gas"          : ["station"],
                      "content"      : ["gas","cng"],
                      "pipeline"     : ["substation","marker","valve","pressure_control_station",select_all],
                      "storage"      : ["gas","cng"],
                      "seamark:type" : ["pipeline_submarine"],
                      "land_use"     : ["industrial:gas"]
                      }
        }

    blackfilter       = [("pipeline","substation"),]
    
    whitefilter=[(("man_made","pipeline"),("waterway","drain")),]
    

    logging.disable(logging.NOTSET)
    logging.basicConfig()
    logger=logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    

    
    Setup_OSM      = Path(os.getcwd() + '/Setup_OSM.ini')
    OSM_Path       = Path(os.getcwd())
    
    if sys.version_info.major == 2:
        raise RuntimeError('Unsupported python version')
    
    InfoOSM     = configparser.ConfigParser(interpolation=ExtendedInterpolation())
    InfoOSM.read(Setup_OSM)
    
    countrycode="LI"

    PBF_inputfile           = os.path.join(os.getcwd(),'tests/input/liechtenstein-latest.osm.pbf')
    JSON_outputfile         = os.path.join(os.getcwd(),'tests/output/LI/liechtenstein-latest.json')


    [Data,Elements]=run_filter('pipeline',countrycode,PBF_inputfile, JSON_outputfile,prefilter,whitefilter,blackfilter, NewPreFilterData = True, CreateElements  = True, LoadElements = True,verbose=True)
    logger.info('')
    logger.info(CC.Cyan+'Data:'+CC.End)
    logger.info(Data)
    logger.info(CC.Cyan+'Elements:'+CC.End)
    logger.info(Elements)


    
