# -*- coding: UTF-8 -*-

import xlsxwriter

############################################################################
class EonetFile(object):

    # ----------------------------------------------------------------------
    def __init__(self, events):
        self.eventList = []
        #self.headings = events[0].keys()
        self.headings = ("category", "eonetId", "event title", "description",
                         "sourceId", "source url", "date", "latitude",
                         "longitude", "coordinate ordering")

        self.eventList.append(self.headings)

        for line in events:
            self.eventList.append(line)

    # ----------------------------------------------------------------------
    def write_file(self, filepath):

        self.workbook = xlsxwriter.Workbook(filepath)

        # Create the worksheet
        self.worksheet = self.workbook.add_worksheet()
        row = 0
        for line in self.eventList:
            self.worksheet.write_row(row, 0, line)
            row += 1

        self.workbook.close()
