from openmedia.player import mixer

import unittest
import os


class TestPlayerFunctionality(unittest.TestCase):

    def setUp(self):
        track_names = ["1.mp3", "2.mp3", "3.mp3"]
        module_folder = os.path.dirname(__file__)
        self.test_folder = os.path.join(module_folder, "test_tracks")
        self.track_paths = [os.path.join(self.test_folder, name)
                            for name in track_names]
        mixer.init(self.track_paths)

    def test_init(self):
        self.assertTrue(mixer.track_count == len(self.track_paths))

    def test_play(self):
        mixer.play()
        self.assertTrue(mixer.is_playing())
        self.assertFalse(mixer.is_paused)
        self.assertFalse(mixer.is_stopped)
        self.assertEqual(mixer.curr_track_index, 0)
        self.assertEqual(mixer.current_track.file_path,
                         self.track_paths[0])

    def test_pause(self):
        mixer.play()
        mixer.pause()
        self.assertFalse(mixer.is_playing())
        self.assertTrue(mixer.is_paused)
        self.assertFalse(mixer.is_stopped)
        self.assertEqual(mixer.curr_track_index, 0)
        self.assertEqual(mixer.current_track.file_path,
                         self.track_paths[0])

    def test_stop(self):
        mixer.play()
        mixer.stop()
        self.assertFalse(mixer.is_playing())
        self.assertFalse(mixer.is_paused)
        self.assertTrue(mixer.is_stopped)
        self.assertEqual(mixer.curr_track_index, 0)
        self.assertEqual(mixer.current_track.file_path,
                         self.track_paths[0])

    def test_unpause(self):
        mixer.play()
        mixer.pause()
        mixer.play()
        self.assertTrue(mixer.is_playing())
        self.assertFalse(mixer.is_paused)
        self.assertFalse(mixer.is_stopped)
        self.assertEqual(mixer.curr_track_index, 0)
        self.assertEqual(mixer.current_track.file_path,
                         self.track_paths[0])

    def test_get_song_index(self):
        for index, path in enumerate(self.track_paths):
            self.assertEqual(index,
                             mixer.get_song_index(path))

    def test_set_volume(self):
        self.assertRaises(mixer.InvalidVolumeError,
                          mixer.set_volume, 1.1)

    def test_play_next(self):
        mixer.play()
        self.assertEqual(mixer.curr_track_index, 0)
        self.assertEqual(mixer.current_track.file_path,
                         self.track_paths[0])
        for i in range(1, 4):
            mixer.play_next()
            self.assertEqual(mixer.curr_track_index, i % 3)
            self.assertEqual(mixer.current_track.file_path,
                             self.track_paths[i % 3])

    def test_add(self):
        song_path = os.path.join(self.test_folder, "4.wav")
        mixer.add(song_path)
        self.assertEqual(mixer.track_count, 4)
        self.assertEqual(mixer.track_list[3].file_path, song_path)

    def test_skip(self):
        mixer.play()
        mixer.skip(1)
        self.assertEqual(mixer.get_pos()/1000, 1)

    def test_get_pos(self):
        self.assertEqual(mixer.get_pos(), 0)
        mixer.play()
        mixer.stop()
        self.assertEqual(mixer.get_pos(), 0)
        mixer.play()
        mixer.skip(1)
        mixer.pause()
        self.assertEqual(mixer.get_pos()/1000, 1)

    def test_reset(self):
        obs = mixer._observable
        player_thread = mixer.player_thread
        mixer.reset_values()
        self.assertEqual(len(mixer.track_list), 0)
        self.assertEqual(mixer.curr_track_index, -1)
        self.assertEqual(mixer.track_count, 0)
        self.assertEqual(mixer.offset, 0)
        self.assertEqual(mixer.current_track, None)
        self.assertEqual(mixer.is_paused, False)
        self.assertEqual(mixer.is_stopped, True)
        self.assertNotEqual(obs, mixer._observable)
        self.assertNotEqual(player_thread, mixer.player_thread)

    def tearDown(self):
        mixer.stop()
        mixer.player_thread.keep_running = False
