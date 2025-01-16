import dearpygui.dearpygui as dpg

from service.armlet import HotkeyService
from service.roshan import RoshanTimer
from view.armlet_window import ArmletWindow
from view.roshan_window import RoshanWindow
from view.settings_window import SettingsWindow  # Импортируем новый класс


def main():
    dpg.create_context()
    # Инициализация сервисов
    timer_service = RoshanTimer()
    hotkey_service = HotkeyService()

    # Создание окон
    roshan_window = RoshanWindow(timer_service)
    armlet_window = ArmletWindow(hotkey_service)
    settings_window = SettingsWindow(hotkey_service)  # Окно настроек

    # Создание вьюпорта
    dpg.create_viewport(title="Dota 2 Helper", width=850, height=400, resizable=False)

    # Создание главного окна с вкладками
    with dpg.window(label="Dota 2 Helper", width=1000, height=400, no_resize=True, no_move=True, no_close=True,
                    no_collapse=True):
        with dpg.tab_bar():
            # Вкладка "Основная"
            with dpg.tab(label="Main"):
                with dpg.group(horizontal=True):  # Горизонтальное расположение
                    # Roshan Timer
                    with dpg.child_window(width=400, height=300):
                        roshan_window.create_window()
                    # Armlet Helper
                    with dpg.child_window(width=400, height=300):
                        armlet_window.create_window()

            # Вкладка "Настройки"
            with dpg.tab(label="Settings"):
                settings_window.create_window()

    # Настройка и запуск приложения
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
