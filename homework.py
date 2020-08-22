import datetime as dt


class Record:
    def __init__(self, amount, comment, date = None): 
        self.amount = amount
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment 

class Calculator:
    def __init__(self,limit):
        self.limit = limit
        self.records = []
        self.remain = 0
    def add_record(self, Record):
        self.records.append(Record)
        return self.records
    def get_today_stats(self):
        today = dt.datetime.now().date()
        for record in self.records:
            if record.date == today:
                self.remain +=  record.amount
        return self.remain
    def get_week_stats(self):
        week = dt.datetime.now()- dt.timedelta(days = 6)
        for record in self.records:
            if week.date() <= record.date <= dt.datetime.now().date():
                self.remain += record.amount
        return self.remain

class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        total_calories = 0
        for record in self.records:
            if record.date == dt.date.today():
                total_calories += record.amount
        if total_calories < self.limit:
            remains = self.limit - total_calories
            answer = f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remains} кКал'
        else:
            answer =  f'Хватит есть!'
        return answer

class CashCalculator(Calculator):
    USD_RATE = 74.75
    EURO_RATE = 88.04
    def get_today_cash_remained(self, currency):
        total_spent = 0
        for record in self.records:
            if record.date == dt.date.today():
                total_spent += record.amount
        if total_spent < self.limit:
            if currency == 'rub':
                remains = self.limit - total_spent
                answer = f'На сегодня осталось {remains} руб'
            elif currency == 'usd':
                remains = round(self.limit / self.USD_RATE - total_spent / self.USD_RATE, 2)
                answer = f'На сегодня осталось {remains} USD'
            elif currency == 'eur':
                remains = round(self.limit / self.EURO_RATE - total_spent / self.EURO_RATE, 2)
                answer = f'На сегодня осталось {remains} Euro'
            return answer
        elif total_spent == self.limit:
            return 'Денег нет, держись'
        else:
            if currency == 'rub':
                remains = total_spent - self.limit
                answer = f'Денег нет, держись: твой долг - {remains} руб'
            elif currency == 'usd':
                remains = round(total_spent / self.USD_RATE - self.limit / self.USD_RATE, 2)
                answer = f'Денег нет, держись: твой долг - {remains} USD'
            elif currency == 'eur':
                remains = round(total_spent / self.EURO_RATE - self.limit / self.EURO_RATE, 2)
                answer = f'Денег нет, держись: твой долг - {remains} Euro'
            return answer