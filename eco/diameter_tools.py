import ast
import math
from typing import List


def get_area(circ: float) -> float:
    return math.pi * (circ / (2.0 * math.pi)) ** 2


def eval_circumferences(input_data: str) -> List[float]:
    try:
        circumferences = ast.literal_eval(input_data)
    except ValueError as e:
        print(input_data, e, type(input_data))
        circumferences = [input_data, ]
    if isinstance(circumferences, int):
        return [float(circumferences), ]
    return [float(c) for c in circumferences]


def get_trunk_diam(input_data: str) -> float:
    """
    Normalize the trunk diameter.

    Assumption: when tree has many trunks, you can sum their areas
    and treat them as a one bigger trunk.
    """
    circumferences = eval_circumferences(input_data)
    area = sum(get_area(circ) for circ in circumferences)
    return math.sqrt(area / math.pi) * 2
