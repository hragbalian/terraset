
import re
import uuid
import zipfile
import os

from .base import TerrasetBase
from .schemas import SupersetObject
from .configs import supported_superset_objects
from .exceptions import (
    FoundExisting,
)

from .logger import LogConfig

logger = LogConfig("initializer").logger


class TerrasetFetch(TerrasetBase):
    """ Fetches resource (e.g. chart, dashboard) settings files """

    @property
    def local_counts(self):
        return dict(
            charts=len(self.charts.local_list),
            dashboards=len(self.dashboards.local_list),
            datasets=len(self.datasets.local_list))

    def _overwrite_check(self, overwrite: bool, object_type: str):
        """ Logic to overwrite existing files or not """

        SupersetObject(superset_object=object_type)

        if not overwrite and \
            self.local_counts[object_type]>0:
            raise FoundExisting(self.local_counts[object_type], object_type)

        if self.local_counts[object_type]>0:
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

        for object_type in supported_superset_objects:

            logger.info(f"Fetching {object_type}")

            self._overwrite_check(overwrite, object_type)
            self._get(object_type, getattr(self, object_type).remote)

            logger.info(f"Successfully fetched {object_type}")


    def fetch_diff(self):
        """ Fetch charts and dashboards that are in remote but not local """

        for object_type in supported_superset_objects:

            logger.info(f"Fetching {object_type}")

            self._get(object_type, getattr(self, object_type).remote_missing_from_local)

            logger.info(f"Successfully fetched {object_type}")
