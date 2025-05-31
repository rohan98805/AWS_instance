from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, BuyerProfile, SellerProfile, LandProperty, LegalCase, OwnershipHistory

from django import forms
from .models import CustomUser

from django import forms
from .models import CustomUser

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_buyer', 'is_seller',
                  'adhar_card', 'pan_card', 'profile_photo', 'is_verified']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'adhar_card': forms.ClearableFileInput(),
            'pan_card': forms.ClearableFileInput(),
            'profile_photo': forms.ClearableFileInput(),
            'is_verified': forms.CheckboxInput(),  # renders checkbox
        }


class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_buyer', 'is_seller',
                  'adhar_card', 'pan_card', 'profile_photo', 'is_verified']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'adhar_card': forms.ClearableFileInput(),
            'pan_card': forms.ClearableFileInput(),
            'profile_photo': forms.ClearableFileInput(),
            'is_verified': forms.CheckboxInput(),  # renders checkbox
        }


# forms.py
from django import forms
from .models import LandRecord, LandImage
from django.forms.models import modelformset_factory

class LandRecordForm(forms.ModelForm):
    class Meta:
        model = LandRecord
        fields = ['place', 'area', 'land_type']

LandImageFormSet = modelformset_factory(
    LandImage,
    fields=('image',),
    extra=5,  # You can allow more if needed
    min_num=5,
    validate_min=True
)

from django import forms
from .models import CustomUser

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'adhar_card', 'pan_card', 'profile_photo', 'is_buyer', 'is_seller']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'adhar_card': forms.ClearableFileInput(),
            'pan_card': forms.ClearableFileInput(),
            'profile_photo': forms.ClearableFileInput(),
        }


# forms.py
from django import forms
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(queryset=User.objects.all(), label='To')

    class Meta:
        model = Message
        fields = ['receiver', 'subject', 'body', 'attachment']
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'body': forms.Textarea(attrs={'placeholder': 'Write your message here...', 'rows': 4}),
        }


class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = BuyerProfile
        fields = ['preferred_area', 'budget_min', 'budget_max']
        widgets = {
            'preferred_area': forms.Select(),
            'budget_min': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Minimum Budget'}),
            'budget_max': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Maximum Budget'}),
        }


class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = []  # Admin sets verification; no user-editable fields currently


class LandPropertyForm(forms.ModelForm):
    class Meta:
        model = LandProperty
        fields = [
            'sellers', 'place', 'location', 'map_url', 'latitude', 'longitude',
            'is_ekhata_registered', 'land_use_type', 'expected_price',
            'description', 'is_sold', 'registration_number', 'last_tax_paid_receipt'
        ]
        widgets = {
            'sellers': forms.SelectMultiple(),
            'place': forms.Select(),
            'location': forms.TextInput(attrs={'placeholder': 'Location'}),
            'map_url': forms.URLInput(attrs={'placeholder': 'Google Map URL'}),
            'latitude': forms.NumberInput(attrs={'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'step': 'any'}),
            'land_use_type': forms.Select(),
            'expected_price': forms.NumberInput(attrs={'min': 0}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'registration_number': forms.TextInput(),
            'last_tax_paid_receipt': forms.ClearableFileInput(),
        }


class LegalCaseForm(forms.ModelForm):
    class Meta:
        model = LegalCase
        fields = ['land', 'case_number', 'document', 'remarks']
        widgets = {
            'land': forms.Select(),
            'case_number': forms.TextInput(),
            'document': forms.ClearableFileInput(),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }


class OwnershipHistoryForm(forms.ModelForm):
    class Meta:
        model = OwnershipHistory
        fields = ['land', 'owner_name', 'ownership_order', 'new_owner']
        widgets = {
            'land': forms.Select(),
            'owner_name': forms.TextInput(),
            'ownership_order': forms.NumberInput(attrs={'min': 1}),
            'new_owner': forms.Select(),
        }
