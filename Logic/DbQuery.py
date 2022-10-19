from banking.models import Transaction

def getAllData():
    model = Transaction
    query = model.objects.all()
    return query

def queryDbDateFilter(d1, d2):
    model = Transaction
    query = model.objects.filter(date__range=[d1, d2])
    return query

def queryTotal():
    model = Transaction
    query = model.objects.all()
    income = 0
    exp = 0
    for data in query:
        if data.type == "Income":
            income+=data.amount
        else:
            exp+=data.amount

    dataIncomeExp = (income, exp)

    return dataIncomeExp

