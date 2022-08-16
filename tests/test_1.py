import json
import pandas as pd
from app import app
from groupbyFunctions import group_by, group_by_1_parameter, group_by_2_parameters, SINGLE_GROUPBY_PARAMETER, TWO_GROUPBY_PARAMETERS
import os

# def test_get_groupby_output():
#     groupByParameters = {
#         "patient":"patientId",
#         "algorithm":"algorithmType",
#         "hospital":"hospital",
#         "bodyPart":"bodyPart",
#         "patientInSameDay":"",
#         "hospitalDepartment":""}
#     for par in groupByParameters:
#         url = "/get_scans?groupby="+par
#         response = app.test_client().get(url)
#         res = json.loads(response.data.decode('utf-8'))
#         assert type(res) is list
#         for item in res:
#             assert type(item) is dict
#             # if par == "patientInSameDay":
#             #     assert list(item.keys())[0] == "patientId"
#             #     assert list(item.keys())[1] == "date"
#             # elif par == "hospitalDepartment":
#             #     assert list(item.keys())[0] == "hospital"
#             #     assert list(item.keys())[1] == "bodyPart"
#             # else:
#             #     assert list(item.keys())[0] == groupByParameters.get(par)
#             scans = item.get("scans")
#             assert type(scans) is list
#             for subItem in scans:
#                 assert type(subItem) is dict
#
#     assert response.status_code == 200


def test_groupby_with_wrong_parameter():
    urls= ["/get_scans?groupby=somethingelse", "/get_scans"]
    for url in urls:
        response = app.test_client().get(url)
        res = response.data.decode('utf-8')
        assert type(res) is str
        assert res == "please enter a valid group-by parameter"
        assert response.status_code == 200


def test_1_parmeter_groupby():
    f = open("mock_aidoc_scans.json", "r")
    jsonStr = f.read()
    df = pd.DataFrame(json.loads(jsonStr))
    for category in SINGLE_GROUPBY_PARAMETER.keys():
        groupby_res = group_by_1_parameter(category, df)
        groupby_res = json.loads(groupby_res)
        assert type(groupby_res) is list
        for item in groupby_res:
            assert type(item) is dict
            group = item.get("group")
            assert type(group) is dict
            groupby_parameters = list(group.keys())
            assert groupby_parameters[0] == SINGLE_GROUPBY_PARAMETER.get(category)
            scans = item.get("scans")
            assert type(scans) is list
            for subItem in scans:
                assert type(subItem) is dict


def test_2_parmeter_groupby():
    f = open("mock_aidoc_scans.json", "r")
    jsonStr = f.read()
    df = pd.DataFrame(json.loads(jsonStr))
    for category in TWO_GROUPBY_PARAMETERS.keys():
        groupby_res = group_by_2_parameters(category, df)
        groupby_res = json.loads(groupby_res)
        assert type(groupby_res) is list
        for item in groupby_res:
            assert type(item) is dict
            group = item.get("group")
            assert type(group) is dict
            groupby_parameters = list(group.keys())
            assert groupby_parameters[0] == TWO_GROUPBY_PARAMETERS.get(category)[0]
            assert groupby_parameters[1] == TWO_GROUPBY_PARAMETERS.get(category)[1]
            scans = item.get("scans")
            assert type(scans) is list
            for subItem in scans:
                assert type(subItem) is dict