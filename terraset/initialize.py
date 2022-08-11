
import re
import uuid
import zipfile
import os

from .base import (
    TerrasetCharts,
    TerrasetDashboards
)


from .exceptions import (
    FoundExistingCharts,
    FoundExistingDashboards
)

from .logger import LogConfig

logger = LogConfig("initializer").logger

class TerrasetInitialize(TerrasetCharts, TerrasetDashboards):
    """ Initializes all of the chart and dashboard files """

    def __init__(self):
        super().__init__()

    @property
    def local_charts_dashboards_counts(self):
        return dict(
            charts=len(self.local_charts_list),
            dashboards=len(self.local_dashboards_list))

    def _get_charts(self, charts: list, overwrite: bool = False):
        """ Helper function to get specified charts

        charts (list): list of Superset charts of type supersetapiclient.charts.Chart
        overwrite (bool): whether to overwrite existing files/folders

        """

        if not overwrite and \
            self.local_charts_dashboards_counts['charts']>0:
            raise FoundExistingCharts(self.local_charts_dashboards_counts['charts'])

        if self.local_charts_dashboards_counts['charts']>0:
            logger.info("Overwriting existing charts with remote")

            ok = input("Are you sure you want to overwrite local charts? y/n")

            if ok in ['y','yes']:
                self.reset_directory(self.charts_dir)
            else:
                logger.info("Aborted overwrite")
                return

        for i in range(len(self.remote_charts)):

            tmp_name = str(uuid.uuid4())
            desired_name = re.sub('[^A-Za-z0-9]+', '_', self.remote_charts[i].slice_name)
            chart_id = str(self.remote_charts[i].id)

            self.remote_charts[i].export(self.charts_dir, tmp_name)

            with zipfile.ZipFile(f'{self.charts_dir}/{tmp_name}.zip', 'r') as zip_ref:
                zip_ref.extractall(f'{self.charts_dir}/{tmp_name}')

            os.rename(f'{self.charts_dir}/{tmp_name}', f'{self.charts_dir}/{desired_name}_{chart_id}')
            os.remove(f'{self.charts_dir}/{tmp_name}.zip')

    def _get_dashboards(self, overwrite: bool = False):

        if not overwrite and \
            self.local_charts_dashboards_counts['dashboards']>0:
            raise FoundExistingDashboards(self.local_charts_dashboards_counts['dashboards'])

        if self.local_charts_dashboards_counts['dashboards']>0:
            logger.info("Overwriting existing dashboards with remote")

            ok = input("Are you sure you want to overwrite local dashboards? y/n")

            if ok in ['y','yes']:
                self.reset_directory(self.dashboards_dir)
            else:
                logger.info("Aborted overwrite")
                return

        for i in range(len(self.remote_dashboards)):

            tmp_name = str(uuid.uuid4())
            desired_name = re.sub('[^A-Za-z0-9]+', '_', self.remote_dashboards[i].dashboard_title)
            dashboard_id = str(self.remote_dashboards[i].id)

            self.remote_dashboards[i].export(self.dashboards_dir, tmp_name)

            with zipfile.ZipFile(f'{self.dashboards_dir}/{tmp_name}.zip', 'r') as zip_ref:
                zip_ref.extractall(f'{self.dashboards_dir}/{tmp_name}')

            os.rename(f'{self.dashboards_dir}/{tmp_name}', f'{self.dashboards_dir}/{desired_name}_{dashboard_id}')
            os.remove(f'{self.dashboards_dir}/{tmp_name}.zip')


    def initialize_all(self, overwrite: bool = False):
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

    def initialize_diff(self):
        """ Fetch charts and dashboards that are in remote but not local """
        pass
