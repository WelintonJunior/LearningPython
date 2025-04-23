def __init__():
    pass

class NegativeValueException:
    pass

class Transaction:
    def __init__(self, value, date_hour):
        try:
            if value >= 0:
                self.value = value
            else:
                raise NegativeValueException
        except NegativeValueException:
            print("Value should be not negative or 0")
            
        self.date_hour = date_hour
    
class Statistics:
    def __init__(self, count = 0, sum = 0, avg = 0, min = 0, max = 0):
        self.count = count
        self.sum = sum
        self.avg = avg
        self.min = min
        self.max = max
    
    def set_count(self, count):
        self.count = count
    def set_sum(self, sum):
        self.sum = sum
    def set_avg(self, avg):
        self.avg = avg
    def set_min(self, min):
        self.min = min
    def set_max(self, max):
        self.max = max
