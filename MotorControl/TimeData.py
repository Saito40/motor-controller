
class TimeData:
    def __init__(self, 
                 label = None, 
                 start_time = 0, 
                 after_id = 0, 
                 start_flag = False):
        self.label = label
        self.start_time = start_time
        self.after_id = after_id
        self.start_flag = start_flag
        self.speed_label_list = []
        self.progressbar = None
