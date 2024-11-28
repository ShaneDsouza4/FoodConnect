import os
import json
import pickle
import numpy as np
import pandas as pd
from datetime import timedelta
from django.shortcuts import render
from users.models import Profile, Restaurant
from alerts.models import Alert
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import ndcg_score, mean_absolute_error, root_mean_squared_error, r2_score
from scipy.stats import kendalltau
from sklearn.model_selection import train_test_split
from django.db.models import Sum, Count

def train_and_save_model():
    data = load_and_prepare_alldata()

    features = ['total_donations', 'donation_frequency', 'donation_variety_count',
                'donation_volume', 'average_rating', 'response_to_emergency_count']
    target = 'score'

    # Train scores/data if not present
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

def calculate_mrr(y_true, y_pred):
    """Calculate Mean Reciprocal Rank (MRR)."""
    sorted_indices = np.argsort(y_pred)[::-1]
    for rank, idx in enumerate(sorted_indices, 1):
        if idx in np.argsort(y_true)[::-1][:1]:
            return 1 / rank
    return 0

# Ranking Donators using Gradient Boosting Regressor
def rank_donators_using_GBC(data):
    features = ['total_donations', 'donation_frequency', 'donation_variety_count',
                'donation_volume', 'average_rating', 'response_to_emergency_count']

    if not os.path.exists('rank_model.pkl') or not os.path.exists('scaler.pkl'):
        print("Model or scaler not found. Training the model...")
        train_and_save_model()

    with open('rank_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    data[features] = scaler.transform(data[features])

    X = data[features]
    y = model.predict(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    proxy_model = GradientBoostingRegressor()
    proxy_model.fit(X_train, y_train)

    predictions = proxy_model.predict(X_test)

    # Calculate Metrics
    ndcg = ndcg_score([y_test], [predictions], k=5)
    print(f"NDCG@5 (Gradient Booster Regressor): {ndcg}")

    true_ranking = y_test.argsort()[::-1]
    predicted_ranking = predictions.argsort()[::-1]
    tau, _ = kendalltau(true_ranking, predicted_ranking)
    print(f"Kendall's Tau (Gradient Booster Regressor): {tau}")

    mrr = calculate_mrr(y_test, predictions)
    print(f"MRR (Gradient Booster Regressor): {mrr}")

    mae = mean_absolute_error(y_test, predictions)
    rmse = root_mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"MAE (Gradient Booster Regressor): {mae}")
    print(f"RMSE (Gradient Booster Regressor): {rmse}")
    print(f"R² (Gradient Booster Regressor): {r2}")

# Ranking Donators using Random Forest
def rank_donators_rf(data):
    features = ['total_donations', 'donation_frequency', 'donation_variety_count',
                'donation_volume', 'average_rating', 'response_to_emergency_count']

    if not os.path.exists('scaler.pkl'):
        print("Scaler not found. Please train and save the scaler first.")
        return

    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    data[features] = scaler.transform(data[features])

    if 'predicted_score' not in data:
        print("`predicted_score` not found. Creating proxy scores.")
        data['predicted_score'] = (
            data['total_donations'] * 0.4 +
            data['donation_frequency'] * 0.15 +
            data['donation_variety_count'] * 0.05 +
            data['donation_volume'] * 0.1 +
            data['average_rating'] * 0.1 +
            data['response_to_emergency_count'] * 0.2
        )

    X = data[features]
    y = data['predicted_score']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    predictions = rf_model.predict(X_test)

    # Calculate Metrics
    ndcg = ndcg_score([y_test], [predictions], k=5)
    print("\n")
    print(f"NDCG@5 (Random Forest): {ndcg}")

    true_ranking = y_test.argsort()[::-1]
    predicted_ranking = predictions.argsort()[::-1]
    tau, _ = kendalltau(true_ranking, predicted_ranking)
    print(f"Kendall's Tau (Random Forest): {tau}")

    mrr = calculate_mrr(y_test, predictions)
    print(f"MRR (Random Forest): {mrr}")

    mae = mean_absolute_error(y_test, predictions)
    rmse = root_mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"MAE (Random Forest): {mae}")
    print(f"RMSE (Random Forest): {rmse}")
    print(f"R² (Random Forest): {r2}")

