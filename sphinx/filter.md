# Filter

The following filter structures are used to filter OSM items by their tags.
Tags are key-value pair, e.g. **"substance":"gas"**.  
In this example, we the pre_filters to any identify gas transport data.
The blackfilter and whitefilter is then used to identify gas transport pipelines from  
the prefiltered data.



pre_filter
----------
The pre_filter is a whitelist filter which will pass any item, if one key-value condition is fulfilled.  
It consists of dictionary separated for each OSM item type, namely node,way and relation.  
For each key, several possible value options can be named.  
For example, **"substance": ["gas","cng"]**, will allow the values 
"gas" and "cng" for the key "gas".  
It is also possible to pass any value of a given key, by setting the True boolean.  



    pre_filter = {
    Node: {
           "substance"    : ["gas","cng"],
           "pipeline"     : ["substation","marker","valve","pressure_control_station",True],
           "product"      : ["gas","cng"],
           "substation"   : ["valve","measurement", "inspection_gauge","compression","valve_group"],
           "man_made"     : ["pipeline","pipeline_marker","pumping_station"],
           "gas"          : ["station",True],
           "content"      : ["gas","cng"],
           "storage"      : ["gas","cng"],
           "industrial"   : ["gas","terminal","wellsite","cng"]
              },

    Way: {
          "substance"     : ["gas","cng"],
          "man_made"      : ["gasometer","pipeline","petroleum_well","pumping_station",
                             "pipeline_marker","pipeline_station","storage_tank","gas_cavern"],
          "industrial"    : ["gas","terminal","cng"],
          "gas"           : ["station"],
          "content"       : ["gas","cng"],
          "pipeline"      : ["substation","marker","valve","pressure_control_station",True],
          "storage"       : ["gas","cng"],
          "seamark:type"  : ["pipeline_submarine"],
          "land_use"      : ["industrial:gas"]
          },

    Relation: {
              "substance"    : ["gas","cng"],
              "man_made"     : ["gasometer","pipeline","petroleum_well","pumping_station",
                               "pipeline_marker","pipeline_station","storage_tank","gas_cavern"],
              "industrial"   : ["gas","terminal","cng"],
              "gas"          : ["station"],
              "content"      : ["gas","cng"],
              "pipeline"     : ["substation","marker","valve","pressure_control_station",True],
              "storage"      : ["gas","cng"],
              "seamark:type" : ["pipeline_submarine"],
              "land_use"     : ["industrial:gas"]
              }
    }
    
blackfilter
-----------

The blacklist is a list of (key,value) tuples, which will not let items pass if one
of the (key,value) tuples is present. It is prioritized above the whitelist.

    blackfilter=[
                ("pipeline","substation"),
                ("substation","distribution"),
                ('usage', 'distribution'),
                ('pipeline:type','water'),
                ('pipeline:type', 'sewer'),
                ("pumping_station","water"),
                ("pumping_station","sewage"),
                ('pumping_station','wastewater'),
                ("type","wastewater"),
                ("type","fuel"),
                ("type","sewage"),
                ("type","oil"),
                ("type","water"),
                ("substance","sewage"),
                ("substance","water"),
                ("substance","hot_water"),
                ("substance","fuel"),
                ("substance","wastewater"),
                ("substance","rainwater"),
                ("substance", "drain"),
                ("substance", "heat"),
                ("substance", "gas,heat"),
                ("substance", "heat,gas"),
                ("substance", "ammonia"),
                ("substance", "ethylen"),
                ("substance","oil")
                ]
                
whitefilter
-----------

The whitelist filter is a list of list of (key,value) tuples.
If any list of (key,value) tuples is present, the item will pass  
if it is not blocked by the blacklist at the same time.


    whitefilter=[
                 (("man_made","pipeline"),("substance","gas")),
                 (("man_made","pipeline"),("substance","cng")),
                 (("man_made","pipeline"),("substance","natural_gas")),
                 (("man_made","pipeline"),("pipeline:type","natural_gas")),
                 (("man_made","pipeline"),("type","gas")),
                 (("man_made","pipeline"),("type","natural_gas")),  
                 (("man_made","pipeline"),("type","cng")), 
                 (("man_made","pipeline"),("industrial","gas")), 
                 (("man_made","pipeline"),("industrial","cng")), 
                 (("man_made","pipeline"),("industrial","natural_gas"))
                ]
