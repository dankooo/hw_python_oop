import datetime as dt

date_format = '%d.%m.%Y'


class Record:

    def __init__(self, amount, comment, date = None): 
        self.amount = amount
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()
        self.comment = comment 

class Calculator:
    today = dt.datetime.now().date()

    def __init__(self,limit):
        self.limit = limit
        self.records = []
        self.remain = 0

    def add_record(self, Record):
        self.records.append(Record)
        return self.records

    def get_today_stats(self):   
        self.remain = sum(record.amount for record in self.records if record.date == self.today)
        return self.remain

    def get_week_stats(self):
        week = dt.datetime.now() - dt.timedelta(days = 6)
        self.remain = sum(record.amount for record in self.records if week.date() <= record.date <= self.today)
        return self.remain

class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        self.remain = self.get_today_stats()
        if self.remain < self.limit:
            self.remain = self.limit - self.remain
            answer = f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {self.remain} кКал'
        else:
            answer =  f'Хватит есть!'
        return answer

class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1.0

    rate_dict = {
        USD_RATE: 'usd',
        EURO_RATE: 'eur',
        RUB_RATE: 'rub'
    }

    rate_sign = {
        'usd': 'USD',
        'eur': 'Euro',
        'rub': 'руб'
    }

    def get_today_cash_remained(self, currency):
        remained = abs(self.remain - self.get_today_stats())
        for rate in self.rate_dict:
            if self.rate_dict[rate] == currency:
                rate_name = self.rate_sign[self.rate_dict[rate]]
                remains = round(self.limit / rate - remained / rate, 2)
                if remained < self.limit:
                    answer = f'На сегодня осталось {remains} {rate_name}'
                    return answer
                elif remained == self.limit:
                    return 'Денег нет, держись'
                else:
                    answer = f'Денег нет, держись: твой долг - {abs(remains)} {rate_name}'
                    
                    return answer
        return 'Неизвестная валюта'