# Legacy algorithm (Gradient Boosting Regressor) for Ranking Donators
def rank_donators(data):
    features = ['total_donations', 'donation_frequency', 'donation_variety_count',
                'donation_volume', 'average_rating', 'response_to_emergency_count']

    # Preserve raw data for output
    raw_data = data.copy()

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
    min_percentile = data['predicted_score'].quantile(0.05)
    max_percentile = data['predicted_score'].quantile(0.95)

    if max_percentile - min_percentile == 0:
        data['score_out_of_100'] = 0
    else:
        data['score_out_of_100'] = (
            (data['predicted_score'] - min_percentile) /
            (max_percentile - min_percentile) * 100
        )

    # Cap scores between 0 and 100
    data['score_out_of_100'] = data['score_out_of_100'].clip(lower=0, upper=100)

    # Add raw data back to the ranked DataFrame for display
    data = pd.concat([raw_data, data[['predicted_score', 'score_out_of_100']]], axis=1)

    # Rank donors by `score_out_of_100`
    ranked_data = data.sort_values(by='score_out_of_100', ascending=False).head(10)

    # Return the required fields
    return ranked_data[['name', 'total_donations', 'donation_volume', 'donation_frequency', 
                        'donation_variety_count', 'response_to_emergency_count', 
                        'predicted_score', 'score_out_of_100']].to_dict(orient='records')

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
    # Load active alerts from the database
    alerts = Alert.objects.filter(is_active=True).values('date_created', 'urgency_level')
    if not alerts:
        return pd.DataFrame()  # Return empty DataFrame if no data is available
    data = pd.DataFrame(alerts)
    data['date_created'] = pd.to_datetime(data['date_created'])
    data.set_index('date_created', inplace=True)
    return data

def train_alert_model():
    # Load alert data
    data = load_alert_data()
    if data.empty:
        print("No data available to train the alert prediction model.")
        return None

    # Prepare daily alert counts
    daily_alerts = data.resample('D').size().reset_index(name='alert_count')
    daily_alerts['day_of_week'] = daily_alerts['date_created'].dt.dayofweek

    # Shift alert counts to create a lag-based target
    daily_alerts['next_day_alerts'] = daily_alerts['alert_count'].shift(-1)
    daily_alerts.dropna(inplace=True)

    # Features and target
    features = ['alert_count', 'day_of_week']
    target = 'next_day_alerts'

    X = daily_alerts[features]
    y = daily_alerts[target]

    # Normalize features
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Gradient Boosting model
    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)

    # Save the model and scaler
    with open('alert_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('alert_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    print("Alert prediction model trained and saved successfully!")

def predict_future_alerts():
    # Ensure model and scaler are available; if not, train them
    if not os.path.exists('alert_model.pkl') or not os.path.exists('alert_scaler.pkl'):
        print("Model or scaler not found. Training the alert prediction model...")
        train_alert_model()

    # Load the model and scaler
    with open('alert_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('alert_scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    # Load alert data
    data = load_alert_data()
    if data.empty:
        # Default prediction if no data is available
        return {str((pd.Timestamp.now() + timedelta(days=i)).date()): 0 for i in range(7)}

    # Prepare recent data for prediction
    daily_alerts = data.resample('D').size().reset_index(name='alert_count')
    last_day = daily_alerts.iloc[-1]
    recent_data = pd.DataFrame({
        'alert_count': [last_day['alert_count']],
        'day_of_week': [last_day['date_created'].dayofweek]
    })

    # Normalize recent data
    recent_data = scaler.transform(recent_data)

    # Predict alerts for the next 7 days
    future_alerts = {}
    for i in range(7):
        predicted_alerts = model.predict(recent_data)[0]
        predicted_alerts = max(0, int(predicted_alerts))
        date = (pd.Timestamp.now() + timedelta(days=i + 1)).strftime('%Y-%m-%d')
        future_alerts[date] = predicted_alerts

        # Update recent_data for the next prediction
        recent_data = scaler.transform(pd.DataFrame({
            'alert_count': [predicted_alerts],
            'day_of_week': [(pd.Timestamp.now() + timedelta(days=i + 1)).weekday()]
        }))

    return future_alerts

def analytics_view(request):
    all_data = load_and_prepare_alldata()
    individual_data = load_and_prepare_individual_data()
    restaurant_data = load_and_prepare_restaurant_data()
    ranked_data = rank_donators(all_data)
    ranked_data_GBC = rank_donators_using_GBC(all_data)
    ranked_data_RF = rank_donators_rf(all_data)
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
        'ranked_donators': ranked_data,
        'ranked_individual_donators': individual_ranked_data,
        'ranked_restaurant_donators': restaurant_ranked_data,
        'top_donor_name': ranked_data[0]['name'] if ranked_data else "No Donors",
        'top_individual_donor_name': individual_ranked_data[0]['name'] if individual_ranked_data else "No Donors",
        'top_restaurant_donor_name': restaurant_ranked_data[0]['name'] if restaurant_ranked_data else "No Donors",
        'total_volume': all_data['donation_volume'].sum(),
        'pie_chart_data': pie_chart_data,
        'response_emergency_data': response_emergency_json,
        'location_data': json.dumps(location_data),
        'future_alerts': json.dumps(future_alerts),
    }

    return render(request, 'webpages/analytics.html', context)