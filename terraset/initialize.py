
import re
import uuid
import zipfile
import os

from .base import (
    TerrasetCharts,
    TerrasetDashboards
)


from .exceptions import (
    FoundExisting,
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

    def _overwrite_check(self, overwrite: bool, object_type: str):
        """ Logic to overwrite existing files or not """

        if not overwrite and \
            self.local_charts_dashboards_counts[object_type]>0:
            raise FoundExisting(self.local_charts_dashboards_counts[object_type], object_type)

        curr_dir = self.charts_dir if object_type == "charts" else self.dashboards_dir

        if self.local_charts_dashboards_counts[object_type]>0:
            logger.info("Overwriting existing charts with remote")

            ok = input(f"Are you sure you want to overwrite local {object_type}? y/n")

            if ok in ['y','yes']:
                self.reset_directory(curr_dir)
            else:
                logger.info("Aborted overwrite")
                return

    def _get_charts(self, charts: list, overwrite: bool = False):
        """ Helper function to get specified charts

        charts (list): list of Superset charts of type supersetapiclient.charts.Chart
        overwrite (bool): whether to overwrite existing files/folders

        """

        for i in range(len(charts)):

            tmp_name = str(uuid.uuid4())
            desired_name = re.sub('[^A-Za-z0-9]+', '_', charts[i].slice_name)
            chart_id = str(charts[i].id)

            charts[i].export(self.charts_dir, tmp_name)

            with zipfile.ZipFile(f'{self.charts_dir}/{tmp_name}.zip', 'r') as zip_ref:
                zip_ref.extractall(f'{self.charts_dir}/{tmp_name}')

            os.rename(f'{self.charts_dir}/{tmp_name}', f'{self.charts_dir}/{desired_name}_{chart_id}')
            os.remove(f'{self.charts_dir}/{tmp_name}.zip')

    def _get_dashboards(self, dashboards: list, overwrite: bool = False):
        """ Helper function to get specified dashboards

        dashboards (list): list of Superset charts of type supersetapiclient.dashboard.Dashboard
        overwrite (bool): whether to overwrite existing files/folders

        """
        for i in range(len(dashboards)):

            tmp_name = str(uuid.uuid4())
            desired_name = re.sub('[^A-Za-z0-9]+', '_', dashboards[i].dashboard_title)
            dashboard_id = str(dashboards[i].id)

            dashboards[i].export(self.dashboards_dir, tmp_name)

            with zipfile.ZipFile(f'{self.dashboards_dir}/{tmp_name}.zip', 'r') as zip_ref:
                zip_ref.extractall(f'{self.dashboards_dir}/{tmp_name}')

            os.rename(f'{self.dashboards_dir}/{tmp_name}', f'{self.dashboards_dir}/{desired_name}_{dashboard_id}')
            os.remove(f'{self.dashboards_dir}/{tmp_name}.zip')


    def init_all(self, overwrite: bool = False):
        """ Fetch all charts and dashboards """
        try:
            logger.info("Initializing charts")

            self._overwrite_check(overwrite, "charts")
            self._get_charts(self.remote_charts, overwrite)

            logger.info("Successfully initialized charts")
        except Exception as e:
            logger.error(f"Could not initialize charts: {e}")

        try:
            logger.info("Initializing dashboards")

            self._overwrite_check(overwrite, "dashboards")
            self._get_dashboards(self.remote_dashboards, overwrite)

            logger.info("Successfully initialized dashboards")
        except Exception as e:
            logger.error(f"Could not initialize dashboards: {e}")

    def init_diff(self):
        """ Fetch charts and dashboards that are in remote but not local """
        try:
            logger.info("Initializing charts")

            self._get_charts(self.remote_charts_missing_from_local)

            logger.info("Successfully initialized charts")
        except Exception as e:
            logger.error(f"Could not initialize charts: {e}")

        try:
            logger.info("Initializing dashboards")

            self._get_dashboards(self.remote_dashboards_missing_from_local)

            logger.info("Successfully initialized dashboards")
        except Exception as e:
            logger.error(f"Could not initialize dashboards: {e}")
