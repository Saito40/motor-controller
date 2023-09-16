
class TimeMain:
    def __init__(self, 
                 time_data_list,
                 label = None, 
                 start_time = 0, 
                 after_id = 0, 
                 start_flag = False):
        self.time_data_list = time_data_list
        self.label = label
        self.start_time = start_time#
        self.after_id = after_id#
        self.start_flag = start_flag#
        self.speed_label_list = []#

class TimeData:
    def __init__(self, 
                 label = None, 
                 start_time = 0, 
                 after_id = 0, 
                 start_flag = False,
                 sum_label = None):
        # self.label = label#
        # self.start_time = start_time#
        # self.after_id = after_id#
        self.speed_label_list = []
        self.start_flag = start_flag
        self.progressbar = None
        self.rap_times = []
        self.rap_labels = []
        self.sum_label = sum_label
