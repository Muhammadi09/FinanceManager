from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.generic import CreateView
from .models import Transaction
from .forms import IncomeExpForm, DateForm
from Logic import DbQuery, TotalsLogic
import datetime

class AddIncomeView(CreateView):
    model = Transaction
    form_class = IncomeExpForm
    template_name = 'addincome.html'

    def form_valid(self, form):
        form.instance.type = 'Income'
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddExpView(CreateView):
    model = Transaction
    form_class = IncomeExpForm
    template_name = 'addExp.html'

    def form_valid(self, form):
        form.instance.type = 'Expenditure'
        form.instance.user = self.request.user
        return super().form_valid(form)


def TotalsView(request):
    if request.user.is_authenticated:
        userId = request.user.pk
        template = loader.get_template('totals.html')
        dbAllData = DbQuery.getAllData(userId)
        incomeExpQuery = DbQuery.queryTotal()
        income, exp = 0, 0
        date1 = datetime.date(datetime.datetime.today().year, 1, 1)
        date2 = datetime.datetime.today().date()
        incomeBreakDown = 0
        expBreakDown = 0



        for data in dbAllData:
            if data.type == 'Income':
                income+=data.amount
            else:
                exp+=data.amount



        filterDateRangeDB = DbQuery.queryDbDateFilter(date1, date2, userId)
        # submitbutton = request.POST.get("submit")

        # GETTING DATA FROM FORM AND PROCESSINGS
        form = DateForm(request.POST or None)
        if form.is_valid():
            date1 = form.cleaned_data.get("date1")
            date2 = form.cleaned_data.get("date2")
            description = form.cleaned_data.get("description")

            if description and not (date1 or date2):
                data = TotalsLogic.gatherDBDataWithDesc(dbAllData, description)
                # UPDATE INCOME AND EXP BREAKDOWN
                expBreakDown, incomeBreakDown = TotalsLogic.breakdownCosts(expBreakDown, incomeBreakDown, data)
                # PASSING IN THE DATA FROM GATHERTRANSACTION TO FILTERDATERANGEDB
                filterDateRangeDB = data

            elif description and (date1 and date2):
                data = TotalsLogic.gatherDBDataWithDesc(DbQuery.queryDbDateFilter(date1, date2, userId), description)
                expBreakDown, incomeBreakDown = TotalsLogic.breakdownCosts(expBreakDown, incomeBreakDown, data)
                filterDateRangeDB = data

            elif (date1 and date2) and not description:
                filterDateRangeDB = DbQuery.queryDbDateFilter(date1, date2, userId)

                expBreakDown, incomeBreakDown = TotalsLogic.breakdownCosts(expBreakDown, incomeBreakDown, filterDateRangeDB)

            else:
                filterDateRangeDB = DbQuery.getAllData(userId)

        context = {
            'form': form,
            'date1': date1,
            'date2': date2,
            'income': income,
            'exp': exp,
            'incomeBreakDown': incomeBreakDown,
            'expBreakDown': expBreakDown,
            'filterDateRangeDB': filterDateRangeDB,
            # 'submitbutton': submitbutton
        }

        return HttpResponse(template.render(context, request))

    return HttpResponseRedirect(reverse('login'))
