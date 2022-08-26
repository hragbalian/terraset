import yaml
import os
import re
import zipfile
import uuid
import shutil

from .superset import SupersetConnectionMgmnt

from .charts import Charts
from .dashboards import Dashboards


def process_export(superset_object,
    superset_object_name_entry: str, directory: str):
    """ A helper function to transform the exported files into a common format """ 

    tmp_name = str(uuid.uuid4())
    desired_name = re.sub('[^A-Za-z0-9]+', '_', getattr(superset_object, superset_object_name_entry))
    id = str(superset_object.id)

    superset_object.export(directory, tmp_name)

    with zipfile.ZipFile(f'{directory}/{tmp_name}.zip', 'r') as zip_ref:
        zip_ref.extractall(f'{directory}/{tmp_name}')

    os.rename(f'{directory}/{tmp_name}', f'{directory}/{desired_name}_{id}')
    os.remove(f'{directory}/{tmp_name}.zip')


class TerrasetBase(SupersetConnectionMgmnt):

    def __init__(self):
        super().__init__()
        self.charts = Charts()
        self.dashboards = Dashboards()

    @staticmethod
    def joiner(*args):
        return "".join(args)

    @staticmethod
    def reset_directory(dir):
        shutil.rmtree(dir)
        os.makedirs(dir)
        pass

    @staticmethod
    def read_yaml(yml_path):
        with open(yml_path, 'r') as stream:
            try:
                parsed_yaml=yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return parsed_yaml

    @staticmethod
    def write_yaml(yml_path, object):
        with open(yml_path, 'w') as stream:
            try:
                yaml.dump(object, stream)
            except yaml.YAMLError as exc:
                print(exc)
