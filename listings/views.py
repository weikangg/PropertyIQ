from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Listing

# Create your views here.
def index(request):
    listings = Listing.objects.all().order_by("-list_date").filter(is_published=True)
    paginator = Paginator(listings,6) # 3 property on each page
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
    return render(request,'listings/search.html')