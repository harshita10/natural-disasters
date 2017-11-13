#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datetime import date, timedelta, datetime
from os import path
import configparser


from defaultargs.defaultargs import ArgumentParser, defaultargs

from sqlitesql import Sql
from api import Eonet
from eonetfile import EonetFile
from eonetemail import Email


# ----------------------------------------------------------------------
def main():

    args = arguments(ArgumentParser(usage="%%prog [options]")).parse_args()
    emailAddress = address(args)
    reportFile = report_file(args)

    if args.dbfile:
        db = Sql(path.join(path.expanduser("~"), args.dbfile))
    else:
        db = Sql()
    db.create_tables()

    rest = Eonet()
    events = rest.events(days())
    filteredEvents = filter_events(events)
    db.insert_events(filteredEvents)
    dbevents = db.select_events()

    f = EonetFile(dbevents)
    thisFile = path.join(path.expanduser("~"), reportFile)
    f.write_file(thisFile)

    e = Email(thisFile, emailAddress)
    e.send()


# ----------------------------------------------------------------------
def report_file(args):
    if args.file:
        if args.file.endswith(".xlsx"):
            fileName = args.file
        else:
            fileName = "{}.xlsx".format(args.file)
    else:
        fileName = "Eonet.xlsx"
    return fileName


# ----------------------------------------------------------------------
def address(args):
    home = path.expanduser("~")
    if args.config and path.isfile(path.join(home, args.config)):
            config = configparser.ConfigParser()
            config.read(path.join(home, args.config))
            emailAddress = config['DEFAULT']['email']
    else:
        emailAddress = args.email

    return emailAddress


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
    parser.add_argument(
        "--dbfile", "-d",
        help="database file (sqlite)"
    )
    parser.add_argument(
        "--file", "-f",
        help="The .xlsx spreadsheet filename"
    )
    return parser


# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()
