from flask import Flask
import requests
from flask import request
from groupbyFunctions import group_by
import json
from requests.exceptions import HTTPError
import time


class Client:
    url = "http://localhost:3000/scans"

    # def get_scans1(self):
    #     try:
    #         aidocServerRes = requests.get(self.URL, headers={"username": "aidoc_user"})
    #     except requests.exceptions.ConnectionError:
    #         return "couldn't connect to aidoc server", 404
    #     # review: what if we wanted to add another error code?
    #     # if type(aidocServerRes) is requests.models.Response:
    #     #     print(type(aidocServerRes))
    #     print(aidocServerRes.raise_for_status())
    #     return json.loads(aidocServerRes.text)
    #     # else:  # TODO: handle other exceptions
    #     # return "authentication changed in aidoc server", 401
    #     # if aidocServerRes.status_code == 401:
    #     #     return "authentication changed in aidoc server", 401

    def get_scans(self):
        retries = 3
        for n in range(retries):
            try:
                aidocServerRes = requests.get(self.url, headers={"username": "aidoc_user"})
                aidocServerRes.raise_for_status()
                break

            except HTTPError as exc:
                code = exc.response.status_code

                if code in [404, 502, 503, 504]:
                    time.sleep(n)
                    continue
                elif code in [401]:
                    return code
                raise
        # if aidocServerRes.raise_for_status() is None:
        return json.loads(aidocServerRes.text)


app = Flask(__name__)


# @app.route("/")
# def index():
#     return "test"


@app.route("/get_scans")
def get_scans():
    client = Client()
    json_data = client.get_scans()
    if isinstance(json_data, int):
        return "status code:"+str(json_data)
    elif not json_data:
        return "no scans data was sent from aidoc server"
    else:
        groupbyCategory = request.args.get("groupby")
        scans = group_by(groupbyCategory, json_data)
        return scans


if __name__ == "__main__":
    app.run(debug=True)
