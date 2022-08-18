
import re
import uuid
import zipfile
import os

from deepdiff import DeepDiff

from .base import TerrasetBase
from .schemas import SupersetObject
from .configs import (
    supported_superset_objects,
    updateable_info
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

    def plan(self):
        """ Evaluate the differences between local and remote """

        store = dict()

        for object_type in supported_superset_objects:

            store[object_type] = dict()

            for item in getattr(self, object_type).local_list:

                item_id = int(item.split("_")[-1])

                local_settings = self.read_yaml(getattr(self, object_type).local_yaml_filepaths[item])

                # if "description" not in local_settings.keys():
                #     local_settings["description"] = ""

                remote_settings = [x for x in getattr(self, object_type).remote if x.id == item_id][0].__dict__

                # Filter the object to specs that can be updated via the API
                local_settings = {x : local_settings[x] for x in updateable_info[object_type]}
                remote_settings = {x : remote_settings[x] for x in updateable_info[object_type]}

                curr_diff = DeepDiff(remote_settings, local_settings)

                if len(curr_diff)>0:
                    store[object_type][item] = curr_diff

        pretty_print_dict(store)

    def apply(self):
        pass
