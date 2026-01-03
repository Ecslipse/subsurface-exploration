import pytest
from pathlib import Path
from core.config import CLASConfig

@pytest.fixture
def sample_las_path():
    return Path(__file__).parent.parent / "sample" / "well01.las"

@pytest.fixture
def cfg():
    return CLASConfig(
        min_thickness = 1.0,
        w_gr = 0.4,
        w_dens = 0.4,
        w_stab  = 0.15,
        w_cal  = 0.05,
        point_threshold=0.8
    )