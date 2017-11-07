#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


from playlists import app, playlists, songs


import os
import json
import unittest
import tempfile

from hamcrest import *
from nose.tools import with_setup

class OperationsPlaylistsTestCase(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)
        app.config['TESTING'] = True

    def tearDown(self):
        del songs[:]
        del playlists[:]
        del self.tester

    
    def add_Playlist(self, playlist):
        return self.tester.put('/playlists/'+playlist, content_type='application/json', data=json.dumps({'description':'mi lista'}))
    
    
    def add_ACDC_Song(self):
        return self.tester.post('/songs', content_type='application/json', data=json.dumps({'title':'Highway to Hell','artist':'ACDC', 'album':'Highway to Hell'}))

    @with_setup(setUp, tearDown)
    def add_Song_To_A_Playlist(self, playlist, song):
        return self.tester.post('/playlists/'+playlist+'/songs', content_type='application/json', data=json.dumps({'song':song}))

    @with_setup(setUp, tearDown)
    def test_add_song_to_playlist(self):
        self.add_Playlist('ps')
        self.add_ACDC_Song()
        response = self.add_Song_To_A_Playlist('ps', 'SGlnaHdheSB0byBIZWxsSGlnaHdheSB0byBIZWxsQUNEQw==')
        print response
        assert_that(response.data, contains_string('ps playlist'))
        self.assertEqual(response.status_code, 200)

    @with_setup(setUp, tearDown)
    def test_add_song_not_saved_to_playlist(self):
        self.add_Playlist('ps')
        response = self.add_Song_To_A_Playlist('ps', 'SGlnaHdheSB0byBIZWxsSGlnaHdheSB0byBIZWxsQUNEQw==')
        self.assertEqual(response.status_code, 400)
    
    @with_setup(setUp, tearDown)
    def test_add_song_to_playlist_not_saved(self):
        response = self.tester.post('/playlists/psNew/songs', content_type='application/json', data=json.dumps({'song':'SGlnaHdheSB0byBIZWxsSGlnaHdheSB0byBIZWxsQUNEQw=='}))
        self.assertEqual(response.status_code, 404)

    @with_setup(setUp, tearDown)    
    def test_delete_song_of_playlist(self):
        self.add_Playlist('ps')
        self.add_ACDC_Song()
        self.add_Song_To_A_Playlist('ps', 'SGlnaHdheSB0byBIZWxsSGlnaHdheSB0byBIZWxsQUNEQw==')
        response = self.tester.delete('/playlists/ps/songs/SGlnaHdheSB0byBIZWxsSGlnaHdheSB0byBIZWxsQUNEQw==', content_type='application/json')
        assert_that(response.data, contains_string('SGlnaHdheSB0byBIZWxsSGlnaHdheSB0byBIZWxsQUNEQw=='))
        assert_that(response.data, contains_string('deleted'))
        self.assertEqual(response.status_code, 200)

    @with_setup(setUp, tearDown)        
    def test_delete_song_not_saved_in_playlist(self):
        self.add_Playlist('psNew')
        self.add_ACDC_Song()
        response = self.tester.delete('/playlists/psNew/songs/Taylor', content_type='application/json')
        self.assertEqual(response.status_code, 404)

        
        
        
if __name__ == '__main__':
    unittest.main()





