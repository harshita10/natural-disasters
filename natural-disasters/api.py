# -*- coding: UTF-8 -*-

import requests


############################################################################
class Eonet(object):

    # ----------------------------------------------------------------------
    def __init__(self):
        self.base = "http://eonet.sci.gsfc.nasa.gov/api/v2.1/"

    # ----------------------------------------------------------------------
    def events(self, days):
        url = "{}{}".format(self.base, "events")
        try:
            r = requests.get(url, params={'days': days})
        except requests.exceptions.HTTPError as e:
            msg = "{}. \n{} \nResponse: {}".format(e.message,
                                                   e.request,
                                                   e.response)
            print(msg)

        response = r.json()
        if isinstance(response, dict):
            return response['events']
