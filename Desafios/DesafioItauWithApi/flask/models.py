def __init__():
    pass

class Transaction:
    def __init__(self, value, dateHour):
        self.value = value
        self.dateHour = dateHour

class Statistics:
    def __init__(self, transactions):
        values = [t.value for t in transactions]
        
        self.count = len(values)
        self.sum = round(sum(values, 2) if values else 0)
        self.avg = round(self.sum / self.count, 3) if self.count > 0 else 0
        self.min = round(min(values), 2) if values else 0
        self.max = round(max(values), 2) if values else 0
    
    def to_dict(self):
        return {
            "count": self.count,
            "sum": self.sum,
            "avg": self.avg,
            "min": self.min,
            "max": self.max
        }