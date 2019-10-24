import os
import sys
import logging

from osmfilter           import osm_colors as CC
from osmfilter.osmfilter import run_filter as run_filter
from osmfilter.pbfreader import Node, Way, Relation

def osmfilter():

    select_all="True" 

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





#    logging.disable(logging.INFO)
    logging.disable(logging.NOTSET)
    logging.basicConfig()
    logger=logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
#    logger.setLevel(WARNING)

    
    logger.info(CC.Caption + "============================="+ CC.End)
    logger.info(CC.Caption + "       osmfilter test        " + CC.End)
    logger.info(CC.Caption + "=============================" + CC.End)
    logger.info(" ")
    logger.info(" ")
    logger.info(" ")
    
    if sys.version_info.major == 2:
        raise RuntimeError('Unsupported python version')
    

    countrycode="LI"

    
    PBF_inputfile           = os.path.join(os.getcwd(),'tests/input/liechtenstein-latest.osm.pbf')
    JSON_outputfile         = os.path.join(os.getcwd(),'tests/output/LI/liechtenstein-latest.json')


    [Data,Elements]=run_filter('pipeline',countrycode,PBF_inputfile, JSON_outputfile,prefilter,whitefilter,blackfilter, NewPreFilterData = True, CreateElements  = True, LoadElements = True,verbose=False)
    logger.info('')
    logger.info('Stored prefilter data to "Data" and filtered elements to "Elements"')
    return Data,Elements
    
def test_osmfilter():
    Data,Elements=osmfilter()

    assert(len(Data['Way'])==2)
    assert(len(Data['Node'])==13)
    
    assert(len(Elements['pipeline']['Way'])==2)
    assert(len(Elements['pipeline']['Node'])==0)
    


    
