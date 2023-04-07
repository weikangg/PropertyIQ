from dotenv import load_dotenv
load_dotenv()
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .property_observer import EmailNotifier, UserObserver

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
