import json
import pandas as pd
from app import app
from groupby import group_by, GROUP_BY_PARAMETERS
import os

GROUP_BY_1_PARAMETER = {
        "patient": ["patientId"],
        "algorithm": ["algorithmType"],
        "hospital": ["hospital"],
        "bodyPart": ["bodyPart"],
        "scanId": ["scanId"]
}

GROUP_BY_MULTIPLE_PARAMETERS = {
        "patientInSameDay": ["patientId", "day"],
        "hospitalDepartment": ["hospital", "bodyPart"],
        "algoBodypartPositive": ["algorithmType", "bodyPart", "isPositive"]
}

DATA = [
        {
            "scanId": 1,
            "patientId": "0a72267e-3e54-4ea3-b033-dd39911be0c9",
            "algorithmType": "ICH",
            "status": "new",
            "isPositive": None,
            "date": "2022-07-10T10:07:54.747Z",
            "hospital": "Sheba",
            "bodyPart": "Brain"
        },
        {
            "scanId": 2,
            "patientId": "0a72267e-3e54-4ea3-b033-dd39911be0c9",
            "algorithmType": "CTP",
            "status": "in progress",
            "isPositive": None,
            "date": "2022-07-10T10:07:52.885Z",
            "hospital": "Mayo",
            "bodyPart": "Brain"
        },
        {
            "scanId": 3,
            "patientId": "0a72267e-3e54-4ea3-b033-dd39911be0c9",
            "algorithmType": "RVLV",
            "status": "new",
            "isPositive": False,
            "date": "2022-07-11T10:07:55.995Z",
            "hospital": "Sheba",
            "bodyPart": "Heart"
        },
        {
            "scanId": 4,
            "patientId": "c4dedcd8-86de-4572-84ba-ff56987dd5b8",
            "algorithmType": "RVLV",
            "status": "done",
            "isPositive": False,
            "date": "2022-07-11T10:07:56.130Z",
            "hospital": "Yale",
            "bodyPart": "Heart"
        },
        {
            "scanId": 5,
            "patientId": "45e602c5-e89a-46ec-8b1b-31cf1faa0b1c",
            "algorithmType": "ICH",
            "status": "done",
            "isPositive": True,
            "date": "2022-07-12T10:07:54.744Z",
            "hospital": "Ichilov",
            "bodyPart": "Brain"
        }
    ]

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


# def test_api_groupby_with_wrong_parameter():
#     urls= ["/get_scans?groupby=somethingelse", "/get_scans"]
#     for url in urls:
#         response = app.test_client().get(url)
#         res = response.data.decode('utf-8')
#         assert type(res) is str
#         assert res == "please enter a valid group-by parameter"
#         assert response.status_code == 200

def test_groupby_with_wrong_parameter():
    categories= ["wrong", None]
    data = []
    for category in categories:
        res = group_by(category, data)
        assert type(res) is str
        assert res == "please enter a valid group-by parameter"


def test_1_parameter_groupby_format():
    for category in GROUP_BY_1_PARAMETER.keys():
        groupby_res = group_by(category, DATA)
        groupby_res = json.loads(groupby_res)
        assert type(groupby_res) is list
        for item in groupby_res:
            assert type(item) is dict
            group = item.get("group")
            assert type(group) is dict
            assert len(group.keys()) == 1
            groupby_parameters = list(group.keys())
            assert groupby_parameters[0] == GROUP_BY_1_PARAMETER.get(category)[0]
            scans = item.get("scans")
            assert type(scans) is list
            for subItem in scans:
                assert type(subItem) is dict


def test_2_parmeters_groupby_format():
    for category in GROUP_BY_MULTIPLE_PARAMETERS.keys():
        groupby_res = group_by(category, DATA)
        print("Multi param:", category)
        print(groupby_res)
        groupby_res = json.loads(groupby_res)
        assert type(groupby_res) is list
        for item in groupby_res:
            assert type(item) is dict
            group = item.get("group")
            assert type(group) is dict
            assert len(group.keys()) == len(GROUP_BY_MULTIPLE_PARAMETERS.get(category))
            groupby_parameters = list(group.keys())
            for i in range(len(groupby_parameters)):
                assert groupby_parameters[i] == GROUP_BY_MULTIPLE_PARAMETERS.get(category)[i]
            scans = item.get("scans")
            assert type(scans) is list
            for subItem in scans:
                assert type(subItem) is dict


def test_1_parameter_groupby_logic():
    category = "algorithm"
    groupby_res = group_by(category, DATA)
    groupby_res = json.loads(groupby_res)
    expected_res = {"CTP": 1, "ICH": 2, "RVLV": 2}
    for item in groupby_res:
        group = item.get("group")
        groupby_parameters = list(group.keys())
        assert groupby_parameters[0] == GROUP_BY_1_PARAMETER.get(category)[0]
        value = group.get("algorithmType")
        scans = item.get("scans")
        assert len(scans) == expected_res.get(value)


def test_multi_parameters_groupby_logic():
    category = "patientInSameDay"
    groupby_res = group_by(category, DATA)
    groupby_res = json.loads(groupby_res)
    expected_res = {("0a72267e-3e54-4ea3-b033-dd39911be0c9", "2022-07-10"): 2,
                     ("0a72267e-3e54-4ea3-b033-dd39911be0c9", "2022-07-11"): 1,
                     ("c4dedcd8-86de-4572-84ba-ff56987dd5b8", "2022-07-11"): 1,
                     ("45e602c5-e89a-46ec-8b1b-31cf1faa0b1c", "2022-07-12"): 1}
    for item in groupby_res:
        group = item.get("group")
        groupby_parameters = list(group.keys())
        pidvalue = group.get(GROUP_BY_MULTIPLE_PARAMETERS.get(category)[0])
        datevalue = group.get(GROUP_BY_MULTIPLE_PARAMETERS.get(category)[1])
        assert groupby_parameters[0] == GROUP_BY_MULTIPLE_PARAMETERS.get(category)[0]
        assert groupby_parameters[1] == GROUP_BY_MULTIPLE_PARAMETERS.get(category)[1]
        scans = item.get("scans")
        assert len(scans) == expected_res.get((pidvalue, datevalue))