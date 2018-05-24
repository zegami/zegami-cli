# Copyright 2018 Zegami Ltd

"""HTTP tests."""

import unittest

import requests

from .. import (
    http
)


class Fake204(object):
    status_code = 204
    content = b''


class ErrorHandlingTestCase(unittest.TestCase):
    def test_handle_response_204(self):
        out = http.handle_response(Fake204)
        self.assertIs(out, None)

    def test_handle_empty_response_200(self):
        resp = requests.Response()
        resp._content = b''
        resp.status_code = 200
        out = http.handle_response(resp)
        self.assertIs(out, None)
