#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-

from myapp import app, db
from myapp.models import Webhook


import os
import json
import unittest
import tempfile

from hamcrest import *


class WebhookTestCase(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)
        app.config['TESTING'] = True

    def tearDown(self):
        Webhook.query.delete()
        db.session.commit()
        del self.tester


    def _add_webhook(self, genre):
        return self.tester.post('/webhook', content_type='application/json', data=json.dumps({'endpoint':'http://localhost','genre':genre}))


    def test_webhook_bad_request(self):
        response = self.tester.post('/webhook', content_type='application/json', data=json.dumps({'endpoint':'http://localhost'}))
        self.assertEqual(response.status_code, 400)

    def test_add_webhook(self):
        response = self._add_webhook('pop')
        assert_that(response.data.decode("utf-8"), contains_string('created'))
        self.assertEqual(response.status_code, 201)
        
    def test_update_webhook(self):
        response1 = self._add_webhook('pop')
        response2 = self._add_webhook('rock')
        assert_that(response1.data.decode("utf-8"), contains_string('created'))
        self.assertEqual(response1.status_code, 201)
        assert_that(response2.data.decode("utf-8"), contains_string('updated'))
        self.assertEqual(response2.status_code, 200)
        
        
        
if __name__ == '__main__':
    unittest.main()





