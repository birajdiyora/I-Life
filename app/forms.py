# from django import forms
# from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

# class RegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput, label="Password")
#     confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
#     phone_number = forms.CharField(max_length=15, label="Phone Number")

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email','phone_number','password','confirm_password']

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")

#         if password and confirm_password and password != confirm_password:
#             raise ValidationError("Passwords do not match")

#         return cleaned_data


from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Product

# class RegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput, label="Password")
#     confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
#     is_superuser = forms.BooleanField(required=False, label='Register as Superuser')

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")

#         if password and confirm_password and password != confirm_password:
#             raise ValidationError("Passwords do not match")

#         return cleaned_data

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        
        return cleaned_data
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image']
