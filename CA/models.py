import django
from django.db import models
from datetime import datetime, timedelta
from .utils import *
from django.utils import timezone

# Create your models here.
class PrsignUp(models.Model):
    name = models.CharField(max_length=30, default='')
    email = models.EmailField(default='')
    number = models.PositiveIntegerField()
    password = models.CharField(default='', max_length=15)
    confirmPassword = models.CharField(default='', max_length=15)
    link=models.CharField(max_length=55,default='')

    recommend_by=models.CharField(max_length=30,default='',blank=False)
    payment_due_date = models.DateField(default=datetime.now()+timedelta(days=15))
    ispaid = models.BooleanField(default=False)
    def __str__(self):
        return self.email

    def save(self,*args,**kwargs):
        code=genrated_ref_code()
        self.link="http://127.0.0.1:8000/prsignup/"+str(code)
        super().save(*args,**kwargs)




class CasignUp(models.Model):
    name = models.CharField(max_length=30, default='')
    email = models.EmailField(default='')
    number = models.PositiveIntegerField()
    password = models.CharField(default='', max_length=15)
    address = models.CharField(default='', max_length=100)
    confirmPassword = models.CharField(default='', max_length=15)
    link=models.CharField(max_length=55,default='')
    payment_due_date = models.DateField(default=datetime.now()+timedelta(days=15))
    created_by = models.CharField(default=0, max_length=100)
    totalNoOfReferrals = models.PositiveIntegerField(default=0)
    
    totalAmount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.email
         
    def save(self,*args,**kwargs):
        code=genrated_ref_code()
        self.link="http://127.0.0.1:8000/prsignup/"+str(code)
        super().save(*args,**kwargs)





class Offerings(models.Model):
    CA=models.ForeignKey(CasignUp,on_delete=models.CASCADE,null=True,blank=True)
    monthlyAmount = models.PositiveIntegerField(default=0)
    pendingAmount = models.PositiveIntegerField(default=0)
    isPaymentRecieved = models.BooleanField(default=False)
    paymentRecievedDate = models.DateTimeField(default=None, null=True, blank=True)
    joiningDate = models.DateTimeField(default=None, null=True, blank=True)
    tierName = models.CharField(default=0, max_length=15)
    tierNo = models.PositiveIntegerField(default=0)
    percentage = models.PositiveIntegerField(default=0)
    noReferals_paid=models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return self.tierName





# class CasignUp(models.Model):
#     name = models.CharField(max_length=30, default='')
#     email = models.EmailField(default='')
#     number = models.PositiveIntegerField()
#     password = models.CharField(default='', max_length=15)
#     confirmPassword = models.CharField(default='', max_length=15)
#     link=models.CharField(max_length=55,default='')
#     payment_due_date = models.DateField(default=datetime.now()+timedelta(days=15))
#     percentage = models.PositiveIntegerField(default=0)
#     totalNoOfReferrals = models.CharField(default=0, max_length=100)
#     amount = models.CharField(default=0, max_length=15)
#     def __str__(self):
#         return self.email


#     def save(self,*args,**kwargs):
#         code=genrated_ref_code()
#         self.link="http://127.0.0.1:8000/prsignup/"+str(code)
#         super().save(*args,**kwargs)    


# class Offerings(models.Model):
#     CA=models.ForeignKey(CasignUp,on_delete=models.CASCADE,null=True,blank=True)
#     created_by = models.CharField(default=0, max_length=100)
#     payment_date = models.DateTimeField(auto_now_add=True)
#     tier1 = models.PositiveIntegerField(default=0)  #0
#     tier2 = models.PositiveIntegerField(default=0)  #100
#     tier3 = models.PositiveIntegerField(default=0)  #200
#     percentage1 = models.PositiveIntegerField(default=10)
#     percentage2 = models.PositiveIntegerField(default=20)
#     percentage3 = models.PositiveIntegerField(default=30)

#     def __str__(self):
#         return self.CA.email
