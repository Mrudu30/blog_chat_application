from django import forms
from .models import Hobby,blogchatUser
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import get_user_model,authenticate

User = get_user_model()

# login and sign up forms for easier integration of user in view.
class CustomUserCreationForm(UserCreationForm):
    hobbies = forms.ModelMultipleChoiceField(queryset=Hobby.objects.all(), required=False)

    class Meta:
        model = blogchatUser
        fields = ['username', 'first_name', 'last_name', 'email', 'dob', 'mobile_number', 'password1', 'password2', 'hobbies']

class CustomAuthenticationForm(AuthenticationForm):
    def get_user(self):
        return self.user

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # Authenticate user
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError("Invalid username or password.")

        return self.cleaned_data

    class Meta:
        model = blogchatUser
        fields = ['username', 'password']