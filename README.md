# FoodConnect: Connecting Communities to Combat Food Insecurity

FoodConnect is a platform that bridges the gap between food donors and food banks, enabling efficient resource allocation to address hunger and food waste. The platform empowers individuals, restaurants, and organizations to donate surplus food and other essential resources, helping food banks meet community needs effectively.

---

## Features

### 🥗 **For Donors**
- **Food Donations**: Donate fresh, frozen, canned, cooked, and packaged food items.
- **Custom Categories**: Easily categorize donations (e.g., beverages, dairy, fresh produce).
- **Real-Time Contribution Tracking**: View the impact of your donations.
- **Donor Rankings**: Ranked system to recognize top contributors using advanced scoring algorithms.

### 🍞 **For Food Banks**
- **Alert System**: Create detailed alerts to request specific items based on urgency and need.
- **Response Management**: Receive real-time updates from donors responding to alerts.
- **Analytics Dashboard**: Gain insights into donation patterns and resource availability.

### 📈 **Advanced Features**
- **Alert Prediction**: Predict future food bank needs using machine learning algorithms like Gradient Boosting Regressor.
- **Donation Scaling**: Conversion factors ensure consistent measurement across different units (e.g., grams to kilograms, milliliters to liters).
- **Community Engagement**: Encourage collaboration between donors and food banks with detailed user profiles and feedback systems.

---

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Django Framework
- Virtual Environment (optional but recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/foodconnect.git
   cd foodconnect

## Technologies Used

- **Backend**: Built using Django, a high-level Python web framework that simplifies complex backend development.
- **Frontend**: Designed with HTML, CSS, and Bootstrap for responsive and user-friendly interfaces.
- **Database**: Utilizes SQLite by default for quick setup, with support for PostgreSQL and MySQL for production environments.
- **Machine Learning**: Incorporates Scikit-learn for:
  - **Alert Prediction**: Predicting future food bank needs.
  - **Donor Ranking**: Implementing non-linear scoring models like Gradient Boosting Regressor.
- **Unit Conversion**: Ensures consistent donation measurements using custom scaling logic for grams, kilograms, milliliters, and liters.
- **Notification System**: Integrated email notification for seamless communication between donors and food banks.
- **Analytics and Visualization**: Real-time dashboards and insights using Pandas and Matplotlib.

---

## Usage

### For Donors
1. **Sign Up**: Register as an individual, restaurant, or organization.
2. **Submit Donations**:
   - Navigate to the "Donate Today" form.
   - Enter details like product type, quantity, weight, and expiration date.
   - Choose between pickup by the food bank or self-delivery.
3. **Track Contributions**:
   - Monitor donation history.
   - View ranking in the Top Donors leaderboard.

### For Food Banks
1. **Sign Up**: Register as a food bank or nonprofit organization.
2. **Create Alerts**:
   - Specify needed items, quantity, and urgency level.
   - Add details like expiration tolerance and pickup options.
3. **Manage Responses**:
   - Approve or decline donor submissions.
   - Communicate with donors for pickup or delivery arrangements.

### Advanced Features
- **Alert Prediction**:
  - Automatically predicts the number of alerts needed in the coming week.
  - Assists food banks in proactive planning and resource allocation.
- **Donor Ranking**:
  - Recognizes top contributors using a weighted scoring system.
  - Encourages community engagement through visible rankings.

By streamlining food donations and enabling better planning, the platform connects donors and food banks effectively to combat food insecurity.

