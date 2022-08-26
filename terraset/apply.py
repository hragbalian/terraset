
import json
import random
from abc import ABC, abstractmethod

from supersetapiclient.charts import Chart
from supersetapiclient.dashboards import Dashboard

from .plan import TerrasetPlan




class ChartApply(TerrasetApplyOperations):

    def __init__(self):
        super().__init__()
        self.object_type = "charts"

    def add(self):

        ymlsettings = self.read_yaml(getattr(self, self.object_type).local_yaml_filepaths[self.item_name])
        # TODO: Validate the yaml settings
        datasource_id, datasource_type = ymlsettings['params']['datasource'].split("__")

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
        getattr(self, object_type).local_yaml_filepaths[item]
        self.reset_directory()

    def change(self):
        pass



class TerrasetApply(TerrasetPlan):

  def apply(self, direction: str = "local-to-remote"):
      """ Apply desired settings

      direction (str): whether to set local settings or remote settings as the direction
          of desired (new) settings. Defaults to local.

      """

      Directions(direction=direction)

      self.plan(direction) # Trigger latest plan

      current_plan = self.latest_plan

      if direction == "local-to-remote":

          for action in actions:

              current_plan_action = current_plan[action]

              for object_type, items in current_plan_action.items():

                  for item in items:

                      if action =="add":

                          self._add_to_remote(object_type, item)

                      if action =="delete":

                          self._delete_from_remote(object_type, int(item.split("_")[-1]))
