from django.urls import path
from .views import AddIncomeView, AddExpView, TotalsView

urlpatterns = [
    path('addincome/', AddIncomeView.as_view(), name='addincome'),
    path('addexp/', AddExpView.as_view(), name='addexp'),
    path('totals/', TotalsView, name='totals'),
]