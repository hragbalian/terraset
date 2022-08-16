
import yaml
import os, shutil
import re

from .superset import SupersetConnectionMgmnt
from .logger import LogConfig

logger = LogConfig("Terraset").logger

class TerrasetBase(SupersetConnectionMgmnt):

    def __init__(self):
        super().__init__()
        self.charts = TerrasetObjectFactory("charts")
        self.dashboards = TerrasetObjectFactory("dashboards")

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


class TerrasetObjectFactory(SupersetConnectionMgmnt):
    """ Factory to create any kind of object supported by Superset (Charts, Dashboards, etc.)"""

    def __init__(self, object_type: str):
        super().__init__()
        self.object_type = object_type # Add validation on this
        self.find = self.find_methods[self.object_type] # Grab the correct method for the object type
        self._remote = None
        self._local_list = []

    @property
    def local_list(self):
        self._local_list = [x for x in os.listdir(self.dir_map[self.object_type])
            if x!=".DS_Store"]
        return self._local_list

    @property
    def remote(self):
        """ These are the actual objects """
        if not self._remote:
            self._remote = self.find()
        return self._remote

    @remote.setter
    def remote(self,value):
        self._remote = value

    @property
    def remote_list(self):
        return [re.sub('[^A-Za-z0-9]+', '_', getattr(x, self.title_attribute[self.object_type])) + "_" + str(x.id) for x in self.remote]

    @property
    def remote_list_missing_from_local(self):
        """ Available in remote not stored in local """
        return list(set(self.remote_list).difference(set(self.local_list)))

    @property
    def remote_ids_missing_from_local(self):
        """ Ids available in remote not stored in local """
        return [int(x.split("_")[-1]) for x in self.remote_list_missing_from_local]

    @property
    def remote_missing_from_local(self):
        return [x for x in self.remote if x.id in self.remote_ids_missing_from_local]
