# holds some values to be printed in the log
class Logger:
    def __init__(self, name=None, count=0):
        self.name = name
        self.count = count

    def display_name(self):
        print("name: " + self.name)

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def increment_num(self):
        self.count += 1

    def get_count(self):
        return self.count
