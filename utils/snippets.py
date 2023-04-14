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
    """Returns your ../hf-decompensation/src directory"""
    return Path(Path(__file__).absolute().parent.parent)


def get_config(yaml_file: Path = Path(get_src_dir().parent, "config.yaml")) -> dict:
    r"""
    Process yaml config.
    ! If this fails, make sure your working directory is hf-decompensation\src or
    provide the yaml_file argument explicitly
    """
    with open(yaml_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config