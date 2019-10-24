from osmfilter.create_elements import create_elements
import osmfilter.osm_colors              as CC
import logging

logging.basicConfig()
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def read(PBF_inputfile,JSON_outputfile,pre_filter,whitefilter,
      blackfilter,elementname='pipelines',countrycode = 'EU',
      NewPreFilterData = False, CreateElements  = False,LoadElements = True
      ):
    
    """ 
    **Purpose**
    This function calls create elements
    This function reads OSM pbf-files, filters data and storages the output as elements in JSON files`
    
    **Input**
    
    PBF_inputfile:
        pathname and filename of the pbf file  
    JSON_outputfile:
        path of the outputdirectory  
    countrycode:    
        2 digit country (will be used to create sub-outputdirectory)  
    prefilter:    
        prefilter-list for prefilter  (see doc filter)
    whitefilter:    
        whitefilterlist for element filter (see doc filter)
    blackfilter:   
        blackfilterlist for element filter (see doc filter)
    NewPreFilterData:    
        create, filter and store data from pbf with prefilter  
    CreateElements:      
        create, filter and store elements with whitefilter and blackfilter  
    LoadElements:        
        load elements from stored elements data  
    
    **Return**

    Data:     
        dict of prefiltered Data
    Elements: 
        dict filtered Elements
    
    **Example**
    
    Access output:
        Data['Node']['6037838916']['lonlat']
    """
        
    logger.info(CC.Caption+' Creating OSM net'+CC.End)
    logger.info (f'Create:{CreateElements}')
    [Data,Elements] = create_elements(elementname,countrycode,PBF_inputfile,
                          JSON_outputfile,pre_filter, whitefilter,blackfilter,NewPreFilterData=NewPreFilterData, 
                          CreateElements=CreateElements, LoadElements=LoadElements)
    return Data,Elements
