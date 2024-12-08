from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, FloorMap

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class FloorMapForm(forms.ModelForm):
    class Meta:
        model = FloorMap
        fields = ['name', 'floor_type', 'width', 'length', 'num_rooms', 'num_bedrooms', 'num_kitchens', 'num_bathrooms', 'num_washrooms', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'prompt': forms.Textarea(attrs={'rows': 4}),
        }

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=[('user', 'User'), ('designer', 'Designer')])

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'user_type')