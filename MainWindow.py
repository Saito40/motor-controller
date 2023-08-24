# import tkinter

# class Display:
#     def __init__(self):
#         pass



# if __name__ == "__main__":
#     pass



# -*- coding:utf-8 -*-
import tkinter
from tkinter.simpledialog import Dialog
# import time
from datetime import datetime, timedelta

# ラベルを更新する間隔[ms]
INTERVAL = 10

# 計測開始時刻
start_time = 0

# 時間計測中フラグ
start_flag = False

# afterメソッドのID
after_id = 0

class SWClass:
    def __init__(self, app, label, start_time, after_id, start_flag):
        self.app = app
        self.label = label
        self.start_time = start_time
        self.after_id = after_id
        self.start_flag = start_flag
        # self.rap_time = timedelta(0)

# 時間更新関数
def update_time(sw_class: SWClass):
    # global start_time
    # global app, label
    # global after_id

    # update_time関数を再度INTERVAL[ms]後に実行
    sw_class.after_id = sw_class.app.after(INTERVAL, lambda:update_time(sw_class))
    # print(sw_class.after_id)

    # 現在の時刻を取得
    # now_time = time.time()
    now_time = datetime.now()

    # 現在の時刻と計測開始時刻の差から計測時間計算
    elapsed_time = now_time - sw_class.start_time

    # 表示したい形式に変換（小数点第２位までに変換）
    # elapsed_time_str = '{:.2f}'.format(elapsed_time)
    # elapsed_time_str = datetime.fromtimestamp(elapsed_time).strftime("%X")
    # elapsed_time_str = '{0:02.0f}:{1:02.0f}'.format(*divmod(elapsed_time * 60, 60))
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
    sw_class.label.config(text=elapsed_time_str)


# スタートボタンの処理
def start(sw_class: SWClass):
    # global app
    # global start_flag
    # global start_time
    # global after_id

    # 計測中でなければ時間計測開始
    if not sw_class.start_flag:
        
        # 計測中フラグをON
        sw_class.start_flag = True

        # 計測開始時刻を取得
        # start_time = time.time()
        sw_class.start_time = datetime.now()

        # update_timeをINTERVAL[ms] 後に実行
        sw_class.after_id = sw_class.app.after(INTERVAL, lambda:update_time(sw_class))

# ストップボタンの処理
def stop(sw_class: SWClass):
    # global start_flag
    # global after_id

    # 計測中の場合は計測処理を停止
    if sw_class.start_flag:

        # update_time関数の呼び出しをキャンセル
        sw_class.app.after_cancel(sw_class.after_id)

        # 計測中フラグをオフ
        sw_class.start_flag = False

# def rap(sw_class: SWClass):
#     pass

class WDialog(Dialog):
    def __init__(self, root):
        self.result = False
        super().__init__(root, title="確認")
        
    def body(self, master):
        asklabel = tkinter.Label(master, text="終了しますか？")
        asklabel.grid(row=0, column=0)
        # ok_btn = tkinter.Button(master, text="OK", command=app.destroy)
        # ok_btn.grid(row=1, column=0)
        # cancel_btn = tkinter.Button(master, text="Cancel", command=master.destroy)
        # cancel_btn.grid(row=1, column=1)
    
    def apply(self):
        self.result = True


# メインウィンドウ作成
app = tkinter.Tk()
app.title("stop watch")
app.geometry("800x300")

def key_event(e):
    print(e.keysym)
    dialog = WDialog(app)
    if dialog.result:
        app.destroy()

app.bind("<Escape>", key_event)
app.bind("<S>", key_event)

# 時間計測結果表示ラベル
label = tkinter.Label(
    app,
    text="00:00.000",
    width=10,
    font=("", 50, "bold"),
)
label.pack(padx=10, pady=10)

sw_class = SWClass(app, label, start_time, after_id, start_flag)

# ストップウォッチのスタートボタン
start_button = tkinter.Button(
    app,
    text="START",
    command=lambda:start(sw_class)
)
start_button.pack(pady=5)

# ストップウォッチのストップボタン
stop_button = tkinter.Button(
    app,
    text="STOP",
    command=lambda:stop(sw_class)
)
stop_button.pack(pady=5)

# rap_button = tkinter.Button(
#     app,
#     text="rap",
#     command=lambda:rap(sw_class)
# )
# rap_button.pack(pady=5)

# メインループ
app.mainloop()



# # Python program to illustrate a stop watch
# # using Tkinter
# #importing the required libraries
# import tkinter as Tkinter
# from datetime import datetime
# counter = 66600
# running = False
# def counter_label(label):
# 	def count():
# 		if running:
# 			global counter

# 			# To manage the initial delay.
# 			if counter==66600:			
# 				display="Starting..."
# 			else:
# 				tt = datetime.fromtimestamp(counter)
# 				string = tt.strftime("%X")
# 				display=string

# 			label['text']=display # Or label.config(text=display)

# 			# label.after(arg1, arg2) delays by
# 			# first argument given in milliseconds
# 			# and then calls the function given as second argument.
# 			# Generally like here we need to call the
# 			# function in which it is present repeatedly.
# 			# Delays by 1000ms=1 seconds and call count again.
# 			label.after(1000, count)
# 			counter += 1

# 	# Triggering the start of the counter.
# 	count()	

# # start function of the stopwatch
# def Start(label):
# 	global running
# 	running=True
# 	counter_label(label)
# 	start['state']='disabled'
# 	stop['state']='normal'
# 	reset['state']='normal'

# # Stop function of the stopwatch
# def Stop():
# 	global running
# 	start['state']='normal'
# 	stop['state']='disabled'
# 	reset['state']='normal'
# 	running = False

# # Reset function of the stopwatch
# def Reset(label):
# 	global counter
# 	counter=66600

# 	# If rest is pressed after pressing stop.
# 	if running==False:	
# 		reset['state']='disabled'
# 		label['text']='Welcome!'

# 	# If reset is pressed while the stopwatch is running.
# 	else:			
# 		label['text']='Starting...'

# root = Tkinter.Tk()
# root.title("Stopwatch")

# # Fixing the window size.
# root.minsize(width=250, height=70)
# label = Tkinter.Label(root, text="Welcome!", fg="black", font="Verdana 30 bold")
# label.pack()
# f = Tkinter.Frame(root)
# start = Tkinter.Button(f, text='Start', width=6, command=lambda:Start(label))
# stop = Tkinter.Button(f, text='Stop',width=6,state='disabled', command=Stop)
# reset = Tkinter.Button(f, text='Reset',width=6, state='disabled', command=lambda:Reset(label))
# f.pack(anchor = 'center',pady=5)
# start.pack(side="left")
# stop.pack(side ="left")
# reset.pack(side="left")
# root.mainloop()

