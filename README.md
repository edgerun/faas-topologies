# faas-topologies
Framework to generate geo-distributed topologies by using the OpencelliD dataset as baseline.

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
The API key can be generated for free by register with an email address at https://opencellid.org/register.php

Following columns are available in the dataset:<br>
`['radio', 'mcc', 'net', 'area', 'cell', 'unit', 'lon', 'lat', 'range', 'samples', 'changeable', 'created', 'updated', 'averageSignal']`<br><br>
Detailed description:<br>
http://wiki.opencellid.org/wiki/Menu_map_view#database:~:text=https%3A//opencellid.org/-,Columns,-present%20in%20database

###Glossary
http://wiki.opencellid.org/wiki/Glossary

##Prepare Dataset
After downloading the `.csv` database file, the dataset has to be prepared for further use.
Use `python prepare_dataset.py --radio "LTE"` to filter the database for LTE (UMTS, GMS, CDMA) radio cells and drop unnecessary columns. The output file is saved in `data/cells_data/cell_towers_filtered.csv`.

##Filter Topology
Use `python filter_dataset.py --name vienna --city Vienna --width 2 --height 2` to create a list of cells `[(radio, cell, lon, lat), ...]` saved as`.csv` file regarding the committed width `--width`, height `--height` in kilometers, coordinate `--lat`, `--lon` or city `--city`.

##Create Cloudlet Membership
Use `python create_cloudlet_membership.py --name newyork_2x2_1x1 --path topologies/newyork_2x2.csv --width 1 --height 1` to associate every cell with a cloudlet number and save it as `.csv`.
The file is going to be saved in `output/`. Also, an image with the cloudlet division is going to be saved there.