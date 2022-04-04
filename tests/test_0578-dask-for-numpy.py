# BSD 3-Clause License; see https://github.com/scikit-hep/uproot4/blob/main/LICENSE


import numpy
import pytest
import skhep_testdata

import uproot


def test_single_dask_array():
    test_path = skhep_testdata.data_path("uproot-Zmumu.root") + ":events"
    ttree = uproot.open(test_path)

    np_arrays = ttree.arrays(library="np")
    dask_arrays = uproot.dask(test_path)

    assert list(dask_arrays.keys()) == list(
        np_arrays.keys()
    ), "Different keys detected in dictionary of dask arrays and dictionary of numpy arrays"

    for key in np_arrays.keys():
        comp = dask_arrays[key].compute() == np_arrays[key]
        assert comp.all(), f"Incorrect array at key {key}"


def test_dask_concatenation():
    test_path1 = skhep_testdata.data_path("uproot-Zmumu.root") + ":events"
    test_path2 = skhep_testdata.data_path("uproot-Zmumu-uncompressed.root") + ":events"
    test_path3 = skhep_testdata.data_path("uproot-Zmumu-zlib.root") + ":events"
    test_path4 = skhep_testdata.data_path("uproot-Zmumu-lzma.root") + ":events"

    np_arrays = uproot.concatenate(
        [test_path1, test_path2, test_path3, test_path4], library="np"
    )
    dask_arrays = uproot.dask([test_path1, test_path2, test_path3, test_path4])

    assert list(dask_arrays.keys()) == list(
        np_arrays.keys()
    ), "Different keys detected in dictionary of dask arrays and dictionary of numpy arrays"

    for key in np_arrays.keys():
        comp = dask_arrays[key].compute() == np_arrays[key]
        assert comp.all(), f"Incorrect array at key {key}"


def test_multidim_array():
    test_path = (
        skhep_testdata.data_path("uproot-sample-6.08.04-uncompressed.root") + ":sample"
    )
    ttree = uproot.open(test_path)

    np_arrays = ttree.arrays(library="np")
    dask_arrays = uproot.dask(test_path)

    assert list(dask_arrays.keys()) == list(
        np_arrays.keys()
    ), "Different keys detected in dictionary of dask arrays and dictionary of numpy arrays"

    comp = dask_arrays["ab"].compute() == np_arrays["ab"]
    assert comp.all(), "Incorrect array at key {}".format("ab")
