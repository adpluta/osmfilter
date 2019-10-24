
import osmfilter.osm_colors    as CC
from   pathlib           import Path
from osmfilter.pbfreader import (osmformat_pb2, read_blob, Node, Way,
                                  Relation, read_entries, pool_file_query)
import sys 
import time 
import contextlib
import multiprocessing
import json
import os
import logging

logging.basicConfig()
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@contextlib.contextmanager
def benchmark(name):
    '''
    **Purpose**
        is used to calculate the execution time of the prefiltering process
    '''
    start = time.time()
    logger.info(f'starting {name}')
    yield
    logger.info(f'done {name} {time.time() - start:.3f}s')
    
def load_entries(filename, ofs, header, selection):
    '''
       **Purpose**
           load entries from pbf file(filename) and stores them in data dictionary
    '''
    data = {Node: [], Way: [], Relation: []}
    with open(filename, 'rb') as fileobj:
        entries = osmformat_pb2.PrimitiveBlock()
        entries.ParseFromString(read_blob(fileobj, ofs, header))
        for entry in read_entries(entries):
            if entry.id not in selection[type(entry)]:
                continue
            data[type(entry)].append(entry)
    return data

def by_id(entry, idset):
    '''
    **Purpose**
        checks if entry id is in the list idset
    '''
    return entry.id in idset

def completefilter(entry,pre_filter):
    '''
    **Purpose**
        checks if an OSM-entry passes the pre_filter
    '''
    filtermap = pre_filter[type(entry)]
    for key in filtermap.keys():
        if key in entry.tags.keys():
            if any(value==True or value in entry.tags.get(key)  for value in filtermap.get(key)):
                return True

def nofilter(entry,way_relation_members):
    '''
    **Purpose**
        checks if an entry is a way and if its id is already stored in the list 
        way_relation_members
    '''
    return type(entry) is Way and entry.id in way_relation_members

def filter_pbf(filename, targetname,pre_filter):
    """
    **Purpose**
        Parallized pre-Filtering of OSM file by a pre_filter
    **Input** 
        filename:
            PBF file
        pre_filter:
            (see doc: filter)
    **Output**
        targetname:
            JSON-file
    """
    if Path(filename).is_file():
        logger.info(CC.Caption+'PreFilter OSM GAS DATA'+CC.End)
        logger.info('InputFile     : ' + CC.Cyan + filename + CC.End ) 
        filesize=str(os.stat(filename).st_size)
        logger.info('Size          : ' '{:<15}'.format(str(round(int(filesize)/1000))) + ' kbyte')
        timeestimate = float(filesize)/(1750000)
        logger.info("Estimated Time: " "{:<15.2f}".format(timeestimate) +' s')
        logger.info("=============================")
    else:
        logger.info(CC.Red + 'OSM_raw_data does not exist' + CC.END)
        sys.exit()
    
    time1 = time.perf_counter()
    
    with multiprocessing.Pool(8) as pool:
        query = pool_file_query(pool, filename)
        entries = list(query(completefilter,pre_filter))
        node_relation_members = set()
        way_relation_members = set()
        way_refs = set()
        relation_way_node_members=set()
        for entry in entries:
            if type(entry) is Relation:
                for id, typename, role in entry.members:
                    if typename == 'NODE':
                        node_relation_members.add(id)
                    elif typename == 'WAY':
                        way_relation_members.add(id)
            if type(entry) is Way:
                way_refs.update(entry.refs)
        
        entries2 = list(query(nofilter, way_relation_members))
        
        for entry in entries2:
                relation_way_node_members.update(entry.refs)
                
        entries.extend(query(by_id, node_relation_members | way_refs | 
                way_relation_members|relation_way_node_members))

        entries.sort(key=lambda entry: entry.id)
        jsondata = {}
        jsondata['Node'] = {
            entry.id: dict(entry._asdict())
            for entry in entries if type(entry) is Node
                
        }
        jsondata['Way'] = {
            entry.id: dict(entry._asdict())
            for entry in entries if type(entry) is Way
        }
        jsondata['Relation'] = {
            entry.id: dict(entry._asdict())
            for entry in entries if type(entry) is Relation
        }

        time2 = time.perf_counter()
        os.makedirs(os.path.dirname(targetname), exist_ok=True)
        #create outputdirectory if it does not exist
        with open(targetname, 'w') as target:
            json.dump(jsondata, target, ensure_ascii=False, indent=4, separators=(',', ':'))

        mesA='Outputfile    : '
        filesize=str(os.stat(targetname).st_size)
        mesB=CC.Cyan + targetname + CC.End +'\n'
        mesC='Size          : ' + '{:<15}'.format(str(round(int(filesize)/1000))) + ' kbyte \n'
        mesD="Time Elapsed  : " "{:<15.2f}".format(time2 - time1) + " s"  + '\n'
        message=mesA + mesB + mesC + mesD + '\n'
        logger.info(message)
