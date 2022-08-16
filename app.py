from flask import Flask
import requests
from flask import request
from groupbyFunctions import groupBy
import json

#review: I don't like comments in code

# import urllib.request
# import urllib.error
# review: show a running example of the app
app = Flask(__name__)


# @app.route("/")
# def index():
#     return "test"


# review: match function name to route
@app.route("/GetScans")
def request_data():
    groupbyCategory = request.args.get("groupby")
    # request scansdata from aidoc server
    # review: extract to client class
    URL = "http://localhost:3000/scans"
    try:
        aidocServerRes = requests.get(URL, headers={"username": "aidoc_user"})
    except requests.exceptions.ConnectionError:
        return "couldn'n connest to aidoc server", 404

    # review: what's this else? where's the if?
    # review: what if we wanted to add another error code?
    if aidocServerRes.status_code == 401:
        return "authentication changed in aidoc server", 401
    else:  # execute groupby
        json_data = json.loads(aidocServerRes.text)
        if not json_data:  # if aidoc server returns an empty list of scans
            return "no scans data was sent from aidoc server"
        # send scansdata to groupby
        strjson = groupBy(groupbyCategory, json_data)
        return strjson


if __name__ == "__main__":
    app.run(debug=True)
