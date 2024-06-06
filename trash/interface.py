
class handle:
    def __init__(self,msg_mode : str):
        self.msg_modes = {'r' : self.handle_r_msg,'l': self.handle_l_msg,'rooms' : self.handle_rooms_msg}
        self.r_ans = {}
        self.l_ans = {}
        self.rooms_ans = {}
    def handle_r_msg(self):
        pass
    def handle_l_msg(self):
        pass
    def handle_rooms_msg(self):
        pass
