"""
description:
    機器がちゃんと動くか確認するためのウインドウを表示します。
"""
from __future__ import annotations
import tkinter
from tkinter import messagebox
import copy
from RPi import GPIO  # pylint: disable=E0401
from gpiozero import Button  # pylint: disable=E0401
from gpiozero.pins.pigpio import PiGPIOFactory  # pylint: disable=E0401
import spidev  # pylint: disable=E0401
import setting
from control.horizontal_scale import HScale
# import pigpio
# pi = pigpio.pi()

GPIO.setmode(GPIO.BCM)
ui_font = list(setting.BUTTON_FONT)
ui_font[1] = int(ui_font[1]*2/3)
ui_font = tuple(ui_font)


class DummyControl:
    """
    description:
        モーターの制御を行います。
    """

    FACTORY = PiGPIOFactory()
    # SPI通信を行うための準備
    spi = spidev.SpiDev()                    # インスタンスを生成
    spi.open(0, 0)                           # CE0(24番ピン)を指定
    spi.max_speed_hz = setting.MAX_SPEED_HZ  # 転送速度 1MHz

    xfer2_l_in_l = [[0x68, 0x00], [0x78, 0x00]]
    id_counter = 0

    def __init__(self):
        self.pin_led_list = []
        self.pin_motor_fw = -1
        self.pin_sw_rap = -1
        self.spi_xfer2_list = \
            DummyControl.xfer2_l_in_l[DummyControl.id_counter]
        DummyControl.id_counter += 1
        self.rap_button = None
        self.motor_fw_pwm = None
        self.volume_func = None
        self.rap_sw_check = None
        self.rap_sw_count = 0
        self.volume_preview = None

    def set_rap_sw_label(self,
                         frame: tkinter.Frame,
                         i: int,
                         row_counter: int) -> int:
        """
        description:
            ラップタイムのラベルを設定します。
        """
        self.rap_sw_check = tkinter.Label(
            frame,
            background="BLACK",
            width=int(setting.PAD_X/5),
            font=ui_font,
            foreground="WHITE",
            text=self.rap_sw_count
        )
        self.rap_sw_check.grid(
            row=row_counter, column=i)
        row_counter += 2
        return row_counter

    def set_volume_preview(self,
                           frame: tkinter.Frame,
                           i: int,
                           row_counter: int) -> int:
        """
        description:
            ボリュームのラベルを設定します。
        """
        self.volume_preview = tkinter.Label(
            frame,
            text="0",
            font=ui_font
        )
        self.volume_preview.grid(
            row=row_counter, column=i, padx=setting.PAD_X)
        row_counter += 2
        return row_counter

    def set_pins(self,
                 pin_led_list: list[int],
                 pin_motor_fw: int,
                 pin_sw_rap: int):
        """
        description:
            ピンを設定します。
        """
        self.pin_led_list = pin_led_list
        self.pin_motor_fw = pin_motor_fw
        self.pin_sw_rap = pin_sw_rap
        self.reset()

    def reset(self):
        """
        description:
            リセットします。
        """
        self.rap_button = Button(
            self.pin_sw_rap,
            pull_up=True,
            pin_factory=DummyControl.FACTORY,
            bounce_time=1e-7
            )
        # ボタンリリース時の処理
        func = DummyControl.rap_script(self)
        self.rap_button.when_released = func

        GPIO.setup(self.pin_motor_fw, GPIO.OUT)
        self.motor_fw_pwm = GPIO.PWM(self.pin_motor_fw, setting.PWM_FREQ)
        self.motor_fw_pwm.start(0)

        for pin in self.pin_led_list:
            GPIO.setup(pin, GPIO.OUT)
        GPIO.output(self.pin_led_list[0], True)

        self.volume_func = DummyControl.check_volume(self)

    def close(self):
        """
        description:
            リセットします。
        """
        self.motor_fw_pwm.ChangeDutyCycle(0)
        for pin in self.pin_led_list:
            GPIO.output(pin, False)

    @staticmethod
    def rap_script(motor_control: DummyControl):
        """
        description:
            ラップを行います。
        """
        def inner():
            motor_control.rap_sw_count += 1
            motor_control.rap_sw_check.configure(
                background="WHITE",
                foreground="BLACK",
                text=str(motor_control.rap_sw_count))
        return inner

    @staticmethod
    def check_volume(motor_control: DummyControl):
        """
        description:
            ボリュームをチェックします。
        """
        def inner():
            # SPI通信で値を読み込む
            resp = DummyControl.spi.xfer2(
                copy.deepcopy(motor_control.spi_xfer2_list))
            motor_control.volume_preview.configure(
                text=str(((resp[0] << 8) + resp[1]) & 0x3FF))
        return inner


