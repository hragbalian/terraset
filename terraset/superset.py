
from supersetapiclient.client import SupersetClient

from .configs import (
    host,
    username,
    password,
    resources_path,
    # charts_path,
    # dashboards_path,
    supported_superset_objects
)
from .schemas import SupersetObject

class SupersetConnectionMgmnt:
    """ Superset connection and static methods """

    def __init__(self):
        self.conn = SupersetClient(
            host=host,
            username=username,
            password=password,
            verify=True
        )

        self.dir_map = dict(
            charts=f"{resources_path}/charts",
            dashboards=f"{resources_path}/dashboards",
            databases=f"{resources_path}/databases",
            datasets=f"{resources_path}/datasets"
        )

        self.title_attribute = dict(
            charts = "slice_name",
            dashboards = "dashboard_title",
            datasets = "table_name",
            databases = "database_name"
        )

        self.find_methods = dict()

        for superset_object in supported_superset_objects:
            self.find_methods[superset_object] = getattr(self, f"find_{superset_object}")


    def find_all(self, object_type: str):

        SupersetObject(superset_object=object_type)

        paginate = True
        page = 0
        resources = list()

        while paginate:

            found_on_page = getattr(getattr(self, "conn"), object_type).find(page=page)

            if found_on_page:
                resources.extend(found_on_page)
                page += 1

            if len(found_on_page) < 100:
                paginate = False

        return resources

    def find_charts(self):
        return self.find_all("charts")

    def find_dashboards(self):
        return self.find_all("dashboards")

    def find_datasets(self):
        return self.find_all("datasets")

    def find_databases(self):
        return self.find_all("databases")
