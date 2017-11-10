#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import namedtuple

from dbconnection.connectionfactory import ConnectionFactory
from defaultargs.defaultargs import ArgumentParser, defaultargs


# ----------------------------------------------------------------------
def main():

    email = arguments(
        ArgumentParser(usage="%%prog [options]")).parse_args().email

    db = sqlite_setup()


# ----------------------------------------------------------------------
def sqlite_setup():
    db = sqlite_connection()
    create_tables(db)
    return db


# ----------------------------------------------------------------------
def create_tables(db):
    event_table(db)

    categories_table(db)

    sources_table(db)

    geometries_table(db)
    coordinates_table(db)

    relation_tables(db)


# ----------------------------------------------------------------------
def coordinates_table(db):
    sql = """
    CREATE TABLE IF NOT EXISTS coordinates(
    longitude numeric,
    latitude numeric,
    eventId integer NOT NULL
    )
    """
    db.change(sql)


# ----------------------------------------------------------------------
def relation_tables(db):
    sql = """
    CREATE TABLE IF NOT EXISTS eventcategories(
    eventId integer NOT NULL,
    categoryId integer NOT NULL
    )
    """
    db.change(sql)

    sql = """
    CREATE TABLE IF NOT EXISTS eventsources(
    eventId integer NOT NULL,
    sourceId integer NOT NULL
    )
    """
    db.change(sql)

# ----------------------------------------------------------------------
def geometries_table(db):
    sql = """
    CREATE TABLE IF NOT EXISTS geometries(
    date datetime NOT NULL,
    type text NOT NULL,
    eventId integer
    )
    """
    db.change(sql)


# ----------------------------------------------------------------------
def sources_table(db):
    sql = """
    CREATE TABLE IF NOT EXISTS sources(
    sourceId text NOT NULL,
    url text NOT NULL
    )
    """
    db.change(sql)

# ----------------------------------------------------------------------
def categories_table(db):
    sql = """
    CREATE TABLE IF NOT EXISTS categories(
    Id integer PRIMARY KEY,
    title text DEFAULT ''
    ) WITHOUT ROWID
    """
    db.change(sql)


# ----------------------------------------------------------------------
def event_table(db):
    sql = """
    CREATE TABLE IF NOT EXISTS categories(
    eonetId text NOT NULL,
    title text NOT NULL,
    description text NOT NULL,
    link text NOT NULL
    )
    """
    db.change(sql)


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