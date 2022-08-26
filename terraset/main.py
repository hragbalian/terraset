import os
import re

from .fetch import TerrasetFetch
from .plan import TerrasetPlan

class Terraset(
    TerrasetFetch,
    TerrasetPlan): pass
