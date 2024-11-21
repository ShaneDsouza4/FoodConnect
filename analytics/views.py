from datetime import timedelta
import pandas as pd
from django.shortcuts import render
from users.models import Profile, Restaurant
from alerts.models import Alert
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from django.db.models import Sum, Count
from django.utils.timezone import now
import json
import pickle
import os

def train_and_save_model():
    data = load_and_prepare_alldata()

    # Features and target
    features = ['total_donations', 'donation_frequency', 'donation_variety_count',
                'donation_volume', 'average_rating', 'response_to_emergency_count']
    target = 'score'

    # Simulate scores if not present (one-time for training)
    if target not in data:
        weights = {
            'total_donations': 0.4,
            'donation_frequency': 0.15,
            'donation_variety_count': 0.05,
            'donation_volume': 0.1,
            'average_rating': 0.1,
            'response_to_emergency_count': 0.2
        }
        data[target] = sum(data[feature] * weight for feature, weight in weights.items())

    # Normalize features
    scaler = MinMaxScaler()
    data[features] = scaler.fit_transform(data[features])

    # Split data
    X = data[features]
    y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)

    # Save the model and scaler
    with open('rank_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

def load_and_prepare_alldata():
    # Profile dataset
    profile_queryset = Profile.objects.all().values(
        'first_name', 'last_name', 'total_donations', 'donation_frequency', 
        'donation_volume', 'donation_variety_count', 'average_rating', 'response_to_emergency_count'
    )
    profile_data = pd.DataFrame(list(profile_queryset))
    profile_data.fillna(0, inplace=True)
    profile_data['name'] = profile_data['first_name'].astype(str) + ' ' + profile_data['last_name'].astype(str)

    # Restaurant dataset
    restaurant_queryset = Restaurant.objects.all().values(
        'restaurant_name', 'total_donations', 'donation_frequency', 
        'donation_volume', 'donation_variety_count', 'average_rating', 'response_to_emergency_count'
    )
    restaurant_data = pd.DataFrame(list(restaurant_queryset))
    restaurant_data.fillna(0, inplace=True)
    restaurant_data.rename(columns={'restaurant_name': 'name'}, inplace=True)

    # Combined dataset
    combined_data = pd.concat([profile_data, restaurant_data], ignore_index=True)
    
    return combined_data[['name', 'total_donations', 'donation_frequency', 'donation_volume', 
                          'donation_variety_count', 'average_rating', 'response_to_emergency_count']].copy()

def load_and_prepare_individual_data():
    queryset = Profile.objects.all().values(
        'first_name', 'last_name', 'total_donations', 'donation_frequency', 
        'donation_volume', 'donation_variety_count', 'average_rating', 'response_to_emergency_count'
    )
    data = pd.DataFrame(list(queryset))
    data.fillna(0, inplace=True)
    data['name'] = data['first_name'].astype(str) + ' ' + data['last_name'].astype(str)
    return data[['name', 'total_donations', 'donation_frequency', 'donation_volume', 'donation_variety_count',  'average_rating', 'response_to_emergency_count']].copy()

def load_and_prepare_restaurant_data():
    queryset = Restaurant.objects.all().values(
        'restaurant_name', 'total_donations', 'donation_frequency', 
        'donation_volume', 'donation_variety_count', 'average_rating', 'response_to_emergency_count'
    )
    data = pd.DataFrame(list(queryset))
    data.fillna(0, inplace=True)
    data.rename(columns={'restaurant_name': 'name'}, inplace=True)
    return data[['name', 'total_donations', 'donation_frequency', 'donation_volume', 'donation_variety_count',  'average_rating', 'response_to_emergency_count']].copy()

def rank_donators(data):
    features = ['total_donations', 'donation_frequency', 'donation_variety_count',
                'donation_volume', 'average_rating', 'response_to_emergency_count']

    # Ensure model and scaler are available; if not, train them
    if not os.path.exists('rank_model.pkl') or not os.path.exists('scaler.pkl'):
        print("Model or scaler not found. Training the model...")
        train_and_save_model()

    # Load pre-trained model and scaler
    with open('rank_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    # Normalize features
    data[features] = scaler.transform(data[features])

    # Predict scores
    data['predicted_score'] = model.predict(data[features])

    # Rank donors
    ranked_data = data.sort_values(by='predicted_score', ascending=False).head(10)
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
    all_data = load_and_prepare_alldata()
    individual_data = load_and_prepare_individual_data()
    restaurant_data = load_and_prepare_restaurant_data()
    ranked_data = rank_donators(all_data)
    individual_ranked_data = rank_donators(individual_data)
    restaurant_ranked_data = rank_donators(restaurant_data)
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
        'ranked_donators': ranked_data[['name', 'total_donations', 'donation_volume', 'predicted_score']].to_dict(orient='records'),
        'ranked_individual_donators': individual_ranked_data[['name', 'total_donations', 'donation_volume', 'predicted_score']].to_dict(orient='records'),
        'ranked_restaurant_donators': restaurant_ranked_data[['name', 'total_donations', 'donation_volume', 'predicted_score']].to_dict(orient='records'),
        'top_donor_name': ranked_data.iloc[0]['name'] if not ranked_data.empty else "No Donors",
        'top_individual_donor_name': individual_ranked_data.iloc[0]['name'] if not individual_ranked_data.empty else "No Donors",
        'top_restaurant_donor_name': restaurant_ranked_data.iloc[0]['name'] if not restaurant_ranked_data.empty else "No Donors",
        'total_volume': all_data['donation_volume'].sum(),
        'pie_chart_data': pie_chart_data,
        'response_emergency_data': response_emergency_json,
        'location_data': json.dumps(location_data),
        'future_alerts': json.dumps(future_alerts),
    }

    return render(request, 'webpages/analytics.html', context)