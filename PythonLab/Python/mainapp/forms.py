from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    '''def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата атрымання замовы'
    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))'''

    class Meta:
        model = Order
        fields = (
            'first_name', 'second_name', 'third_name', 'phone', 'address', 'buying_type', 'order_data', 'comment'
        )
