import json
import pandas as pd
from app import app
import groupbyFunctions

def test_get_groupby_output():
    groupByParameters = {
        "patient":"patientId",
        "algorithm":"algorithmType",
        "hospital":"hospital",
        "bodyPart":"bodyPart",
        "patientInSameDay":"",
        "hospitalDepartment":""}
    for par in groupByParameters:
        url = "/get_scans?groupby="+par
        response = app.test_client().get(url)
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is list
        for item in res:
            assert type(item) is dict
            # if par == "patientInSameDay":
            #     assert list(item.keys())[0] == "patientId"
            #     assert list(item.keys())[1] == "date"
            # elif par == "hospitalDepartment":
            #     assert list(item.keys())[0] == "hospital"
            #     assert list(item.keys())[1] == "bodyPart"
            # else:
            #     assert list(item.keys())[0] == groupByParameters.get(par)
            scans = item.get("scans")
            assert type(scans) is list
            for subItem in scans:
                assert type(subItem) is dict

    assert response.status_code == 200


def test_groupby_with_wrong_parameter():
    urls= ["/get_scans?groupby=somethingelse", "/get_scans"]
    for url in urls:
        response = app.test_client().get(url)
        res = response.data.decode('utf-8')
        assert type(res) is str
        assert res == 'please enter a valid group-by parameter'
        assert response.status_code == 200


def test_1_parmeter_groupby():
    f = open('mock_aidoc_scans.json')
    df = pd.DataFrame(f)
    assert type(res) is list
    for item in res:
        assert type(item) is dict
        # if par == "patientInSameDay":
        #     assert list(item.keys())[0] == "patientId"
        #     assert list(item.keys())[1] == "date"
        # elif par == "hospitalDepartment":
        #     assert list(item.keys())[0] == "hospital"
        #     assert list(item.keys())[1] == "bodyPart"
        # else:
        #     assert list(item.keys())[0] == groupByParameters.get(par)
        scans = item.get("scans")
        assert type(scans) is list
        for subItem in scans:
            assert type(subItem) is dict