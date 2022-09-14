
import os

from supersetapiclient.datasets import Datasets

from ..factory import TerrasetObjectFactory
from ..mixins import StaticMixins

from ..logger import LogConfig

logger = LogConfig("datasets").logger

class Datasets(TerrasetObjectFactory, StaticMixins):

    object_type = "datasets"

    def __init__(self):
        super().__init__()
        if not os.path.exists(self.dir_map[self.object_type]):
            os.makedirs(self.dir_map[self.object_type])

    def add(self):
        pass

    def change(self):
        pass
