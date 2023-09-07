import os
import sys
import pandas as pd
from pandas import DataFrame


class AutoTracking(object):
    def __init__(self, input_file_path: str):
        self.input_file_path: str = input_file_path

    @staticmethod
    def write_rows_by_terminal(df: DataFrame, value: str, path: str) -> None:
        df: DataFrame = df.loc[df['terminal'] == value]
        year_distribution = df.groupby('year')
        monthly_distribution = df.groupby('month')
        for year in year_distribution:
            for month in monthly_distribution:
                month[1].to_excel(f"{path}/{year[0]}.{month[0]:02d} auto_tracking.xlsx", index=False)

    def main(self) -> None:
        """
        The main function where we read the Excel file and write the file to json.
        """
        df: DataFrame = pd.read_excel(self.input_file_path)
        self.write_rows_by_terminal(df, "НУТЭП", f"{os.environ['XL_IDP_PATH_IMPORT']}/lines_nutep/flat_import_nutep")
        self.write_rows_by_terminal(df, "ВСК", f"{os.environ['XL_IDP_PATH_VSK_IMPORT']}/flat_import_vsk")


if __name__ == "__main__":
    auto_tracking: AutoTracking = AutoTracking(sys.argv[1])
    auto_tracking.main()
