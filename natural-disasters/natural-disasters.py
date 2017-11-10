#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datetime import date, timedelta, datetime


from defaultargs.defaultargs import ArgumentParser, defaultargs

from sqlitesql import Sql
from api import Eonet


# ----------------------------------------------------------------------
def main():

    email = arguments(
        ArgumentParser(usage="%%prog [options]")).parse_args().email

    db = Sql()
    db.create_tables()

    rest = Eonet()
    events = rest.events(days())
    filteredEvents = filter_events(events)
    db.insert_events(filteredEvents)


# ----------------------------------------------------------------------
def filter_events(events):
    filteredEvents = []
    firstThisMonth = first_of_month()
    firstLastMonth = first_of_last_month()


    for event in events:
        if in_category(event['categories']):
            for geometry in event['geometries']:
                geodate = datetime.strptime(
                    geometry['date'], "%Y-%m-%dT%H:%M:%SZ").date()

                if geodate < firstThisMonth and geodate >= firstLastMonth:
                    filteredEvents.append(event)
                    continue
    return filteredEvents


# ----------------------------------------------------------------------
def in_category(eventCategories):
    categories = ["wildfires", "severe storms", "landslides"]
    for category in eventCategories:
        if category['title'].lower() in categories:
            return True
    else:
        return False


# ----------------------------------------------------------------------
def first_of_month():
    today = date.today()
    return (date(today.year, today.month, 1))


# ----------------------------------------------------------------------
def first_of_last_month():
    lastMonth = (date.today() - timedelta(days=28))
    return date(lastMonth.year, lastMonth.month, 1)

# ----------------------------------------------------------------------
def days():
    """
    returns the number of days between today and the 1st of last month
    """

    days = (date.today() - first_of_last_month()).days
    return days


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