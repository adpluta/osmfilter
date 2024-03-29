#!/usr/bin/env python3

import osmfilter.osm_colors           as CC
import osmfilter.pre_filter           as pre_filter
import osmfilter.osm_info             as osm_info
import osmfilter.osm_pickle           as osm_pickle
import os
from osmfilter.element_filter     import GetOSM_IDs

import json
import sys
import pprint
import logging

logging.basicConfig()
logger=logging.getLogger(__name__)
#logger.setLevel(logging.INFO)
logger.setLevel(logging.WARNING)

def write_overview(elements,elementname,outputdir):
    """
    **Purpose**
        writes overview of elements to outputdir
        
    **Input**
        elements:   
            list of filtered element items
        elementname: 
            name of the elements (e.g. 'pipelines')
        outputdir: 
            relative name of outputdir
    """
    
    original = sys.stdout
    if outputdir  != "":
        filename   = elementname+"_short.json"
        logdirbase = (os.path.dirname(outputdir)+"/Analysis/Elements")
        logfile    = os.path.join(logdirbase,filename)
#        print("Outputfile: ", logfile)
        os.makedirs(os.path.dirname(logfile), exist_ok=True)
        f = open(logfile, 'w')
        sys.stdout = f#Tee(f)
    sys.stdout.write("Overview OSM "+elementname +"\n")
    sys.stdout.write("===========\n")
    sys.stdout.write("Nodes:       " + "{:>26}".format(str(len(elements["Node"])))+"\n")
    sys.stdout.write("Ways:        " + "{:>26}".format(str(len(elements["Way"])))+"\n")
    sys.stdout.write("Relations:   " + "{:>26}".format(str(len(elements["Relation"])))+"\n")
    sys.stdout.write("===========\n\n\n")
    counter=0

    for entry in elements["Node"]:
        sys.stdout.write('\n------Node--------\n')
        counter+=1
        sys.stdout.write('\n'+'Nr. '+str(counter)+" of "+ elementname+"\n")
        sys.stdout.write('Id: ' +str(elements["Node"][entry]['id'])+"\n")
        sys.stdout.write('Tags:\n')
        dictstring = pprint.pformat(elements["Node"][entry]['tags'],width=35)
        sys.stdout.write(dictstring +"\n")
    counter=0
    for entry in elements["Way"]:
        sys.stdout.write('\n------Way--------\n')
        counter+=1
        sys.stdout.write('\n'+'Nr. '+str(counter)+" of "+ elementname+"\n")
        sys.stdout.write('Id: ' +str(elements["Way"][entry]['id'])+"\n")
        sys.stdout.write('Tags:\n')
        dictstring = pprint.pformat(elements["Way"][entry]['tags'],width=35)
        sys.stdout.write(dictstring +"\n")
    counter=0
    for entry in elements["Relation"]:
        sys.stdout.write('\n------Relation--------\n')
        counter+=1
        sys.stdout.write('\n'+'Nr. '+str(counter)+" of "+ elementname+"\n")
        sys.stdout.write('Id: ' +str(elements["Relation"][entry]['id'])+"\n")
        sys.stdout.write('Tags:\n')
        dictstring = pprint.pformat(elements["Relation"][entry]['tags'],width=35)
        sys.stdout.write(dictstring +"\n")
    sys.stdout = original
    pass

def write_elements(elements,elementname,outputdir):
    """
    **Purpose**
        writes elements to JSON file in outputdir
        
    **Input**
        elements:   
            list of filtered element items
        elementname: 
            name of the elements (e.g. 'pipelines')
        
    **Return**
        writes elements to jsonfile at outputdir
    """
    
    write_overview(elements,elementname,outputdir)
    filename   = elementname+".json"
    logdirbase = (os.path.dirname(outputdir)+"/Analysis/Elements/")
    logfile    = os.path.join(logdirbase,filename)
    
    os.makedirs(os.path.dirname(logfile), exist_ok=True)
    with open(logfile, 'w') as target:
            json.dump(elements, target, indent=4, separators=(',', ':'))
    pass

def find_elements(data, ID_type_list):
    """
    **Purpose**
        use ID_type_list to find items in the prefiltered data and return 
        them in a dict
    
    **Input**
        data: 
            dictionary of prefiltered Data  
        ID_type_list: 
            [({OSM_id},{OSM_item_type}),]  
            
            e.g. [('457320703','Node'),('457320703','Node')] 
             
    **Output**
        elements:
            dictionary of Nodes, Ways and Relation
    """
    
    elements={'Node':{},'Way':{},'Relation':{}}

    for i in range(len(ID_type_list)):
        if ID_type_list[i][1] == "Way":
                elements['Way'][ID_type_list[i][0]]=data["Way"][ID_type_list[i][0]]
        elif ID_type_list[i][1] == "Node":
                elements['Node'][ID_type_list[i][0]]=data["Node"][ID_type_list[i][0]]
        elif ID_type_list[i][1] == "Relation":
                elements['Relation'][ID_type_list[i][0]]=data["Relation"][ID_type_list[i][0]]
    return elements


