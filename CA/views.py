import email
from django.shortcuts import render,redirect
from django.http import HttpResponse
from razorpay import Payment
from requests import request
from .models import *
from django.contrib import messages
from datetime import datetime
# Create your views here.

# CA signup form
def SignupView(self, ref_code):
    if self.POST:
        Name = self.POST['name']
        Email = self.POST['email']
        Number = self.POST['number']
        Password = self.POST['password']
        ConfirmPassword = self.POST['confirmPassword']
        address = self.POST['address']

        tier1 = int(self.POST['tier1'])
        percentage1 = int(self.POST['percentage1'])
        tier2 = int(self.POST['tier2'])
        percentage2 = int(self.POST['percentage2'])
        tier3 = int(self.POST['tier3'])
        percentage3 = int(self.POST['percentage3'])
        created_by = self.POST['created_by']

        try:
            data=CasignUp.objects.get(email=Email)
            msg = 'Email already taken'

        except:     
            if  tier1==0 and tier2>tier1 and tier3 >tier2:
                
                if ConfirmPassword == Password:

                    CasignUp.objects.create(name = Name, email = Email, number = Number, password = Password, confirmPassword = ConfirmPassword,address = address)
                    data=CasignUp.objects.get(email=Email)
                   
                    Offerings.objects.create(CA=data,tierName='tier1',tierNo=0,percentage=percentage1,paymentRecievedDate=datetime.now())
                    Offerings.objects.create(CA=data,tierName='tier2',tierNo=tier2,percentage=percentage2,paymentRecievedDate=datetime.now())
                    Offerings.objects.create(CA=data,tierName='tier3',tierNo=tier3,percentage=percentage3,paymentRecievedDate=datetime.now())
                    return redirect('CALOGIN')

                else:
                   msg = 'Enter Same Password'
                    
            else:
                msg = 'please follow tier formate'

        return render(self , 'signup.html',{'msg':msg})
                                          

    return render(self,'signup.html')

# ca login
def login(self):
    if self.POST:
        em = self.POST.get('email')
        pass1 = self.POST.get('password')
        try:
            print("Inside first try block")
            check = CasignUp.objects.get(email = em)
            print("Email is ",em,check.email)
            if check.password == pass1:
                # print(check.Password)
                self.session['email'] = check.email
                return redirect('CADASHBOARD')
                # nameMsg = CasignUp.objects.get(email = em)
                # msg = 'User Successfully logged in'
                # print(msg)
                # return render(self, 'dashboard.html', {'key':nameMsg})
            else:
                return HttpResponse('Invalid Password')
        except:
            print("Inside first except block")
            return HttpResponse('Invalid Email ID')

    return render(self,'login.html')

#ca dashboard
def dashboard(request):
    if 'email' in request.session:
        try:
            # nameMsg = logged in user's email
            nameMsg = CasignUp.objects.get(email = request.session['email'])
            print(nameMsg.link,"This is the referral link")
            # obj = giving queryset of all promoter's data
            obj=PrsignUp.objects.filter(recommend_by=nameMsg.email)
            newdate = datetime.today().strftime('%Y-%m-%d')
            
            # amountHasToBePaid = 0
            # for i in obj:
            #     if i.ispaid == True:
            #         amountHasToBePaid += ((10000*20)/100)
            #     else:
            #         print(f"{i} user has not paid yet")
                    
        


            print('inside try dashboard')

            if newdate >= str(nameMsg.payment_due_date):
                msg = 'Please pay the payment'
            else:
                msg = f'You can use it till {nameMsg.payment_due_date}'
            print("redirct")
            return render(request, 'dashboard.html', {'key':nameMsg,'obj':obj,'len':len(obj), 'time' : msg})

        except:
            print("Inside except of dashboard section")
            del request.session['email']
            return redirect('CALOGIN')

    return redirect('CALOGIN')


