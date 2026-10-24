from django import forms
from .models import Customer, LaundryOrder, Payment, Service, BusinessInformation


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['full_name', 'phone', 'email', 'address']

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter address'
            }),
        }


class LaundryOrderForm(forms.ModelForm):

    class Meta:
        model = LaundryOrder

        fields = [
            'customer',
            'service',
            'quantity',
            'total_amount',
            'status',
            'pickup_date'
        ]

        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-select'
            }),

            'service': forms.Select(attrs={
                'class': 'form-select'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),

            'total_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount in UGX'
            }),

            'status': forms.Select(attrs={
                'class': 'form-select'
            }),

            'pickup_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }


class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ['service_name', 'price', 'description']

        widgets = {
            'service_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter service name'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price in UGX'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter a brief description (optional)'
            }),
        }


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ['order', 'amount_paid', 'payment_method', 'payment_date', 'reference']

        widgets = {
            'order': forms.Select(attrs={
                'class': 'form-select'
            }),
            'amount_paid': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount paid'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'payment_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),
            'reference': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Transaction ID (Optional)'
            }),
        }

class BusinessInformationForm(forms.ModelForm):
    class Meta:
        model = BusinessInformation
        fields = [
            'business_name',
            'phone',
            'email',
            'address',
            'receipt_footer',
        ]

        widgets = {
            'business_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter laundry shop name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter business email'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter physical address'
            }),
            'receipt_footer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter message for customers'
            }),
        }

    def clean_business_name(self):
        name = self.cleaned_data['business_name'].strip()

        if not name:
            raise forms.ValidationError(
                'Please enter the business name.'
            )

        return name
