# -*- coding:utf-8 -*-
import tkinter
from tkinter.simpledialog import Dialog
from tkinter import messagebox
import tkinter.ttk as ttk
# import time
from datetime import datetime, timedelta
from MotorControl.TimeData import TimeData

WINDOW_SIZE_W = 1200
WINDOW_SIZE_H = 300
EXIT_KEY = "<Escape>"
TIMER_FONT = ("", 50, "bold")
PAD_X = 20

LABEL_ON_ = "●"
LABEL_OFF = "◌"
ONOFF_FONT = ("", 20, "bold")

X00_00_000 = "00:00.000"

# ラベルを更新する間隔[ms]
INTERVAL = 10

window_size = str(WINDOW_SIZE_W) + "x" + str(WINDOW_SIZE_H)

class MainWindow:
    Root = tkinter.Tk()

    def __init__(self, MotorControlList: list, debug = False):
        MainWindow.Root.title("スロットカー")
        MainWindow.Root.geometry(window_size)
        # MainWindow.Root.resizable(False, False)
        MainWindow.Root.bind("<Escape>", MainWindow.exit_key_event)
        MainWindow.Root.protocol("WM_DELETE_WINDOW", MainWindow.exit_key_event)
        self.frame = tkinter.Frame(MainWindow.Root)
        self.frame.pack()
        for i, td in enumerate([mc.speed_change.timedata for mc in MotorControlList]):

            button = tkinter.Button(
                self.frame,
                text="retire"
            )
            button.td = td
            func = MainWindow.retire(button)
            button.config(command=func)
            button.grid(row=0, column=i, sticky=tkinter.E)

            td.label = tkinter.Label(
                self.frame,
                text=X00_00_000,
                font=TIMER_FONT,
            )
            td.label.grid(row=1, column=i, padx=PAD_X, pady=10)

            min_frame = tkinter.Frame(self.frame)
            min_frame.grid(row=2, column=i, sticky=tkinter.W)

            colors = ["red", "green", "green", "green"]
            onoff = [LABEL_ON_, LABEL_OFF, LABEL_OFF, LABEL_OFF]
            for j in range(4):
                speed_label = tkinter.Label(
                    min_frame,
                    text=onoff[j],
                    font=ONOFF_FONT,
                    fg = colors[j]
                )
                speed_label.grid(row=0, column=j)
                td.speed_label_list.append(speed_label)

            td.progressbar = ttk.Progressbar(
                self.frame, orient="horizontal",
                length=300, mode="determinate")#, style="Horizontal.TProgressbar")
            td.progressbar.grid(row=3, column=i)
            td.progressbar.configure(maximum=300,value=300)

            if debug:
                last = 4

                test = tkinter.Button(
                    self.frame,
                    text="t_start"
                )
                test.td = td
                func = MainWindow.test_start(test)
                test.config(command=func)
                test.grid(row=last, column=i, sticky=tkinter.E)

                test = tkinter.Button(
                    self.frame,
                    text="t_stop"
                )
                test.td = td
                func = MainWindow.test_stop(test)
                test.config(command=func)
                test.grid(row=last+1, column=i, sticky=tkinter.E)

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
            MainWindow.reset_label(button.td)
        return inner
    
    @staticmethod
    def update_time(td: TimeData):
        if not td.start_flag: return

        # update_time関数を再度INTERVAL[ms]後に実行
        td.after_id = MainWindow.Root.after(INTERVAL, lambda:MainWindow.update_time(td))
        # print(sw_class.after_id)

        # 現在の時刻を取得
        # now_time = time.time()
        now_time = datetime.now()

        # 現在の時刻と計測開始時刻の差から計測時間計算
        elapsed_time = now_time - td.start_time

        # 表示したい形式に変換（小数点第２位までに変換）
        mm, ss = divmod(elapsed_time.seconds, 60)
        hh, mm = divmod(mm, 60)
        if 0 < hh:
            raise Exception("時間がオーバーしました")
        s = "%02d:%02d" % (mm, ss)
        if elapsed_time.days:
            def plural(n):
                return n, abs(n) != 1 and "s" or ""
            s = ("%d day%s, " % plural(elapsed_time.days)) + s
        if elapsed_time.microseconds:
            s = s + ".%03d" % (elapsed_time.microseconds / 1000)

        elapsed_time_str = s
        
        # 計測時間を表示
        td.label.config(text=elapsed_time_str)
        td.progressbar.configure(value = 300-elapsed_time.seconds*30)
        td.progressbar.update()
        # td.progressbar.config(width = 200-elapsed_time.seconds*20)

    @staticmethod
    def reset_label(td: TimeData):
        td.label.config(text=X00_00_000)
        td.progressbar.configure(value = 300)
        # td.progressbar.config(width = 200)

    @staticmethod
    def test_stop(button):
        def inner():
            if not button.td.start_flag: return

            # update_time関数の呼び出しをキャンセル
            MainWindow.Root.after_cancel(button.td.after_id)

            # 計測中フラグをオフ
            button.td.start_flag = False
        return inner
    
    @staticmethod
    def test_start(button):
        def inner():
            # MainWindow.update_time(td)
            # 計測中でなければ時間計測開始
            if button.td.start_flag: return
                
            # 計測中フラグをON
            button.td.start_flag = True

            # 計測開始時刻を取得
            # start_time = time.time()
            button.td.start_time = datetime.now()

            # update_timeをINTERVAL[ms] 後に実行
            button.td.after_id = MainWindow.Root.after(INTERVAL, lambda:MainWindow.update_time(button.td))
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
    main = MainWindow(tds, debug = True)

