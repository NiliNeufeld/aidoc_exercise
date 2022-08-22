import pandas as pd
import json

GROUP_BY_PARAMETERS = {
    "patient": ["patientId"],
    "algorithm": ["algorithmType"],
    "hospital": ["hospital"],
    "bodyPart": ["bodyPart"],
    "scanId": ["scanId"],
    "isPositive": ["isPositive"],
    "date": ["date"],
    "patientInSameDay": ["patientId", "day"],
    "hospitalDepartment": ["hospital", "bodyPart"],
    "algoPositive": ["algorithmType", "isPositive"],
    "algoBodypartPositive": ["algorithmType", "bodyPart", "isPositive"]
}


class Group:
    def __init__(self, category, value, scans):

        group_by_parameters = {}
        keys = GROUP_BY_PARAMETERS.get(category)
        for k, v in zip(keys, value.split("_")):
            if k == "scanId":
                v = int(v)
            group_by_parameters[k] = v
        self.group = group_by_parameters
        self.scans = scans


# def group_by_all_parameters(category, df):
#     concatenated = "concatenated_group_by_parameters"
#     if category == "patientInSameDay":
#         df["day"] = pd.to_datetime(df["date"]).dt.date
#     df[concatenated] = df[GROUP_BY_PARAMETERS.get(category)].apply(lambda x: '_'.join(str(column) for column in x), axis=1)
#     group_key_values = sorted(df[concatenated].unique())
#     output = []
#     for value in group_key_values:
#         value_df = df.loc[df[concatenated] == value]
#         if not list(value_df.index.values):
#             continue
#         value_df = value_df.drop(GROUP_BY_PARAMETERS.get(category)+[concatenated], axis=1)
#         value_df = value_df.to_dict("records")
#         group = Group(category, value, value_df)
#         output.append(group)
#     json_string = json.dumps([group.__dict__ for group in output], default=str)
#     return json_string


def group_by(category, data):
    if category not in GROUP_BY_PARAMETERS.keys():
        return "please enter a valid group-by parameter"
    else:
        df = pd.DataFrame(data)
        concatenated = "concatenated_group_by_parameters"
        if category == "patientInSameDay":
            df["day"] = pd.to_datetime(df["date"]).dt.date
        df[concatenated] = df[GROUP_BY_PARAMETERS.get(category)].apply(lambda x: '_'.join(str(column) for column in x), axis=1)
        group_key_values = sorted(df[concatenated].unique())
        output = []
        for value in group_key_values:
            value_df = df.loc[df[concatenated] == value]
            if not list(value_df.index.values):
                continue
            value_df = value_df.drop(GROUP_BY_PARAMETERS.get(category)+[concatenated], axis=1)
            value_df = value_df.to_dict("records")
            group = Group(category, value, value_df)
            output.append(group)
        json_string = json.dumps([group.__dict__ for group in output], default=str)
        return json_string
