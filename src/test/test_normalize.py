import numpy as np
from core.preprocessing import robust_normalize

def test_normalize_range():
    data = [0, 50, 100]
    norm = robust_normalize(data)

    assert min(norm) >= 0.0
    assert max(norm) <= 1.0


def test_normalize_constant():
    data = [5, 5, 5]
    norm = robust_normalize(data)

    assert all(x == 0.0 for x in norm)