
import re
import uuid
import zipfile
import os

from deepdiff import DeepDiff

from .base import TerrasetBase
from .schemas import Bases
from .configs import (
    supported_superset_objects,
    find_to_export_map
    )
from .logger import LogConfig

logger = LogConfig("operations").logger


def pretty_print_dict(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty_print_dict(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))



class TerrasetOperation(TerrasetBase):
    """ Plan and Apply """

    def __init__(self):
        super().__init__()
        self._latest_plan = None

    @property
    def latest_plan(self):
        self.plan()
        return self._latest_plan

    @latest_plan.setter
    def latest_plan(self, value):
        self._latest_plan = value

    def refresh_from_remote(self):
        """ Refresh the chart and dashboard objects from remote """
        self.charts.remote = self.conn.charts.find()
        self.dashboards.remote = self.conn.dashboards.find()

    def plan(self, base: str = "local-to-remote"):
        """ Evaluate the differences between local and remote

        base (str): whether to set local settings or remote settings as the base
            of desired (new) settings. Defaults to local-to-remote.
        """

        Bases(base=base)

        store = dict()
        store['base'] = base

        self.refresh_from_remote()

        for object_type in supported_superset_objects:

            store[object_type] = dict()

            find_entries = find_to_export_map[object_type]

            for item in getattr(self, object_type).local_list:

                item_id = int(item.split("_")[-1])

                remote_settings = [x for x in getattr(self, object_type).remote if x.id == item_id][0].__dict__
                local_settings = self.read_yaml(getattr(self, object_type).local_yaml_filepaths[item])

                if object_type == "charts":

                    if "description" not in local_settings.keys():
                        local_settings["description"] = remote_settings['description']
                        self.write_yaml(getattr(self, object_type).local_yaml_filepaths[item], local_settings)

                # local settings translated to remote settings due to inconsistency in API
                local_settings = {x: local_settings[find_entries[x]]
                    if find_entries[x] in local_settings.keys() else None
                    for x in find_entries}

                # Filter the object to specs that can be updated via the API
                remote_settings = {x : remote_settings[x] for x in find_entries}
                local_settings = {x : local_settings[x] for x in find_entries}

                if base == "local-to-remote":
                    curr_diff = DeepDiff(remote_settings, local_settings)
                elif base == "remote-to-local":
                    curr_diff = DeepDiff(local_settings, remote_settings)

                if len(curr_diff)>0:
                    store[object_type][item] = curr_diff

        self.latest_plan = store

        pretty_print_dict(store)

    def apply(self, base: str = "local-to-remote"):
        """ Apply desired settings

        base (str): whether to set local settings or remote settings as the base
            of desired (new) settings. Defaults to local.

        """

        Bases(base=base)

        pass
