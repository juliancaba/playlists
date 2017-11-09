#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


from playlists import app, playlists, songs


import os
import json
import unittest
import tempfile

from hamcrest import *


class SongsAndPlaylistsTestCase(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)
        app.config['TESTING'] = True

    def tearDown(self):
        del songs[:]
        del playlists[:]
        del self.tester

    
    def _add_playlist(self, playlist):
        return self.tester.put('/playlists/'+playlist, content_type='application/json', data=json.dumps({'description':'mi lista'}))
    
    
    def _add_ACDC_Song(self):
        return self.tester.post('/songs', content_type='application/json', data=json.dumps({'title':'Highway to Hell','artist':'ACDC', 'album':'Highway to Hell'}))


    def _add_song_to_playlist(self, playlist, song):
        return self.tester.post('/playlists/'+playlist+'/songs', content_type='application/json', data=json.dumps({'song':song}))


    def test_add_song_to_playlist(self):
        resp = self._add_playlist('ps')
        self._add_ACDC_Song()
        response = self._add_song_to_playlist('ps', 'SGlnaHdheSB0byBIZWxsSGlnaHdheSB0byBIZWxsQUNEQw==')
        assert_that(response.data, contains_string('ps playlist'))
        self.assertEqual(response.status_code, 200)


    def test_add_null_song_in_playlist(self):
        self._add_playlist('ps')
        response = self._add_song_to_playlist('ps', 'SGlnaHdheSB0byBIZWxsSGlnaHdheSB0byBIZWxsQUNEQ==')
        self.assertEqual(response.status_code, 404)
    

    def test_add_song_in_null_playlist(self):
        response = self.tester.post('/playlists/psNew/songs', content_type='application/json', data=json.dumps({'song':'SGlnaHdheSB0byBIZWxsSGlnaHdheSB0byBIZWxsQUNEQw=='}))
        self.assertEqual(response.status_code, 404)


    def test_delete_song_of_playlist(self):
        self._add_playlist('ps')
        self._add_ACDC_Song()
        self._add_song_to_playlist('ps', 'SGlnaHdheSB0byBIZWxsSGlnaHdheSB0byBIZWxsQUNEQw==')
        response = self.tester.delete('/playlists/ps/songs/SGlnaHdheSB0byBIZWxsSGlnaHdheSB0byBIZWxsQUNEQw==', content_type='application/json')
        assert_that(response.data, contains_string('SGlnaHdheSB0byBIZWxsSGlnaHdheSB0byBIZWxsQUNEQw=='))
        assert_that(response.data, contains_string('Deleted'))
        self.assertEqual(response.status_code, 200)


    def test_delete_null_song_of_playlist(self):
        self._add_playlist('psNew')
        self._add_ACDC_Song()
        response = self.tester.delete('/playlists/psNew/songs/Taylor', content_type='application/json')
        self.assertEqual(response.status_code, 404)

        
        
        
if __name__ == '__main__':
    unittest.main()





