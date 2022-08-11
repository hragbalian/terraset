import os
import re

from .initialize import TerrasetInitialize

class Terraset(
    TerrasetInitialize):

    def refresh_from_remote(self):
        """ Refresh the chart and dashboard objects from remote """
        self._remote_charts = self.conn.charts.find()
        self._remote_dashboards = self.conn.dashboards.find()