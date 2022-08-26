
import re
import uuid
import zipfile
import os

from .base import TerrasetBase
from .schemas import SupersetObject
from .exceptions import (
    FoundExisting,
)

from .logger import LogConfig

logger = LogConfig("initializer").logger


class TerrasetFetch(TerrasetBase):
    """ Fetches resource (e.g. chart, dashboard) settings files """

    @property
    def local_charts_dashboards_counts(self):
        return dict(
            charts=len(self.charts.local_list),
            dashboards=len(self.dashboards.local_list))

    def _overwrite_check(self, overwrite: bool, object_type: str):
        """ Logic to overwrite existing files or not """

        SupersetObject(superset_object=object_type)

        if not overwrite and \
            self.local_charts_dashboards_counts[object_type]>0:
            raise FoundExisting(self.local_charts_dashboards_counts[object_type], object_type)

        if self.local_charts_dashboards_counts[object_type]>0:
            logger.info("Overwriting existing charts with remote")

            ok = input(f"Are you sure you want to overwrite local {object_type}? y/n")

            if ok in ['y','yes']:
                self.reset_directory(self.dir_map[object_type])
            else:
                logger.info("Aborted overwrite")
                return

    def _get(self, object_type: str, object_list: list):
        """ Helper function to get specified charts

        object_list (list): list of Superset charts of type supersetapiclient.charts.Chart or
            supersetapiclient.dasbhoards.Dashboard

        """

        SupersetObject(superset_object=object_type)

        for i in range(len(object_list)):

            self.process_export(
                object_list[i],
                self.title_attribute[object_type],
                self.dir_map[object_type]
                )


    def fetch_all(self, overwrite: bool = False):
        """ Fetch all charts and dashboards """
        try:
            logger.info("Fetching charts")

            self._overwrite_check(overwrite, "charts")
            self._get("charts",self.charts.remote)

            logger.info("Successfully fetched charts")
        except Exception as e:
            logger.error(f"Could not fetched charts: {e}")

        try:
            logger.info("Fetching dashboards")

            self._overwrite_check(overwrite, "dashboards")
            self._get("dashboards", self.dashboards.remote)

            logger.info("Successfully fetched dashboards")
        except Exception as e:
            logger.error(f"Could not fetched dashboards: {e}")

    def fetch_diff(self):
        """ Fetch charts and dashboards that are in remote but not local """
        try:
            logger.info("Fetching charts")

            self._get("charts",self.charts.remote_missing_from_local)

            logger.info("Successfully fetched charts")
        except Exception as e:
            logger.error(f"Could not fetched charts: {e}")

        try:
            logger.info("Fetching dashboards")

            self._get("dashboards",self.dashboards.remote_missing_from_local)

            logger.info("Successfully fetched dashboards")
        except Exception as e:
            logger.error(f"Could not fetched dashboards: {e}")
