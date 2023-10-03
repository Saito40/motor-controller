"""
description:
    このファイルは、設定ファイルです。
"""

# コース名
COURSE_NAME = "2023_10_1__test_cource"

# データ保存関連
DATA_SAVE_DIR = "cource_time_files/"
SAVE_EXTENTION = ".csv"

# ピン番号
A_LED_PIN_LIST = [21, 26, 20, 19]  # stop, 1,...
A_MOTOR_FW_PIN = 24
A_SW_RAP___PIN = 25

B_LED_PIN_LIST = [16, 13, 6, 12]  # stop, 1,...
B_MOTOR_FW_PIN = 23
B_SW_RAP___PIN = 18

# SPIのピン番号をチェックに流す
# ここを変更してもSPIのピン番号は変わりません
SPI_PIN = [8, 9, 10, 11]

# モーター関連
# 0 < MOTOR_SPEED < 15(motor=3V) < 100(MAX)
MOTOR_LOW__SPEED = 10   # 1段階目のスピード
MOTOR_HIGH_SPEED = 100  # 最終段階のスピード
RAP_COUNT = 3           # ラップ数
TIME_SPAN = 1           # ラップタイムがのチェック間隔[s]
STOP_SPEED = 0.
PWM_FREQ = 1            # Hz

# ROTARY_MAX_STEPS = 200
VOLUME_MAX = 1024           # ボリューム検知の最大値
# MIN|MAX < BREAK < ROTATE_DEG
VOLUME_ROTATE_DEG = 210     # ボリュームの回転角度
VOLUME_RANGE_MIN_DEG = 10   # ボリュームの回転範囲の最小値、断線時を想定して実装
VOLUME_RANGE_MAX_DEG = 200  # ボリュームの回転範囲の最大値、断線時を想定して実装
VOLUME_SPEED_MIN_DEG = 180  # ボリューム最小の角度
VOLUME_SPEED_MAX_DEG = 120  # ボリューム最大の角度
MAX_SPEED_HZ = 1000_000     # SPI通信の周波数[Hz]

# ウインドウ関連
WINDOW_SIZE_W = 600
WINDOW_SIZE_H = 400
EXIT_KEY = "<Escape>"
TIMER_FONT = ("", 50, "bold", "italic")
RAP_FONT = ("", 20, "italic")
PAD_X = 20

# ラベル関連
LABEL_ON_ = "●"
LABEL_OFF = "◌"
ONOFF_FONT = ("", 20, "bold")
X00_00_000 = "00:00.000"
INTERVAL = 10  # ラベルを更新する間隔[ms]


def rap_time_label_format(rap_id: int, time_str: str) -> str:
    """description: ここで、ラップタイムのラベルの文字列を設定します。"""
    return "RAP" + str(rap_id) + ": " + time_str


def sum_time_label_format(time_str: str) -> str:
    """description: ここで、合計タイムのラベルの文字列を設定します。"""
    return "合計: " + time_str
