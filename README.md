# natural-disasters
Reports on natural disaster data extracted from the EONET API from NASA


## Install

`pip install git+git://github.com/keithlee-co-uk/natural-disasters&&pip install -r natural-disaters/requirements.txt`



## Usage

python natural-disasters/natural-disasters/natural-disasters.py [options]

### Options

[-c | --config] <path to config file>


[-f | --file ] <name of report file>  -  An Excel spreadsheet file (.xlsx) with the name provided, which will be placed into the home directory of the initiating user. (the default name is Eonet.xlsx)


[--db | -d ] <name of the database file>  -  The SQLite database file name which will be placed into the home directory of the initiating user. (the default uses the memory to store the database)

---

## Examples

`python natural-disasters/natural-disasters/natural-disasters.py --config .ngconfig.cfg`

* use the file $HOME/.ngconfig.cfg as the configuration file containing the email address
* place the database in memory
* place the file Eonet.xlsx in the user's home

--

`python natural-disasters/natural-disasters/natural-disasters.py --email user@localhost --file reportFile --db Eonet.db`

* send an email to address 'user@localhost'
* place the database file Eonet.db in the user's home
* place the file reportFile.xlsx in the user's home

---

## Critique

### The code

* natural-disasters.filter_events - In th spirit of 'clean code' and testing, this could be broken down more.


### My approach

* An attempt to keep each concern seperate was made to enable reuse and easier replacement.


## Potential extentions depending on need

* alternative database usage

* An configuration option for producing .csv files, rather than the requested Excel file to make possible easy machine parsing (eg grep), if required.

* An configuration option to specify the smtp server

* Additional flexabilty for the placement of the report and database files

* Allow more choice of filters on events
