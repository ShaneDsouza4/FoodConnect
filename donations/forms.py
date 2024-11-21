from django import forms

from donations.models import Category, Product


class CreateDonationForm(forms.Form):
    item = forms.CharField(
        label="Item Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name'})
    )

    quantity= forms.IntegerField(
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

class AddProductForm(forms.Form):
    name = forms.CharField(
        label="Product Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Product Name'}),
    )
    description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter a brief description', 'rows': 4}),
    )
    category = forms.ChoiceField(
        label="Category",
        choices=[(cat.id, cat.name) for cat in Category.objects.all()],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    quantity = forms.IntegerField(
        label="Quantity",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Quantity'}),
    )
    weight = forms.IntegerField(
        label="Weight",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Weight'}),
    )
    unit = forms.ChoiceField(
        label="Unit",
        choices=Product.UNIT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    expiry_date = forms.DateField(
        label="Expiry Date",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    image = forms.URLField(
        label="Image URL",
        max_length=300,
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter Image URL'}),
    )