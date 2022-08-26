import os
import re

from .fetch import TerrasetFetch
from .plan import TerrasetPlan
from .apply import TerrasetApply

class Terraset(
    TerrasetFetch,
    TerrasetPlan,
    TerrasetApply
    ): pass
