from datetime import timedelta
import pandas as pd
from django.shortcuts import render
from users.models import Profile, Restaurant
from alerts.models import Alert
from sklearn.preprocessing import MinMaxScaler
from django.db.models import Sum, Count
from django.utils.timezone import now
import json

def load_and_prepare_data():
    queryset = Profile.objects.all().values(
        'first_name', 'last_name', 'total_donations', 'donation_frequency', 
        'donation_volume', 'donation_variety_count', 'average_rating', 'response_to_emergency_count'
    )
    data = pd.DataFrame(list(queryset))
    data.fillna(0, inplace=True)
    data['name'] = data['first_name'].astype(str) + ' ' + data['last_name'].astype(str)
    return data[['name', 'total_donations', 'donation_frequency', 'donation_volume', 'donation_variety_count',  'average_rating', 'response_to_emergency_count']].copy()

def rank_donators(data):
    scaler = MinMaxScaler()
    data['normalized_donations'] = scaler.fit_transform(data[['total_donations']])
    data['normalized_frequency'] = scaler.fit_transform(data[['donation_frequency']])
    data['normalized_variety'] = scaler.fit_transform(data[['donation_variety_count']])
    data['normalized_volume'] = scaler.fit_transform(data[['donation_volume']])
    data['normalized_rating'] = scaler.fit_transform(data[['average_rating']])
    data['normalized_emergency_response'] = scaler.fit_transform(data[['response_to_emergency_count']])

    weight_donations = 0.4
    weight_frequency = 0.15
    weight_variety = 0.05
    weight_volume = 0.1
    weight_rating = 0.1
    weight_emergency_response = 0.2


    data['score'] = (
        data['normalized_donations'] * weight_donations +
        data['normalized_frequency'] * weight_frequency +
        data['normalized_variety'] * weight_variety +
        data['normalized_volume'] * weight_volume +
        data['normalized_rating'] * weight_rating +
        data['normalized_emergency_response'] * weight_emergency_response
    )

    ranked_data = data.sort_values(by='score', ascending=False).head(10)
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
    labels = [data['city'] for data in location_data if data['city']]
    values = [data['total'] for data in location_data if data['city']]
    return {
        'labels': labels,
        'values': values
    }

def get_response_to_emergency_data():
    response_individual = Profile.objects.aggregate(sum=Sum('response_to_emergency_count'))['sum'] or 0
    response_restaurant = Restaurant.objects.aggregate(sum=Sum('response_to_emergency_count'))['sum'] or 0

    return {
        'individual': response_individual,
        'restaurant': response_restaurant
    }

def load_alert_data():
    alerts = Alert.objects.filter(is_active=True).values('date_created', 'urgency_level')
    data = pd.DataFrame(alerts)
    data['date_created'] = pd.to_datetime(data['date_created'])
    data.set_index('date_created', inplace=True)
    
    return data

def predict_future_alerts():
    data = load_alert_data()
    daily_alerts = data.resample('D').size()

    if daily_alerts.empty:
        return { (pd.Timestamp.now() + timedelta(days=i)).strftime('%Y-%m-%d'): 0 for i in range(1, 8) }

    daily_alerts.index = daily_alerts.index.dayofweek
    avg_by_day = daily_alerts.groupby(daily_alerts.index).mean()
    future_dates = [pd.Timestamp.now() + timedelta(days=i) for i in range(1, 8)]
    future_days_of_week = [date.weekday() for date in future_dates]

    future_predictions = [
        max(0, int(avg_by_day.get(day, 0)))
        for day in future_days_of_week
    ]

    future_alerts = {
        date.strftime('%Y-%m-%d'): pred
        for date, pred in zip(future_dates, future_predictions)
    }

    return future_alerts

def analytics_view(request):
    data = load_and_prepare_data()
    ranked_data = rank_donators(data)
    funds_raised = Profile.objects.aggregate(total=Sum('total_donations'))['total'] or 0
    total_donors = Profile.objects.count() + Restaurant.objects.count()
    progress_to_yearly_target = round((funds_raised / 1750) * 100, 2)
    donation_data = get_donation_data_by_type()
    pie_chart_data = json.dumps(donation_data) 
    location_data = get_donor_location_distribution()
    response_emergency_data = get_response_to_emergency_data()
    response_emergency_json = json.dumps(response_emergency_data)
    future_alerts = predict_future_alerts()

    context = {
        'funds_raised': funds_raised,
        'progress_to_yearly_target': progress_to_yearly_target,
        'total_donors': total_donors,
        'ranked_donators': ranked_data[['name', 'total_donations', 'donation_volume', 'score']].to_dict(orient='records'),
        'top_donor_name': ranked_data.iloc[0]['name'] if not ranked_data.empty else "No Donors",
        'total_volume': data['donation_volume'].sum(),
        'pie_chart_data': pie_chart_data,
        'response_emergency_data': response_emergency_json,
        'location_data': json.dumps(location_data),
        'future_alerts': json.dumps(future_alerts),
    }

    return render(request, 'webpages/analytics.html', context)
