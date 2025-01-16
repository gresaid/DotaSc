import dearpygui.dearpygui as dpg

from view.base_window import BaseWindow


class ArmletWindow(BaseWindow):
    def __init__(self, hotkey_service):
        super().__init__()
        self.hotkey_service = hotkey_service

    def create_window(self):
        with dpg.group():  # Используем group для встраивания в другие элементы
            # Header
            with dpg.group(horizontal=True):
                dpg.add_text("Armlet Helper")

            dpg.add_separator()

            # Status and control
            with dpg.group():
                dpg.add_button(
                    label="Enable Armlet Script",
                    tag="autoclick_button",
                    callback=self._toggle_autoclick,
                    width=200,
                    height=40
                )

                dpg.add_text("Script is disabled", tag="autoclick_status")

    def _toggle_autoclick(self):
        is_active = self.hotkey_service.toggle()
        if is_active:
            dpg.set_item_label("autoclick_button", "Disable Armlet Script")
            dpg.set_value("autoclick_status", "Script is enabled")
        else:
            dpg.set_item_label("autoclick_button", "Enable Armlet Script")
            dpg.set_value("autoclick_status", "Script is disabled")
