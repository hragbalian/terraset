
import random
import json

from supersetapiclient.charts import Chart

from ..factory import TerrasetObjectFactory
from ..mixins import StaticMixins

from ..logger import LogConfig

logger = LogConfig("operations").logger

class Charts(TerrasetObjectFactory, StaticMixins):

    object_type = "charts"

    def add(self, item_name: str):

        ymlsettings = self.read_yaml(self.local_yaml_filepaths[item_name])
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

        logger.info(f"Item {item_name} added to remote")

        # Replace the settings file with a full export from superset since there could be inconsistencies with the ids
        self.remove_directory(f"{self.dir_map[self.object_type]}/{item_name}")
        chart = self.conn.charts.find_one(id = new_id)

        self.process_export(chart,
            self.title_attribute[self.object_type],
            self.dir_map[self.object_type]
            )

    def change(self):
        pass
