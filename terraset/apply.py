

from .base import TerrasetBase
from .schemas import Directions
from .configs import actions

class TerrasetApply(TerrasetBase):

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

                          getattr(self, object_type).add(item)

                      if action =="delete":

                          getattr(self, object_name).delete(
                            self.conn, int(item.split("_")[-1]))
