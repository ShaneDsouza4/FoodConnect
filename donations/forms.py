from django import forms


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

