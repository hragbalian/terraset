from supersetapiclient.client import SupersetClient

from .configs import (
    host,
    username,
    password,
    charts_path,
    dashboards_path
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
            charts=charts_path,
            dashboards=dashboards_path
        )

        self.title_attribute = dict(
            charts = "slice_name",
            dashboards = "dashboard_title"
        )

        self.find_methods = dict(
            charts = self.find_charts,
            dashboards = self.find_dashboards
        )


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
