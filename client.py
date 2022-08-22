import requests
import json
from requests.exceptions import HTTPError
import time


class Client:
    url = "http://localhost:3000/scans"

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