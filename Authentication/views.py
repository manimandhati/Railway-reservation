from base64 import urlsafe_b64decode, urlsafe_b64encode
from email.message import EmailMessage
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from login import settings
##from django.core.mail import send_mail
#from django.contrib.sites.shortcuts import get_current_site
#from django.template.loader import render_to_string
from django.utils.http import *
from django.utils.encoding import *
from . tokens import generate_token
from . models import trains,Books,payment

# Create your views here.
def home(request):
    return render(request,"index.html")
def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email'] 
        pw=request.POST['pw'] 
        cpw=request.POST['cpw']

        if User.objects.filter(username=username):
            messages.error(request,"Username already exist Please enter other username")
            return redirect('home')
        if User.objects.filter(email=email):
            messages.error(request,"email already used")
            return redirect('home') 
        if len(username)>10:
            messages.error(request,"USername must be under 10 characters") 
        if len(pw)<6:
            messages.error(request,"Please enter Strong password")
        if pw!=cpw:
            messages.error(request,"Passwords must be same") 
        if not username.isalnum():
            messages.error(request,"Username must be alphabets") 
            return redirect('home')


        user=User.objects.create_user(username,email,pw) 
        user.first_name=fname
        user.last_name=lname
        user.save()
        messages.success(request,"Your Account is Successfully Created. ") 

        ''' subject="Welcome to KNRRR group of industries" 
        message='Hello '+user.first_name+"!! \n"+"Welcome to KNRRR group of industries \n Thank you visiting our website \n We have also sent you a confrimation mail ,  please confirm your mail address in order to activate your account. \n\n\n Thanking you \n\n\n KATKAM NITHIN REDDY" 
        from_email=settings.EMAIL_HOST_USER 
        to_list=[user.email] 
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        current_site=get_current_site(request)
        email_subject="Confirm your email @katkamnithi"
        message2=render_to_string('email.html',{
            'name':user.first_name,
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user),
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.fail_silently = True
        email.send()'''


        return redirect('signin')

    return render(request,"signup.html")

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_b64decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user,token):
        user.is_active = True
        # user.profile.signup_confirmation = True
        user.save()
        login(request,user)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')

def signin(request):
    if request.method=="POST":
        username=request.POST['username'] 
        pw=request.POST['pw'] 
        user=authenticate(username=username,password=pw)
        if user is not None:
            login(request,user) 
            fname=user.first_name
            return render(request,"index.html",{'fname':fname})
        else:
            return render(request,'signin.html',{'msg':"PLEASE CHECK YOUR DETAILS"})

    return render(request,"signin.html")


def signout(request):
    logout(request)
    messages.success(request,"logged out sucess")
    return redirect('home')


def show(request):
    l=trains.objects.all()
    use=User.objects.all()
    return render(request,'show.html',{'data':l,'user':use})
 
def add(request):
    #add train to database
    l = []
    if request.method=="POST":
        train_name=request.POST['train_name']
        train_number=request.POST['trainnumber']
        source=request.POST['source']
        destination=request.POST['destination']
        date=request.POST['date']
        time=request.POST['time']
        seats_available=request.POST['seats_available']
        price=request.POST['price']
        l.append(train_name)
        l.append(train_number)
        l.append(source)
        l.append(destination)
        l.append(date)
        l.append(time)
        l.append(seats_available)
        l.append(price)
        print(l)
        train=trains(trainname=train_name,trainnumber=train_number,source=source,destination=destination,date=date,time=time,seats=seats_available,price=price)
        train.save()
        
    return render(request,'add.html')
def search(request):
    global trains
    if request.method=="POST":
        source=request.POST['source']
        destination=request.POST['destination']
        train=trains.objects.filter(source=source,destination=destination)
        return render(request,'show.html',{'data':train})
    return render(request,'search.html',)

def booking(request):
    ll = []
    if request.method=="POST":
        trainnumber=request.POST['trainnumber']
        source=request.POST['source']
        destination=request.POST['destination']
        personname=request.POST['personname']
        email=request.POST['email']
        agee=request.POST['age'] 
        genderr=request.POST['gender']
        ll.append(trainnumber)
        ll.append(source)
        ll.append(destination)
        ll.append(personname)
        ll.append(email)
        ll.append(agee)
        ll.append(genderr)
        tt=trains.objects.get(trainnumber=trainnumber)
        if tt.seats=='0':
            return render(request,"error.html",{'msg':"seats full"})
        tt.seats=str(int(tt.seats)-1)
        print(ll)
        book=Books(trainnumber=trainnumber,source=source,destination=destination,personname=personname,email=email,age=agee,gender=genderr)
        book.save()
        
    return render(request,"mybookings.html")
    

def mybookings(request):
    if request.user.is_authenticated:
        p = Books.objects.filter(email=request.user.email)
        return render(request, 'mybookings.html', {'persons': p})

def makepayment(request):
    m=[]
    if request=="POST":
        statuss=request.POST['status']
        amountpaid=request.POST['amount']
        m.append(statuss)
        m.append(amountpaid)
        pay=payment(status=statuss,amount=amountpaid)
        pay.save()
    return render(request,"makepayment.html")
    




def bookform(request):
    t = trains.objects.all()
    sources = []
    destinations = []
    trainno=[]
    for i in t:
        sources.append(i.source)
        destinations.append(i.destination)
        trainno.append(i.trainnumber)
    sources = list(set(sources))
    destinations = list(set(destinations))
    trainno=list(set(trainno))

    return render(request, 'booking.html', {'sources': sources, 'destinations':destinations,'trainno':trainno})
    





