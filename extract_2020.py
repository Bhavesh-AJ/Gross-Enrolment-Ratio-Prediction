import pandas as pd

from extract_utils import clean_state_column


def get_2020_data(file):
    # GER: first "Total" column is All Categories total GER.
    df_ger = pd.read_excel(file, sheet_name="19GER(2011)", skiprows=2)
    df_ger = df_ger.rename(columns={
        df_ger.columns[1]: "state",
        "Total": "ger",
    })
    df_ger = clean_state_column(df_ger[["state", "ger"]])
    df_ger["ger"] = pd.to_numeric(df_ger["ger"], errors="coerce")
    df_ger = df_ger.dropna()

    df_students = pd.read_excel(file, sheet_name="6TotalEnr", skiprows=4, header=None)
    df_students = df_students.rename(columns={1: "state", 28: "students"})
    df_students = clean_state_column(df_students[["state", "students"]])
    df_students["students"] = pd.to_numeric(df_students["students"], errors="coerce")
    df_students = df_students.dropna()

    df_uni = pd.read_excel(file, sheet_name="40NoUni", skiprows=4, header=None)
    df_uni = df_uni.rename(columns={1: "state", df_uni.columns[-1]: "universities"})
    df_uni = clean_state_column(df_uni[["state", "universities"]])
    df_uni["universities"] = pd.to_numeric(df_uni["universities"], errors="coerce")
    df_uni = df_uni.dropna()

    df_fac = pd.read_excel(file, sheet_name="22TeacherPost", skiprows=4, header=None)
    df_fac = df_fac.rename(columns={1: "state", 22: "faculty"})
    df_fac = clean_state_column(df_fac[["state", "faculty"]])
    df_fac["faculty"] = pd.to_numeric(df_fac["faculty"], errors="coerce")
    df_fac = df_fac.dropna()

    df_pop = pd.read_excel(file, sheet_name="38Pop2020(2011)", skiprows=4, header=None)
    df_pop = df_pop.rename(columns={1: "state", 4: "population_18_23"})
    df_pop = clean_state_column(df_pop[["state", "population_18_23"]])
    df_pop["population_18_23"] = pd.to_numeric(df_pop["population_18_23"], errors="coerce")
    df_pop = df_pop.dropna()

    df = df_ger.merge(df_students, on="state") \
               .merge(df_uni, on="state") \
               .merge(df_fac, on="state") \
               .merge(df_pop, on="state")
    df["year"] = 2020
    return df
