
import re
import uuid
import zipfile
import os

from .base import (
    TerrasetBase,
    TerrasetObjectFactory,
)


from .exceptions import (
    FoundExisting,
)

from .logger import LogConfig

logger = LogConfig("initializer").logger

class TerrasetInitialize(TerrasetBase):
    """ Initializes all of the files """

    def __init__(self):
        super().__init__()
        

    @property
    def local_charts_dashboards_counts(self):
        return dict(
            charts=len(self.charts.local_list),
            dashboards=len(self.dashboards.local_list))

    def _overwrite_check(self, overwrite: bool, object_type: str):
        """ Logic to overwrite existing files or not """

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

    def _get(self, object_type: str, object_list: list, overwrite: bool = False):
        """ Helper function to get specified charts

        object_list (list): list of Superset charts of type supersetapiclient.charts.Chart
        overwrite (bool): whether to overwrite existing files/folders

        """
        # if object_type is 'charts' validate that the entries in object_list are charts also

        for i in range(len(object_list)):

            tmp_name = str(uuid.uuid4())
            desired_name = re.sub('[^A-Za-z0-9]+', '_', getattr(object_list[i],self.title_attribute[object_type]))
            id = str(object_list[i].id)

            object_list[i].export(self.dir_map[object_type], tmp_name)

            with zipfile.ZipFile(f'{self.dir_map[object_type]}/{tmp_name}.zip', 'r') as zip_ref:
                zip_ref.extractall(f'{self.dir_map[object_type]}/{tmp_name}')

            os.rename(f'{self.dir_map[object_type]}/{tmp_name}', f'{self.dir_map[object_type]}/{desired_name}_{id}')
            os.remove(f'{self.dir_map[object_type]}/{tmp_name}.zip')


    def init_all(self, overwrite: bool = False):
        """ Fetch all charts and dashboards """
        try:
            logger.info("Initializing charts")

            self._overwrite_check(overwrite, "charts")
            self._get("charts",self.charts.remote, overwrite)

            logger.info("Successfully initialized charts")
        except Exception as e:
            logger.error(f"Could not initialize charts: {e}")

        try:
            logger.info("Initializing dashboards")

            self._overwrite_check(overwrite, "dashboards")
            self._get("dashboards", self.dashboards.remote, overwrite)

            logger.info("Successfully initialized dashboards")
        except Exception as e:
            logger.error(f"Could not initialize dashboards: {e}")

    def init_diff(self):
        """ Fetch charts and dashboards that are in remote but not local """
        try:
            logger.info("Initializing charts")

            self._get("charts",self.charts.remote_missing_from_local)

            logger.info("Successfully initialized charts")
        except Exception as e:
            logger.error(f"Could not initialize charts: {e}")

        try:
            logger.info("Initializing dashboards")

            self._get("dashboards",self.dashboards.remote_missing_from_local)

            logger.info("Successfully initialized dashboards")
        except Exception as e:
            logger.error(f"Could not initialize dashboards: {e}")
