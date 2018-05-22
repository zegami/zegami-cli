# Copyright 2018 Zegami Ltd

"""Imageset tests."""

from . import HTTPBaseTestCase
from .. import imagesets


class ImagesetTestCase(HTTPBaseTestCase):
    def test_update_to_url_imageset(self):
        session = self.make_session(200, {
            'imageset': {
                "test": "data"
            }
        })
        ims_url = "test:my-test"
        configuration = {
            "dataset_column": "foo",
            'dataset_id': "my ds id"
        }
        exp_imageset = {
            'name': 'Imageset created by CLI',
            'source':
                {
                    'dataset_id': "my ds id",
                    'transfer':
                        {
                            'url': {
                                'dataset_column': 'foo'}
                        }
                }
        }

        imagesets._update_to_url_imageset(
            session, configuration, ims_url
        )
        self.assertEqual(
            session.adapters["test:"].log,
            [('PUT',
              'test:my-test',
              exp_imageset,
              'application/json')]
        )
