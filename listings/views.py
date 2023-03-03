from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .choices import bedroom_choices, state_choices, price_choices
from .models import Listing

# Create your views here.
def index(request):
    listings = Listing.objects.all().order_by("-list_date").filter(is_published=True)
    paginator = Paginator(listings,6) # 6 property on each page
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    
    context = {
        'listings' : paged_listings
    }
    return render(request,'listings/allListings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing
    }
    return render(request,'listings/singleListing.html', context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET.get('keywords')
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords) # Check that the description contains the keywords

    # City
    if 'city' in request.GET:
        city = request.GET.get('city')
        if city:
            queryset_list = queryset_list.filter(city__iexact=city) # Check that the city matches the city inputted

    # State
    if 'state' in request.GET:
        state = request.GET.get('state')
        if state:
            queryset_list = queryset_list.filter(state__iexact=state) # Check that the state matches the state inputted

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET.get('bedrooms')
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms) # Check that the no of bedrooms is less than or equal to the no of bedrooms

    # Price
    if 'price' in request.GET:
        price = request.GET.get('price')
        if price:
            queryset_list = queryset_list.filter(price__lte=price) # Check that the no of price is less than or equal to the no of price
        
    paginator = Paginator(queryset_list,6) # 6 property on each page
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': paged_listings,
        'values': request.GET
    }
    return render(request,'listings/search.html', context)