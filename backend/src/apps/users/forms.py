from django import forms
from django.forms import ImageField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserCreationForm(UserCreationForm):
    """ UserCreationForm extended with email"""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        profile = UserProfile(user=user)
        if commit:
            user.save()
            profile.save()
        return user


class UserProfileForm(forms.ModelForm):
    avatar = ImageField(required=True)

    class Meta:
        model = UserProfile
        fields = [
            "avatar",
        ]