def create_single_element(data,JSON_outputfile,whitefilter,blackfilter):
    '''
    **Purpose** 
        the prefiltered OSM data are filtered for a specific element.

    **Input**
        data:
            dictionary of prefiltered data
        whitefilter:
            (see doc: filter)
        blackfilter:
            (see doc: filter)
        
    **Return** 
        elements:
           dictionaries with filtered elements
    '''
    
    elementIDs = GetOSM_IDs(data,whitefilter,blackfilter)
    elements = find_elements(data,elementIDs)
    write_elements(elements,"pipelines",JSON_outputfile)
    
    logging.info('Save elements as jsonfiles at\n'+CC.Cyan+ os.path.dirname(JSON_outputfile)+"/Analysis/Elements\n"+CC.End)
    return elements


def run_filter(elementname,countrycode,PBF_inputfile,JSON_outputfile,
                    prefilter,whitefilter,blackfilter, NewPreFilterData=True, 
                    CreateElements=True, LoadElements=True,verbose=False):
    '''
    **Purpose**
        Reads OSM pbf-files, filters data and storages the output as elements in JSON files`
 
           
    **Input**
        elementname:
            name of the element (e.g. 'pipelines')
        countrycode: 
            two digits, (e.g. 'EU')
        PBF_inputfile: 
            filepathname of inputfile
        JSON_outputfile: 
            filedir of output
        prefilter: 
            prefilter data (see doc: filter)
        whitefilter:
            whitefilter data (see doc:   :ref:`filter <filter>' )
        blackfilter:
            blackfilter data (see doc: filter)
        NewPreFilterData:
            prefilter and store Data from pbf
        CreateElements:
            filter and store Elements from Data
        LoadElements:
            load Elements 
           
    **Return**
       Data:
           prefiltered Data of pbf
       Elements:
           filtered Elements from Data
              
    **Example**
    
    Access output:
        Data['Node']['6037838916']['lonlat']
    '''
    if verbose == False: logging.disable(logging.INFO)

    element         = ()
    Data           = {}
    
    if NewPreFilterData==True:
        ###Create and Save Gas Data
        logger.info(CC.Script+'Filter Gas Data for country ' + countrycode+ CC.End)
        logger.info('Load OSM data from '+CC.Cyan+ PBF_inputfile+'\n'+CC.End)
        pre_filter.filter_pbf(PBF_inputfile, JSON_outputfile,prefilter)
        logger.info('\nRead gas data from \n'+CC.Cyan+ JSON_outputfile+CC.End)
        Data = osm_info.ReadJason(JSON_outputfile,verbose='no')
        ###Save Gas Data (Pickle)
        DataDict = {"Data":Data}
        logger.info('\nPickle gas data to \n'+os.path.join(os.getcwd(),os.path.dirname(JSON_outputfile))+CC.End)
        osm_pickle.picklesave(DataDict,os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(JSON_outputfile))))
    
    # loading of OSM Gas daten filtered data
    DataDict      = {"Data":Data}
    DataDict      = osm_pickle.pickleload(DataDict,os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(JSON_outputfile))))
    Data      = DataDict["Data"]
    
    if CreateElements==True:
        ###Create Elements
        logger.info(CC.Script+'\nCreate the OSM-elements\n'+CC.End)
        element = create_single_element(Data,JSON_outputfile,whitefilter,blackfilter)
        ###Save Elements(Pickle)
    Elements = { 
                  elementname:element
                }

    if CreateElements==True:
        logger.info('\nPickle OSM-elements to \n'+CC.Cyan+ os.path.join(os.getcwd(),os.path.dirname(JSON_outputfile), 'Elements/')+'\n'+CC.End)
        osm_pickle.picklesave(Elements,os.path.join(os.getcwd(),os.path.dirname(JSON_outputfile), 'Elements/'))
        
    if LoadElements==True:
        logger.info('\nUnpickle OSM-elements from \n'+CC.Cyan +os.path.join(os.getcwd(),os.path.dirname(JSON_outputfile), 'Elements/')+CC.End)

        Elements = osm_pickle.pickleload(Elements,os.path.join(os.getcwd(),os.path.dirname(JSON_outputfile), 'Elements/'))    
            
    return Data, Elements


