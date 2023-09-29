"""
description:
    このファイルではtkinterのウインドウを動かします。
"""
# -*- coding:utf-8 -*-
from __future__ import annotations
import tkinter
from tkinter import messagebox
from datetime import datetime, timedelta
from control.time_data import RapData, TimerData
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
        Window.root.title("スロットカー")
        Window.root.geometry(Window.window_size)
        # MainWindow.Root.resizable(False, False)
        Window.root.bind("<Escape>", Window.exit_key_event)
        Window.root.protocol("WM_DELETE_WINDOW", Window.exit_key_event)
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

        row_counter = 0

        self.start_button = tkinter.Button(
            self.frame,
            text="start"
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

        row_counter = self.timer_data.set_timer_label(self.frame, row_counter)
        row_counter += 1

        cache = row_counter
        for i, rap_data in enumerate([
                mc.rap_data for mc in self.motor_control_list]):
            self.timer_data.rap_data_list.append(rap_data)

            row_counter = cache

            min_frame = tkinter.Frame(self.frame)
            min_frame.grid(row=row_counter, column=i, sticky=tkinter.W)
            row_counter += 1

            rap_data.set_speed_label_list(min_frame)
            row_counter = rap_data.set_rap_labels(self.frame, i, row_counter)
            row_counter = rap_data.set_sum_label(self.frame, i, row_counter)

            if debug:
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
    def exit_key_event(*args):  # pylint disable=W0613
        """
        description:
            ウインドウを閉じるときに呼び出されます。
        """
        *args, = args
        res = messagebox.askyesno(title="確認", message="終了しますか？")
        if res:
            Window.root.destroy()

    @staticmethod
    def update_time(main_window: Window):
        """
        description:
            時間を更新します。
        """
        for motor_control in main_window.motor_control_list:
            motor_control.volume_func()
        # update_time関数を再度INTERVAL[ms]後に実行
        timemain = main_window.timer_data
        timemain.after_id = Window.root.after(
            setting.INTERVAL, lambda: Window.update_time(main_window))
        if not timemain.start_flag:
            return

        # 現在の時刻と計測開始時刻の差から計測時間計算
        elapsed_time = datetime.now() - timemain.start_time

        elapsed_time_str = Window.time_to_str(elapsed_time)

        # 計測時間を表示
        timemain.label.config(text=elapsed_time_str)

    @staticmethod
    def time_to_str(time_delta: timedelta):
        """
        description:
            timedeltaを文字列に変換します。
        """
        # 表示したい形式に変換（小数点第3位までに変換）
        minutes, seconds = divmod(time_delta.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if 0 < hours:
            raise OverflowError("時間がオーバーしました")
        result_str = f"{minutes:02d}:{seconds:02d}"
        if time_delta.microseconds != 0:
            microseconds = int(time_delta.microseconds/1000)
            result_str = result_str + f".{microseconds:03d}"
        return result_str

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
            if not timer_data.start_flag:
                return

            if not rap_data.start_flag:
                return
            rap_count = len(rap_data.rap_times)
            time = datetime.now() - timer_data.start_time
            if rap_count != 0:
                time = time - sum(rap_data.rap_times, timedelta(0))
            if time < timedelta(seconds=setting.TIME_SPAN):
                return
            rap_data.rap_times.append(time)
            rap_data.rap_labels[rap_count].config(
                text=setting.rap_time_label_format(
                    rap_count+1, Window.time_to_str(time)))

            if setting.RAP_COUNT <= len(rap_data.rap_times):
                rap_data.start_flag = False
                rap_data.sum_label.config(
                    text=setting.sum_time_label_format(
                        Window.time_to_str(
                            sum(rap_data.rap_times, timedelta(0))
                        )
                    )
                )

            if all((not rap_data.start_flag)
                    for rap_data in timer_data.rap_data_list):
                timer_data.start_flag = False
        return inner

    @staticmethod
    def start(main_window: Window):
        """
        description:
            スタートボタンを押したときに呼び出されます。
        """
        def inner():
            # MainWindow.update_time(td)
            # 計測中でなければ時間計測開始
            # if timemain.start_flag:
            res = messagebox.askyesno(title="確認", message="初めますか？")
            if not res:
                return

            Window.reset(main_window.timer_data)
            # 計測中フラグをON
            main_window.timer_data.start_flag = True

            # 計測開始時刻を取得
            # start_time = time.time()
            main_window.timer_data.start_time = datetime.now()
            for rap_label in main_window.timer_data.rap_data_list:
                rap_label.move = True

            # update_timeをINTERVAL[ms] 後に実行
            main_window.timer_data.after_id = Window.root.after(
                setting.INTERVAL, lambda: Window.update_time(main_window))
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
