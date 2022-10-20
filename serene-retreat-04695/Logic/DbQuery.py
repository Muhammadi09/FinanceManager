from banking.models import Transaction

def getAllData(userId):
    model = Transaction
    query = model.objects.all()
    filteredData = []

    for data in query:
        if data.user.pk == userId:
            filteredData.append(data)

    return filteredData

def queryDbDateFilter(d1, d2, userId):
    model = Transaction
    query = model.objects.filter(date__range=[d1, d2])
    filteredData = []

    for data in query:
        if data.user.pk == userId:
            filteredData.append(data)

    return filteredData

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

