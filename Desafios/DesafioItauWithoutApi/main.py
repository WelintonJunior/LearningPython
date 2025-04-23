from models import Transaction
from usecase import GetStatistics, CreateTransaction
import datetime as dt;

def __init__():
    transaction1 = Transaction(10.2, dt.datetime.now())
    CreateTransaction(transaction1)
    transaction2 = Transaction(15.2, dt.datetime.now())
    CreateTransaction(transaction2)

    statistics = GetStatistics()
    print(f"\n Count: {statistics.count} \n Sum: {statistics.sum} \n Avg: {statistics.avg} \n Min: {statistics.min} \n Max: {statistics.max}")

__init__()
