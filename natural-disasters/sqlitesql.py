# -*- coding: UTF-8 -*-
from collections import namedtuple
from datetime import datetime

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

    def select_events(self):
        sql = """
        select c.title as category, e.eonetId, e.title as 'event_title',
        e.description, s.sourceId, s.url 'source_url', g.date, co.latitude,
        co.longitude, co.ordering
        FROM categories c
        JOIN eventcategories ec on ec.categoryId = c.id
        JOIN events e on e.id = ec.eventId
        JOIN eventsources es on es.eventId = e.id
        JOIN sources s on s.id = es.sourceId
        JOIN eventgeometries eg on eg.eventId = e.id
        JOIN geometries g on g.id = eg.geometryId
        JOIN coordinates co on co.geometryId = g.id
        order by c.title, e.id,co.ordering
        """
        return self.db.select(sql)

    # ----------------------------------------------------------------------
    def insert_events(self, events):
        for event in events:
            eventId = self.event(event)
            for category in event['categories']:
                self.categories(category)
                self.eventcategories(category['id'], eventId)

            for source in event['sources']:
                sourceId = self.sources(source)
                self.eventsources(sourceId, eventId)

            for geometry in event['geometries']:
                self.geometries(geometry, eventId)

    # ----------------------------------------------------------------------
    def eventgeometries(self, geometryId, eventId):
        sql = """
        INSERT INTO eventgeometries
        (eventId, geometryId)
        VALUES(?, ?)
        """
        self.db.change(sql, (eventId, geometryId))

    # ----------------------------------------------------------------------
    def geometry_id(self, date, eventId):
        sql = """
        SELECT id
        FROM geometries
        WHERE eventId=?
        AND date=?
        """
        result = self.db.select(sql, (eventId, date))
        if result:
            return result[0][0]

    # ----------------------------------------------------------------------
    def geometries(self, geometry, eventId):
        geodate = datetime.strptime(geometry['date'], "%Y-%m-%dT%H:%M:%SZ")
        Id = self.geometry_id(geodate, eventId)
        if not Id:
            sql = """
            INSERT INTO geometries
            (date, type, eventId)
            VALUES(?, ?, ?)
            """
            params = (geodate,
                      geometry['type'],
                      eventId
                      )

            self.db.change(sql, params)
            Id = self.geometry_id(geodate, eventId)
            self.eventgeometries(Id, eventId)

        order = 1
        if geometry['type'].lower() == "polygon":
            for coordinate in geometry['coordinates']:
                ## Order the Coordintaes
                self.coordinate(order, coordinate, Id)
                order += 1
        else:
            self.coordinates(order, geometry['coordinates'], Id)

    # ----------------------------------------------------------------------
    def coordinates(self, order, coordinate, Id):
        sql = """
            INSERT INTO coordinates
            (ordering, geometryId, latitude, longitude)
            VALUES(?, ?, ?, ?)
            """
        self.db.change(sql, (order, Id, coordinate[0], coordinate[1]))

    # ----------------------------------------------------------------------
    def eventsources(self, sourceId, eventId):
        sql = """
        INSERT INTO eventsources
        (eventId, sourceId)
        VALUES(?, ?)
        """
        self.db.change(sql, (eventId, sourceId))

    # ----------------------------------------------------------------------
    def source_id(self, Id):
        sql = """
        SELECT id
        FROM sources
        WHERE sourceId=?
        """
        result = self.db.select(sql, (Id,))
        if result:
            return result[0][0]

    # ----------------------------------------------------------------------
    def sources(self, source):
        Id = self.source_id(source['id'])
        if Id:
            return Id
        sql = """
        INSERT INTO sources
        (sourceId, url)
        VALUES(?, ?)
        """
        params = (source['id'],
                  source['url']
                  )

        self.db.change(sql, params)
        return self.source_id(source['id'])

    # ----------------------------------------------------------------------
    def eventcategories(self, categoryId, eventId):
        sql = """
        INSERT INTO eventcategories
        (eventId, categoryId)
        VALUES(?, ?)
        """
        self.db.change(sql, (eventId, categoryId))

    # ----------------------------------------------------------------------
    def categories(self, category):
        if self.category_id(category['id']):
            return
        sql = """
        INSERT INTO categories
        (id, title)
        VALUES(?, ?)
        """
        params = (category['id'],
                  category['title']
                  )

        self.db.change(sql, params)

    # ----------------------------------------------------------------------
    def category_id(self, Id):
        sql = """
        SELECT id
        FROM categories
        WHERE id=?
        """
        result = self.db.select(sql, (Id,))
        if result:
            return result[0][0]

    # ----------------------------------------------------------------------
    def event(self, event):
        self._insert_event(event)
        return self.event_id(event['id'])

    # ----------------------------------------------------------------------
    def _insert_event(self, event):
        sql = """
        INSERT INTO events
        (eonetId, title, description, link, closed)
        VALUES(?, ?, ?, ?, ?)
        """
        if "closed" in event:
            closed = datetime.strptime(event['closed'], "%Y-%m-%dT%H:%M:%SZ")
        else:
            closed = None
        params = (event['id'],
                  event['title'],
                  event['description'],
                  event['link'],
                  closed)
        self.db.change(sql, params)

    # ----------------------------------------------------------------------
    def event_id(self, eonetId):
        sql = """
        SELECT id
        FROM events
        WHERE eonetId=?
        """
        result = self.db.select(sql, (eonetId,))
        if result:
            return result[0][0]

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
        id integer PRIMARY KEY AUTOINCREMENT,
        longitude numeric,
        latitude numeric,
        ordering integer,
        geometryId integer NOT NULL
        )
        """
        self.db.change(sql)

    # ----------------------------------------------------------------------
    def relation_tables(self):
        sql = """
        CREATE TABLE IF NOT EXISTS eventcategories(
        id integer PRIMARY KEY AUTOINCREMENT,
        eventId integer NOT NULL,
        categoryId integer NOT NULL
        )
        """
        self.db.change(sql)

        sql = """
        CREATE TABLE IF NOT EXISTS eventsources(
        id integer PRIMARY KEY AUTOINCREMENT,
        eventId integer NOT NULL,
        sourceId integer NOT NULL
        )
        """
        self.db.change(sql)

        sql = """
        CREATE TABLE IF NOT EXISTS eventgeometries(
        id integer PRIMARY KEY AUTOINCREMENT,
        eventId integer NOT NULL,
        geometryId integer NOT NULL
        )
        """
        self.db.change(sql)

    # ----------------------------------------------------------------------
    def geometries_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS geometries(
        id integer PRIMARY KEY AUTOINCREMENT,
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
        id integer PRIMARY KEY AUTOINCREMENT,
        sourceId text NOT NULL,
        url text NOT NULL
        )
        """
        self.db.change(sql)

    # ----------------------------------------------------------------------
    def categories_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS categories(
        id integer PRIMARY KEY,
        title text DEFAULT ''
        ) WITHOUT ROWID
        """
        self.db.change(sql)

    # ----------------------------------------------------------------------
    def event_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS events(
        id integer PRIMARY KEY AUTOINCREMENT,
        eonetId text NOT NULL,
        title text NOT NULL,
        description text NOT NULL,
        link text NOT NULL,
        closed datetime
        )
        """
        self.db.change(sql)

