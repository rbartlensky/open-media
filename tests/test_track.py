import unittest
import os
import math

from openmedia.player.track import Track


class TestTrackMetaData(unittest.TestCase):

    def setUp(self):
        track_names = ["1.mp3", "2.mp3", "3.mp3"]
        module_folder = os.path.dirname(__file__)
        self.test_folder = os.path.join(module_folder, "test_tracks")
        self.track_paths = [os.path.join(self.test_folder, name)
                            for name in track_names]

    def test_tracks(self):
        for i, track_path in enumerate(self.track_paths):
            tr = Track(track_path)
            self.assertEqual(tr.metadata.artist_name, "test_artist"+str(i+1))
            self.assertEqual(tr.metadata.album_name, "test_album"+str(i+1))
            self.assertEqual(tr.metadata.track_name, "test_title"+str(i+1))
            self.assertEqual(math.ceil(tr.duration), 4)

    def tearDown(self):
        pass
