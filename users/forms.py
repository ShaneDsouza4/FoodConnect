from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

CANADA_PROVINCES_AND_TERRITORIES = [
    ('', 'Select State'),
    ('AB', 'Alberta'),
    ('BC', 'British Columbia'),
    ('MB', 'Manitoba'),
    ('NB', 'New Brunswick'),
    ('NL', 'Newfoundland and Labrador'),
    ('NS', 'Nova Scotia'),
    ('ON', 'Ontario'),
    ('PE', 'Prince Edward Island'),
    ('QC', 'Quebec'),
    ('SK', 'Saskatchewan'),
    ('NT', 'Northwest Territories'),
    ('NU', 'Nunavut'),
    ('YT', 'Yukon')
]

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

# Restaruraant form
class CreateRestaurantForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    restaurant_name = forms.CharField(
        label="Restaurant Name",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Restaurant Name'})
    )
    restaurant_phone = forms.CharField(
        label="Phone Number",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    street = forms.CharField(
        label="Street Address",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'})
    )
    city = forms.CharField(
        label="City",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    state = forms.ChoiceField(
        label="State",
        choices=CANADA_PROVINCES_AND_TERRITORIES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    country = forms.CharField(
        label="Country",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'})
    )
    postal_code = forms.CharField(
        label="Postal Code",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'})
    )
    website = forms.URLField(
        label="Website (optional)",
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website (optional)'})
    )
    id_verification = forms.ImageField(
        label="ID Card image",
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

# Foodbank Form
class CreateFoodBankForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    foodbank_name = forms.CharField(
        label="Food Bank Name",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Food Bank Name'})
    )
    foodbank_phone = forms.CharField(
        label="Phone Number",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    street = forms.CharField(
        label="Street Address (Shipping Accessible)",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'})
    )
    city = forms.CharField(
        label="City",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    state = forms.ChoiceField(
        label="State",
        choices=CANADA_PROVINCES_AND_TERRITORIES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    country = forms.CharField(
        label="Country",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'})
    )
    postal_code = forms.CharField(
        label="Postal Code",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'})
    )
    website = forms.URLField(
        label="Website (optional)",
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website (optional)'})
    )
    id_verification = forms.ImageField(
        label="ID Verification",
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

# Individual Form
class CreateIndividualForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    phone_number = forms.CharField(
        label="Phone Number",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    street_address = forms.CharField(
        label="Street Address (Shipping Accessible)",
        max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'})
    )
    city = forms.CharField(
        label="City",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    state = forms.ChoiceField(
        label="State",
        choices=CANADA_PROVINCES_AND_TERRITORIES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    country = forms.CharField(
        label="Country",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'})
    )
    postal_code = forms.CharField(
        label="Postal Code",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'})
    )
    id_verification = forms.ImageField(
        label="ID Verification (optional)",
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

#Edit Restaurant Form
class EditRestaurantForm(forms.Form):
    restaurant_name = forms.CharField(
        label="Restaurant Name",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Restaurant Name'})
    )
    restaurant_phone = forms.CharField(
        label="Phone Number",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    street = forms.CharField(
        label="Street Address (Shipping Accessible)",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'})
    )
    city = forms.CharField(
        label="City",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    state = forms.ChoiceField(
        label="State",
        choices=CANADA_PROVINCES_AND_TERRITORIES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    country = forms.CharField(
        label="Country",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'})
    )
    postal_code = forms.CharField(
        label="Postal Code",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'})
    )
    website = forms.URLField(
        label="Website (optional)",
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website (optional)'})
    )

#Edit Food Bank Form
class EditFoodBankForm(forms.Form):
    foodbank_name = forms.CharField(
        label="Food Bank Name",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Food Bank Name'})
    )
    foodbank_phone = forms.CharField(
        label="Phone Number",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    street = forms.CharField(
        label="Street Address (Shipping Accessible)",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'})
    )
    city = forms.CharField(
        label="City",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    state = forms.ChoiceField(
        label="State",
        choices=CANADA_PROVINCES_AND_TERRITORIES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    country = forms.CharField(
        label="Country",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'})
    )
    postal_code = forms.CharField(
        label="Postal Code",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'})
    )
    website = forms.URLField(
        label="Website (optional)",
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website (optional)'})
    )

#Edit Individual Form
class EditIndividualForm(forms.Form):
    first_name = forms.CharField(
        label="First Name",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    phone_number = forms.CharField(
        label="Phone Number",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    street_address = forms.CharField(
        label="Street Address (Shipping Accessible)",
        max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'})
    )
    city = forms.CharField(
        label="City",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    state = forms.ChoiceField(
        label="State",
        choices=CANADA_PROVINCES_AND_TERRITORIES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    country = forms.CharField(
        label="Country",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'})
    )
    postal_code = forms.CharField(
        label="Postal Code",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'})
    )