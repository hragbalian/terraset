
import yaml
import os, shutil
import glob
import re

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
    """ Superset connection and static methods """

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
    def reset_directory(dir):
        shutil.rmtree(dir)
        os.makedirs(dir)
        pass

    @staticmethod
    def read_yaml(yml_path):
        with open(yml_path, 'r') as stream:
            try:
                parsed_yaml=yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return parsed_yaml


class TerrasetCharts(TerrasetBase):
    """ Chart objects and list """

    def __init__(self):
        super().__init__()
        self._remote_charts = None
        self._local_charts_list = []

    @property
    def local_charts_list(self):
        self._local_charts_list = [x for x in os.listdir(self.charts_dir) if x!=".DS_Store"]
        return self._local_charts_list

    @property
    def remote_charts(self):
        """ These are the actual chart objects """
        if not self._remote_charts:
            self._remote_charts = self.conn.charts.find()
        return self._remote_charts

    @remote_charts.setter
    def remote_charts(self,value):
        self._remote_charts = value

    @property
    def remote_charts_list(self):
        return [re.sub('[^A-Za-z0-9]+', '_', x.slice_name) + "_" + str(x.id) for x in self.remote_charts]

    @property
    def remote_charts_list_missing_from_local(self):
        """ Charts available in remote not stored in local """
        return list(set(self.remote_charts_list).difference(set(self.local_charts_list)))

    @property
    def remote_chart_ids_missing_from_local(self):
        """ Charts ids available in remote not stored in local """
        return [int(x.split("_")[-1]) for x in self.remote_charts_list_missing_from_local]

    @property
    def remote_charts_missing_from_local(self):
        return [x for x in self.remote_charts if x.id in self.remote_chart_ids_missing_from_local]


class TerrasetDashboards(TerrasetBase):
    """ Dashboard objects and list """

    def __init__(self):
        super().__init__()
        self._remote_dashboards = None
        self._local_dashboards_list = []

    @property
    def local_dashboards_list(self):
        self._local_dashboards_list = [x for x in os.listdir(self.dashboards_dir) if x!=".DS_Store"]
        return self._local_dashboards_list

    @property
    def remote_dashboards(self):
        """ These are the actual dashboard objects """
        if not self._remote_dashboards:
            self._remote_dashboards = self.conn.dashboards.find()
        return self._remote_dashboards

    @remote_dashboards.setter
    def remote_dashboards(self,value):
        self._remote_dashboards = value

    @property
    def remote_dashboards_list(self):
        return [re.sub('[^A-Za-z0-9]+', '_', x.dashboard_title) + "_" + str(x.id) for x in self.remote_dashboards]

    @property
    def remote_dashboards_missing_from_local(self):
        """ Charts available in remote not stored in local """
        return list(set(self.remote_dashboards_list).difference(set(self.local_dashboards_list)))
