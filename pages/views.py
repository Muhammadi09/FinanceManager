from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from banking.models import Transaction
from Logic.DbQuery import queryDbDateFilter
import datetime

import calendar

def retrieveTransactionDataForMonth(request):
    model = Transaction
    userId = request.user.pk
    payDay = 20
    cycleStartDate = datetime.datetime.now().date()
    todaysDate = datetime.datetime.now()

    if cycleStartDate.day != payDay:

        if cycleStartDate.day > payDay:
            cycleStartDate = datetime.datetime(cycleStartDate.year, cycleStartDate.month, 20)
        else:
            cycleStartDate = datetime.datetime(cycleStartDate.year, cycleStartDate.month-1, 20)

    # GET THE RANGE FROM cycleStartDate to today - SHOW ALL DATA WITHIN THAT RANGE
    query = queryDbDateFilter(cycleStartDate, todaysDate, userId)

    income = 0
    expenditure = 0

    for data in query:
        if data.type == "Income":
            income+=data.amount
        else:
            expenditure+=data.amount

    dataIncomeExp = (income, expenditure)

    return dataIncomeExp

def HomePageView(request):

    if request.user.is_authenticated:

        currentMonth = calendar.month_name[datetime.datetime.now().month]
        previousMonth = calendar.month_name[datetime.datetime.now().date().month - 1]

        if datetime.datetime.today().date().day == 20:
            previousMonth = currentMonth
            currentMonth = calendar.month_name[datetime.datetime.now().date().month + 1]

        datesFiltered = retrieveTransactionDataForMonth(request)
        remaining = datesFiltered[0] - datesFiltered[1]


        template = loader.get_template('pages/home.html')
        context = locals()
        context['currentMonth'] = currentMonth
        context['prevousMonth'] = previousMonth
        context['data'] = datesFiltered
        context['remaining'] = remaining
        return HttpResponse(template.render(context, request))

    return HttpResponseRedirect(reverse('login'))

