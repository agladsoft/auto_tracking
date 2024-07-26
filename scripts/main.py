import os
import sys
import pandas as pd
from pandas import DataFrame
from typing import Tuple, Optional
from pandas.core.groupby import DataFrameGroupBy


DIRECTIONS = {
    "import": ["ИМПОРТ", f"{os.environ['XL_IDP_PATH_VSK_IMPORT']}/flat_import_vsk_tracking_update"],
    "export": ["ЭКСПОРТ", f"{os.environ['XL_IDP_PATH_VSK_EXPORT']}/flat_export_vsk_tracking_update"]
}


def all_(iterable):
    return all(iterable) if iterable else False


class AutoTracking(object):
    def __init__(self, input_file_path: str):
        self.input_file_path: str = input_file_path

    @staticmethod
    def write_cabotage(direction: str, path: Optional[str], group_columns: DataFrameGroupBy, directions: list) -> None:
        """
        Find and save cabotage in file.
        :param direction: Value of direction.
        :param path: The path of the folder to save.
        :param group_columns: Grouped data by columns ['enforce_auto_tracking', 'original_file_name'].
        :param directions: Found directions in files.
        :return:
        """
        filtered_groups = {
            direction: group_columns.filter(
                lambda x: x['original_file_name'].str.contains(direction, case=False).all()
            )
            for direction in directions
        }
        if not directions:
            raise AssertionError("В наименовании файла не указано направление для каботажа")
        column: DataFrame
        for direction_, column in list(filtered_groups.items()):
            if column.empty:
                continue
            column['is_auto_tracking'] = False
            column['is_auto_tracking_ok'] = None
            for key, value in DIRECTIONS.items():
                if direction_ in value:
                    path = value[1]
            column.to_excel(
                f"{path}/{column['original_file_name'].unique()[0].replace('.csv', '').replace('.XLSX', '.xlsx')}",
                index=False
            )

    def write_rows_by_terminal(self, df: DataFrame, direction: str, terminals: list, path: Optional[str]) -> None:
        """
        We group by 'enforce_auto_tracking', 'year', 'month' and write it to a separate xlsx file.
        :param df: DataFrame.
        :param direction: Value of direction.
        :param terminals: List of value of terminal.
        :param path: The path of the folder to save.
        :return:
        """
        if path and not os.path.exists(path):
            os.mkdir(path)
        for terminal in terminals:
            df: DataFrame = df.loc[(df['terminal'] == terminal) & (df['direction'] == direction)]
            group_columns = df.groupby(['enforce_auto_tracking', 'original_file_name'])
            directions = [direction_[0] for direction_ in list(DIRECTIONS.values())]
            if direction == "cabotage":
                self.write_cabotage(direction, path, group_columns, directions)
                continue
            column: Tuple[Tuple, DataFrame]
            for column in group_columns:
                if not column[0][0]:
                    column[1]['is_auto_tracking'] = False
                    column[1]['is_auto_tracking_ok'] = None
                column[1].to_excel(f"{path}/{column[0][1].replace('.csv', '').replace('.XLSX', '.xlsx')}", index=False)

    @staticmethod
    def change_types_in_columns(df: DataFrame) -> None:
        """
        Change types in columns to bool.
        :param df: DataFrame.
        :return:
        """
        df["enforce_auto_tracking"] = df["enforce_auto_tracking"].astype(bool)
        df["is_auto_tracking"] = df["is_auto_tracking"].astype(bool)
        df["is_auto_tracking_ok"] = df["is_auto_tracking_ok"].astype(bool)

    def main(self) -> None:
        """
        The main function where we read the Excel file and write the file to json.
        :return:
        """
        df: DataFrame = pd.read_excel(self.input_file_path)
        self.change_types_in_columns(df)
        self.write_rows_by_terminal(df, list(DIRECTIONS.keys())[0], ["НУТЭП"],
                                    f"{os.environ['XL_IDP_PATH_IMPORT']}/lines_nutep/flat_import_nutep_tracking_update")
        self.write_rows_by_terminal(df, list(DIRECTIONS.keys())[0], ["ВСК"],
                                    f"{os.environ['XL_IDP_PATH_VSK_IMPORT']}/flat_import_vsk_tracking_update")
        self.write_rows_by_terminal(df, list(DIRECTIONS.keys())[1], ["ПКТ", "УЛКТ", "ПЛП"],
                                    f"{os.environ['XL_IDP_PATH_NW_IMPORT']}/flat_import_nw_tracking_update")
        self.write_rows_by_terminal(df, "cabotage", ["ВСК"], None)
        self.write_rows_by_terminal(df, list(DIRECTIONS.keys())[1], ["НУТЭП"],
                                    f"{os.environ['XL_IDP_PATH_EXPORT']}/lines_nutep/flat_export_nutep_tracking_update")
        self.write_rows_by_terminal(df, list(DIRECTIONS.keys())[1], ["ВСК"],
                                    f"{os.environ['XL_IDP_PATH_VSK_EXPORT']}/flat_export_vsk_tracking_update")
        self.write_rows_by_terminal(df, list(DIRECTIONS.keys())[1], ["ПКТ", "УЛКТ", "ПЛП"],
                                    f"{os.environ['XL_IDP_PATH_NW_EXPORT']}/flat_export_nw_tracking_update")


if __name__ == "__main__":
    auto_tracking: AutoTracking = AutoTracking(sys.argv[1])
    auto_tracking.main()
