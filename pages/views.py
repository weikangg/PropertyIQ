from django.shortcuts import render
from property.models import Property
from django.core.paginator import Paginator
from listings.choices import bedroom_choices, price_choices, propertyType_Choices, area_choices

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
        'price_choices': price_choices,
        'area_choices': area_choices
    }
    return render(request,'pages/index.html', context)

def about(request):
    team_members = [
        {
            'name': 'Aditya',
            'position': 'CEO',
            'img': 'img/Picture5.png'
        },
        {
            'name': 'Wei Kang',
            'position': 'CTO',
            'img': 'img/Picture1.png'
        },
        {
            'name': 'Don',
            'position': 'Doc Master',
            'img': 'img/Picture3.png'
        },
        {
            'name': 'John',
            'position': 'Slides Ninja',
            'img': 'img/Picture4.png'
        },
        {
            'name': 'Nicholas',
            'position': 'Diagrams Guru',
            'img': 'img/Picture2.png'
        }
    ]
    context = {'team_members': team_members}
    return render(request, 'pages/about.html', context)
