
from .superset import SupersetConnectionMgmnt

from .object_types.charts import Charts
from .object_types.dashboards import Dashboards
from .mixins import StaticMixins

class TerrasetBase(SupersetConnectionMgmnt, StaticMixins):

    def __init__(self):
        super().__init__()
        self.charts = Charts()
        self.dashboards = Dashboards()
