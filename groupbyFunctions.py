import pandas as pd


# I built the json with a string and not a list dictionaries because I remembered dictonaries are unordered,
# but now I see this changed since 3.7


# Group scans of same patient in same date
# review: can we make it more generic?
def GroupbyPatientInSameDay(df):
    patientValues = df["patientId"].unique()
    df["datetype"] = pd.to_datetime(df["date"])
    dayValues = df["datetype"].dt.date.unique()
    output = "["
    for pid in patientValues:
        for (
            day
        ) in (
            dayValues
        ):  # shouldn't present patient with dates they didn't have any scans in (also in previous function)
            value_df = df.loc[
                (df["patientId"] == pid) & (df["datetype"].dt.date == day)
            ]
            if len(list(value_df.index.values)) == 0:
                continue
            output = output + '{{"patientId":"{}","date":"{}","details":'.format(
                pid, day
            )
            value_df = value_df.drop(["patientId", "datetype"], axis=1)
            valuejsonString = value_df.to_json(orient="records")
            output = output + valuejsonString + "},"
    return output


# Group scans with same hospital and department
# review: can we make it more generic?
def GroupbyHospitalDepartment(df):
    hospitalValues = df["hospital"].unique()
    bodyPartValues = df["bodyPart"].unique()
    output = "["
    # review: full variable name "hospital"
    for hos in hospitalValues:
        for bod in bodyPartValues:
            output = output + '{{"hospital":"{}","bodyPart":"{}","details":'.format(
                hos, bod
            )
            value_df = df.loc[(df["hospital"] == hos) & (df["bodyPart"] == bod)]
            if len(list(value_df.index.values)) == 0:
                continue
            value_df = value_df.drop(["hospital", "bodyPart"], axis=1)
            valuejsonString = value_df.to_json(orient="records")
            output = output + valuejsonString + "},"
    return output


# Group scans with same patient/algorithm/hospital/bodyPart
def GroupbyOthers(category, df):
    # review: what if wanted to add more mappings?
    if category == "patient":
        category = "patientId"
    elif category == "algorithm":
        category = "algorithmType"
    catValues = df[category].unique()
    output = "["
    for value in catValues:
        output = output + '{"' + category + '":"' + value + '","details":'
        value_df = df.loc[df[category] == value]
        value_df = value_df.drop(category, axis=1)
        valuejsonString = value_df.to_json(orient="records")
        output = output + valuejsonString + "},"
    return output


# group scans by given category
def groupBy(category, data):
    df = pd.DataFrame(data)
    # review: duplicate definition of allowed categories
    if category not in [
        "patient",
        "algorithm",
        "hospital",
        "bodyPart",
        "patientInSameDay",
        "hospitalDepartment",
    ]:
        return "please enter a valid groupby parameter"
    # review: what if we want to add another class of groupings?
    # review: I think the ifs logic should be reordered
    if category in ["patient", "algorithm", "hospital", "bodyPart"]:
        output = GroupbyOthers(category, df)
    elif category == "hospitalDepartment":
        output = GroupbyHospitalDepartment(df)
    else:
        output = GroupbyPatientInSameDay(df)

    output = output[:-2] + "}]"
    # jsonFile = open("scansGrouped.json", "w")
    # jsonFile.write(output)
    # jsonFile.close()
    return output
