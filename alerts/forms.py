# alerts/forms.py
from django import forms
from .models import Alert, ResponseToDonation

class CreateAlertForm(forms.Form):
    item_name = forms.CharField(
        label="Item Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name'})
    )
    quantity_needed = forms.IntegerField(
        label="Quantity Needed",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity Needed'})
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
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': 4})
    )

class ResponseToDonationForm(forms.ModelForm):
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