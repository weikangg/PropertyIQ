import decimal
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from .choices import bedroom_choices, price_choices, propertyType_Choices, area_choices
from property.models import Property,UserProperty
from datetime import datetime
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
from pmdarima.arima import auto_arima
import os
import numpy as np

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
    start_time = datetime.now()
    # Actual Listing
    listing = get_object_or_404(Property, pk=listing_id)

    # Whether the variable is bookmarked already or not
    bookmarked = False  

    # only if the user is logged in, then can do bookmarks
    if request.user.is_authenticated:

        # Add to Property
        user_property, created = UserProperty.objects.get_or_create(user=request.user, property=listing)

        # Whether it's created or not, we want to update the last viewed whenever they click on something and save it in the database
        user_property.last_viewed = datetime.now()
        user_property.save()

        # To show whether the property was already bookmarked before or not in our templates
        if listing.bookmarks.filter(id=request.user.id).exists():
            bookmarked = True

    # Recommendations
    rec_temp = Property.objects.all()
    # Extending the latitude 
    lat_range = [listing.latitude + decimal.Decimal(0.002), listing.latitude - decimal.Decimal(0.002)]
    # Extending the longitude
    long_range = [listing.longitude + decimal.Decimal(0.002), listing.longitude - decimal.Decimal(0.002)]
    # Filtering nearby properties based on location
    rec_temp = rec_temp.filter(Q(Q(latitude__lte = lat_range[0]) & Q(latitude__gte = lat_range[1])) | Q(Q(longitude__lte = long_range[0]) & Q(longitude__gte = long_range[1])))
    # Filtering out the properties with the same project title
    rec_temp = rec_temp.filter(~Q(project_Title__iexact = listing.project_Title))
    
    rec_temp = rec_temp.filter(Q(propertyType__iexact = listing.propertyType))
    # Ordering them by ascending rent.
    rec_temp.order_by("rent")
    # Show top 3 recommendations
    rec = []
    rec_list = {}
    for property in rec_temp:
        if len(rec) == 3:
            break
        if property.project_Title in rec_list:
            continue
        else:
            rec_list[property.project_Title] = 1
            rec.append(property)
    
    print(f'Amount of listings for recommended properties: {rec_temp.count()}')   

    # Trend plots (df is for Historical Trend, df2 is for Nearby Trend)

    # Build the path for the static file
    historical_trend = f'plots/historicalTrends/{listing.id}.png'
    nearby_trend = f'plots/nearbyTrends/{listing.id}.png'
    
    plot_file_path_historical = os.path.join(settings.STATICFILES_DIRS[0], historical_trend)
    plot_file_path_nearby = os.path.join(settings.STATICFILES_DIRS[0], nearby_trend)

    # Check if the file already exists
    if os.path.isfile(plot_file_path_historical) and os.path.isfile(plot_file_path_nearby):
        # File already exists, just use it
        print('Plot image found, skipping model run')
    else:
        print('plot image not found, calculate models')
        # Load the data from the Property model into a pandas dataframe
        df = pd.DataFrame.from_records(Property.objects.all().filter(project_Title=listing.project_Title).values())
        df2 = pd.DataFrame.from_records(rec_temp.values())
        # Convert the leaseDate column to a pandas datetime object
        df['leaseDate'] = pd.to_datetime(df['leaseDate'])
        df2['leaseDate'] = pd.to_datetime(df2['leaseDate'])

        # # Set the leaseDate column as the dataframe index
        df.set_index('leaseDate', inplace=True)
        df2.set_index('leaseDate', inplace=True)

        # Resample the data to a quarterly frequency and take the mean of each quarter
        df = df[['rent']].resample('Q').mean().reset_index()
        df2 = df2[['rent']].resample('Q').mean().reset_index()

        # Rename the columns to match ARIMA's requirements
        df.rename(columns={'leaseDate': 'ds', 'rent': 'y'}, inplace=True)
        df2.rename(columns={'leaseDate': 'ds', 'rent': 'y'}, inplace=True)

        # Fill NAs
        df = df.fillna(df.mean())
        df = df[np.isfinite(df['y'])]

        df2 = df2.fillna(df2.mean())
        df2 = df2[np.isfinite(df2['y'])]

        
        try:
            # Use auto_arima to find the optimal p, d, and q values
            model = auto_arima(df['y'], seasonal=True, m=4, stepwise=True, suppress_warnings=True)
            model2 = auto_arima(df2['y'], seasonal=True, m=4, stepwise=True, suppress_warnings=True)

            # Fit the ARIMA model to the data
            results = SARIMAX(df['y'], order=model.order, seasonal_order=(1, 1, 1, 4)).fit()
            results2 = SARIMAX(df2['y'], order=model2.order, seasonal_order=(1, 1, 1, 4)).fit()

        # If error for autoarima
        except ValueError as e:
            print('AutoArima Error.')
            results =  SARIMAX(df['y'], order=(1,1,1), seasonal_order=(1, 1, 1, 4)).fit()
            results2 =  SARIMAX(df['y'], order=(1,1,1), seasonal_order=(1, 1, 1, 4)).fit()

        # Get the predicted values for the next 4 quarters (1 year)
        pred = results.predict(start=len(df), end=len(df)+3, typ='levels')
        pred2 = results2.predict(start=len(df2), end=len(df2)+3, typ='levels')
    
        # Create a new dataframe with the predicted values and the corresponding dates
        pred_df = pd.DataFrame({'ds': pd.date_range(start=df['ds'].max()+pd.DateOffset(months=3), periods=4, freq='Q'), 'y': pred})
        pred_df2 = pd.DataFrame({'ds': pd.date_range(start=df2['ds'].max()+pd.DateOffset(months=3), periods=4, freq='Q'), 'y': pred2})

        # Merge the original dataframe with the predicted values dataframe
        df = pd.concat([df, pred_df])
        df2 = pd.concat([df2, pred_df2])

        # Set the leaseDate column as the dataframe index
        # df.set_index('ds', inplace=True)

        # Set the date range for the plot to start from the first date in the DataFrame and end at the last date
        date_range = pd.date_range(start=df['ds'].min(), end=df['ds'].max(), freq='Q')
        date_range2 = pd.date_range(start=df2['ds'].min(), end=df2['ds'].max(), freq='Q')

        # Plot the time series (historical plot)
        fig, ax = plt.subplots(figsize=(20,12))
        df.plot(x='ds', y='y', ax=ax, label = "Rent")
        ax.set_xticks(date_range)
        ax.set_xticklabels(date_range.strftime('%Y-%m-%d'), rotation='vertical', fontsize=10)
        ax.set_xlabel('Lease Date')
        ax.set_ylabel('Rental Price')
        ax.set_title('Historical and Predicted Trends for {}'.format(listing.project_Title.title()))
        # Add data labels to the bars
        for i, row in df.iterrows():
            ax.text(row['ds'], row['y'], f"{row['y']:.0f}", ha='center', va='bottom', fontsize=12, color='red', rotation=45)
        ax.annotate('Predicted Prices',
                    xy=(0.87, 0.05), xycoords='axes fraction',
                    xytext=(15, 0), textcoords='offset points',
                    fontsize=14, color='red',
                    bbox=dict(facecolor='none', edgecolor='red', boxstyle='round'))

        # Plot the time series (nearby plot)
        fig2, ax = plt.subplots(figsize=(20,12))
        df2.plot(x='ds', y='y', ax=ax, label = "Rent")
        ax.set_xticks(date_range2)
        ax.set_xticklabels(date_range2.strftime('%Y-%m-%d'), rotation='vertical', fontsize=10)
        ax.set_xlabel('Lease Date')
        ax.set_ylabel('Rental Price')
        ax.set_title('Nearby Trends for {}'.format(listing.project_Title.title()))
        # Add data labels to the bars
        for i, row in df2.iterrows():
            ax.text(row['ds'], row['y'], f"{row['y']:.0f}", ha='center', va='bottom', fontsize=12, color='red', rotation=45)
        ax.annotate('Predicted Prices',
                    xy=(0.87, 0.05), xycoords='axes fraction',
                    xytext=(15, 0), textcoords='offset points',
                    fontsize=14, color='red',
                    bbox=dict(facecolor='none', edgecolor='red', boxstyle='round'))


        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(plot_file_path_historical), exist_ok=True)
        os.makedirs(os.path.dirname(plot_file_path_nearby), exist_ok=True)
        print('Saving Plot Image...')
        # Save the plot image to the static file path
        try:
            fig.savefig(plot_file_path_historical, format='png')
            fig2.savefig(plot_file_path_nearby, format='png')
            print('Saved Plot Image.')
        except Exception as e:
            print(e)
            print('Error occurred while saving the plot.')  

    context = {
        'listing': listing,
        'rec' : rec,
        'bookmarked': bookmarked,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'historical_trend': historical_trend,
        'nearby_trend': nearby_trend
    }
    end_time = datetime.now()
    timeTaken = end_time-start_time
    timeTakenFormatted = divmod(timeTaken.total_seconds(), 60)
    print(f"Time taken: {int(timeTakenFormatted[0])} minutes {int(timeTakenFormatted[1])} seconds")
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
                queryset_list = queryset_list.filter(sqft__lte=int(area)) # Check that the area is less than or equal to the area inserted
            else:
                print('reached here')
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
    return render(request,'listings/search.html', context)