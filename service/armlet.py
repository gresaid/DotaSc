# -*- coding: utf-8 -*-
import os
import time
from threading import Thread, Lock

import keyboard
import yaml


class HotkeyService:
    def __init__(self):
        self.active = False
        self.config = self._load_config()
        self.listener_thread = None
        self.lock = Lock()
        self.last_trigger_time = 0
        self.is_trigger_pressed = False
        self.cooldown = 0.1  # Защитный интервал между срабатываниями в секундах

    def _load_config(self):
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'settings.yaml')
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)['hotkeys']

    def toggle(self):
        self.active = not self.active
        if self.active and not self.listener_thread:
            self.listener_thread = Thread(target=self._start_listening, daemon=True)
            self.listener_thread.start()
        return self.active

    def _start_listening(self):
        while self.active:
            current_time = time.time()

            # Проверяем состояние кнопки-триггера
            if keyboard.is_pressed(self.config['trigger_key']):
                if not self.is_trigger_pressed:  # Кнопка только что была нажата
                    with self.lock:
                        if current_time - self.last_trigger_time > self.cooldown:
                            self._perform_double_press()
                            self.last_trigger_time = current_time
                    self.is_trigger_pressed = True
            else:
                self.is_trigger_pressed = False  # Кнопка отпущена

            time.sleep(0.001)  # Небольшая задержка для снижения нагрузки на CPU

    def _perform_double_press(self):
        try:
            key = self.config['action_key']
            delay = self.config['delay_ms'] / 1000.0

            # Первое нажатие
            keyboard.press(key)
            keyboard.release(key)
            time.sleep(delay)

            # Второе нажатие
            keyboard.press(key)
            keyboard.release(key)

        except Exception as e:
            print(f"Ошибка при выполнении двойного нажатия: {e}")
        finally:
            # Убеждаемся, что клавиша точно отпущена
            keyboard.release(key)

    def update_config(self, new_config):
        with self.lock:
            self.config = new_config
