from django.conf.urls import url
from . import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SignUpView, ChangePasswordResetDoneSuccessView, ChangePasswordResetDoneView

app_name = 'portfolio'
urlpatterns = [
    path('', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('customer/create/', views.customer_new, name='customer_new'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('stock_list', views.stock_list, name='stock_list'),
    path('stock/create/', views.stock_new, name='stock_new'),
    path('stock/<int:pk>/edit/', views.stock_edit, name='stock_edit'),
    path('stock/<int:pk>/delete/', views.stock_delete, name='stock_delete'),
    path('investment_list', views.investment_list, name='investment_list'),
    path('investment/create/', views.investment_new, name='investment_new'),
    path('investment/<int:pk>/edit/', views.investment_edit, name='investment_edit'),
    path('investment/<int:pk>/delete/', views.investment_delete, name='investment_delete'),
    url(r'^mutualfund/$', views.mutualfund_list, name='mutualfund_list'),
    url(r'^mutualfund/(?P<pk>\d+)/delete/$', views.mutualfund_delete, name='mutualfund_delete'),
    url(r'^mutualfund/(?P<pk>\d+)/edit/$', views.mutualfund_edit, name='mutualfund_edit'),
    url(r'^mutualfund/create/$', views.mutualfund_new, name='mutualfund_new'),
    path('customer/<int:pk>/portfolio/', views.portfolio, name='portfolio'),
    url(r'^customers_json/', views.CustomerList.as_view()),
    path('password-change/', ChangePasswordResetDoneView.as_view(), name='password-change'),
    path('password_changedone/', ChangePasswordResetDoneSuccessView.as_view(), name = 'password_changedone'),
    path('reset_password/', views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password/done/', views.PasswordResetDoneView.as_view(), name='reset_password_done'),
    path('reset_confirmation/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(), name='reset_password_confirmation'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='reset_password_complete'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
urlpatterns = format_suffix_patterns(urlpatterns)