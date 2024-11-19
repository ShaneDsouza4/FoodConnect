# alerts/forms.py
from django import forms
from .models import Alert, ResponseToDonation

class CreateAlertForm(forms.Form):
    item_name = forms.CharField(
        label="Item Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specify the name of the item needed.'})
    )
    quantity_needed = forms.IntegerField(
        label="Quantity Needed",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Provide an estimated amount required'})
    )
    urgency_level = forms.ChoiceField(
        label="Urgency Level",
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        initial='medium',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add any additional details to clarify your request.', 'rows': 4})
    )

class ResponseToDonationFormX(forms.ModelForm):
    # Adding additional fields for user input
    name = forms.CharField(
        max_length=100,
        label="Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'})
    )
    address = forms.CharField(
        max_length=255,
        label="Address",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Address'})
    )
    item = forms.CharField(
        max_length=100,
        label="Item",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item you wish to donate'})
    )
    quantity = forms.IntegerField(
        label="Quantity",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity to donate'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional Details', 'rows': 4}),
        required=False,
        label="Additional Details"
    )

    class Meta:
        model = ResponseToDonation
        fields = ['description', 'name', 'address', 'item', 'quantity']

class RespondToDonationForm(forms.Form):
    quantity_donated = forms.IntegerField(
        label="Quantity Donated",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity to donate', 'min': 1})
    )
    description = forms.CharField(
        label="Additional Details",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional details about the donation', 'rows': 3})
    )
    pickup_method = forms.ChoiceField(
        label="Pickup/Delivery Method",
        choices=[
            ('pickup', 'Pickup by Food Bank'),
            ('delivery', 'Delivery by Donor'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    pickup_delivery_date = forms.DateField(
        label="Pickup/Delivery Date",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    donor_address = forms.CharField(
        label="Donor Address",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your address for pickup (if applicable)', 'rows': 2})
    )