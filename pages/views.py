from django.shortcuts import render
from property.models import Property
from django.core.paginator import Paginator
from realtors.models import Realtor
from listings.choices import bedroom_choices, price_choices, propertyType_Choices

# Create your views here.

def index(request):
    listings = Property.objects.all().order_by("-leaseDate")[:3]
    paginator = Paginator(listings,6) # 6 property on each page
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    
    context = {
        'propertyType_choices': propertyType_Choices, 
        'listings' : paged_listings,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices
    }
    return render(request,'pages/index.html', context)

def about(request):
    # Get all realtors
    realtors = Realtor.objects.all().order_by('-hire_date')

    # Get MVP
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

    context = {
        'realtors': realtors,
        'mvp_realtors' : mvp_realtors
    }

    return render(request,'pages/about.html',context)