import os
import random
import json

from supersetapiclient.charts import Chart

from ..factory import TerrasetObjectFactory
from ..mixins import StaticMixins

from ..logger import LogConfig

logger = LogConfig("charts").logger

class Charts(TerrasetObjectFactory, StaticMixins):

    object_type = "charts"

    def __init__(self):
        super().__init__()
        if not os.path.exists(self.dir_map[self.object_type]):
            os.makedirs(self.dir_map[self.object_type])

    def _read_chart(self, item_name: str, id_strategy: str = "random"):
        """ Read chart settings and return the chart object

            id_strategy (str): random id "random" or read from settings "settings"

        """
        ymlsettings = self.read_yaml(self.local_yaml_filepaths[item_name])
        # TODO: Validate the yaml settings
        datasource_id, datasource_type = ymlsettings['params']['datasource'].split("__")

        object = Chart(
            id=random.randint(1,10) if id_strategy == "random" else int(item_name.split("_")[-1]), # Chart object needs id, but the actual id is set on Superset's side by the database, so just setting random id here
            slice_name=ymlsettings['slice_name'],
            description=ymlsettings['description'],
            params=json.dumps(ymlsettings['params']),
            datasource_id=datasource_id,
            datasource_type=datasource_type,
            viz_type=ymlsettings['viz_type'])

        logger.info(object.id)

        return object, ymlsettings, datasource_id, datasource_type

    def add(self, item_name: str):

        object, ymlsettings, datasource_id, datasource_type = self._read_chart(item_name, "random")

        new_id = self.conn.charts.add(object) # When adding chart, responds with new id

        logger.info(f"Item {item_name} added to remote")

        # Replace the settings file with a full export from superset since there could be inconsistencies with the ids
        self.remove_directory(f"{self.dir_map[self.object_type]}/{item_name}")
        chart = self.conn.charts.find_one(id = new_id)

        self.process_export(chart,
            self.title_attribute[self.object_type],
            self.dir_map[self.object_type]
            )

    def change(self, item_name: str):

        object, ymlsettings, datasource_id, datasource_type = self._read_chart(item_name, "settings")

        remote = self.conn.charts.get(int(item_name.split("_")[-1])) # Fresh API call to grab the chart

        for key, value in ymlsettings.items():

            setattr(remote, key, value)

        setattr(remote, "datasource_id", int(datasource_id))
        setattr(remote, "datasource_type", datasource_type)

        logger.info("Persisting changes in remote")

        remote.save()
