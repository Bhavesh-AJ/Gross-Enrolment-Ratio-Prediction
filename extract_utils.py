import re


STATE_ALIASES = {
    "A & N Islands": "Andaman and Nicobar Islands",
    "Andaman & Nicobar Islands": "Andaman and Nicobar Islands",
    "Chhatisgarh": "Chhattisgarh",
    "Jammu & Kashmir": "Jammu and Kashmir",
}


def clean_state(value):
    value = str(value).replace("\n", " ").strip()
    value = re.sub(r"\s+", " ", value)
    return STATE_ALIASES.get(value, value)


def clean_state_column(df, column="state"):
    df = df[df[column].notna()].copy()
    df[column] = df[column].map(clean_state)
    df = df[df[column].str.contains("[A-Za-z]", regex=True, na=False)]
    df = df[~df[column].str.fullmatch(r"\d+", na=False)]
    df = df[~df[column].str.contains("India", case=False, na=False)]
    return df
