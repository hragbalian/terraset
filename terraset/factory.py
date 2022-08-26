
import os
import re

from abc import ABC, abstractmethod

from .superset import SupersetConnectionMgmnt
from .schemas import SupersetObject
from .logger import LogConfig

logger = LogConfig("Terraset").logger

class TerrasetObjectFactory(SupersetConnectionMgmnt, ABC):
    """ Factory to create any kind of object supported by Superset (Charts, Dashboards, etc.)"""

    def __init__(self):
        super().__init__()
        self._object_type = None
        self._find = None
        self._remote = None
        self._local_list = []
        self._direction = None # Used for Apply
        self._item_name = None # Used for Apply

    @property
    def object_type(self):
        return self._object_type

    @object_type.setter
    def object_type(self, value):
        SupersetObject(superset_object=value)
        self._object_type = value

    @property
    def find(self):
        return self.find_methods[self.object_type] # Grab the correct method for the object type

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    @property
    def item_name(self):
        return self._item_name

    @item_name.setter
    def item_name(self, value):
        self._item_name = value

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def change(self):
        pass

    def delete(self, superset_connection, id: int):
        logger.info(f"Deleted {self.object_type} {id}")
        getattr(getattr(self, "conn"), self.object_type).delete(id)
        
    @staticmethod
    def find_chart_yaml_filename(path) -> str:
        return [x for x in os.listdir(path) if x!=".DS_Store"][0]

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
    def remote_list(self) -> list:
        return [re.sub('[^A-Za-z0-9]+', '_', getattr(x, self.title_attribute[self.object_type])) + "_" + str(x.id) for x in self.remote]

    @property
    def remote_list_missing_from_local(self) -> list:
        """ Available in remote not stored in local """
        return list(set(self.remote_list).difference(set(self.local_list)))

    @property
    def remote_ids_missing_from_local(self) -> list:
        """ Ids available in remote not stored in local """
        return [int(x.split("_")[-1]) for x in self.remote_list_missing_from_local]

    @property
    def remote_missing_from_local(self) -> list:
        return [x for x in self.remote if x.id in self.remote_ids_missing_from_local]

    @property
    def local_list_missing_from_remote(self) -> list:
        """ Available in local but not stored in remote """
        return list(set(self.local_list).difference(set(self.remote_list)))

    @property
    def local_ids_missing_from_remote(self) -> list:
        """ Ids available in local not stored in remote """
        return [int(x.split("_")[-1]) for x in self.local_list_missing_from_remote]

    @property
    def overlap_local_and_remote(self) -> list:
        """ Available in both remote and local """
        return list(set(self.local_list).intersection(set(self.remote_list)))

    @property
    def local_yaml_filepaths(self) -> dict:
        """ Key/value pairs of local object and filepath to object specs """
        store = dict()
        for x in self.local_list:
            path_to_yaml = f"{self.dir_map[self.object_type]}/{x}/{self.object_type}"
            curr_yaml = self.find_chart_yaml_filename(path_to_yaml)
            store[x] = f"{path_to_yaml}/{curr_yaml}"
        return store
