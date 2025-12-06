import pandas as pd

# Handles loading and analyzing a CSV dataset.
class DatasetAnalyzer:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.df = pd.read_csv(filepath)

    # Returns number of rows and columns.
    def shape(self) -> dict:
        rows, cols = self.df.shape
        return {"rows": rows, "columns": cols}

    # Returns a preview of the top rows as plain text.
    def preview(self, n: int = 5) -> str:
        return self.df.head(n).to_string()

    # Returns summary statistics for all columns.
    def summary(self) -> str:
        return self.df.describe(include="all").to_string()

    # Returns missing value counts per column.
    def missing_values(self) -> dict:
        return self.df.isna().sum().to_dict()

    # Returns correlation matrix for numeric columns as text.
    def correlations(self) -> str:
        corr_df = self.df.corr(numeric_only=True)
        return corr_df.to_string()

    # Returns data types of each column.
    def column_types(self) -> dict:
        return self.df.dtypes.astype(str).to_dict()
