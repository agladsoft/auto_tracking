import os
import sys
import pandas as pd
from typing import Optional
from pandas import DataFrame
from pandas.core.groupby import DataFrameGroupBy


class AutoTracking:
    def __init__(self, input_file_path: str):
        self.input_file_path: str = input_file_path
        # Keys is direction, values is direction in data file and path of directories. Terminal is None.
        self.directions_cabotage: dict = {
            "import": ["ИМПОРТ", f"{os.environ['XL_IDP_PATH_VSK_IMPORT']}/flat_import_vsk_tracking_update"],
            "export": ["ЭКСПОРТ", f"{os.environ['XL_IDP_PATH_VSK_EXPORT']}/flat_export_vsk_tracking_update"]
        }

    @staticmethod
    def save_to_excel(group_columns: DataFrameGroupBy, path: Optional[str]) -> None:
        """
        Save grouped DataFrame to Excel files in the specified directory.

        :param group_columns: The grouped DataFrame by original file name.
        :param path: The directory path where the Excel files will be saved.  If None, no files will be saved.
        :return: None
        """
        if path:
            os.makedirs(path, exist_ok=True)
            filename: str
            for filename, df in group_columns:
                df.to_excel(f"{path}/{filename.replace('.csv', '').replace('.XLSX', '.xlsx')}", index=False)

    def write_cabotage(self, group_columns: DataFrameGroupBy) -> None:
        """
        Write grouped DataFrame to Excel files in the specified directory, depending on the direction in the file name.

        :param group_columns: The grouped DataFrame by original file name.
        :return: None
        """
        directions: dict = {d[0]: d[1] for d in self.directions_cabotage.values()}
        filtered_groups: dict = {
            d: group_columns.filter(lambda x: x['original_file_name'].str.contains(d, case=False).all())
            for d in directions
        }
        if not directions:
            raise AssertionError("В наименовании файла не указано направление для каботажа")

        for direction, column in filtered_groups.items():
            if column.empty:
                continue
            column[['is_auto_tracking', 'is_auto_tracking_ok']] = [False, None]
            self.save_to_excel(column.groupby(['original_file_name']), directions[direction])

    def write_rows_by_terminal(self, df: DataFrame, direction: str, terminals: list, path: Optional[str]) -> None:
        """
        Write grouped DataFrame to Excel files in the specified directory, depending on the direction in the file name
        and terminal in the DataFrame.

        :param df: The DataFrame to filter and save.
        :param direction: The direction in the file name.
        :param terminals: The list of terminals to filter the DataFrame.
        :param path: The directory path where the Excel files will be saved.  If None, no files will be saved.
        :return: None
        """
        df_filtered: pd.DataFrame = df[df['terminal'].isin(terminals) & (df['direction'] == direction)]
        if df_filtered.empty:
            return

        group_columns: DataFrameGroupBy = df_filtered.groupby(['original_file_name'])
        if direction == "cabotage":
            self.write_cabotage(group_columns)
        else:
            self.save_to_excel(group_columns, path)

    @staticmethod
    def change_types_in_columns(df: DataFrame) -> None:
        """
        Change type of columns to bool.

        :param df: The DataFrame to change column types of.
        :return: None
        """
        for col in ["enforce_auto_tracking", "is_auto_tracking", "is_auto_tracking_ok"]:
            df[col] = df[col].astype(bool)

    def main(self) -> None:
        """
        Read an Excel file, change types of columns to bool, and write each terminal to its own Excel file.

        :return: None
        """
        df: pd.DataFrame = pd.read_excel(self.input_file_path)  # type: ignore
        self.change_types_in_columns(df)

        # Keys is direction, values is (keys is terminals and values is path of directories)
        paths: dict = {
            "import": {
                "НУТЭП": f"{os.environ['XL_IDP_PATH_IMPORT']}/lines_nutep/flat_import_nutep_tracking_update",
                "ВСК": f"{os.environ['XL_IDP_PATH_VSK_IMPORT']}/flat_import_vsk_tracking_update",
                "ПКТ,УЛКТ,ПЛП": f"{os.environ['XL_IDP_PATH_NW_IMPORT']}/flat_import_nw_tracking_update"
            },
            "export": {
                "НУТЭП": f"{os.environ['XL_IDP_PATH_EXPORT']}/lines_nutep/flat_export_nutep_tracking_update",
                "ВСК": f"{os.environ['XL_IDP_PATH_VSK_EXPORT']}/flat_export_vsk_tracking_update",
                "ПКТ,УЛКТ,ПЛП": f"{os.environ['XL_IDP_PATH_NW_EXPORT']}/flat_export_nw_tracking_update"
            },
            "cabotage": {
                "ВСК": None
            }
        }

        for direction, terminals in paths.items():
            for terminal, path in terminals.items():
                self.write_rows_by_terminal(df, direction, terminal.split(','), path)

if __name__ == "__main__":
    AutoTracking(sys.argv[1]).main()
