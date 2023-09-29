"""
description:
    タイマーのデータを保持するクラス
"""


import tkinter
import setting


class TimerData:
    """
    description:
        タイマーのデータを保持するクラス
    """
    def __init__(self):
        self.rap_data_list = []
        self.label = None
        self.start_time = None
        self.after_id = ""
        self.start_flag = False

    def set_timer_label(
            self,
            frame: tkinter.Frame,
            row_counter: int
            ) -> int:
        """
        description:
            タイマーのラベルを設定します。
        """
        timer_label = tkinter.Label(
            frame,
            font=setting.TIMER_FONT,
        )
        timer_label.grid(
            row=row_counter,
            column=0,
            columnspan=2,
            padx=setting.PAD_X,
            pady=10
        )
        self.label = timer_label
        return row_counter

    def reset(self):
        """
        description:
            リセットします。
        """
        self.start_flag = False
        self.label.config(text=setting.X00_00_000)
        for rap_data in self.rap_data_list:
            rap_data.reset()


class RapData:
    """
    description:
        ラップタイムのデータを保持するクラス
    """
    def __init__(self):
        self.speed_label_list = []
        self.rap_labels = []
        self.rap_times = None
        self.sum_label = None
        self.start_flag = False

    def set_speed_label_list(self, min_frame: tkinter.Frame):
        """
        description:
            ラップタイムのラベルを設定します。
        """
        colors = ["red", "green", "green", "green"]
        onoff = [
            setting.LABEL_ON_,
            setting.LABEL_OFF,
            setting.LABEL_OFF,
            setting.LABEL_OFF
        ]
        for j in range(4):
            speed_label = tkinter.Label(
                min_frame,
                text=onoff[j],
                font=setting.ONOFF_FONT,
                fg=colors[j]
            )
            speed_label.grid(row=0, column=j, sticky=tkinter.W)
            self.speed_label_list.append(speed_label)

    def set_rap_labels(
            self,
            frame: tkinter.Frame,
            i: int,
            row_counter: int
            ) -> int:
        """
        description:
            ラップタイムのラベルを設定します。
        """
        for _ in range(1, setting.RAP_COUNT+1):
            rap_label = tkinter.Label(
                frame,
                font=setting.RAP_FONT,
            )
            rap_label.grid(
                row=row_counter,
                column=i,
                padx=setting.PAD_X,
                pady=0,
                sticky=tkinter.E
            )
            self.rap_labels.append(rap_label)
            row_counter += 1
        return row_counter

    def set_sum_label(
            self,
            frame: tkinter.Frame,
            i: int,
            row_counter: int
            ) -> int:
        """
        description:
            合計タイムのラベルを設定します。
        """
        sum_label = tkinter.Label(
            frame,
            font=setting.RAP_FONT,
        )
        sum_label.grid(
            row=row_counter,
            column=i,
            padx=setting.PAD_X,
            pady=0,
            sticky=tkinter.E
        )
        self.sum_label = sum_label
        row_counter += 1
        return row_counter

    def reset(self):
        """
        description:
            リセットします。
        """
        self.start_flag = True
        self.move = False
        for i, rap_label in enumerate(self.rap_labels):
            rap_label.config(
                text=setting.rap_time_label_format(
                    i+1, setting.X00_00_000))
        self.sum_label.config(
            text=setting.sum_time_label_format(setting.X00_00_000))
        self.rap_times = []
