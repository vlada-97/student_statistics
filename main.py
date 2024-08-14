from typing import Any

from entities import klass

import pandas as pd
import random
import argparse

from logger_config import setup_logger

logger = setup_logger()


def setup_data() -> pd.DataFrame:
    """
    Initializes and returns the DataFrame with random grades and mean calculations.

    :return: DataFrame
    """
    df = pd.DataFrame(klass).melt(var_name="class", value_name="surname")

    subjects = ["math", "ru", "info"]
    for subject in subjects:
        df[subject] = [random.randint(2, 5) for _ in range(len(df))]

    df["mean"] = df[subjects].mean(axis=1)
    df["parallel"] = [9 if i % 2 == 0 else 10 for i in range(len(df))]
    df = df[["parallel", "class", "surname", "math", "ru", "info", "mean"]]

    return df


def classes_top(df, top_n, group_columns) -> tuple[Any, Any]:
    """
    Generates a pivot table and retrieves the top_n students.

    :param df: class DataFrame
    :param top_n: count of top performers
    :param group_columns: group by class | parallel
    :return: tuple[DataFrame | Any]
    """
    logger.info("Generating pivot table and selecting top students.")

    result = df.pivot_table(
        index=group_columns,
        columns="math",
        values="surname",
        aggfunc="count",
        fill_value=0,
    )

    top_students = (
        df.sort_values(by="mean", ascending=False).head(top_n).reset_index(drop=True)
    )

    return result, top_students


def main():
    parser = argparse.ArgumentParser(
        description="Analyze student grades and generate performance metrics."
    )
    parser.add_argument(
        "--top_n", type=int, default=5, help="Number of top students to display."
    )
    parser.add_argument(
        "--group_columns",
        type=str,
        nargs="+",
        default=["parallel", "class"],
        help="Columns to group by in the pivot table.",
    )

    args = parser.parse_args()
    top_n = args.top_n
    group_columns = args.group_columns

    logger.info(f"Top N: {top_n}")
    logger.info(f"Group Columns: {group_columns}")

    df = setup_data()

    result, top_students = classes_top(df, top_n, group_columns)

    logger.info("Displaying results.")
    print(f"\n*** ORIGINAL DATAFRAME ***\n{df}\n")
    print(
        f'\n*** AVERAGE ACADEMIC PERFORMANCE BY {" & ".join(group_columns)} ***\n{result}\n'
    )
    print(f"\n*** TOP {len(top_students)} STUDENTS ***\n{top_students}\n")


if __name__ == "__main__":
    main()
