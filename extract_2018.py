import pandas as pd

from extract_utils import clean_state_column


def _state_value(file, sheet_name, state_col, value_col, skiprows=0):
    df = pd.read_excel(file, sheet_name=sheet_name, skiprows=skiprows, header=None)
    df = df.rename(columns={state_col: "state", value_col: "value"})
    df = clean_state_column(df[["state", "value"]])
    df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0)
    return df


def get_2018_data(file):
    df_uni = _state_value(file, "Table001 (Page 1)", 1, 13)
    df_uni = df_uni.rename(columns={"value": "universities"})

    # 2018 total enrolment is split across university, college, and stand-alone institution tables.
    uni_students = _state_value(file, "Table104 (Page 120)", 1, 13, skiprows=3)
    college_students = _state_value(file, "Table027 (Page 27)", 1, 10)
    standalone_students = _state_value(file, "Table031 (Page 31)", 1, 12)

    df_students = uni_students.merge(
        college_students, on="state", how="outer", suffixes=("_uni", "_college")
    ).merge(
        standalone_students, on="state", how="outer"
    )
    df_students = df_students.rename(columns={"value": "value_standalone"}).fillna(0)
    df_students["students"] = (
        df_students["value_uni"] + df_students["value_college"] + df_students["value_standalone"]
    )
    df_students = df_students[["state", "students"]]

    df_fac = _state_value(file, "Table071 (Page 79)", 1, 7)
    df_fac = df_fac.rename(columns={"value": "faculty"})

    df_pop = _state_value(file, "Table101 (Page 117)", 1, 4)
    df_pop = df_pop.rename(columns={"value": "population_18_23"})

    df = df_students.merge(df_uni, on="state") \
                    .merge(df_fac, on="state") \
                    .merge(df_pop, on="state")

    # GER is defined as enrolment divided by 18-23 population, multiplied by 100.
    df["ger"] = (df["students"] / df["population_18_23"]) * 100
    df["year"] = 2018
    return df[["state", "ger", "students", "universities", "faculty", "population_18_23", "year"]]
