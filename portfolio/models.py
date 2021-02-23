from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email')

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    cust_number = models.IntegerField(blank=False, null=False)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    email = models.EmailField(max_length=200)
    cell_phone = models.CharField(max_length=50)
    created_date = models.DateTimeField(
        default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.cust_number)


class Investment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='investments')
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    acquired_value = models.DecimalField(max_digits=10, decimal_places=2)
    acquired_date = models.DateField(default=timezone.now)
    recent_value = models.DecimalField(max_digits=10, decimal_places=2)
    recent_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.acquired_date = timezone.now()
        self.save()

    def updated(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.customer)

    def results_by_investment(self):
        return self.recent_value - self.acquired_value

class Stock(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='stocks')
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    shares = models.DecimalField (max_digits=10, decimal_places=1)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.customer)

    def initial_stock_value(self):
        return float(self.shares) * float(self.purchase_price)

    def current_stock_price(self):
        symbol_f = str(self.symbol)
        main_api = 'http://api.marketstack.com/v1/eod?'
        api_key = 'access_key=9aae7e6ad72a6dc8b6d998276798d7cf&limit=1&symbols='
        url = main_api + api_key + symbol_f
        json_data = requests.get(url).json()
        open_price = float(json_data["data"][0]["open"])
        share_value = open_price
        return share_value

    def current_stock_value(self):
        return float(self.current_stock_price()) * float(self.shares)

    def results_by_stock(self):
        return self.current_stock_value() - self.initial_stock_value()

class Mutualfund(models.Model):
    customer = models.ForeignKey(Customer, related_name='mutualfunds', on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    shares = models.DecimalField(max_digits=10, decimal_places=1)
    purchased_value = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_date = models.DateField(default=timezone.now)
    recent_value = models.DecimalField(max_digits=10, decimal_places=2)
    recent_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.customer)

    def results_by_mutualfund(self):
        return self.recent_value - self.purchased_value