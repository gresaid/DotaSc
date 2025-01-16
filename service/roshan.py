import os
import threading
import time

import pyperclip
from playsound3 import playsound


class RoshanTimer:
    def __init__(self):
        self.remaining_time = 0
        self.timer_active = False
        self.timer_thread = None
        self.roshan_respawn_time = 11 * 60  # 11 минут в секундах
        self.on_timer_update = None
        self.on_timer_finish = None
        self.roshan_respawn_sound_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sounds',
                                                      'roshan_respawn.mp3')

    def start_timer(self):
        if not self.timer_active:
            self.timer_active = True
            self.remaining_time = self.roshan_respawn_time
            self.timer_thread = threading.Thread(target=self._update_timer)
            self.timer_thread.start()

    def _update_timer(self):
        while self.timer_active and self.remaining_time > 0:
            if self.on_timer_update:
                self.on_timer_update(self.remaining_time)
            time.sleep(1)
            self.remaining_time -= 1

        if self.remaining_time <= 0 and self.on_timer_finish:
            self.on_timer_finish()
            self.timer_active = False
            self._play_roshan_respawn_sound()

    def copy_to_clipboard(self):
        if self.timer_active:
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            clipboard_text = u"Rosh spawn after {:02d}:{:02d}".format(minutes, seconds)
            pyperclip.copy(clipboard_text)

    def reset_timer(self):
        self.timer_active = False
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join()
        self.remaining_time = self.roshan_respawn_time
        if self.on_timer_update:
            self.on_timer_update(self.remaining_time)

    def _play_roshan_respawn_sound(self):
        def play_sound_async():
            try:
                playsound(self.roshan_respawn_sound_path)
            except Exception as e:
                print(f"Ошибка при воспроизведении звука: {e}")

        # Запуск воспроизведения звука в отдельном потоке
        sound_thread = threading.Thread(target=play_sound_async)
        sound_thread.start()
