import json
from app import app

# def test_get_root_dir():
#     response = app.test_client().get('/')
#     res = response.data.decode('utf-8')
#     assert type(res) is str
#     assert res == 'test'
#     assert response.status_code == 200

#testing the output for optinal parameters of groupby
def test_get_groupby_output():
    groupByParameters = {"patient":"patientId","algorithm":"algorithmType","hospital":"hospital",
                         "bodyPart":"bodyPart","patientInSameDay":"","hospitalDepartment":""}
    for par in groupByParameters:
        url = "/GetScans?groupby="+par
        response = app.test_client().get(url)
        res = json.loads(response.data.decode('utf-8'))
        assert type(res) is list
        for item in res:
            assert type(item) is dict
            if par == "patientInSameDay":
                assert list(item.keys())[0] == "patientId"
                assert list(item.keys())[1] == "date"
            elif par == "hospitalDepartment":
                assert list(item.keys())[0] == "hospital"
                assert list(item.keys())[1] == "bodyPart"
            else:
                assert list(item.keys())[0] == groupByParameters.get(par)
            details = item.get("details")
            assert type(details) is list
            for subItem in details:
                assert type(subItem) is dict

    assert response.status_code == 200

#testing the output for wrong/no parameters of groupby
def test_groupby_with_wrong_parameter():
    urls= ["/GetScans?groupby=somethingelse", "/GetScans"]
    for url in urls:
        response = app.test_client().get(url)
        res = response.data.decode('utf-8')
        assert type(res) is str
        assert res == 'please enter a valid groupby parameter'
        assert response.status_code == 200


# def test_groupby_with_no_parameter():
#     url =
#     response = app.test_client().get(url)
#     res = response.data.decode('utf-8')
#     assert type(res) is str
#     assert res == 'please enter a valid groupby parameter'
#     assert response.status_code == 200

