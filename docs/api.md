# API

# osmfilter


#### osmfilter.osmfilter.create_single_element(data, JSON_outputfile, whitefilter, blackfilter)
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


#### osmfilter.osmfilter.find_elements(data, ID_type_list)
**Purpose**

    use ID_type_list to find items in the prefiltered data and return 
    them in a dict

**Input**

    data: 

        dictionary of prefiltered Data

    ID_type_list: 

        [({OSM_id},{OSM_item_type}),]

        e.g. [(‘457320703’,’Node’),(‘457320703’,’Node’)]

**Output**

    elements:

        dictionary of Nodes, Ways and Relation


#### osmfilter.osmfilter.run_filter(elementname, countrycode, PBF_inputfile, JSON_outputfile, prefilter, whitefilter, blackfilter, NewPreFilterData=True, CreateElements=True, LoadElements=True, verbose=False)
**Purpose**

    Reads OSM pbf-files, filters data and storages the output as elements in JSON files\`

**Input**

    elementname:

        name of the element (e.g. ‘pipelines’)

    countrycode: 

        two digits, (e.g. ‘EU’)

    PBF_inputfile: 

        filepathname of inputfile

    JSON_outputfile: 

        filedir of output

    prefilter: 

        prefilter data (see doc: filter)

    whitefilter:

        whitefilter data (see doc:   :ref:

        ```
        `
        ```

        filter <filter>’ )

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

    Data[‘Node’][‘6037838916’][‘lonlat’]


#### osmfilter.osmfilter.write_elements(elements, elementname, outputdir)
**Purpose**

    writes elements to JSON file in outputdir

**Input**

    elements:   

        list of filtered element items

    elementname: 

        name of the elements (e.g. ‘pipelines’)

**Return**

    writes elements to jsonfile at outputdir


#### osmfilter.osmfilter.write_overview(elements, elementname, outputdir)
**Purpose**

    writes overview of elements to outputdir

**Input**

    elements:   

        list of filtered element items

    elementname: 

        name of the elements (e.g. ‘pipelines’)

    outputdir: 

        relative name of outputdir

# element_filter

Module to applicate the whitelist and blacklist filter for elements


#### osmfilter.element_filter.GetOSM_IDs(data, whitefilter, blackfilter)
**Purpose**

    method to sums up all filter results

**Return**

    returning unique list of OSM ids, that fulfill filter request


#### osmfilter.element_filter.filter4entry(data, blackfilter, whitefilter_entry)
**Purpose**

    filter prefiltered Data for elements

**Input** 

    Data:

        dictionary of prefiltered data

    blackfilter:

        blackfilterlist (see doc: filter)

    entry:

        entry from whitefilter (see doc: filter)

**Output**

    filterIDlist

        list of IDs which pass the check


#### osmfilter.element_filter.sum_filter_results(\*args)
**Purpose**

    helper method to sums up all filter results

**Return**

    returning unique list of OSM ids, that fulfill filter request

# osm_pickle

Module for pickle load and saving.


#### osmfilter.osm_pickle.pickleload(elements, filedir)
**Purpose**

    Restore elements dictionary from filedir


#### osmfilter.osm_pickle.picklesave(elements, filedir)
**Purpose**

    Saves elements dictionary at filedir

# pre_filter


#### osmfilter.pre_filter.benchmark(name)
**Purpose**

    is used to calculate the execution time of the prefiltering process


#### osmfilter.pre_filter.by_id(entry, idset)
**Purpose**

    checks if entry id is in the list idset


#### osmfilter.pre_filter.completefilter(entry, pre_filter)
**Purpose**

    checks if an OSM-entry passes the pre_filter


#### osmfilter.pre_filter.filter_pbf(filename, targetname, pre_filter)
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


#### osmfilter.pre_filter.load_entries(filename, ofs, header, selection)
**Purpose**

    load entries from pbf file(filename) and stores them in data dictionary


#### osmfilter.pre_filter.nofilter(entry, way_relation_members)
**Purpose**

    checks if an entry is a way and if its id is already stored in the list 
    way_relation_members

# osm_info

This module analysis the data dictionary for tags


#### osmfilter.osm_info.ReadJason(inputfile, verbose='yes')
**Purpose**

    Reading prefiltered OSM data from JSON file into dictionary
    Writes Nodes,Ways,Relation count into logfile

**Input**

    inputfile:

        dirpathname of JSON-file

**Calls** 

    showtagcount

**Output** 

    Data:

        dictionary of prefiltered data


#### class osmfilter.osm_info.Tee(\*files)
**Purpose**

    Parallel output to stdout and logfile=f

**Example**

    original = sys.stdout
    sys.stdout = Tee(sys.stdout, f)
    sys.stdout = original


#### osmfilter.osm_info.data2NodeWayRelation(data)
**Purpose**

    Splits data dictionary into 3 dictionaries for nodes, ways and relations


#### osmfilter.osm_info.showtagcount(OSMdict)
**Purpose**

    Calculates the tagcount for each tag in OSMdict

**Input**

    OSMdict

        prefiltered Data

**Output**

    Writes list with tags and their occurence count to stdout

# osm_colors

Helper string variables for colorized logging output in debugmode
