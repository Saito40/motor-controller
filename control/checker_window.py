"""
description:
    機器がちゃんと動くか確認するためのウインドウを表示します。
"""
from __future__ import annotations
import tkinter
from tkinter import messagebox
import setting

ui_font = list(setting.BUTTON_FONT)
ui_font[1] = int(ui_font[1]*2/3)
ui_font = tuple(ui_font)


class HScale(tkinter.Scale):
    """
    description:
        水平方向にスケールを表示します。
    """
    def __init__(self, *args, **kwargs):
        kwargs["orient"] = tkinter.HORIZONTAL
        super().__init__(*args, **kwargs)


class CheckerWindow:
    """
    description:
        機器がちゃんと動くか確認するためのウインドウを表示します。
    """
    root = tkinter.Tk()
    window_size = str(setting.WINDOW_SIZE_W) + "x" + str(setting.WINDOW_SIZE_H)

    def __init__(self, motor_control_list: list = None):
        motor_control_list = ["mcA", "mcB"]
        self.frame = tkinter.Frame(CheckerWindow.root)
        self.frame.pack()
        self.motor_control_list = motor_control_list
        self.start_button = None
        self.after_id = ""
        self.in_list = []
        self.out_list = []

    def create_window(self):
        """
        description:
            ウインドウを作成します。
        """

        # ウインドウの設定
        CheckerWindow.root.title("チェック")
        CheckerWindow.root.geometry(CheckerWindow.window_size)
        # MainWindow.Root.resizable(False, False)
        CheckerWindow.root.bind(setting.EXIT_KEY, CheckerWindow.exit_key_event)
        CheckerWindow.root.protocol(
            "WM_DELETE_WINDOW", CheckerWindow.exit_key_event)

        row_counter = 0
        rap_sw_label = tkinter.Label(
            self.frame,
            text="RAP_SW",
            font=setting.BUTTON_FONT
        )
        rap_sw_label.grid(
            row=row_counter, column=0, padx=setting.PAD_X, sticky=tkinter.W)
        row_counter += 2

        motor_label = tkinter.Label(
            self.frame,
            text="MOTOR",
            font=setting.BUTTON_FONT
        )
        motor_label.grid(
            row=row_counter, column=0, padx=setting.PAD_X, sticky=tkinter.W)
        row_counter += 2

        volume_label = tkinter.Label(
            self.frame,
            text="VOLUME",
            font=setting.BUTTON_FONT
        )
        volume_label.grid(
            row=row_counter, column=0, padx=setting.PAD_X, sticky=tkinter.W)
        row_counter += 2

        led_label = tkinter.Label(
            self.frame,
            text="LED",
            font=setting.BUTTON_FONT
        )
        led_label.grid(
            row=row_counter, column=0, padx=setting.PAD_X, sticky=tkinter.W)

        cache = row_counter = 1
        wigget_list = []
        for i, rap_data in enumerate(self.motor_control_list):
            print(rap_data)
            wigget_dict = {}

            row_counter = cache

            rap_sw_check = tkinter.Label(
                self.frame,
                background="BLACK",
                width=int(setting.PAD_X/5),
                font=ui_font,
                foreground="WHITE",
                text="0"
            )
            rap_sw_check.grid(
                row=row_counter, column=i)
            wigget_dict["rap_sw_check"] = rap_sw_check
            row_counter += 2

            def volume_func(itr):
                def inner(volume):
                    print(itr, volume)
                return inner
            motor_frame = tkinter.Frame(self.frame)
            motor_volume = HScale(
                motor_frame,
                width=30,
                length=300,
                from_=0,
                to=100,
                resolution=1,
                tickinterval=50,
                font=ui_font,
                command=volume_func(i)
            )
            motor_volume.grid(
                row=0, column=1, padx=setting.PAD_X)

            def mv_stop_func(motor_volume):
                def inner():
                    motor_volume.set(0)
                return inner
            motor_stop = tkinter.Button(
                motor_frame,
                text="STOP",
                font=ui_font,
                command=mv_stop_func(motor_volume)
            )
            motor_stop.grid(
                row=0, column=0, padx=setting.PAD_X)
            motor_frame.grid(
                row=row_counter, column=i, padx=setting.PAD_X)
            wigget_dict["motor_volume"] = motor_volume
            row_counter += 2

            volume_preview = tkinter.Label(
                self.frame,
                text="0",
                font=ui_font
            )
            volume_preview.grid(
                row=row_counter, column=i, padx=setting.PAD_X)
            wigget_dict["volume_preview"] = volume_preview
            row_counter += 2

            led_preview = tkinter.Frame(self.frame)
            variable = tkinter.IntVar()
            variable.set("0")
            speed_list = ["X", "0", "1", "2", "3"]
            wigget_dict["led_button_list"] = []
            for j in range(5):
                stop_func = CheckerWindow.changed_raddio_button(variable)
                led_button = tkinter.Radiobutton(
                    led_preview,
                    text=speed_list[j],
                    value=j,
                    font=ui_font,
                    indicatoron=False,
                    variable=variable,
                    command=stop_func,
                    width=int(setting.PAD_X/8),
                )
                led_button.grid(row=0, column=j)
                wigget_dict["led_button_list"].append(led_button)
            led_preview.grid(
                row=row_counter, column=i, padx=setting.PAD_X*3)
            wigget_list.append(wigget_dict)
        row_counter += 1

        def reset_func():
            for wigget_dict in wigget_list:
                wigget_dict["rap_sw_check"].configure(text="0")
                wigget_dict["motor_volume"].set(0)
                wigget_dict["volume_preview"].configure(text="0")
                wigget_dict["led_button_list"][0].select()
                wigget_dict["led_button_list"][0].invoke()

        stop_button = tkinter.Button(
            self.frame,
            text="RESET",
            font=setting.BUTTON_FONT,
            command=reset_func
        )
        stop_button.grid(
            row=row_counter, column=0, padx=setting.PAD_X, sticky=tkinter.W)

    def show_window(self):
        """
        description:
            ウインドウを表示します。
        """
        # CheckerWindow.update(self)
        CheckerWindow.root.mainloop()

    # def volume_set(self):
    #     pass

    @staticmethod
    def update(window: CheckerWindow):
        """
        description:
            時間を更新します。
        """
        # volumeがどの程度かチェックし、モーターのスピードを変更
        # for motor_control in window.motor_control_list:
        #     motor_control.volume_func()
        # # update_time関数を再度INTERVAL[ms]後に実行
        # window.after_id = CheckerWindow.root.after(
        #     setting.INTERVAL, lambda: CheckerWindow.update(window))
        # window.volume_set()

    @staticmethod
    def exit_key_event(*args):
        """
        description:
            ウインドウを閉じるときに呼び出されます。
        """
        *args, = args
        res = messagebox.askyesno(title="確認", message="終了しますか？")
        if res:
            CheckerWindow.root.destroy()

    @staticmethod
    def changed_raddio_button(variable: tkinter.StringVar):
        """
        description:
            ラジオボタンが変更されたときに呼び出されます。
        """
        def inner():
            value = variable.get()
            if value == 0:
                print("stop")
                return
            print(variable.get()-1)
        return inner
