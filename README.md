# Magnet Database

Tools for creating and manipulating a database designed for Magnet simulations.
Data may be partly retreived from **Lncmi control and monitoringwebsite**.
See `python_magnetrun` for more details

## Structure

Viewing the database: `sqlitebrowser`

Note that you shall not perform any operations while viewing the database with `sqlitebrowser`

To generate a diagram:

```
java -jar schemaspy-6.1.0.jar -debug -t sqlite -o tutut -sso -cat magnets -s magnets -db magnets.db
```

## Python

Running the app to create the database

```
python3 -m python_magnetdb.app --createdb
``` 

To populate the database with an exemple msite

```
python3 -m python_magnetdb.app --createsite
```

To see more

```
python3 -m python_magnetdb.app --help
```

## API

Running the FastAPI Application:

```
uvicorn python_magnetdb.main:app [--host 0.0.0.0] --reload
``` 

use `--host` option to make the server available for other machines in the same vlan as the host running the container.

To view the API interface

```
firefox http://localhost:8000/docs
```

## Requirements

* sqlmodel
* fastapi
* uvicorn
* sqlitebrowser

```
python -m pip install sqlmodel
python -m pip install fastapi "uvicorn[standard]"
export PATH=$PATH:$HOME/.local/bin
```

## References

(sqlmodel)[https://sqlmodel.tiangolo.com/tutorial]
(fastapi)[https://fastapi.tiangolo.com/]
(panel)[https://panel.holoviz.org/getting_started/index.html]

## TODO

* add machine selection htm with:
** create file for jobmanager if any

* bokeh add several plots on the same panel (see panel_bmap)
* in panel how to show/hide param 
* in bokeh panel how to create a button with a href to localhost
* mrecords: add statistics, fits, smoothers, outliers...

* In simulations:
** create forms for cfg/json 
** fix update cfg/json files
** how to create/setup cfg/json for workflows like fixcurrent.py (see github/hifimagnet.cases/cfpdes)

* In parts/magnets/sites:
** more info in desc for magnets index.html (see routes/magnets.py),
** more info in desc for  site index.html (see routes/sites.py),
** add view/create CAD geoms (connection with pythonocc-core)

* In mrecords:
** list add headers for table
** add duration, plateaux, max B in desc field
** show.html: add button for HeatBalance, Flow + fit
** add selections
*** add view dataset for selections
** panel mrecord:
** add filter for smooth data
** add outliers like in panel tutorials