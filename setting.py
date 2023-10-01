## 設定
# ピン番号
A_ROTARY_CLK_A_PIN   = 9
A_ROTARY_DT__B_PIN   = 10
A_LED_R__PIN         = 21
A_LED_Y1_PIN         = 26
A_LED_Y2_PIN         = 20
A_LED_Y3_PIN         = 19
A_MOTOR_FW_PIN       = 24
A_SW_RAP_PIN         = 25

B_ROTARY_CLK_A_PIN   = 22
B_ROTARY_DT__B_PIN   = 27
B_LED_R_PIN          = 16
B_LED_Y1_PIN         = 13
B_LED_Y2_PIN         = 6
B_LED_Y3_PIN         = 12
B_MOTOR_FW_PIN       = 23
B_SW_RAP_PIN         = 18

# モーターの速度
# 0 < MOTOR_SPEED < 15(motor=3V) < 100(MAX)
MOTOR_LOW_SPEED  = 10
MOTOR_HIGH_SPEED = 100
MOTOR_SPEED_STEP = 3
RAP_COUNT = 3
TIME_SPAN = 1

WINDOW_SIZE_W = 600
WINDOW_SIZE_H = 400
EXIT_KEY = "<Escape>"
TIMER_FONT = ("", 50, "bold", "italic")
RAP_FONT = ("", 20, "italic")
PAD_X = 20

LABEL_ON_ = "●"
LABEL_OFF = "◌"
ONOFF_FONT = ("", 20, "bold")

def rap_time_label_format(rap_id: int, time_str: str)->str:
    return "RAP" + str(rap_id) + ": " + time_str

def sum_time_label_format(time_str: str)->str:
    return "合計: " + time_str

X00_00_000 = "00:00.000"

# ラベルを更新する間隔[ms]
INTERVAL = 10

STOP_SPEED = 0.
PWM_FREQ = 1 #Hz
ROTARY_MAX_STEPS = 200
# VOLUME_MIN = 0
# VOLUME_MAX = 0

