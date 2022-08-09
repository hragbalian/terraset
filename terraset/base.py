
import yaml
import os
import glob

from supersetapiclient.client import SupersetClient

from .logger import LogConfig

from .configs import (
    host,
    username,
    password,
    charts_path,
    dashboards_path,
    chart_info
)

logger = LogConfig("Terraset").logger


class TerrasetBase:

    def __init__(self):
        self.conn = SupersetClient(
            host=host,
            username=username,
            password=password,
            verify=True
        )
        self.charts_dir = charts_path
        self.dashboards_dir = dashboards_path

    @staticmethod
    def find_chart_yaml_filename(path):
        return [x for x in os.listdir(path) if x!=".DS_Store"][0]

    @staticmethod
    def joiner(*args):
        return "".join(args)

    @staticmethod
    def read_yaml(yml_path):
        with open(yml_path, 'r') as stream:
            try:
                parsed_yaml=yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return parsed_yaml









class SupersetCIClient:
    base_dir = os.getcwd()
    charts_dir = "/charts"
    dashboards_dir = "/dashboards"

    def __init__(self):
        self.superset_conn = SupersetClient(
            host=host,
            username=username,
            password=password,
            verify=True
        )

    @property
    def list_of_chart_exports(self):
        return ["/"+x+self.charts_dir for x in os.listdir(self.base_dir+self.charts_dir) if x!=".DS_Store"]

    @property
    def list_of_dashboard_exports(self):
        return ["/"+x+self.dashboards_dir for x in os.listdir(self.base_dir+self.dashboards_dir) if x!=".DS_Store"]

    def sync_charts(self):
        """ Sync changes in local files to remote """
        for exported_chart in self.list_of_chart_exports:

            try:

                curr_path = joiner(self.base_dir,self.charts_dir,exported_chart) # Iterate over list_of_chart_exports

                chart_yaml_filename = find_chart_yaml_filename(curr_path)

                # Read yaml file from the repo
                parsed_yaml = read_yaml(joiner(curr_path,"/",chart_yaml_filename))

                # Grab chart id from the yaml filename
                chart_id = int(chart_yaml_filename.split(".")[0].split("_")[-1])

                # Make API call to get latest remote chart info
                chart = self.superset_conn.charts.get(chart_id)

                for info in chart_info:

                    if info in parsed_yaml.keys():

                        setattr(chart, info, parsed_yaml[info])

                        logger.info(f"{info} updated to {parsed_yaml[info]}")

                # Grab dataset_id and datasource_type from the params
                datasource_id, datasource_type = chart.params['datasource'].split("__")

                setattr(chart, "datasource_id", int(datasource_id))
                setattr(chart, "datasource_type", datasource_type)

                logger.info("Persisting changes in remote")

                chart.save()

                # Check to see if this chart is used by any dashboard, and if so,
                # update the file
                # chart_in_dashboards = [x for x in glob.iglob('dashboards/'+'**', recursive=True) if "Age_33" in x]

            except Exception as e:

                logger.error(str(e))
#
#
# if __name__=="__main__":
#
#     dd = SupersetCIClient()
#     dd.list_of_chart_exports
#     dd.sync_charts()
