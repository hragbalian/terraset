
import re
import uuid
import zipfile
import os

from deepdiff import DeepDiff


from .base import TerrasetBase
from .schemas import Directions
from .configs import (
    supported_superset_objects,
    find_to_export_map,
    actions
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



class TerrasetPlan(TerrasetBase):
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
        for supported_object in supported_superset_objects:
            getattr(self, supported_object).remote = getattr(self, f"find_{supported_object}")()


    def plan(self, direction: str = "local-to-remote"):
        """ Evaluate the differences between local and remote

        direction (str): whether to set local settings or remote settings as the direction
            of desired (new) settings. Defaults to local-to-remote.
        """

        Directions(direction=direction)

        store = dict(
            direction = direction,
            **{x: {} for x in actions})

        self.refresh_from_remote()

        for object_type in supported_superset_objects:

            # Look for additions
            if direction == "local-to-remote":
                store['add'][object_type] = getattr(self, object_type).local_list_missing_from_remote
            elif direction == "remote-to-local":
                store['add'][object_type] = getattr(self, object_type).remote_list_missing_from_local

            # Look for changes
            store['change'][object_type] = dict()

            find_entries = find_to_export_map[object_type]

            for item in getattr(self, object_type).overlap_local_and_remote:

                item_id = int(item.split("_")[-1])

                remote_settings = [x for x in getattr(self, object_type).remote if x.id == item_id][0].__dict__
                local_settings = self.read_yaml(getattr(self, object_type).local_yaml_filepaths[item])

                if object_type == "charts":
                    # This if statement is a patch until there is a fix in the API for the 'description' entry for charts
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

                if direction == "local-to-remote":
                    curr_diff = DeepDiff(remote_settings, local_settings)
                elif direction == "remote-to-local":
                    curr_diff = DeepDiff(local_settings, remote_settings)

                if len(curr_diff)>0:
                    store['change'][object_type][item] = curr_diff

            # Look for deletions
            if direction == "local-to-remote":
                store['delete'][object_type] = getattr(self, object_type).remote_list_missing_from_local
            elif direction == "remote-to-local":
                store['delete'][object_type] = getattr(self, object_type).local_list_missing_from_remote

        self.latest_plan = store

        pretty_print_dict(store)
