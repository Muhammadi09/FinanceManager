from django.db import models
from django.urls import reverse
from django.conf import settings


class Transaction(models.Model):
    Income = 'Income'
    Expenditure = 'Expenditure'

    all_types = [
        (Income, 'Income'),
        (Expenditure, 'Expenditure'),
    ]
    type = models.CharField(max_length=15, choices=all_types, default=Income,)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(auto_now=False, auto_now_add=False)
    description = models.CharField(max_length=150)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        string_builder = "{0} | {1} | {2} | {3}".format(self.date, self.type, self.description, self.user)
        return string_builder

    def get_absolute_url(self):
        return reverse('home')