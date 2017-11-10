# natural-disasters
Reports on natural disaster data extracted from the EONET API from NASA


## Requirements

### Somethings I created earlier

These demostrate my use of packaging for pip.
+ Sadly I seem, so far, unable to get this format/syntax to work in the
   requirements file and I've just spent an hour trying also within setup.py.
So these will need to be installed to your [virtual] environment by hand.

#### For the database connection
`pip install git+git://github.com/keithlee-co-uk/dbconnection`


#### For capturing the email address
+ Not really needed because I'm not actually using the defaults this provides
  but it shows off the use of decorators.

`pip install git+git://github.com/keithlee-co-uk/defaultargs`
