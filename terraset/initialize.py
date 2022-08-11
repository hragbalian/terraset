
import re

from .base import TerrasetBase


from .exceptions import (
    FoundExistingCharts
)

from .logger import LogConfig

logger = LogConfig("initializer").logger

class TerrasetInitialize(TerrasetBase):
    """ Initializes all of the chart and dashboard files """

    def __init__(self):
        super().__init__()

    def _get_charts(self, overwrite: bool = False):

        if not overwrite and \
            self.local_charts_dashboards_counts['charts']>0:
            raise FoundExistingCharts(self.local_charts_dashboards_counts['charts'])

        if self.local_charts_dashboards_counts['charts']>0:
            logger.info("Overwriting existing charts with remote")

            ok = input("Are you sure you want to overwrite charts? y/n")

            if ok in ['y','yes']:
                self.reset_directory(self.charts_dir)
            else:
                logger.info("Aborted overwrite")
                return

        for i in range(len(self.remote_charts)):
            name = re.sub('[^A-Za-z0-9]+', '_', self.remote_charts[i].slice_name)
            self.remote_charts[i].export(self.charts_dir, name)

    def _get_dashboards(self, overwrite: bool = False):

        if not overwrite and \
            self.local_charts_dashboards_counts['dashboards']>0:
            raise FoundExistingCharts(self.local_charts_dashboards_counts['dashboards'])

        if self.local_charts_dashboards_counts['dashboards']>0:
            logger.info("Overwriting existing dashboards with remote")

            ok = input("Are you sure you want to overwrite dashboards? y/n")

            if ok in ['y','yes']:
                self.reset_directory(self.dashboards_dir)
            else:
                logger.info("Aborted overwrite")
                return

        for i in range(len(self.remote_dashboards)):
            name = re.sub('[^A-Za-z0-9]+', '_', self.remote_dashboards[i].dashboard_title)
            self.remote_dashboards[i].export(self.dashboards_dir, name)

    def initialize_local(self, overwrite: bool = False):
        """ Fetch all charts and dashboards """
        try:
            logger.info("Initializing charts")
            self._get_charts(overwrite)
            logger.info("Successfully initialized charts")
        except Exception as e:
            logger.error(f"Could not initialize charts: {e}")

        try:
            logger.info("Initializing dashboards")
            self._get_dashboards(overwrite)
            logger.info("Successfully initialized dashboards")
        except Exception as e:
            logger.error(f"Could not initialize dashboards: {e}")