class CheckerWindow:
    """
    description:
        機器がちゃんと動くか確認するためのウインドウを表示します。
    """
    root = tkinter.Tk()
    window_size = str(setting.WINDOW_SIZE_W) + "x" + str(setting.WINDOW_SIZE_H)

    def __init__(self, dummy_control_list: list = None):
        self.frame = tkinter.Frame(CheckerWindow.root)
        self.frame.pack()
        self.dummy_control_list = dummy_control_list
        self.start_button = None
        self.after_id = ""

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

        _row_counter = 0
        _rap_sw_label = tkinter.Label(
            self.frame,
            text="RAP_SW",
            font=setting.BUTTON_FONT
        )
        _rap_sw_label.grid(
            row=_row_counter, column=0, padx=setting.PAD_X, sticky=tkinter.W)
        _row_counter += 2

        _motor_label = tkinter.Label(
            self.frame,
            text="MOTOR",
            font=setting.BUTTON_FONT
        )
        _motor_label.grid(
            row=_row_counter, column=0, padx=setting.PAD_X, sticky=tkinter.W)
        _row_counter += 2

        _volume_label = tkinter.Label(
            self.frame,
            text="VOLUME",
            font=setting.BUTTON_FONT
        )
        _volume_label.grid(
            row=_row_counter, column=0, padx=setting.PAD_X, sticky=tkinter.W)
        _row_counter += 2

        _led_label = tkinter.Label(
            self.frame,
            text="LED",
            font=setting.BUTTON_FONT
        )
        _led_label.grid(
            row=_row_counter, column=0, padx=setting.PAD_X, sticky=tkinter.W)

        _cache = _row_counter = 1
        _wigget_list = []
        for i, dummy_control in enumerate(self.dummy_control_list):
            _wigget_dict = {}

            _row_counter = _cache

            _row_counter = dummy_control.set_rap_sw_label(
                    self.frame, i, _row_counter)
            _wigget_dict["rap_sw_check"] = dummy_control.rap_sw_check

            def volume_func(itr, dummy_control):
                def inner(volume):
                    print(itr, volume)
                    dummy_control.motor_fw_pwm.ChangeDutyCycle(int(volume))
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
                command=volume_func(i, dummy_control)
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
                row=_row_counter, column=i, padx=setting.PAD_X)
            _wigget_dict["motor_volume"] = motor_volume
            _row_counter += 2

            _row_counter = dummy_control.set_volume_preview(
                    self.frame, i, _row_counter)
            _wigget_dict["volume_preview"] = dummy_control.volume_preview

            led_preview = tkinter.Frame(self.frame)
            variable = tkinter.IntVar()
            variable.set(0)
            speed_list = ["X", "0", "1", "2", "3"]
            _wigget_dict["led_button_list"] = []
            for j in range(5):
                stop_func = CheckerWindow.changed_raddio_button(
                    variable, dummy_control)
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
                _wigget_dict["led_button_list"].append(led_button)
            led_preview.grid(
                row=_row_counter, column=i, padx=setting.PAD_X*3)
            _wigget_list.append(_wigget_dict)
        _row_counter += 1

        def reset_func():
            for wigget_dict in _wigget_list:
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
            row=_row_counter, column=0, padx=setting.PAD_X, sticky=tkinter.W)
        reset_func()

    def show_window(self):
        """
        description:
            ウインドウを表示します。
        """
        CheckerWindow.update(self)
        CheckerWindow.root.mainloop()

    @staticmethod
    def update(window: CheckerWindow):
        """
        description:
            時間を更新します。
        """
        # volumeがどの程度かチェックし、モーターのスピードを変更
        for dummy_control in window.dummy_control_list:
            dummy_control.volume_func()
        # update_time関数を再度INTERVAL[ms]後に実行
        window.after_id = CheckerWindow.root.after(
            setting.INTERVAL, lambda: CheckerWindow.update(window))

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
    def changed_raddio_button(variable: tkinter.StringVar,
                              dummy_control: DummyControl):
        """
        description:
            ラジオボタンが変更されたときに呼び出されます。
        """
        def inner():
            value = variable.get()
            if value == 0:
                print("stop")
                for i in range(4):
                    GPIO.output(dummy_control.pin_led_list[i], False)
                return
            print(value-1)
            for i in range(4):
                GPIO.output(dummy_control.pin_led_list[i], value-1 == i)
        return inner
