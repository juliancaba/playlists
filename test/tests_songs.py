#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from playlists import app, songs


import os
import json
import unittest
import tempfile

from hamcrest import *



class SongsTestCase(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)
        app.config['TESTING'] = True
        self.del_ACDC_Song()

    def tearDown(self):
        del songs[:]
        del self.tester

    def del_ACDC_Song(self):
        return self.tester.delete('/songs/SGlnaHdheSB0byBIZWxsSGlnaHdheSB0byBIZWxsQUNEQw==')
    
    def add_ACDC_Song(self):
        return self.tester.post('/songs', content_type='application/json', data=json.dumps({'title':'Highway to Hell','artist':'ACDC', 'album':'Highway to Hell'}))
        

    def test_get_empty(self):
        response= self.tester.get('/songs', content_type='application/json')
        self.assertEqual(json.loads(response.data), {'songs':[]})
        self.assertEqual(response.status_code, 200)

        
    def test_get_song(self):
        response= self.add_ACDC_Song()
        response= self.tester.get('/songs/SGlnaHdheSB0byBIZWxsSGlnaHdheSB0byBIZWxsQUNEQw==', content_type='application/json')
        assert_that(response.data, contains_string('Highway to Hell'))
        self.assertEqual(response.status_code, 200)

        
    def test_get_song_not_found(self):
        response= self.tester.get('/songs/NONE', content_type='application/json')
        self.assertEqual(response.status_code, 404)
        

    def test_new_song_error(self):
        response= self.tester.post('/songs', content_type='application/json', data=json.dumps({'title':'a1'}))
        self.assertEqual(response.status_code, 400)

    

    def test_new_song(self):
        response= self.add_ACDC_Song()
        self.assertEqual(json.loads(response.data), {'created':'SGlnaHdheSB0byBIZWxsSGlnaHdheSB0byBIZWxsQUNEQw=='})
        self.assertEqual(response.status_code, 201)


    def test_add_song_conflict(self):
        resp=self.add_ACDC_Song()
        self.assertEqual(resp.status_code, 201)
        resp=self.add_ACDC_Song()
        self.assertEqual(resp.status_code, 409)
        

    def test_get_songs(self):
        self.add_ACDC_Song()
        response=self.tester.get('/songs', content_type='application/json')
        self.assertEqual(json.loads(response.data),{'songs':[{'album': 'Highway to Hell','artist': 'ACDC','id':'SGlnaHdheSB0byBIZWxsSGlnaHdheSB0byBIZWxsQUNEQw==','title':'Highway to Hell','year':''}]})
        assert_that(response.data, contains_string('Highway to Hell'))
        self.assertEqual(response.status_code, 200)


    def test_delete_not_song_found(self):
        response=self.tester.delete('/songs/taylor', content_type='application/json')        
        self.assertEqual(response.status_code, 404)


    def test_delete_song(self):
        responsePost = self.add_ACDC_Song()
        code = json.loads(responsePost.data)['created']
        response=self.tester.delete('/songs/'+code, content_type='application/json')        
        self.assertEqual(json.loads(response.data), {'deleted':str(code)})
        self.assertEqual(response.status_code, 200)
    
        
        
if __name__ == '__main__':
    unittest.main()


