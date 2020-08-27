import datetime as dt

DATE_FORMAT = '%d.%m.%Y'
TODAY = dt.datetime.now()


class Record:

    def __init__(self, amount, comment, date = None): 
        self.amount = amount
        if date is None:
            self.date = TODAY.date()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()
        self.comment = comment 

class Calculator:

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
            if record.date == TODAY.date()
            )

    def get_week_stats(self):
        week = TODAY - dt.timedelta(days = 7)
        return sum(
            record.amount 
            for record in self.records 
            if week.date() <= record.date <= TODAY.date()
            )

class CaloriesCalculator(Calculator):
    ANSWER = ('Сегодня можно съесть что-нибудь ещё,'
             ' но с общей калорийностью не более {value} кКал')

    def get_calories_remained(self): 
        self.remain = self.limit - self.get_today_stats() 
        if self.remain > 0:
            return self.ANSWER.format(value = self.remain)
        else: 
            return  'Хватит есть!' 

class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1.0
    ANSWER_POS = 'На сегодня осталось {value} {cur}'
    ANSWER_NEG = 'Денег нет, держись: твой долг - {value} {cur}'

    rate_dict = {
        'usd':(USD_RATE,'USD'),
        'eur':(EURO_RATE,'Euro'),
        'rub':(RUB_RATE,'руб')
    }

    def get_today_cash_remained(self, currency):
        remained = self.get_today_stats()
        rate_name = self.rate_dict[currency][1]
        remains = round(
            self.limit / self.rate_dict[currency][0] 
            - 
            remained / self.rate_dict[currency][0], 
            2
            )
        if remained < self.limit:
            return self.ANSWER_POS.format(value = remains, cur = rate_name)
        elif remained > self.limit:
            return self.ANSWER_NEG.format(value = abs(remains), cur = rate_name)
        else:
            return 'Денег нет, держись'

cash_calculator = CaloriesCalculator(1000)
        
# дата в параметрах не указана, 
# так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=1000, comment="кофе")) 
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=0, comment="Серёге за обед"))
# а тут пользователь указал дату, сохраняем её
                
print(cash_calculator.get_calories_remained())