def amountCalculation(request):
    if 'email' in request.session:
        per=0
        tier_selection=''
        nameMsg = CasignUp.objects.get(email = request.session['email'])
        print(nameMsg.email)
        obj=PrsignUp.objects.filter(recommend_by=nameMsg.email)

        offer1=Offerings.objects.filter(CA=nameMsg,tierName='tier1').last()
        print(offer1)
        offer2=Offerings.objects.filter(CA=nameMsg,tierName='tier2').last()
        print(offer2)
        offer3=Offerings.objects.filter(CA=nameMsg,tierName='tier3').last()
        print(offer3)

        if nameMsg.totalNoOfReferrals <= offer2.tierNo - 1:
            print('tier1')
            per=offer1.percentage
            tier_selection='tier1'
            noReferals_paid=offer1.noReferals_paid
          

        elif  nameMsg.totalNoOfReferrals >= offer2.tierNo and  nameMsg.totalNoOfReferrals <= offer3.tierNo - 1:  
            print('tier2')
            per=offer2.percentage 
            tier_selection='tier2'
            noReferals_paid=offer2.noReferals_paid
           
        elif nameMsg.totalNoOfReferrals >= offer3.tierNo :
            print('tier1')
            per=offer3.percentage
            tier_selection='tier3'
            noReferals_paid=offer3.noReferals_paid
           
        amountHasToBePaid = 0
        
        count=0
        for i in range(noReferals_paid,len(obj)):
            if obj[i].ispaid == True:
                amountHasToBePaid += ((10000*per)/100)
                count+=1
            else:
                print(f"{i} user has not paid yet")
        
        
        tier_selection=tier_selection[4]
        print(tier_selection) 

        if tier_selection=='1':
            offer1.monthlyAmount=amountHasToBePaid
            offer1.noReferals_paid+=count
            if offer1.isPaymentRecieved==False:
                offer1.pendingAmount=offer1.monthlyAmount
            else:
                offer1.pendingAmount=0
                # offer1.isPaymentRecieved=datetime.now()
            offer1.save()

        elif tier_selection=='2':
            offer2.monthlyAmount=amountHasToBePaid
            offer2.noReferals_paid+=count
           
            if offer2.isPaymentRecieved==False:
                offer2.pendingAmount=offer2.monthlyAmount
            else:
                offer2.pendingAmount=0
                # offer2.isPaymentRecieved=datetime.now()
            offer2.save()

        else :
            offer3.monthlyAmount=amountHasToBePaid
            offer3.noReferals_paid+=count
            if offer3.isPaymentRecieved==False:
                offer3.pendingAmount=offer3.monthlyAmount
            else:
                offer3.pendingAmount=0
                # offer3.isPaymentRecieved=datetime.now()
            offer3.save()



        total=nameMsg.totalAmount
        print(total,amountHasToBePaid)

        total+=amountHasToBePaid
        CasignUp.objects.filter(email = request.session['email']).update(totalAmount=total)
        
        print(amountHasToBePaid)
        return HttpResponse(amountHasToBePaid)
    return HttpResponse('amount')   
       
                

# promoter signup
def prSignupView(self,ref_code):
    if self.POST:
        Name = self.POST['name']
        Email = self.POST['email']
        Number = self.POST['number']
        Password = self.POST['password']
        ConfirmPassword = self.POST['confirmPassword']
        try:
            data=PrsignUp.objects.filter(email=Email)
            if data:
                msg = 'Email already taken'
                return render(self , 'prsignup.html',{'msg':msg})
            elif ConfirmPassword == Password:
                v = PrsignUp(name = Name, email = Email, number = Number, password = Password, confirmPassword = ConfirmPassword)
                try:
                        d=CasignUp.objects.get(link="http://127.0.0.1:8000/prsignup/"+ref_code)
                except:
                        d=PrsignUp.objects.get(link="http://127.0.0.1:8000/prsignup/"+ref_code)
                print(d.id)
                v.recommend_by=d.email
                v.save()
            # --------------------------------------------------------------------------------
                q1 = PrsignUp.objects.filter(recommend_by = d.email)
                d.totalNoOfReferrals = len(q1)     
                d.save()
                return redirect('PRLOGIN')
            else:
                msg = 'Enter Same Password'
                return render(self , 'prsignup.html',{'msg':msg},{'ref_code':ref_code})                  
        except:
            msg = 'Invalid email id'
            return render(self , 'prsignup.html',{'msg':msg})

    return render(self,'prsignup.html')


# promoter login
def prlogin(self):
    if self.POST:
        em = self.POST.get('email')
        pass1 = self.POST.get('password')
        try:
            print("Inside first try block")
            check = PrsignUp.objects.get(email = em)
            print("Email is ",em,check.email)
            if check.password == pass1:
                self.session['email'] = check.email
                return redirect('PRDASHBOARD')
                
            else:
                return HttpResponse('Invalid Password')
        except:
            print("Inside first except block")
            return HttpResponse('Invalid Email ID')
    return render(self,'prlogin.html')    


# dashboard for promoter    
def PRdashboard(request):
    if 'email' in request.session:
        print("Inside promoter dashboard")
        try:
            nameMsg = PrsignUp.objects.get(email =  request.session['email'])  
            obj=PrsignUp.objects.filter(recommend_by=nameMsg.email)

            print(obj)
            due_id = PrsignUp.objects.get(id=nameMsg.id)
            newdate = datetime.today().strftime('%Y-%m-%d')
            if newdate >= str(due_id.payment_due_date):
                z = 'Please pay the payment'
            else:
                z = f'You can use it till {due_id.payment_due_date}'
            return render(request, 'prdashboard.html', {'key':nameMsg,'obj':obj,'len':len(obj), 'time' : z })
        except:
            del request.session['email']
            return redirect('PRLOGIN')
    return redirect('PRLOGIN')

