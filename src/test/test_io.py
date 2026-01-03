import lasio
from core.io import read_las

def test_load_las_returns_lasio_object(sample_las_path):
    las = read_las(sample_las_path)
    assert isinstance(las, lasio.LASFile)
    assert "GR" in las.keys()  # gamma ray curve must exist
    assert "DEPTH" in las.keys() # depth curve must exist