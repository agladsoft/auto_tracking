import os
import pytest
import pandas as pd
from pathlib import Path
from _pytest.monkeypatch import MonkeyPatch
from scripts.main import AutoTracking, DataFrameGroupBy, Optional

@pytest.fixture

def sample_dataframe() -> pd.DataFrame:
    data: dict = {
        'enforce_auto_tracking': [True, False, True, True, False, True],
        'original_file_name': ['file1_ИМПОРТ.xlsx', 'file2_ЭКСПОРТ.xlsx', 'file3_ИМПОРТ.xlsx',
                               'file4_ИМПОРТ.xlsx', 'file5_ЭКСПОРТ.xlsx', 'file6_ИМПОРТ.xlsx'],
        'terminal': ['НУТЭП', 'ВСК', 'НУТЭП', 'ПКТ', 'ВСК', 'УЛКТ'],
        'direction': ['import', 'export', 'import', 'import', 'export', 'import'],
        'is_auto_tracking': [True, False, True, True, False, True],
        'is_auto_tracking_ok': [True, None, True, True, None, True],
        'year': [2024, 2024, 2024, 2024, 2024, 2024],
        'month': [1, 1, 1, 1, 1, 1]
    }
    return pd.DataFrame(data)


@pytest.fixture
def auto_tracking_instance(
    sample_dataframe: pd.DataFrame,
    tmp_path: Path,
    monkeypatch: MonkeyPatch
) -> AutoTracking:
    temp_file: Path = tmp_path / "temp_excel.xlsx"
    sample_dataframe.to_excel(temp_file, index=False)
    monkeypatch.setenv('XL_IDP_PATH_IMPORT', str(tmp_path))
    monkeypatch.setenv('XL_IDP_PATH_VSK_IMPORT', str(tmp_path))
    monkeypatch.setenv('XL_IDP_PATH_NW_IMPORT', str(tmp_path))
    monkeypatch.setenv('XL_IDP_PATH_EXPORT', str(tmp_path))
    monkeypatch.setenv('XL_IDP_PATH_VSK_EXPORT', str(tmp_path))
    monkeypatch.setenv('XL_IDP_PATH_NW_EXPORT', str(tmp_path))
    return AutoTracking(str(temp_file))

@pytest.mark.parametrize(
    "path, expected_files",
    [
        ("test_dir", [
            'file1_ИМПОРТ.xlsx', 'file2_ЭКСПОРТ.xlsx', 'file3_ИМПОРТ.xlsx',
            'file4_ИМПОРТ.xlsx', 'file5_ЭКСПОРТ.xlsx', 'file6_ИМПОРТ.xlsx'
        ]),  # Test case 1: Directory creation and multiple files
        (None, []),  # Test case 2: No directory provided
    ]
)
def test_save_to_excel(
    auto_tracking_instance: AutoTracking,
    sample_dataframe: pd.DataFrame,
    tmp_path: Path,
    path: Optional[str],
    expected_files: list
):
    if path:
        path: Path = tmp_path / path

    group_columns: DataFrameGroupBy = sample_dataframe.groupby(['original_file_name'])
    auto_tracking_instance.save_to_excel(group_columns, str(path) if path else None)
    if path:
        for file in expected_files:
            assert os.path.exists(path / file)
        assert os.path.isdir(path)  # Verify directory creation


@pytest.mark.parametrize(
    "expected_files",
    [
        (['file2_ЭКСПОРТ.xlsx', 'file5_ЭКСПОРТ.xlsx']),
        ([]),  # Test case 2: No directory provided
    ]
)
def test_write_cabotage(
    auto_tracking_instance: AutoTracking,
    sample_dataframe: pd.DataFrame,
    tmp_path: Path,
    expected_files: list
) -> None:
    group_columns: DataFrameGroupBy = sample_dataframe.groupby(['enforce_auto_tracking', 'original_file_name'])
    auto_tracking_instance.write_cabotage(group_columns)

    for file in expected_files:
        for direction, path in auto_tracking_instance.directions_cabotage.values():
            if direction in file:
                assert os.path.exists(f"{str(path)}/{file}")


@pytest.mark.parametrize(
    "expected_files",
    [
        (['file1_ИМПОРТ.xlsx', 'file3_ИМПОРТ.xlsx']),
        ([]),  # Test case 2: No directory provided
    ]
)
def test_write_rows_by_terminal(
    auto_tracking_instance: AutoTracking,
    sample_dataframe: pd.DataFrame,
    tmp_path: Path,
    expected_files: list
) -> None:
    auto_tracking_instance.write_rows_by_terminal(sample_dataframe, "import", ["НУТЭП"], str(tmp_path))

    for file in expected_files:
        assert os.path.exists(f"{str(tmp_path)}/{file}")


def test_change_types_in_columns(sample_dataframe: pd.DataFrame) -> None:
    AutoTracking.change_types_in_columns(sample_dataframe)
    assert sample_dataframe["enforce_auto_tracking"].dtype == bool
    assert sample_dataframe["is_auto_tracking"].dtype == bool
    assert sample_dataframe["is_auto_tracking_ok"].dtype == bool


@pytest.mark.parametrize(
    "expected_files",
    [
        ({
            'file1_ИМПОРТ.xlsx', 'file2_ЭКСПОРТ.xlsx', 'file3_ИМПОРТ.xlsx',
            'file4_ИМПОРТ.xlsx', 'file5_ЭКСПОРТ.xlsx', 'file6_ИМПОРТ.xlsx'
        }),
        (set()),  # Test case 2: No directory provided
    ]
)
def test_main(auto_tracking_instance: AutoTracking, tmp_path: Path, expected_files: set) -> None:
    auto_tracking_instance.main()

    found_files = set()
    for root, _, files in os.walk(tmp_path):
        found_files.update(files)

    assert expected_files.issubset(found_files), f"Missing files: {expected_files - found_files}"

