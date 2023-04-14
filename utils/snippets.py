from __future__ import annotations

from pathlib import Path
from typing import Any
from typing import List

import numpy as np
import pandas as pd
import yaml
from nptyping import NDArray, DataFrame
from nptyping.shape import Shape

np1d = NDArray[Shape["*"], Any]


def get_src_dir() -> Path:
    """Returns your src directory"""
    return Path(Path(__file__).absolute().parent)


def get_config(yaml_file: Path = Path(get_src_dir().parent, "config.yaml")) -> dict:
    r"""
    Process yaml config.
    """
    with open(yaml_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config