# ca logout
def userLogOut(request):
    del request.session['email']
    print('User logged out')
    return redirect('CALOGIN')

# pr logout
def prLogOut(request):
    del request.session['email']
    print('User logged out')
    return redirect('PRLOGIN')    

# ca timeout
def timeout1(request):
    if 'email' in request.session:
        v=CasignUp.objects.get(email=request.session['email'])
        due_id = CasignUp.objects.get(id=v.id)
        newdate = datetime.today().strftime('%Y-%m-%d')
        print("This is new date", newdate)
        print("This is due date",str(due_id.payment_due_date))
        if newdate >= str(due_id.payment_due_date):
            return HttpResponse('Please pay the payment')
        else:
            return HttpResponse(f'You can use it till {due_id.payment_due_date}')
    return redirect('CALOGIN')

# pr timeout
def PRtimeout(request):
    if 'email' in request.session:

        due_id = PrsignUp.objects.get(email=request.session['email'])
        print(due_id, "this is the due_id1")

        # due_id = PrsignUp.objects.get(id=PrsignUp.objects.get(email=request.session['email']).id)
        newdate = datetime.today().strftime('%Y-%m-%d')
        # print("This is new date", newdate)
        # print("This is due date",str(due_id.payment_due_date))
        if newdate >= str(due_id.payment_due_date):
            return HttpResponse(f'{due_id} Please pay the payment')
        else:
            print(f'You can use it till {due_id.payment_due_date}')
            return HttpResponse(f'You can use it till {due_id.payment_due_date}')
    return redirect('PRLOGIN')

# Dashboard for main Host
def MAINDASH(request):
    li = []
    caobj =  CasignUp.objects.all()
    probj =  PrsignUp.objects.all()
    for i in caobj:
        caRefCount = PrsignUp.objects.filter(recommend_by = i.email)
        li.append(len(caRefCount))
    link  = 'http://127.0.0.1:8000/casignup/j75mnhd67v4m18r'
    
    context = {
        'caobj': caobj,
        'probj': probj,        
        'calen': len(caobj),
        'prlen': len(probj),
        'link' : link,
        'li' : li,
    }
    return render(request, 'maindash.html', context)


def payment(request):
    if 'email' in request.session:
        nameMsg = CasignUp.objects.get(email = request.session['email'])
        offer1=Offerings.objects.filter(CA=nameMsg,tierName='tier1').last()
        print('offer1')
        offer2=Offerings.objects.filter(CA=nameMsg,tierName='tier2').last()
        print('offer2')
        offer3=Offerings.objects.filter(CA=nameMsg,tierName='tier3').last()
        print('offer3')
    
        if nameMsg.totalNoOfReferrals <= offer2.tierNo - 1:
            
            tier_selection='tier1'
           
        elif  nameMsg.totalNoOfReferrals >= offer2.tierNo and  nameMsg.totalNoOfReferrals <= offer3.tierNo - 1:  
          
            tier_selection='tier2'
           
        elif nameMsg.totalNoOfReferrals >= offer3.tierNo :
         
            tier_selection='tier3'
            
        tier_selection=tier_selection[4]

        print(tier_selection) 
        if tier_selection=='1':
            offer1.paymentRecievedDate=datetime.now()
            offer1.isPaymentRecieved=True
            REF=offer1.noReferals_paid
            offer1.save()
            Offerings.objects.create(CA=nameMsg,tierNo=offer1.tierNo,percentage=offer1.percentage,tierName='tier1',noReferals_paid=REF,joiningDate=datetime.now())
        elif tier_selection=='2':
            offer2.paymentRecievedDate=datetime.now()
            offer2.isPaymentRecieved=True
            REF=offer2.noReferals_paid
            offer2.save()
            Offerings.objects.create(CA=nameMsg,tierNo=offer2.tierNo,percentage=offer2.percentage,tierName='tier2',noReferals_paid=REF,joiningDate=datetime.now())
    
        else :
            offer3.paymentRecievedDate=datetime.now()
            offer3.isPaymentRecieved=True
            REF=offer3.noReferals_paid
            offer3.save()
            Offerings.objects.create(CA=nameMsg,tierNo=offer3.tierNo,percentage=offer3.percentage,tierName='tier3',noReferals_paid=REF,joiningDate=datetime.now())


    return HttpResponse('paid succesfully')         





