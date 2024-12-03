import numpy as np
import json

from typing import Any


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        elif isinstance(obj, np.ndarray):
            return list(obj)
        elif isinstance(obj, np.int32):
            return int(obj)
        else:
            return json.JSONEncoder.default(self, obj)
