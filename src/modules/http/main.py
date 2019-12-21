from .utils.erequest import HTTPResp

import requests
import json


class HTTP:

    def get(self, url="", headers={}):
        return self._safe_request("GET", url, headers)

    def post(self, url="", headers={}, payload={}, json_encoded=False):
        return self._safe_request("POST", url, headers, (payload, json.dumps(payload))[json_encoded])

    @staticmethod
    def _safe_request(_type, url, headers={}, payload={}):
        if url:
            try:
                if _type == "POST":
                    _response = requests.post(url, headers=headers, data=payload, timeout=30)
                else:
                    _response = requests.get(url, headers=headers, timeout=15)

                return HTTPResp(_response)

            except requests.exceptions.ConnectionError as connection_error:
                print(connection_error)
                return HTTPResp(connection_error, True, "conn_error")
            except requests.exceptions.Timeout as timeout_error:
                print(timeout_error)
                return HTTPResp(timeout_error, True, "conn_timeout")
            except requests.exceptions.RequestException as request_exception:
                print(request_exception)
                return HTTPResp(request_exception, True, "conn_generic")
        else:
            return False
