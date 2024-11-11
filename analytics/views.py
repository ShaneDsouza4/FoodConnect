import pandas as pd
from django.shortcuts import render
from users.models import Profile, Restaurant  # Import your Profile model
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

def analytics_view(request):
    data = load_and_prepare_data()
    ranked_data = rank_donators(data)
    funds_raised = Profile.objects.aggregate(total=Sum('total_donations'))['total'] or 0
    total_donors = Profile.objects.count() + Restaurant.objects.count()
    progress_to_yearly_target = (funds_raised / 17500000) * 100  # Example fixed target
    donation_data = get_donation_data_by_type()
    pie_chart_data = json.dumps(donation_data) 

    context = {
        'funds_raised': funds_raised,
        'progress_to_yearly_target': progress_to_yearly_target,
        'total_donors': total_donors,
        'ranked_donators': ranked_data[['name', 'total_donations', 'donation_volume', 'score']].to_dict(orient='records'),
        'total_volume': data['donation_volume'].sum(),
        'pie_chart_data': pie_chart_data,
    }

    return render(request, 'webpages/analytics.html', context)