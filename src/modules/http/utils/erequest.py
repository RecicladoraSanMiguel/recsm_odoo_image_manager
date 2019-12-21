import json


class HTTPResp:

    def __init__(self, http_response, error=False, exception_type=""):
        self._raw_response = http_response
        self._error = error
        self._exception_type = exception_type
        self._status_code = ""

        if not self._error:
            self._status_code = self._raw_response.status_code
            if self._status_code >= 400:
                self._error = True
                self._set_status_code_error()
        else:
            self._set_exception_error()

    def is_valid(self):
        """
        :return: Returns if the request was valid once it was triggered and has no errors
        """
        return not self._error

    def get_response_time(self):
        return self._raw_response.elapsed.total_seconds()

    def get_response(self):
        """
        :return: Returns raw response object
        """
        return self._raw_response

    def get_response_headers(self):
        """
        :return: Returns raw response headers
        """
        return self._raw_response.headers

    def get_response_body(self):
        """
        :return: Returns raw response body
        """
        return self._raw_response.text

    def get_response_body_json(self):
        """
        ;validation: Validates JSON parse and returns False if an error was raised during parsing
        :return: parses the raw response to a valid JSON object
        """
        try:
            return json.loads(self._raw_response.text)
        except ValueError:
            return False

    def get_response_body_binary(self):
        """
        :return: Returns raw response object
        """
        return self._raw_response.content

    def get_error_details(self):
        if self._error:
            return({
                "status_code": self._status_code,
                "exception_summary": self._error_description
            })
        return False

    def _set_exception_error(self):
        #@TODO: Evaluate specific expection time and provide error accordingly
        self._status_code = 0

        if self._exception_type == "conn_timeout":
            self._error_description = "Connection timed out"
        elif self._exception_type == "conn_error":
            self._error_description = "Error while trying to establish the connection"
        elif self._exception_type == "conn_generic":
            self._error_description = "Generic connection error"
        else:
            self._error_description = "Unhandled connection exception"

    def _set_status_code_error(self):
        """
        :return: Parses error made on the connection and gives human readable errors
        """
        if self._status_code < 500:
                self._error_description = "Bad Client Request"
        else:
            self._error_description = "Server side error"
