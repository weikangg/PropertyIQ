from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'listings/allListings.html')

def listing(request):
    return render(request,'listings/singleListing.html')

def search(request):
    return render(request,'listings/search.html')