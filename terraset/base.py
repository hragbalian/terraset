
from .superset import SupersetConnectionMgmnt

from .object_types.charts import Charts
from .object_types.dashboards import Dashboards
from .object_types.datasets import Datasets
from .object_types.databases import Databases

from .mixins import StaticMixins

class TerrasetBase(SupersetConnectionMgmnt, StaticMixins):

    def __init__(self):
        super().__init__()
        self.charts = Charts()
        self.dashboards = Dashboards()
        self.datasets = Datasets()
        # self.databases = Databases()
