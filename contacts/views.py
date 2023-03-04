from django.shortcuts import redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
from os import getenv
from dotenv import load_dotenv
load_dotenv()

# Create your views here.
def contact(request):
    if request.method == "POST":
        listing_id = request.POST.get('listing_id')
        listing = request.POST.get('listing') # listing title
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        user_id = request.POST.get('user_id')
        realtor_email = request.POST.get('realtor_email')

        # Check if user has made an enquiry before
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this listing before!')
                return redirect('/listings/'+listing_id)        

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email,phone=phone,message=message,user_id=user_id)

        contact.save()

        # Send Email To Realtor!
        send_mail(
            'Property Listing Inquiry',
            'There has been an inquiry for ' + listing +'. Sign in to the admin panel for more info.',
            getenv("GMAIL_EMAIL"),
            [realtor_email,'chongweikang4@gmail.com'],
            fail_silently=False
        )

        messages.success(request,'Your request has been submitted, a realtor will get back to you soon!')

        return redirect('/listings/'+listing_id)