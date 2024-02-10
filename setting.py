"""
description:
    このファイルは、設定ファイルです。
"""

# コース名
COURSE_NAME = "2024_01_1__test_cource"

# データ保存関連
DATA_SAVE_DIR = "cource_time_files/"
SAVE_EXTENTION = ".csv"

# ピン番号
A_LED_PIN_LIST = [26, 19, 13, 6]  # stop, 1,...
A_MOTOR_FW_PIN = 18
A_SW_RAP___PIN = 23

B_LED_PIN_LIST = [22, 27, 17, 4]  # stop, 1,...
B_MOTOR_FW_PIN = 25
B_SW_RAP___PIN = 24

# 使用されているピン(SPIのピン)をチェックに流す
USED_PIN = [0, 1, 8, 9, 10, 11]

# モーター関連
# 0 < MOTOR_SPEED < 15(motor=3V) < 100(MAX)
MOTOR_LOW__SPEED = 10   # 1段階目のスピード
MOTOR_HIGH_SPEED = 100  # 最終段階のスピード
RAP_COUNT = 3           # ラップ数
TIME_SPAN = 1           # ラップタイムがのチェック間隔[s]
STOP_SPEED = 0.
PWM_FREQ = 9000            # Hz

# ROTARY_MAX_STEPS = 200
VOLUME_MAX = 1024           # ボリューム検知の最大値
# MIN|MAX < BREAK < ROTATE_DEG
VOLUME_ROTATE_DEG = 330     # ボリュームの回転角度
VOLUME_RANGE_MIN_DEG = 10   # ボリュームの回転範囲の最小値、断線時を想定して実装
VOLUME_RANGE_MAX_DEG = 320  # ボリュームの回転範囲の最大値、断線時を想定して実装
VOLUME_SPEED_MIN_DEG = 150  # ボリューム最小の角度
VOLUME_SPEED_MAX_DEG = 240  # ボリューム最大の角度
MAX_SPEED_HZ = 1000_000     # SPI通信の周波数[Hz]

# ウインドウ関連
WINDOW_SIZE_W = 1000
WINDOW_SIZE_H = 600
EXIT_KEY = "<Escape>"
START_KEY = "<F5>"
TIMER_FONT = ("", 80, "bold", "italic")
RAP_FONT = ("", 40, "italic")
BUTTON_FONT = ("", 40)
PAD_X = 20

# ラベル関連
LABEL_ON_ = "●"
LABEL_OFF = "◌"
ONOFF_FONT = ("", 40, "bold")
X00_00_000 = "00:00.000"
INTERVAL = 50  # ラベルを更新する間隔[ms]

# 音関連
RACE_BGM = "./redistribution_prohibited_folder/追い抜け駆け抜けろ!的なBGM.mp3"


def rap_time_label_format(rap_id: int, time_str: str) -> str:
    """description: ここで、ラップタイムのラベルの文字列を設定します。"""
    return "RAP" + str(rap_id) + ": " + time_str


def sum_time_label_format(time_str: str) -> str:
    """description: ここで、合計タイムのラベルの文字列を設定します。"""
    return "合計: " + time_str
