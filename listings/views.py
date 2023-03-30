import decimal
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .choices import bedroom_choices, price_choices, propertyType_Choices, area_choices
from property.models import Property

# Create your views here.
def index(request):
    listings = Property.objects.all().order_by("-leaseDate")
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
    return render(request,'listings/allListings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Property, pk=listing_id)
    bookmarked = False
    rec_temp = Property.objects.all()
    # Extending the latitude 
    lat_range = [listing.latitude + decimal.Decimal(0.009), listing.latitude - decimal.Decimal(0.009)]
    # Extending the longitude
    long_range = [listing.longitude + decimal.Decimal(0.009), listing.longitude - decimal.Decimal(0.009)]
    # Filtering nearby properties based on location
    rec_temp = rec_temp.filter(Q(Q(latitude__lte = lat_range[0]) & Q(latitude__gte = lat_range[1])) | Q(Q(longitude__lte = long_range[0]) & Q(longitude__gte = long_range[1])))
    # Filtering nearby properties based on project title if possible
    rec_temp = rec_temp.filter(~Q(project_Title__iexact = listing.project_Title))
    # Ordering them by ascending rent.
    rec_temp.order_by("rent")
    # Show top 3 recommendations
    rec = rec_temp[:3]

    # To show whether the property was already bookmarked before or not
    if listing.bookmarks.filter(id=request.user.id).exists():
        bookmarked = True
    context = {
        'listing': listing,
        'rec' : rec,
        'bookmarked': bookmarked
    }
    return render(request,'listings/singleListing.html', context)

def search(request):
    queryset_list = Property.objects.order_by('-leaseDate')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET.get('keywords')
        if keywords:
            # Check that the title contains the keywords
            queryset_list = queryset_list.filter(Q(project_Title__icontains=keywords) | Q(street__icontains = keywords))


    # Property Type
    if 'property_type' in request.GET:
        property_type = request.GET.get('property_type')
        if property_type != '' and property_type != 'All':
            queryset_list = queryset_list.filter(propertyType__iexact=property_type) # Check that the property_type matches the city inputted

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET.get('bedrooms')
        if bedrooms != '' and bedrooms != 'All':
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms) # Check that the no of bedrooms is less than or equal to the no of bedrooms

    # Price
    if 'price' in request.GET:
        price = request.GET.get('price')
        if price != '' and price != 'All':
            if price != '10001':
                queryset_list = queryset_list.filter(rent__lte=price) # Check that the rent is less than or equal to the no of price
            else:
                queryset_list = queryset_list.filter(rent__gt=10000) # Check that the rent is greater than 10,000

    # Area
    if 'area' in request.GET:
        area = request.GET.get('area')
        if area != 'All' and area != '':
            if area != '5001':
                queryset_list = queryset_list.filter(sqft__lte=area) # Check that the area is less than or equal to the area inserted
            else:
                queryset_list = queryset_list.filter(sqft__gt=5000) # Check that the area is greater than 5000 sqft

    paginator = Paginator(queryset_list,6) # 6 property on each page
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'propertyType_choices': propertyType_Choices, 
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'area_choices': area_choices,
        'listings': paged_listings,
        'values': request.GET
    }
    print('end queryset list:', queryset_list)
    return render(request,'listings/search.html', context)