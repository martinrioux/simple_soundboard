
import os
from pygame import mixer
from pygame import error as pygame_error
import logging

mixer.init()

class SoundEngine:
    def __init__(self):
        self.sounds = {}

    def init(self):
        return

    def stop_all_sounds(self):
        for sound in self.sounds:
            self.sounds[sound].stop()
        mixer.music.stop()

    def fadeout_music(self, delay=3):
        mixer.music.fadeout(delay*1000)

    def pause_music(self):
        mixer.music.pause()

    def resume_music(self):
        mixer.music.play()

    def play_music(self, music_path, volume=0.5, loop_playback=False):
        if not os.path.exists(music_path):
            logging.error(f"Music file '{music_path}' not found")
            return

        mixer.music.stop()
        mixer.music.load(music_path)
        mixer.music.set_volume(volume)
        if loop_playback:
            mixer.music.play(loops=-1, start=0.0, fade_ms=1500)
        else:
            mixer.music.play()

    def play_sound(self, sound_path, volume=0.5):
        if not os.path.exists(sound_path):
            logging.error(f"Sound file '{sound_path}' not found")
            return

        if sound_path not in self.sounds:
            self.sounds[sound_path] = mixer.Sound(sound_path)
        else:
            self.sounds[sound_path].stop()
        self.sounds[sound_path].set_volume(volume)
        self.sounds[sound_path].play()