from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from contacts.models import Contact

# Create your views here.
def register(request):
    if request.method == "POST":
        # Register User
        
        # Get form values
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Check if passwords match
        if password == password2:
            # check if the username exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is taken!')
                return redirect('register')
            # check if the email exists
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email is taken!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username,password=password, email = email, first_name = first_name, last_name = last_name)
                    user.save()
                    messages.success(request,'You are now registered and can log in!')
                    return redirect('login')
        else:
            messages.error(request,"Passwords do not match!")
            return redirect('register')
                
    else:
        return render(request,'accounts/register.html')

def login(request):
    if request.method == "POST":
        # Login User
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = auth.authenticate(username=username,password=password)

        # If user matched.
        if user is not None:
            auth.login(request,user)
            return redirect('dashboard')
        
        # If failed to match
        else:
            messages.error(request,"Invalid credentials! Try again!")
            return redirect('login')

    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.method == "POST":
        auth.logout(request)
    return redirect('index')

def dashboard(request):
    # user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    # context = {
    #     'contacts': user_contacts
    # }
    # return render(request,'accounts/dashboard.html', context)
    return render(request,'accounts/dashboard.html')

def update(request):
    id = request.user.id
    user = User.objects.get(pk=id)
    if request.method == "POST":
        # Update User Account
        # Get form values
        first_name = request.POST.get('first_name')
        user.first_name = first_name
        last_name = request.POST.get('last_name')
        user.last_name = last_name
        email = request.POST.get('email')
        user.email = email
        username = request.POST.get('username')
        user.username = username
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            user.password = make_password(password)

        user.save()
        update_session_auth_hash(request, user)
        messages.success(request,"Account details successfully updated!")
        return redirect('dashboard')
        # # Check if passwords match
        # if password == password2:
        #     # check if the username exists
        #     if User.objects.filter(username=username).exists():
        #         messages.error(request, 'Username is taken!')
        #         return redirect('register')
        #     # check if the email exists
        #     else:
        #         if User.objects.filter(email=email).exists():
        #             messages.error(request, 'Email is taken!')
        #             return redirect('register')
        #         else:
        #             user = User.objects.create_user(username=username,password=password, email = email, first_name = first_name, last_name = last_name)
        #             user.save()
        #             messages.success(request,'You are now registered and can log in!')
        #             return redirect('login')
        # else:
        #     messages.error(request,"Passwords do not match!")
            # return redirect('register')
                
    else:
        context = {
            'user' : request.user
        }
        return render(request,'accounts/update.html', context)