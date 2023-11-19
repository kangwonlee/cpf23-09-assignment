import os
import pandas as pd
import pathlib
import sys


import pytest


file_path = pathlib.Path(__file__)
test_folder = file_path.parent.absolute()
proj_folder = test_folder.parent.absolute()


sys.path.insert(
    0,
    str(proj_folder)
)


from ex09 import func09


@pytest.fixture
def root(tmp_path):
    return tmp_path / "test_data"


@pytest.fixture
def a_time() -> float:
    return 1647232000.0


@pytest.fixture
def b_time() -> float:
    return 1647235600.0


@pytest.fixture
def test_folder_tree(root, a_time, b_time):
    # Create test folder tree
    root.mkdir(parents=True)
    files = [
        (root / "a.txt"),
        (root / "b.txt"),
    ]
    for f in files:
        f.touch()

    # Set modification times
    os.utime(root / "a.txt", (a_time, a_time))
    os.utime(root / "b.txt", (b_time, b_time))

    return root


def test_func09(test_folder_tree, a_time, b_time):
    start = a_time
    end = b_time
    root = test_folder_tree

    df = func09(start, end, root)

    expected_df = pd.DataFrame(
        [
            {
                "fname": "a.txt",
                "size": 0,
                "time": a_time,
            },
            {
                "fname": "b.txt",
                "size": 0,
                "time": b_time,
            },
        ]
    )

    df.sort_values(by=["fname"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    pd.testing.assert_frame_equal(df, expected_df)


def test_func09_empty(test_folder_tree, a_time, b_time):
    start = a_time - 1.0
    end = start + 0.5
    root = test_folder_tree

    df = func09(start, end, root)

    expected_df = pd.DataFrame()

    pd.testing.assert_frame_equal(df, expected_df)


if "__main__" == __name__:
    pytest.main(["-qq", __file__])
