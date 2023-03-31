from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from django.db.models import Q
from .validators import validate
from property.models import Property, UserProperty

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

        # Check if passwords meet the basic requirements of containing at least:
            # 1. 1 Special Character (!@#$%^&*_)
            # 2. 1 Uppercase Character
            # 3. 1 Lowercase Character
            # 4. At least 8 characters long
        if validate(request,password) == False or validate(request,password2) == False:
            return redirect('register')

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
    # if we find a property that has a bookmarks field with the userid within, we return it
    bookmarks = Property.objects.filter(bookmarks=request.user)
    queryset_length = bookmarks.count()
    paginator = Paginator(bookmarks,6) # 6 property on each page
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'bookmarks': paged_listings,
        'queryset_length':queryset_length
    }
    return render(request,'accounts/dashboard.html', context)

def update(request):
    id = request.user.id
    user = User.objects.get(pk=id)
    if request.method == "POST":
        # Update User Account
        # Get form values
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        # Check if passwords meet the basic requirements of containing at least:
            # 1. 1 Special Character (!@#$%^&*_)
            # 2. 1 Uppercase Character
            # 3. 1 Lowercase Character
            # 4. At least 8 characters long
        if validate(request,password) == False or validate(request,password2) == False:
            return redirect('update')
        
        if password == password2:
            # check if the username exists
            if username != user.username and User.objects.filter(username=username).exists():
                messages.error(request, 'Username is taken!')
                return redirect('update')
            # check if the email exists
            else:
                if email != user.email and User.objects.filter(email=email).exists():
                    messages.error(request, 'Email is taken!')
                    return redirect('update')
                else:
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.username = username
                    user.password = make_password(password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request,"Account details successfully updated!")
                    return redirect('dashboard')

        else:
            messages.error(request,"Passwords do not match!")
            return redirect('update')
                
    else:
        context = {
            'user' : request.user
        }
        return render(request,'accounts/update.html', context)
    
def bookmarks(request, listing_id):
    property = get_object_or_404(Property, pk = listing_id)
    # If the user id is inside this field, the user has already added this to the bookmarks
    if property.bookmarks.filter(id = request.user.id).exists():
        # remove it 
        property.bookmarks.remove(request.user)
        messages.success(request,"Bookmark successfully removed!")
    else:
        # add it
        property.bookmarks.add(request.user)
        messages.success(request,"Bookmark successfully added!")
    return redirect('listing', listing_id)



def searchHistory(request):
    recentListings = Property.objects.filter(
        userproperty__user=request.user
    ).order_by('-userproperty__last_viewed').distinct()
    queryset_length = recentListings.count()
    paginator = Paginator(recentListings,6) # 6 property on each page
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'recentListings': paged_listings,
        'queryset_length': queryset_length
    }
    return render(request,'accounts/searchHistory.html', context)

def clearSearchHistory(request):
    recentListings = Property.objects.filter(searchHistory=request.user)
    recentListings.all().delete()
    messages.success(request,'Search History successfully cleared!')
    return redirect('searchHistory')