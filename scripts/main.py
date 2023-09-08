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
    def write_rows_by_terminal(df: DataFrame, value: str, path: str) -> None:
        """
        We group by 'enforce_auto_tracking', 'year', 'month' and write it to a separate xlsx file.
        :param df: DataFrame.
        :param value: Value of terminal.
        :param path: The path of the folder to save.
        :return:
        """
        df: DataFrame = df.loc[df['terminal'] == value]
        group_columns: DataFrameGroupBy = df.groupby(['enforce_auto_tracking', 'year', 'month'])
        column: Tuple[Tuple, DataFrame]
        for column in group_columns:
            if not column[0][0]:
                column[1]['is_auto_tracking'] = False
                column[1]['is_auto_tracking'] = None
            column[1].to_excel(f"{path}/{column[0][1]}.{column[0][2]:02d} auto_tracking.xlsx", index=False)

    def main(self) -> None:
        """
        The main function where we read the Excel file and write the file to json.
        :return:
        """
        df: DataFrame = pd.read_excel(self.input_file_path)
        self.write_rows_by_terminal(df, "НУТЭП", f"{os.environ['XL_IDP_PATH_IMPORT']}/"
                                                 f"lines_nutep/flat_import_nutep_tracking_update")
        self.write_rows_by_terminal(df, "ВСК", f"{os.environ['XL_IDP_PATH_VSK_IMPORT']}/"
                                               f"flat_import_vsk_tracking_update")


if __name__ == "__main__":
    auto_tracking: AutoTracking = AutoTracking(sys.argv[1])
    auto_tracking.main()
