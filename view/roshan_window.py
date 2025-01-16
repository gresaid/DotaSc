import dearpygui.dearpygui as dpg

from view.base_window import BaseWindow


class RoshanWindow(BaseWindow):
    def __init__(self, timer_service):
        super().__init__()
        self.timer_service = timer_service
        self.timer_service.on_timer_update = self._on_timer_update
        self.timer_service.on_timer_finish = self._on_timer_finish

    def create_window(self):
        with dpg.group():  # Используем group вместо window
            # Header
            with dpg.group(horizontal=True):
                dpg.add_text("Roshan Timer")

            dpg.add_separator()

            # Timer display
            with dpg.group():
                dpg.add_text("", tag="timer_text")

            dpg.add_spacing(count=5)

            # Control buttons
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Start Timer",
                    callback=self._start_timer,
                    width=130,
                    height=40
                )
                dpg.add_button(
                    label="Reset Timer",
                    callback=self._reset_timer,
                    width=130,
                    height=40
                )

            dpg.add_spacing(count=5)

            with dpg.group():
                dpg.add_button(
                    label="Copy Time",
                    callback=self._copy_to_clipboard,
                    width=200,
                    height=40
                )

            dpg.add_separator()

    def _start_timer(self):
        self.timer_service.start_timer()

    def _reset_timer(self):
        self.timer_service.reset_timer()

    def _copy_to_clipboard(self):
        self.timer_service.copy_to_clipboard()

    def _on_timer_update(self, remaining_time):
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        dpg.set_value("timer_text", f"{minutes:02d}:{seconds:02d}")

    def _on_timer_finish(self):
        dpg.set_value("timer_text", "Roshan respawn!")
