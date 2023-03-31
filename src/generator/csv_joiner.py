import pandas as pd
import numpy as np


# join a list of csv files
def join_csv(files: list, output: str) -> None:
    """
    Join a list of csv files into one csv file.

    Args:
        files (list): A list of csv files.
        output (str): The name of the output file.
    """
    df = pd.DataFrame()
    for file in files:
        df = df.append(pd.read_csv(file, sep=";"))
    df = df.drop_duplicates()
    
    df = df.astype(int)
    # Save to csv as int
    df.to_csv(output, sep=";", index=False)


if __name__ == "__main__":
    files = ["src/train_data/all_edges_5_10_4_4step.csv", "src/train_data/all_edges_5_10_4_8step.csv",
             "src/train_data/all_edges_5_10_4_10step.csv", "src/train_data/all_edges_5_10_4_13step.csv"]
    join_csv(files, "src/train_data/all_edges_5_10_4step.csv")
