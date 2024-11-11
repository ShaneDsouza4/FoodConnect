import pandas as pd
from django.shortcuts import render
from users.models import Profile, Restaurant
from sklearn.preprocessing import MinMaxScaler
from django.db.models import Sum, Count
from django.utils.timezone import now
import json

def load_and_prepare_data():
    queryset = Profile.objects.all().values(
        'first_name', 'last_name', 'total_donations', 'donation_frequency', 
        'donation_volume', 'donation_variety_count'
    )
    data = pd.DataFrame(list(queryset))
    data.fillna(0, inplace=True)  # Handle missing data

    # Convert first_name and last_name into a single full name
    data['name'] = data['first_name'].astype(str) + ' ' + data['last_name'].astype(str)

    # Explicitly return a copy of the DataFrame
    return data[['name', 'total_donations', 'donation_frequency', 'donation_volume', 'donation_variety_count']].copy()

def rank_donators(data):
    scaler = MinMaxScaler()
    data.loc[:, 'normalized_donations'] = scaler.fit_transform(data[['total_donations']])
    data.loc[:, 'normalized_volume'] = scaler.fit_transform(data[['donation_volume']])
    data['score'] = data['normalized_donations'] * 0.5 + data['normalized_volume'] * 0.5
    ranked_data = data.sort_values(by='score', ascending=False)
    return ranked_data

def get_donation_data_by_type():
    individual_donations = Profile.objects.aggregate(total=Sum('total_donations'))['total'] or 0
    restaurant_donations = Restaurant.objects.aggregate(total=Sum('total_donations'))['total'] or 0

    donation_data = {
        'Individual': individual_donations,
        'Restaurant': restaurant_donations
    }
    return donation_data

def get_donor_location_distribution():
    location_data = Profile.objects.values('city').annotate(total=Count('id')).order_by('-total')
    labels = [data['city'] for data in location_data if data['city']]  # Ensure city is not None or empty
    values = [data['total'] for data in location_data if data['city']]
    return {
        'labels': labels,
        'values': values
    }

def get_response_to_emergency_data():
    # Assuming that 'response_to_emergency_count' exists only in the Restaurant model
    # and does not exist in the Profile model.
    response_individual = Profile.objects.aggregate(sum=Sum('donation_frequency'))['sum'] or 0
    response_restaurant = Restaurant.objects.aggregate(sum=Sum('response_to_emergency_count'))['sum'] or 0
    print(response_individual)
    print(response_restaurant)
    return {
        'individual': response_individual,
        'restaurant': response_restaurant
    }

def get_verification_status_data():
    verified_count = Profile.objects.filter(is_verified=True).count()
    not_verified_count = Profile.objects.filter(is_verified=False).count()
    return [verified_count, not_verified_count]

def get_average_ratings_data():
    ratings = Restaurant.objects.values_list('average_rating', flat=True)
    return list(ratings)

def analytics_view(request):
    data = load_and_prepare_data()
    ranked_data = rank_donators(data)
    funds_raised = Profile.objects.aggregate(total=Sum('total_donations'))['total'] or 0
    total_donors = Profile.objects.count() + Restaurant.objects.count()
    progress_to_yearly_target = (funds_raised / 17500000) * 100  # Example fixed target
    donation_data = get_donation_data_by_type()
    pie_chart_data = json.dumps(donation_data) 

    # Fetch additional data for charts
    location_data = get_donor_location_distribution()
    response_emergency_data = get_response_to_emergency_data()
    verification_status_data = get_verification_status_data()
    average_ratings_data = get_average_ratings_data()

    # Serialize JSON data for JavaScript charts
    response_emergency_json = json.dumps(response_emergency_data)
    verification_status_json = json.dumps({
        'labels': ['Verified', 'Not Verified'],
        'data': verification_status_data
    })
    average_ratings_json = json.dumps({
        'labels': ['Ratings'],
        'data': average_ratings_data
    })

    context = {
        'funds_raised': funds_raised,
        'progress_to_yearly_target': progress_to_yearly_target,
        'total_donors': total_donors,
        'ranked_donators': ranked_data[['name', 'total_donations', 'donation_volume', 'score']].to_dict(orient='records'),
        'total_volume': data['donation_volume'].sum(),
        'pie_chart_data': pie_chart_data,
        'response_emergency_data': response_emergency_json,
        'verification_status_data': verification_status_json,
        'average_ratings_data': average_ratings_json,
        'location_data': json.dumps(location_data),
    }

    return render(request, 'webpages/analytics.html', context)
