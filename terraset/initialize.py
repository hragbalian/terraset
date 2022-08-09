
import os

from .base import TerrasetBase


from .exceptions import (
    FoundExistingCharts
)

from .logger import LogConfig

logger = LogConfig("initializer").logger

class TerrasetInitialize(TerrasetBase):

    def __init__(self, overwrite: bool = False):
        super().__init__()
        self.overwrite = overwrite
        self._local_charts = []
        self._local_dashboards = []

    @property
    def local_charts(self):
        self._check_charts = [x for x in os.listdir(self.charts_dir) if x!=".DS_Store"]
        return self._check_charts

    @property
    def local_dashboards(self):
        self._local_dashboards = [x for x in os.listdir(self.dashboards_dir) if x!=".DS_Store"]
        return self._local_dashboards

    @property
    def local_charts_dashboards(self):
        return dict(
            charts=len(self.local_charts),
            dashboards=len(self.local_dashboards))

    def pull_charts(self):

        if not self.overwrite and \
            self.local_charts_dashboards['charts']>0:
            raise FoundExistingCharts(self.local_charts_dashboards['charts'])

        charts = self.conn.charts.find()

        for i in range(len(charts)):
            name = charts[i].slice_name.replace(" ", "_")
            charts[i].export(self.charts_dir, name)



class Terraset:
    initializer = TerrasetInitialize

    def __init__(self):
        self._remote_charts = None
        self._remote_dashboards = None
