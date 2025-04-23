from models import Statistics

def __init__():
    pass

transactions = []

def GetStatistics():
    statisticsToBeCalculated = []

    for each in transactions:
        # if (dt.datetime.now().second - each.date_hour.second) <= dt.time.:
        statisticsToBeCalculated.append(each)

    statisticsToBeReturned = Statistics()
    sumOfValues = 0

    for each in statisticsToBeCalculated:
        sumOfValues += each.value
        statisticsToBeReturned.set_count(len(statisticsToBeCalculated))
        statisticsToBeReturned.set_sum(sumOfValues)
        statisticsToBeReturned.set_avg(len(statisticsToBeCalculated))
        statisticsToBeReturned.set_min(len(statisticsToBeCalculated))
        statisticsToBeReturned.set_max(len(statisticsToBeCalculated))
    return statisticsToBeReturned

def CreateTransaction(transaction):
    transactions.append(transaction)

def DeleteTransaction():
    transactions.clear()

    