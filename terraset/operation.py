
import re
import uuid
import zipfile
import os
import json
import random


from deepdiff import DeepDiff

from supersetapiclient.charts import Chart
from supersetapiclient.dashboards import Dashboard

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

actions = ['add', 'change', 'delete']

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
        self.charts.remote = self.find_charts()
        self.dashboards.remote = self.find_dashboards()

    def plan(self, base: str = "local-to-remote"):
        """ Evaluate the differences between local and remote

        base (str): whether to set local settings or remote settings as the base
            of desired (new) settings. Defaults to local-to-remote.
        """

        Bases(base=base)

        store = dict(
            base = base,
            **{x: {} for x in actions})

        self.refresh_from_remote()

        for object_type in supported_superset_objects:

            # Look for additions
            if base == "local-to-remote":
                store['add'][object_type] = getattr(self, object_type).local_list_missing_from_remote
            elif base == "remote-to-local":
                store['add'][object_type] = getattr(self, object_type).remote_list_missing_from_local

            # Look for changes
            store['change'][object_type] = dict()

            find_entries = find_to_export_map[object_type]

            for item in getattr(self, object_type).overlap_local_and_remote:

                item_id = int(item.split("_")[-1])

                remote_settings = [x for x in getattr(self, object_type).remote if x.id == item_id][0].__dict__
                local_settings = self.read_yaml(getattr(self, object_type).local_yaml_filepaths[item])

                if object_type == "charts":
                    # This is a patch until there is a fix in the API for the 'description' entry
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
                    store['change'][object_type][item] = curr_diff

            # Look for deletions
            if base == "local-to-remote":
                store['delete'][object_type] = getattr(self, object_type).remote_list_missing_from_local
            elif base == "remote-to-local":
                store['delete'][object_type] = getattr(self, object_type).local_list_missing_from_remote

        self.latest_plan = store

        pretty_print_dict(store)

    def _add_to_remote(self, object_type: str, item: str):
        """ Add a resource from yaml file to remote

        item (str): the name of the resource e.g. Age_33, where the first prefix is the name and
            the suffix is the id. Items are unique.
        """

        ymlsettings = self.read_yaml(getattr(self, object_type).local_yaml_filepaths[item])
        # TODO: Validate the yaml settings
        # TODO: Validate the item name relative to other resources.  The remote infrastructure controls the actual
        # ids so setting an id here will get overwritten.
        datasource_id, datasource_type = ymlsettings['params']['datasource'].split("__")

        if object_type == "charts":

            object = Chart(
                id=random.randint(1,10), # Chart object needs id, but the actual id is set on Superset's side by the database, so just setting random id here
                slice_name=ymlsettings['slice_name'],
                description=ymlsettings['description'],
                params=json.dumps(ymlsettings['params']),
                datasource_id=datasource_id,
                datasource_type=datasource_type,
                viz_type=ymlsettings['viz_type'])

            new_id = self.conn.charts.add(object)

            logger.info(f"Item {item} added to remote")

            # Replace the settings file with a full export from superset since there could be inconsistencies with the ids
            

        elif object_type == "dashboards":
            pass


    def _delete_from_remote(self, object_type: str, id: int):
        getattr(getattr(self, "conn"), object_type).delete(id)


    def apply(self, base: str = "local-to-remote"):
        """ Apply desired settings

        base (str): whether to set local settings or remote settings as the base
            of desired (new) settings. Defaults to local.

        """

        Bases(base=base)

        self.plan(base) # Trigger latest plan

        current_plan = self.latest_plan

        if base == "local-to-remote":

            for action in actions:

                current_plan_action = current_plan[action]

                for object_type, items in current_plan_action.items():

                    for item in items:

                        if action =="add":

                            self._add_to_remote(object_type, item)

                        if action =="delete":

                            self._delete_from_remote(object_type, int(item.split("_")[-1]))
