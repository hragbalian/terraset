import os

from .initialize import TerrasetInitialize

class Terraset(
    TerrasetInitialize):

    def __init__(self):
        super().__init__()
        self._remote_charts = None
        self._remote_dashboards = None
        self._local_charts_list = []
        self._local_dashboards_list = []

    @property
    def local_charts_list(self):
        self._local_charts_list = [x for x in os.listdir(self.charts_dir) if x!=".DS_Store"]
        return self._local_charts_list

    @property
    def local_dashboards_list(self):
        self._local_dashboards_list = [x for x in os.listdir(self.dashboards_dir) if x!=".DS_Store"]
        return self._local_dashboards_list

    @property
    def local_charts_dashboards_counts(self):
        return dict(
            charts=len(self.local_charts_list),
            dashboards=len(self.local_dashboards_list))

    @property
    def remote_charts(self):
        if not self._remote_charts:
            self._remote_charts = self.conn.charts.find()
        return self._remote_charts

    @remote_charts.setter
    def remote_charts(self,value):
        self._remote_charts = value

    @property
    def remote_dashboards(self):
        if not self._remote_dashboards:
            self._remote_dashboards = self.conn.dashboards.find()
        return self._remote_dashboards

    @remote_dashboards.setter
    def remote_dashboards(self,value):
        self._remote_dashboards = value
