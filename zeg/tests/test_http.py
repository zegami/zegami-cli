# Copyright 2018 Zegami Ltd

"""HTTP tests."""

import unittest


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
