from django.shortcuts import render, HttpResponse, redirect 
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render (request,'login.html')
def register(request):
    if request.method =='POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  
            print(pw_hash)
            request.session['username'] = fname + " "+ lname
            request.session['status']="Registered"
            User.objects.create(first_name=fname, last_name=lname,email=email, password=pw_hash)
    return redirect("/wall")
def login(request):
    if request.method =='POST':
        errors2 = User.objects.login_validator(request.POST)
        if len(errors2) > 0:
            for key, value in errors2.items():
                messages.error(request, value)
            return redirect('/')

        users = User.objects.filter(email=request.POST['email2'])
        if users:
            logged_user = users[0]
            if bcrypt.checkpw(request.POST['password2'].encode(), logged_user.password.encode()):
                request.session['username'] = logged_user.first_name
                request.session['status']="logged in"
                request.session['user_id'] = logged_user.id
                return redirect('/wall')
            print("""Wrong password""")
        return redirect("/")
def wall(request):
    context = {
        'messages': Message.objects.all(),
        'comments':Comment.objects.all(),
        'user':User.objects.all()
    }
    return render(request,'wall.html',context)
        
    

def post_msg(request):
    if request.method =='POST':
        msg = request.POST['message-user']
        user = User.objects.get(request.session['user_id'])
        Message.objects.create(
            message_text = msg,
            user = user
        )
    return redirect('/wall')

 

def comment(request,msg_id):
    
    if request.method =='POST':
        comment = request.POST['comment-user']
        user = User.objects.get(request.session['user_id'])
        message = Message.objects.get(request.session['user_id'])
        Comment.objects.create(
            comment = comment,
            user = user,
            message = message
        )
    return redirect('/wall') 


