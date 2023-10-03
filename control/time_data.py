"""
description:
    タイマーのデータを保持するクラス
"""


from datetime import datetime, timedelta
import tkinter
import setting


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
        self.move = False
        self.sum_time = None

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

    def try_rap_and_stop(self, timer_start: datetime) -> bool:
        """
        description:
            ラップとストップを行います。
        """
        if not self.start_flag:
            return False
        rap_count = len(self.rap_times)
        time = datetime.now() - timer_start
        if rap_count != 0:
            time = time - sum(self.rap_times, timedelta(0))
        if time < timedelta(seconds=setting.TIME_SPAN):
            return False
        self.rap_times.append(time)
        self.rap_labels[rap_count].config(
            text=setting.rap_time_label_format(
                rap_count+1, time_to_str(time)))

        if setting.RAP_COUNT <= len(self.rap_times):
            self.start_flag = False
            self.sum_time = sum(self.rap_times, timedelta(0))
            self.sum_label.config(
                text=setting.sum_time_label_format(
                    time_to_str(self.sum_time)
                )
            )
        return True


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

    def update_timer(self):
        """
        description:
            時間を更新します。
        """
        if not self.start_flag:
            return

        # 計測時間を表示
        self.label.config(
            text=time_to_str(datetime.now()-self.start_time))

    def rap_and_stop(self, rap_data: RapData):
        """
        description:
            ラップとストップを行います。
        """
        if not self.start_flag:
            return
        if not rap_data.try_rap_and_stop(self.start_time):
            return
        if all((not rap_data.start_flag)
                for rap_data in self.rap_data_list):
            self.start_flag = False

    def start(self):
        """
        description:
            スタートを行います。
        """
        # 計測中フラグをON
        self.start_flag = True

        # 計測開始時刻を取得
        self.start_time = datetime.now()
        for rap_label in self.rap_data_list:
            rap_label.move = True
