from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from LmsApp.EmailBackend import EmailBackEnd

def Register(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(username," ", password," ",email)
        if User.objects.filter(email=email).exists():
            messages.warning(request,"Email Already Exits")
            print("i am try here gupa ji ")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            print("i am warning rahulla")
            messages.warning(request,"Email Already Exits")
            return redirect('register')
        try:
            user = User(
                    username=username,
                    email=email,
                )
            user.set_password(password)
            user.save()
            print("i am try here")
        except:
             print("i am here exception")
             messages.warning(request,"Database Integirity error")
            
        
        
        return redirect('login')


    return render(request,'registration/register.html')



	
def DOLOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password,"wooooowwwww great learning")
		
        user = EmailBackEnd.authenticate(request,
                                     username=email,
                                     password=password)
        if user!=None:
           login(request,user)
           return redirect('home')
        else:
           messages.error(request,'Email and Password Are Invalid !')
           return redirect('login')


def Profile(request):
    print("i am tester profile")
    return render(request,'registration/profile_update.html')
def Profile_Update(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request,'Profile Are Successfully Updated. ')
        return redirect('profile')
		   