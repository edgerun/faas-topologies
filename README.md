# faas-topologies
Framework to generate geo-distributed and `ether` based topologies by using the OpencelliD dataset as baseline. 


##ether: Edge Topology Synthesizer
Details: https://github.com/edgerun/ether
##OpencelliD
This project offers a public database and includes worldwide data of geo-distributed cell towers. The corresponding database is being updated on a daily basis.
<div class="license">
    <span xmlns:dct="http://purl.org/dc/terms/" property="dct:title"><a xmlns:cc="https://creativecommons.org/ns#" href="https://opencellid.org" property="cc:attributionName" rel="cc:attributionURL">OpenCelliD Project</a></span><a xmlns:cc="https://creativecommons.org/ns#" href="https://opencellid.org" property="cc:attributionName" rel="cc:attributionURL">
    </a> is licensed under a 
    <a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank">
        Creative Commons Attribution-ShareAlike 4.0 International License
    </a>
</div>

###Dataset
Download the dataset by using the download script in `bin/download_opencell_db.sh <API_KEY>`<br><br>
The API key can be generated for free by registering with an email address at https://opencellid.org/register.php

Columns:<br>
`['radio', 'mcc', 'net', 'area', 'cell', 'unit', 'lon', 'lat', 'range', 'samples', 'changeable', 'created', 'updated', 'averageSignal']`<br><br>
Detailed description:<br>
http://wiki.opencellid.org/wiki/Menu_map_view#database:~:text=https%3A//opencellid.org/-,Columns,-present%20in%20database

###Glossary
http://wiki.opencellid.org/wiki/Glossary

##Prepare Dataset
After downloading the `.csv` database file, the dataset has to be prepared for further use.
Use `python prepare_dataset.py --radio "LTE"` to filter the database for LTE (UMTS, GMS, CDMA) radio cells and drop unnecessary columns. The output file is saved in `data/cells_data/cell_towers_filtered.csv`.

##Generate Topology
`python create_topology.py --`

##Utils
`calc_distance(lon1, lat1, lon2, lat2)`:<br> Returns the distance in kilometers between two points.
<br><br>
`get_max_bounds(df)`:<br> Returns the maximal and minimal latitude and longitude `[max_lat, min_lat, max_lon, min_lon]` of a given dataframe.
<br><br>
`get_rectangle_bounds(coordinates, width, length)`:<br> Returns the the outer bounds of a given center coordinate and a given area (width & height).
<br><br>
`isfloat(num)`:<br> Returns if a given number has the data type `float`.