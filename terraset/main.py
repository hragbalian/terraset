import os
import re

from .fetch import TerrasetFetch
from .operation import TerrasetOperation

class Terraset(
    TerrasetFetch,
    TerrasetOperation): pass
