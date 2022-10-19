from django.http import HttpResponse
from django.template import loader
from django.views.generic import CreateView
from .models import Transaction
from .forms import IncomeExpForm, DateForm
from Logic import DbQuery, TotalsLogic


class AddIncomeView(CreateView):
    model = Transaction
    form_class = IncomeExpForm
    template_name = 'addincome.html'

    def form_valid(self, form):
        form.instance.type = 'Income'
        return super().form_valid(form)


class AddExpView(CreateView):
    model = Transaction
    form_class = IncomeExpForm
    template_name = 'addExp.html'

    def form_valid(self, form):
        form.instance.type = 'Expenditure'
        return super().form_valid(form)


def TotalsView(request):
    template = loader.get_template('totals.html')
    dbAllData = DbQuery.getAllData()
    incomeExpQuery = DbQuery.queryTotal()
    income = incomeExpQuery[0]
    exp = incomeExpQuery[1]
    date1 = dbAllData[0].date
    date2 = dbAllData[len(dbAllData) - 1].date
    incomeBreakDown = 0
    expBreakDown = 0
    filterDateRangeDB = DbQuery.queryDbDateFilter(date1, date2)
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
            data = TotalsLogic.gatherDBDataWithDesc(DbQuery.queryDbDateFilter(date1, date2), description)
            expBreakDown, incomeBreakDown = TotalsLogic.breakdownCosts(expBreakDown, incomeBreakDown, data)
            filterDateRangeDB = data

        elif (date1 and date2) and not description:
            filterDateRangeDB = DbQuery.queryDbDateFilter(date1, date2)

            expBreakDown, incomeBreakDown = TotalsLogic.breakdownCosts(expBreakDown, incomeBreakDown, filterDateRangeDB)

        else:
            filterDateRangeDB = DbQuery.getAllData()

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
