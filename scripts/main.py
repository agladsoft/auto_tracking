import os
import sys
import pandas as pd
from typing import Tuple
from pandas import DataFrame
from pandas.core.groupby import DataFrameGroupBy


class AutoTracking(object):
    def __init__(self, input_file_path: str):
        self.input_file_path: str = input_file_path

    @staticmethod
    def write_rows_by_terminal(df: DataFrame, direction: str, terminals: list, path: str) -> None:
        """
        We group by 'enforce_auto_tracking', 'year', 'month' and write it to a separate xlsx file.
        :param df: DataFrame.
        :param direction: Value of direction.
        :param terminals: List of value of terminal.
        :param path: The path of the folder to save.
        :return:
        """
        if not os.path.exists(path):
            os.mkdir(path)
        for terminal in terminals:
            df: DataFrame = df.loc[(df['terminal'] == terminal) & (df['direction'] == direction)]
            group_columns: DataFrameGroupBy = df.groupby(['enforce_auto_tracking', 'original_file_name'])
            column: Tuple[Tuple, DataFrame]
            for column in group_columns:
                if not column[0][0]:
                    column[1]['is_auto_tracking'] = False
                    column[1]['is_auto_tracking_ok'] = None
                column[1].to_excel(f"{path}/{column[0][1].replace('.csv', '')}", engine="xlsxwriter", index=False)

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
        self.write_rows_by_terminal(df, "import", ["НУТЭП"],
                                    f"{os.environ['XL_IDP_PATH_IMPORT']}/lines_nutep/flat_import_nutep_tracking_update")
        self.write_rows_by_terminal(df, "import", ["ВСК"],
                                    f"{os.environ['XL_IDP_PATH_VSK_IMPORT']}/flat_import_vsk_tracking_update")
        self.write_rows_by_terminal(df, "export", ["НУТЭП"],
                                    f"{os.environ['XL_IDP_PATH_EXPORT']}/lines_nutep/flat_export_nutep_tracking_update")
        self.write_rows_by_terminal(df, "export", ["ВСК"],
                                    f"{os.environ['XL_IDP_PATH_VSK_EXPORT']}/flat_export_vsk_tracking_update")
        self.write_rows_by_terminal(df, "export", ["ПКТ", "УЛКТ", "ПЛП"],
                                    f"{os.environ['XL_IDP_PATH_NW_EXPORT']}/flat_export_nw_tracking_update")


if __name__ == "__main__":
    auto_tracking: AutoTracking = AutoTracking(sys.argv[1])
    auto_tracking.main()
