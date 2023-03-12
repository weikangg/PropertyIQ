from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .choices import bedroom_choices, price_choices
from property.models import Property

# Create your views here.
def index(request):
    listings = Property.objects.all().order_by("-leaseDate")
    paginator = Paginator(listings,6) # 6 property on each page
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    
    context = {
        'listings' : paged_listings,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices
    }
    return render(request,'listings/allListings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Property, pk=listing_id)

    context = {
        'listing': listing
    }
    return render(request,'listings/singleListing.html', context)

def search(request):
    queryset_list = Property.objects.order_by('-leaseDate')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET.get('keywords')
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords) # Check that the description contains the keywords

    # City
    if 'property_type' in request.GET:
        property_type = request.GET.get('property_type')
        if property_type:
            queryset_list = queryset_list.filter(property_type__iexact=property_type) # Check that the property_type matches the city inputted

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET.get('bedrooms')
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms) # Check that the no of bedrooms is less than or equal to the no of bedrooms

    # Price
    if 'price' in request.GET:
        price = request.GET.get('price')
        if price:
            queryset_list = queryset_list.filter(rent__lte=price) # Check that the rent is less than or equal to the no of price
        
    paginator = Paginator(queryset_list,6) # 6 property on each page
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': paged_listings,
        'values': request.GET
    }
    return render(request,'listings/search.html', context)