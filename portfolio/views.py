from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer
from django.contrib.auth import views as auth_views, forms as auth_forms
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'portfolio/signup.html'

now = timezone.now()
def home(request):
   return render(request, 'portfolio/home.html',
                 {'portfolio': home})

@login_required
def customer_new(request):
   if request.method == "POST":
       form = CustomerForm(request.POST)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.created_date = timezone.now()
           customer.save()
           return render(request, 'portfolio/customer_list.html',
                         {'customer': customer})
   else:
       form = CustomerForm()
       # print("Else")
   return render(request, 'portfolio/customer_new.html', {'form': form})

@login_required
def customer_list(request):
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'portfolio/customer_list.html',
                 {'customers': customer})

@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           customer = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'portfolio/customer_list.html',
                         {'customers': customer})
   else:
        # edit
       form = CustomerForm(instance=customer)
   return render(request, 'portfolio/customer_edit.html', {'form': form})

@login_required
def customer_delete(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   customer.delete()
   return redirect('portfolio:customer_list')

@login_required
def stock_list(request):
   stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/stock_list.html', {'stocks': stocks})

@login_required
def stock_new(request):
   if request.method == "POST":
       form = StockForm(request.POST)
       if form.is_valid():
           stock = form.save(commit=False)
           stock.created_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html',
                         {'stocks': stocks})
   else:
       form = StockForm()
       # print("Else")
   return render(request, 'portfolio/stock_new.html', {'form': form})

