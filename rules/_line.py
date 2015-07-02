class Line(object):
    def __init__(self, line_num, line_real,line_altered):
        self.num = line_num

        self.real = line_real
        self.altered = line_altered

    def __repr__(self):
        return str(self.num)+": "+self.real.rstrip()
