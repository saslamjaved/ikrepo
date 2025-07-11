# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))

class CustomUserCreationForm(UserCreationForm):
    # Additional fields for the custom user model
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=False, help_text='Optional.')
    avatar = forms.ImageField()
    address = forms.CharField(widget=forms.Textarea, required=False, help_text='Optional.')
    street_address = forms.CharField(widget=forms.Textarea, required=False, help_text='Optional.')
    city = forms.CharField(widget=forms.Textarea, required=False, help_text='Optional.')
    state = forms.CharField(widget=forms.Textarea, required=False, help_text='Optional.')
    postal_code = forms.CharField(widget=forms.Textarea, required=False, help_text='Optional.')
    country = forms.CharField(widget=forms.Textarea, required=False, help_text='Optional.')
    user_type = forms.ChoiceField(choices=User.USER_GROUPS, initial='consumer')
    acceptTerms = forms.BooleanField(initial=False)
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'address', 'user_type', 'password1','password2', 'acceptTerms')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email address already exists.")
        return email


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar','first_name', 'last_name', 'phone_number', 'address', 'country', 'state', 'city', 'postal_code', 'street_address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

