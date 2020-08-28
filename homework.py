import datetime as dt

DATE_FORMAT = '%d.%m.%Y'


class Record:

    def __init__(self, amount, comment, date = None): 
        self.amount = amount
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()
        self.comment = comment 

class Calculator:
    TODAY = dt.datetime.now()

    def __init__(self,limit):
        self.limit = limit
        self.records = []

    def add_record(self, Record):
        self.records.append(Record)
        return self.records

    def get_today_stats(self):   
        return sum(
            record.amount 
            for record in self.records 
            if record.date == self.TODAY.date()
            )

    def get_week_stats(self):
        week = self.TODAY - dt.timedelta(days = 7)
        return sum(
            record.amount 
            for record in self.records 
            if week.date() <= record.date <= self.TODAY.date()
            )

class CaloriesCalculator(Calculator):
    ANSWER_POS = ('Сегодня можно съесть что-нибудь ещё,'
             ' но с общей калорийностью не более {value} кКал')
    ANSWER_NEG = 'Хватит есть!' 

    def get_calories_remained(self): 
        remained = self.limit - self.get_today_stats() 
        if remained > 0:
            return self.ANSWER_POS.format(value = remained)
        else: 
            return  self.ANSWER_NEG

class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1.0
    ANSWER_POS = 'На сегодня осталось {value} {cur}'
    ANSWER_NEG = 'Денег нет, держись: твой долг - {value} {cur}'

    RATE_DICT = {
        'usd':(USD_RATE,'USD'),
        'eur':(EURO_RATE,'Euro'),
        'rub':(RUB_RATE,'руб')
    }

    def get_today_cash_remained(self, currency):
        remained = self.get_today_stats()
        rate, name = self.RATE_DICT[currency]
        remains = round(
            self.limit / rate
            - 
            remained / rate, 
            2
            )
        if remained < self.limit:
            return self.ANSWER_POS.format(value = remains, cur = name) 
        elif remained > self.limit:
            return self.ANSWER_NEG.format(value = abs(remains), cur = name)
        else:
            return 'Денег нет, держись'