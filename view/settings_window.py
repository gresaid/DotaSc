import os

import dearpygui.dearpygui as dpg
import yaml

from view.base_window import BaseWindow


class SettingsWindow(BaseWindow):
    def __init__(self, hotkey_service):
        super().__init__()
        self.hotkey_service = hotkey_service
        self.config = self._load_config()

    def _load_config(self):
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'settings.yaml')
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)['hotkeys']

    def create_window(self):
        with dpg.group():
            # Trigger Key
            dpg.add_text("Trigger Key:")
            dpg.add_input_text(tag="trigger_key_input", default_value=self.config['trigger_key'], width=100)
            # Action Key
            dpg.add_text("Action Key:")
            dpg.add_input_text(tag="action_key_input", default_value=self.config['action_key'], width=100)
            # Delay in ms
            dpg.add_text("Delay (ms):")
            dpg.add_input_int(tag="delay_input", default_value=self.config['delay_ms'], width=100)
            # Save Button
            dpg.add_button(label="Save Settings", callback=self._save_settings, width=200)

    def _save_settings(self):
        trigger_key = dpg.get_value("trigger_key_input")
        action_key = dpg.get_value("action_key_input")
        delay_ms = dpg.get_value("delay_input")

        new_config = {
            'trigger_key': trigger_key,
            'action_key': action_key,
            'delay_ms': delay_ms
        }

        # Update hotkey service
        self.hotkey_service.update_config(new_config)

        # Save to YAML
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'settings.yaml')
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        config['hotkeys'] = new_config
        with open(config_path, 'w', encoding='utf-8') as file:
            yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
