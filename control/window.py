"""
description:
    このファイルではtkinterのウインドウを動かします。
"""
from __future__ import annotations
import tkinter
from tkinter import messagebox
import pygame
from control.time_data import RapData, TimerData
from control.horizontal_scale import HScale
import setting


class Window:
    """
    description:
        このクラスはtkinterのウインドウを動かします。
    """

    root = tkinter.Tk()
    window_size = str(setting.WINDOW_SIZE_W) + "x" + str(setting.WINDOW_SIZE_H)

    def __init__(
            self,
            motor_control_list: list,
            timer_data: TimerData
            ):
        self.motor_control_list = motor_control_list
        self.timer_data = timer_data
        self.frame = tkinter.Frame(Window.root)
        self.frame.pack()
        self.start_button = None

    def create_window(self, debug: bool = False):
        """
        description:
            ウインドウを作成します。
        """

        # ウインドウの設定
        Window.root.title("スロットカー")
        Window.root.geometry(Window.window_size)
        if debug:
            Window.root.geometry(
                str(setting.WINDOW_SIZE_W) + "x" +
                str(setting.WINDOW_SIZE_H + 100))
        # MainWindow.Root.resizable(False, False)
        Window.root.bind(setting.EXIT_KEY, Window.exit_key_event)
        func = Window.start(self)
        Window.root.bind(setting.START_KEY, func)
        Window.root.protocol("WM_DELETE_WINDOW", Window.exit_key_event)

        # ラベルの設定
        row_counter = 0

        # スタートボタンの設定
        self.start_button = tkinter.Button(
            self.frame,
            text="start",
            font=setting.BUTTON_FONT
        )
        func = Window.start(self)
        self.start_button.config(command=func)
        self.start_button.grid(
            row=row_counter,
            column=0,
            columnspan=2,
            sticky=tkinter.E
        )
        row_counter += 1

        # タイマーのラベルを設定
        row_counter = self.timer_data.set_timer_label(self.frame, row_counter)
        row_counter += 1

        # コントローラーごとのラベルを設定
        cache = row_counter
        for i, rap_data in enumerate([
                mc.rap_data for mc in self.motor_control_list]):
            self.timer_data.rap_data_list.append(rap_data)

            row_counter = cache

            # スピードのmin-frameのラベルを設定
            min_frame = tkinter.Frame(self.frame)
            min_frame.grid(row=row_counter, column=i, sticky=tkinter.W)
            row_counter += 1

            # スピード表示のラベルを設定
            rap_data.set_speed_label_list(min_frame)
            # ラップタイムのラベルを設定
            row_counter = rap_data.set_rap_labels(self.frame, i, row_counter)
            # 合計タイムのラベルを設定
            row_counter = rap_data.set_sum_label(self.frame, i, row_counter)

            # テスト用のボタンを設定
            if debug:
                def create_command(rap_data):
                    def inner(value):
                        rap_data.volume = float(value)
                    return inner

                test_scale = HScale(
                    self.frame,
                    width=30,
                    length=300,
                    from_=0,
                    to=setting.VOLUME_MAX,
                    resolution=1,
                    # tickinterval=0,
                    font=setting.BUTTON_FONT,
                    command=create_command(rap_data)
                )
                test_scale.grid(row=row_counter, column=i, sticky=tkinter.E)
                row_counter += 1

                test = tkinter.Button(
                    self.frame,
                    text="t_rap&stop"
                )
                func = Window.test_rap_and_stop(rap_data, self.timer_data)
                test.config(command=func)
                test.grid(row=row_counter, column=i, sticky=tkinter.E)
                row_counter += 1

        Window.reset(self.timer_data)

    def show_window(self):
        """
        description:
            ウインドウを表示します。
        """
        Window.update_time(self)
        Window.root.mainloop()

    @staticmethod
    def exit_key_event(*args):
        """
        description:
            ウインドウを閉じるときに呼び出されます。
        """
        *args, = args
        res = messagebox.askyesno(title="確認", message="終了しますか？")
        if res:
            Window.root.destroy()

    @staticmethod
    def update_time(window: Window):
        """
        description:
            時間を更新します。
        """
        # volumeがどの程度かチェックし、モーターのスピードを変更
        for motor_control in window.motor_control_list:
            motor_control.volume_func()
        # update_time関数を再度INTERVAL[ms]後に実行
        window.timer_data.after_id = Window.root.after(
            setting.INTERVAL, lambda: Window.update_time(window))
        window.timer_data.update_timer()

    @staticmethod
    def reset(timer_data: TimerData):
        """
        description:
            表示等をリセットします。
        """
        timer_data.reset()

    @staticmethod
    def test_rap_and_stop(rap_data: RapData, timer_data: TimerData):
        """
        description:
            ラップとストップをテストします。
        """
        def inner():
            timer_data.rap_and_stop(rap_data)
        return inner

    @staticmethod
    def start(window: Window):
        """
        description:
            スタートボタンを押したときに呼び出されます。
        """
        def inner(*args):
            *args, = args
            # 計測中でなければ時間計測開始
            res = messagebox.askyesno(title="確認", message="初めますか？")
            if not res:
                return

            try:
                # BGM再生
                pygame.mixer.init(frequency=44100)
                pygame.mixer.music.load(setting.RACE_BGM)
                pygame.mixer.music.play(-1)
            except Exception as ex:  # pylint: disable=broad-except
                print(ex)

            Window.reset(window.timer_data)
            window.timer_data.start()
            # update_timeをINTERVAL[ms] 後に実行
            window.timer_data.after_id = Window.root.after(
                setting.INTERVAL, lambda: Window.update_time(window))
        return inner

    @staticmethod
    def speed_change(rap_label: RapData, speed: int):
        """
        description:
            スピードの表示を変更します。
        """
        for i, label in enumerate(rap_label.speed_label_list):
            if i <= speed:
                label.config(text=setting.LABEL_ON_)
            else:
                label.config(text=setting.LABEL_OFF)
