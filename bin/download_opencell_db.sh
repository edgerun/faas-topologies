#!/usr/bin/env bash
API_KEY=${1}
if [ ${1} ];
  then
    mkdir data;
    mkdir data/cells_data;
    wget "https://opencellid.org/ocid/downloads?token=$API_KEY%20&type=full&file=cell_towers.csv.gz" -O "./data/cells_data/cell_towers.csv.gz";
    if gzip -t ./data/cells_data/cell_towers.csv.gz;
    then
      gzip -d ./data/cells_data/cell_towers.csv.gz;
    else
      echo 'file is corrupt';
    fi
  else
    echo "Please set API_KEY parameter from OpencelliD";
fi