from supersetapiclient.client import SupersetClient

from .configs import (
    host,
    username,
    password,
    charts_path,
    dashboards_path
)

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
            charts = self.conn.charts.find,
            dashboards = self.conn.dashboards.find
        )
