# -*- coding:utf-8 -*-
import tkinter
from tkinter.simpledialog import Dialog
from tkinter import messagebox
import tkinter.ttk as ttk
# import time
from datetime import datetime, timedelta
from MotorControl.TimeData import TimeData, TimeMain
from setting import *

window_size = str(WINDOW_SIZE_W) + "x" + str(WINDOW_SIZE_H)

class MainWindow:
    Root = tkinter.Tk()

    def __init__(self, MotorControlList: list, debug = False):
        
        MainWindow.Root.title("スロットカー")
        MainWindow.Root.geometry(window_size)
        # MainWindow.Root.resizable(False, False)
        MainWindow.Root.bind("<Escape>", MainWindow.exit_key_event)
        MainWindow.Root.protocol("WM_DELETE_WINDOW", MainWindow.exit_key_event)
        self.time_main = TimeMain([])
        self.frame = tkinter.Frame(MainWindow.Root)
        self.frame.pack()

        row_counter = 0

        self.start_button = tkinter.Button(
            self.frame,
            text="start"
        )
        func = MainWindow.start(self.time_main)
        self.start_button.config(command=func)

        self.start_button.grid(row=row_counter, column=0, columnspan=2, sticky=tkinter.E)
        row_counter += 1

        timer_label = tkinter.Label(
            self.frame,
            # text=X00_00_000,
            font=TIMER_FONT,
        )
        timer_label.grid(row=row_counter, column=0, columnspan=2, padx=PAD_X, pady=10)
        row_counter += 1
        self.time_main.label = timer_label
        
        cache = row_counter
        for i, td in enumerate([mc.speed_change.timedata for mc in MotorControlList]):
            self.time_main.time_data_list.append(td)
            # td.start_flag = True

            row_counter = cache
            
            min_frame = tkinter.Frame(self.frame)
            min_frame.grid(row=row_counter, column=i, sticky=tkinter.W)
            row_counter += 1

            colors = ["red", "green", "green", "green"]
            onoff = [LABEL_ON_, LABEL_OFF, LABEL_OFF, LABEL_OFF]
            for j in range(4):
                speed_label = tkinter.Label(
                    min_frame,
                    text=onoff[j],
                    font=ONOFF_FONT,
                    fg = colors[j]
                )
                speed_label.grid(row=0, column=j, sticky=tkinter.W)
                td.speed_label_list.append(speed_label)

            td.rap_labels = []
            for j in range(1, RAP_COUNT+1):
                rap_label = tkinter.Label(
                    self.frame,
                    # text=rap_time_label_format(j, X00_00_000),
                    font=RAP_FONT,
                )
                rap_label.grid(row=row_counter, column=i, padx=PAD_X, pady=0, sticky=tkinter.E)
                td.rap_labels.append(rap_label)
                row_counter += 1
            
            sum_label = tkinter.Label(
                self.frame,
                font=RAP_FONT,
            )
            sum_label.grid(row=row_counter, column=i, padx=PAD_X, pady=0, sticky=tkinter.E)
            td.sum_label = sum_label
            row_counter += 1

            if debug:
                test = tkinter.Button(
                    self.frame,
                    text="t_rap&stop"
                )
                func = MainWindow.test_rap_and_stop(td, self.time_main)
                test.config(command=func)
                test.grid(row=row_counter, column=i, sticky=tkinter.E)
                row_counter += 1

        MainWindow.reset(self.time_main)
        
        MainWindow.Root.mainloop()

    @staticmethod
    def exit_key_event(*args):
        res = messagebox.askyesno(title = "確認", message = "終了しますか？")
        if res:
            MainWindow.Root.destroy()
    
    @staticmethod
    def retire(button):
        def inner():
            if not button.td.start_flag: return
            res = messagebox.askyesno(title = "確認", message = "リタイアしますか？")
            if not res: return
            # 計測中の場合は計測処理を停止

            # update_time関数の呼び出しをキャンセル
            MainWindow.Root.after_cancel(button.td.after_id)

            # 計測中フラグをオフ
            button.td.start_flag = False
            MainWindow.reset(button.td)
        return inner
    
    @staticmethod
    def update_time(timemain: TimeMain):
        if not timemain.start_flag: return

        # update_time関数を再度INTERVAL[ms]後に実行
        timemain.after_id = MainWindow.Root.after(INTERVAL, lambda:MainWindow.update_time(timemain))
        # print(sw_class.after_id)

        # 現在の時刻を取得
        # now_time = time.time()
        now_time = datetime.now()

        # 現在の時刻と計測開始時刻の差から計測時間計算
        elapsed_time = now_time - timemain.start_time

        elapsed_time_str = MainWindow.time_to_str(elapsed_time)
        
        # 計測時間を表示
        timemain.label.config(text=elapsed_time_str)
        # td.progressbar.config(width = 200-elapsed_time.seconds*20)

    @staticmethod
    def time_to_str(time_delta: timedelta):
        # 表示したい形式に変換（小数点第２位までに変換）
        mm, ss = divmod(time_delta.seconds, 60)
        hh, mm = divmod(mm, 60)
        if 0 < hh:
            raise Exception("時間がオーバーしました")
        s = "%02d:%02d" % (mm, ss)
        if time_delta.days:
            def plural(n):
                return n, abs(n) != 1 and "s" or ""
            s = ("%d day%s, " % plural(time_delta.days)) + s
        if time_delta.microseconds:
            s = s + ".%03d" % (time_delta.microseconds / 1000)
        return s


    @staticmethod
    def reset(timemain: TimeMain):
        timemain.label.config(text=X00_00_000)
        for td in timemain.time_data_list:
            td.start_flag = True
            for i, rap_label in enumerate(td.rap_labels):
                rap_label.config(text=rap_time_label_format(i+1, X00_00_000))
            td.sum_label.config(text=sum_time_label_format(X00_00_000))
            td.rap_times = []

    @staticmethod
    def test_rap_and_stop(timedata: TimeData, timemain: TimeMain):
        def inner():
            if not timemain.start_flag: return

            if not timedata.start_flag: return
            rap_count = len(timedata.rap_times)
            if rap_count <= RAP_COUNT:
                time = datetime.now() - timemain.start_time
                if rap_count!=0:
                    time = time - sum(timedata.rap_times, timedelta(0))
                timedata.rap_times.append(time)
                timedata.rap_labels[rap_count].config(
                    text=rap_time_label_format(rap_count+1, MainWindow.time_to_str(time)))

            if RAP_COUNT <= len(timedata.rap_times):
                timedata.start_flag = False
                timedata.sum_label.config(
                    text=sum_time_label_format(
                        MainWindow.time_to_str(
                            sum(timedata.rap_times, timedelta(0))
                        )
                    )
                )
                
            if all([(not timedata.start_flag) for timedata in timemain.time_data_list]):
                timemain.start_flag = False
        return inner
    
    @staticmethod
    def start(timemain: TimeMain):
        def inner():
            # MainWindow.update_time(td)
            # 計測中でなければ時間計測開始
            # if timemain.start_flag:
            res = messagebox.askyesno(title = "確認", message = "初めますか？")
            if not res: return
                
            # 計測中フラグをON
            timemain.start_flag = True

            # 計測開始時刻を取得
            # start_time = time.time()
            timemain.start_time = datetime.now()
            MainWindow.reset(timemain)

            # update_timeをINTERVAL[ms] 後に実行
            timemain.after_id = MainWindow.Root.after(INTERVAL, lambda:MainWindow.update_time(timemain))
        return inner

    @staticmethod
    def speed_change(td, speed: int):
        for i, label in enumerate(td.speed_label_list):
            if i <= speed:
                label.config(text=LABEL_ON_)
            else:
                label.config(text=LABEL_OFF)



if __name__ == "__main__":
    class sp:
        def __init__(self):
            self.timedata = TimeData()
    class mc:
        def __init__(self):
            self.speed_change = sp()
    tds = [
        mc(),
        mc(),
    ]
    MainWindow(tds, debug = True)

