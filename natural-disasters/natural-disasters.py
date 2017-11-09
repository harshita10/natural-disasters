#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import namedtuple

from dbconnection.connectionfactory import ConnectionFactory
from defaultargs.defaultargs import ArgumentParser, defaultargs


# ----------------------------------------------------------------------
def main():

    email = arguments(
        ArgumentParser(usage="%%prog [options]")).parse_args().email
    print(email)
    db = sqlite_setup()


# ----------------------------------------------------------------------
def sqlite_setup():
    db = sqlite_connection()
    create_tables()
    return db


# ----------------------------------------------------------------------
def create_tables(db):
    pass

# ----------------------------------------------------------------------
def sqlite_connection():
    Parameters = namedtuple('Parameters', "database")
    parameters = Parameters(database=":memory:")

    return ConnectionFactory(
        engine="sqlite",
        connectionParameters=parameters)

# ----------------------------------------------------------------------
@defaultargs
def arguments(parser):
    parser.add_argument(
      "--email", "-e",
      help="destination smtp email address"
  )
    return parser

# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()