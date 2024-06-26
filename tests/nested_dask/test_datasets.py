import nested_dask as nd
import pytest


def test_generate_data():
    """test the dataset generator function"""

    # test the seed
    generate_1 = nd.datasets.generate_data(10, 100, npartitions=2, seed=1)
    generate_2 = nd.datasets.generate_data(10, 100, npartitions=2, seed=1)
    generate_3 = nd.datasets.generate_data(10, 100, npartitions=2, seed=2)

    assert generate_1.compute().equals(generate_2.compute())
    assert not generate_1.compute().equals(generate_3.compute())

    # test npartitions
    assert generate_1.npartitions == 2

    # test the length
    assert len(generate_1) == 10
    assert len(generate_1.nested.nest.to_flat()) == 1000

    # test seed stability
    assert pytest.approx(generate_1.compute().loc[0]["a"], 0.1) == 0.417
    assert pytest.approx(generate_1.compute().loc[0]["b"], 0.1) == 0.838
    assert pytest.approx(generate_1.nested.nest.to_flat().compute().iloc[0]["t"], 0.1) == 16.015
