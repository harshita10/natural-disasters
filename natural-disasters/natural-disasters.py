#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from defaultargs.defaultargs import ArgumentParser, defaultargs

from sqlitesql import Sql


# ----------------------------------------------------------------------
def main():

    email = arguments(
        ArgumentParser(usage="%%prog [options]")).parse_args().email

    db = Sql()
    db.create_tables()

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