@login_required
def stock_edit(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   if request.method == "POST":
       form = StockForm(request.POST, instance=stock)
       if form.is_valid():
           stock = form.save()
           # stock.customer = stock.id
           stock.updated_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html', {'stocks': stocks})
   else:
       # print("else")
       form = StockForm(instance=stock)
   return render(request, 'portfolio/stock_edit.html', {'form': form})

@login_required
def stock_delete(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   stock.delete()
   return redirect('portfolio:stock_list')

@login_required
def investment_list(request):
   investments = Investment.objects.filter(recent_date__lte=timezone.now())
   return render(request, 'portfolio/investment_list.html', {'investments': investments})

@login_required
def investment_new(request):
   if request.method == "POST":
       form = InvestmentForm(request.POST)
       if form.is_valid():
           investment = form.save(commit=False)
           investment.created_date = timezone.now()
           investment.save()
           investments = Investment.objects.filter(recent_date__lte=timezone.now())
           return render(request, 'portfolio/investment_list.html',
                         {'investments': investments})
   else:
       form = InvestmentForm()
       # print("Else")
   return render(request, 'portfolio/investment_new.html', {'form': form})

@login_required
def investment_edit(request, pk):
   investment = get_object_or_404(Investment, pk=pk)
   if request.method == "POST":
       form = InvestmentForm(request.POST, instance=investment)
       if form.is_valid():
           investment = form.save()
           # investment.customer = investment.id
           investment.updated_date = timezone.now()
           investment.save()
           investments = Investment.objects.filter(recent_date__lte=timezone.now())
           return render(request, 'portfolio/investment_list.html', {'investments': investments})
   else:
       # print("else")
       form = InvestmentForm(instance=investment)
   return render(request, 'portfolio/investment_edit.html', {'form': form})

@login_required
def investment_delete(request, pk):
   investment = get_object_or_404(Investment, pk=pk)
   investment.delete()
   return redirect('portfolio:investment_list')

@login_required
def portfolio(request,pk):
   global sum_purchased_value, sum_recent_value_mutual, result_mutual
   customer = get_object_or_404(Customer, pk=pk)
   customers = Customer.objects.filter(created_date__lte=timezone.now())
   investments =Investment.objects.filter(customer=pk)
   stocks = Stock.objects.filter(customer=pk)
   mutualfunds = Mutualfund.objects.filter(customer=pk)
   sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
   sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
   #overall_investment_results = sum_recent_value-sum_acquired_value
   # Initialize the value of the stocks
   sum_current_stocks_value = 0
   sum_of_initial_stock_value = 0
   sum_of_initial_investment_value = 0
   sum_current_investment_value = 0
   investment_result = 0

   # Loop through each stock and add the value to the total
   for stock in stocks:
        sum_current_stocks_value += stock.current_stock_value()
        sum_of_initial_stock_value += stock.initial_stock_value()

   for investment in investments:
       sum_of_initial_investment_value += investment.acquired_value
       sum_current_investment_value += investment.recent_value
       investment_result += investment.results_by_investment()

   # for mutualfund in mutualfunds:
   sum_purchased_value = mutualfunds.aggregate(Sum('purchased_value'))
   sum_recent_value_mutual = mutualfunds.aggregate(Sum('recent_value'))
   result_mutual = mutualfunds.aggregate(sum_result=Sum('recent_value') - Sum('purchased_value'))

   portfolio_initial_investment = float(sum_of_initial_investment_value) + float(sum_of_initial_stock_value)
   portfolio_current_investment = float(sum_current_investment_value) + float(sum_current_stocks_value)

   return render(request, 'portfolio/portfolio.html', {'customers': customers,
                                                       'investments': investments,
                                                       'stocks': stocks,
                                                       'mutualfunds': mutualfunds,
                                                       'sum_purchased_value': sum_purchased_value,
                                                       'sum_recent_value_mutual': sum_recent_value_mutual,
                                                       'result_mutual': result_mutual,
                                                       'sum_acquired_value': sum_acquired_value,
                                                       'sum_recent_value': sum_recent_value,
                                                       'sum_current_stocks_value': sum_current_stocks_value,
                                                       'sum_of_initial_stock_value': sum_of_initial_stock_value,
                                                       'sum_of_initial_investment_value': float(sum_of_initial_investment_value),
                                                       'sum_current_investment_value': float(sum_current_investment_value),
                                                       'investment_result': float(investment_result),
                                                       'portfolio_initial_investment': portfolio_initial_investment,
                                                       'portfolio_current_investment': portfolio_current_investment,})

# List at the end of the views.py
# Lists all customers
class CustomerList(APIView):

    def get(self,request):
        customers_json = Customer.objects.all()
        serializer = CustomerSerializer(customers_json, many=True)
        return Response(serializer.data)

#Mutualfund added

def mutualfund_list(request):
    mutualfunds = Mutualfund.objects.filter( purchased_date__lte=timezone.now())
    return render(request, 'portfolio/mutualfund_list.html' , {'mutualfunds': mutualfunds})


@ login_required
def mutualfund_new(request):
    if request.method == "POST" :
        form = MutualfundForm(request.POST)
        if form.is_valid():
            mutualfund = form.save(commit=False)
            mutualfund.created_date = timezone.now()
            mutualfund.save()
            mutualfunds = Mutualfund.objects.filter( purchased_date__lte=timezone.now())
            return render(request, 'portfolio/mutualfund_list.html', {'mutualfunds': mutualfunds})
    else :
        form = MutualfundForm()
        # print("Else")
        return render(request, 'portfolio/mutualfund_new.html', { 'form': form})


@ login_required
def mutualfund_edit(request, pk):
    mutualfund = get_object_or_404(Mutualfund, pk=pk)
    if request.method == "POST":
        form = MutualfundForm(request.POST, instance=mutualfund)
        if form.is_valid():
            mutualfund = form.save()
            # investment.customer = investment.id
            mutualfund.updated_date = timezone.now()
            mutualfund.save()
            mutualfunds = Mutualfund.objects.filter(purchased_date__lte=timezone.now())
            return render(request, 'portfolio/mutualfund_list.html', {'mutualfunds': mutualfunds})
    else:
        # print("else")
        form = MutualfundForm(instance=mutualfund)
        return render(request, 'portfolio/mutualfund_edit.html', {'form': form})


@ login_required
def mutualfund_delete(request, pk):
    mutualfund = get_object_or_404(Mutualfund, pk =pk)
    mutualfund.delete()
    mutualfunds = Mutualfund.objects.filter( purchased_date__lte=timezone.now())
    return render(request, 'portfolio/mutualfund_list.html', { 'mutualfunds': mutualfunds})

class ChangePasswordResetDoneView(auth_views.PasswordChangeView):
    form_class = auth_forms.PasswordChangeForm
    template_name = 'portfolio/password_change.html'
    success_url = reverse_lazy('portfolio:password_changedone')

class ChangePasswordResetDoneSuccessView(auth_views.PasswordChangeView):
    form_class = auth_forms.PasswordChangeForm
    template_name = 'portfolio/password_changedone.html'

class PasswordResetView(auth_views.PasswordResetView):
    form_class = auth_forms.PasswordResetForm
    template_name = 'portfolio/reset_password.html'
    email_template_name = 'portfolio/reset_password_email.html'
    success_url = reverse_lazy('portfolio:reset_password_done')

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    form_class = auth_forms.PasswordResetForm
    template_name = 'portfolio/reset_password_done.html'
    #success_url = reverse_lazy('reset_password_done')

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = auth_forms.SetPasswordForm
    template_name = 'portfolio/reset_password_confirm.html'
    success_url = reverse_lazy('portfolio:reset_password_complete')

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    form_class = auth_forms.PasswordResetForm
    template_name = 'portfolio/reset_password_complete.html'
    #success_url = reverse_lazy('login.html')