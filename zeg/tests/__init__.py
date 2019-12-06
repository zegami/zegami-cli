# Copyright 2018 Zegami Ltd
"""Test implementation of the python requests interface."""

import io
import json
import unittest

import requests.adapters

from .. import log

JSON_TYPE = 'application/json'


def _request_details(request):
    content_type = request.headers.get('Content-Type')
    body = request.body
    if content_type == JSON_TYPE:
        body = json.loads(body.decode('utf-8'))
    return request.method, request.url, body, content_type


def create_response(url, code, body, content_type=None):
    response = requests.models.Response()
    response.url = url
    response.status_code = code
    if not isinstance(body, bytes):
        body = json.dumps(body).encode('utf-8')
        response.content_type = JSON_TYPE
    if content_type is not None:
        response.content_type = content_type
    response.raw = io.BytesIO(body)
    return response


class ResolverAdapter(requests.adapters.BaseAdapter):
    """Testing requests Adapter that uses a resolver function."""

    def __init__(self, resolver):
        super(ResolverAdapter, self).__init__()
        self._resolver = resolver
        self.log = []

    def send(self, request, **send_kwargs):
        """Record request details and send pre-canned response."""
        try:
            details = _request_details(request)
            return create_response(*self._resolver(request.url))
        except Exception as e:
            details = e
        finally:
            self.log.append(details)

    def close(self):
        """Do nothing close."""


class HTTPBaseTestCase(unittest.TestCase):
    @staticmethod
    def make_session(code, body):
        session = requests.Session()

        def canned_answer(url):
            return url, code, body
        adapter = ResolverAdapter(canned_answer)
        session.mount('test:', adapter)
        return session


class FakeLogger(log.Logger):
    def __init__(self, verbose=False):
        super(FakeLogger, self).__init__(verbose)
        self.entries = []

    def __call__(self, format_string, **kwargs):
        self.entries.append(format_string.format(**kwargs))
