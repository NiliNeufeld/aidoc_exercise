import pandas as pd
import json

SINGLE_GROUPBY_PARAMETER = {
        "patient": "patientId",
        "algorithm": "algorithmType",
        "hospital": "hospital",
        "bodyPart": "bodyPart"
}

TWO_GROUPBY_PARAMETERS = {
        "patientInSameDay": ["patientId", "date"],
        "hospitalDepartment": ["hospital", "bodyPart"]
}


class Group:
    def __init__(self, group_by_parameters, scans):
        self.group = group_by_parameters
        self.scans = scans


def group_by_patient_in_same_day(category, df):
    group_key1 = TWO_GROUPBY_PARAMETERS.get(category)[0]
    group_values = df[group_key1].unique()
    df["date_type"] = pd.to_datetime(df["date"])
    dayValues = df["date_type"].dt.date.unique()
    output = []
    for value in group_values:
        for day in dayValues:
            value_df = df.loc[(df[group_key1] == value) & (df["date_type"].dt.date == day)]
            if len(list(value_df.index.values)) == 0:
                continue
            value_df = value_df.drop([group_key1, "date_type"], axis=1)
            value_df = value_df.to_dict("records")
            group = Group({group_key1: value, TWO_GROUPBY_PARAMETERS.get(category)[1]: day}, value_df)
            output.append(group)
    json_string = json.dumps([group.__dict__ for group in output], default=str)
    return json_string


def group_by_2_parameters(category, df):
    group_key1 = TWO_GROUPBY_PARAMETERS.get(category)[0]
    group_key2 = TWO_GROUPBY_PARAMETERS.get(category)[1]
    group_values1 = df[group_key1].unique()
    group_values2 = df[group_key2].unique()
    output = []
    for value1 in group_values1:
        for value2 in group_values2:
            value_df = df.loc[(df[group_key1] == value1) & (df[group_key2] == value2)]
            if len(list(value_df.index.values)) == 0:
                continue
            value_df = value_df.drop([group_key1, group_key2], axis=1)
            value_df = value_df.to_dict("records")
            group = Group({group_key1: value1, group_key2: value2}, value_df)
            output.append(group)
    json_string = json.dumps([group.__dict__ for group in output])
    return json_string


def group_by_1_parameter(category, df):
    group_key = SINGLE_GROUPBY_PARAMETER.get(category)
    group_key_values = df[group_key].unique()
    output = []
    for value in group_key_values:
        value_df = df.loc[df[group_key] == value]
        value_df = value_df.drop(group_key, axis=1)
        value_df = value_df.to_dict("records")
        group = Group({group_key: value}, value_df)
        output.append(group)
    json_string = json.dumps([group.__dict__ for group in output])
    return json_string


def group_by(category, data):
    df = pd.DataFrame(data)
    if category == "patientInSameDay":
        output = group_by_patient_in_same_day(category, df)
    elif category in SINGLE_GROUPBY_PARAMETER.keys():
        output = group_by_1_parameter(category, df)
    elif category in TWO_GROUPBY_PARAMETERS.keys():
        output = group_by_2_parameters(category, df)
    else:
        return "please enter a valid group-by parameter"

    return output
