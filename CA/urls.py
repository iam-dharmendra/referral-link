from django.urls import path
from . import views

urlpatterns = [
            path('',views.MAINDASH,name='MAINDASH'),

            path('casignup/<str:ref_code>',views.SignupView,name='CASIGNUP'),
            path('calogin/',views.login,name='CALOGIN'),
            path('prsignup/<str:ref_code>',views.prSignupView,name='PRSIGNUP'),
            path('prlogin/',views.prlogin,name='PRLOGIN'),
            path('calogout/',views.userLogOut,name='CALOGOUT'),
            path('prlogout/',views.prLogOut,name='PRLOGOUT'),
            path('cadash/', views.dashboard, name='CADASHBOARD'),
            path('prdash/', views.PRdashboard, name='PRDASHBOARD'),
            path('amountCalculation/', views.amountCalculation, name='amountCalculation'),
            path('payment/', views.payment, name='payment'),
            path('prometers_by_ca/<int:id>', views.prometers_by_ca, name='prometers_by_ca'),

]
