# -*- coding: UTF-8 -*-
from collections import namedtuple

from dbconnection.connectionfactory import ConnectionFactory


############################################################################
class Sql(object):

    # ----------------------------------------------------------------------
    def __init__(self, dbfile=":memory:"):
        Parameters = namedtuple('Parameters', "database")
        parameters = Parameters(database=dbfile)

        self.db = ConnectionFactory(
            engine="sqlite",
            connectionParameters=parameters)


    # ----------------------------------------------------------------------
    def create_tables(self):
        self.event_table()

        self.categories_table()

        self.sources_table()

        self.geometries_table()
        self.coordinates_table()

        self.relation_tables()


    # ----------------------------------------------------------------------
    def coordinates_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS coordinates(
        longitude numeric,
        latitude numeric,
        eventId integer NOT NULL
        )
        """
        self.db.change(sql)


    # ----------------------------------------------------------------------
    def relation_tables(self):
        sql = """
        CREATE TABLE IF NOT EXISTS eventcategories(
        eventId integer NOT NULL,
        categoryId integer NOT NULL
        )
        """
        self.db.change(sql)

        sql = """
        CREATE TABLE IF NOT EXISTS eventsources(
        eventId integer NOT NULL,
        sourceId integer NOT NULL
        )
        """
        self.db.change(sql)

    # ----------------------------------------------------------------------
    def geometries_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS geometries(
        date datetime NOT NULL,
        type text NOT NULL,
        eventId integer
        )
        """
        self.db.change(sql)


    # ----------------------------------------------------------------------
    def sources_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS sources(
        sourceId text NOT NULL,
        url text NOT NULL
        )
        """
        self.db.change(sql)

    # ----------------------------------------------------------------------
    def categories_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS categories(
        Id integer PRIMARY KEY,
        title text DEFAULT ''
        ) WITHOUT ROWID
        """
        self.db.change(sql)


    # ----------------------------------------------------------------------
    def event_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS categories(
        eonetId text NOT NULL,
        title text NOT NULL,
        description text NOT NULL,
        link text NOT NULL
        )
        """
        self.db.change(sql)

