from flask import Flask
from flask import request
from client import Client
from groupby import group_by

app = Flask(__name__)


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
