import os
from ura_api import ura_api
from dotenv import load_dotenv
load_dotenv()
from django.shortcuts import redirect
from .models import Property
from random import randint
from pyproj import Proj
import pyproj
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.urls import reverse
import warnings
from .property_observer import EmailNotifier, UserObserver
warnings.filterwarnings('ignore')

# Create your views here.

def savePropertyToDatabase(request):
    email_notifier = EmailNotifier()
    users = User.objects.all()
    for user in users:
        user_observer = UserObserver(user)
        email_notifier.attach(user_observer)
    email_notifier.update_listings(request)
    
def index(request):
    if request.user.is_superuser:
        savePropertyToDatabase(request)
    return redirect('index')

def property(request):
    pass
