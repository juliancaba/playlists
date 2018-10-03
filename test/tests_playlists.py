#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from playlists import app, playlists


import os
import json
import unittest
import tempfile

from hamcrest import *


class PlaylistsTestCase(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)
        app.config['TESTING'] = True

    def tearDown(self):
        del playlists[:]
        del self.tester

        
    def _add_playlist(self):
        return self.tester.put('/playlists/psmon', content_type='application/json', data=json.dumps({'description':'mi lista de los lunes'}))


    def test_empty(self):
        response = self.tester.get('/playlists', content_type='application/json')
        self.assertEqual(json.loads(response.data.decode("utf-8")), {'playlists':[]})
        self.assertEqual(response.status_code, 200)


    def test_new_playlists_error(self):
        response = self.tester.put('/playlists/psmon', content_type='application/json')
        self.assertEqual(response.status_code, 400)


    def test_new_playlists(self):
        response = self._add_playlist()
        self.assertEqual(json.loads(response.data.decode("utf-8")), {'id':'psmon'})
        self.assertEqual(response.status_code, 201)
        

    def test_update_playlists(self):
        self._add_playlist()
        response = self.tester.put('/playlists/psmon', content_type='application/json', data=json.dumps({'description':'mi lista preferida de los lunes'}))
        self.assertEqual(json.loads(response.data.decode("utf-8")), {'updated':'psmon'})
        self.assertEqual(response.status_code, 200)


    def test_delete_not_found(self):
        response = self.tester.delete('/playlists/psfri', content_type='application/json')
        self.assertEqual(response.status_code, 404)


    def test_delete(self):
        self._add_playlist()
        response = self.tester.delete('/playlists/psmon', content_type='application/json')
        self.assertEqual(json.loads(response.data.decode("utf-8")), {'deleted':'psmon'})
        self.assertEqual(response.status_code, 200)
        
        
        
        
if __name__ == '__main__':
    unittest.main()


