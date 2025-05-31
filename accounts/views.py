from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .models import *
from .forms import *
from .web3_setup import web3
from web3 import Web3
import json

# Web3 Connection
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

def base(request):
    return render(request, 'base.html')

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# Only allow staff users to view this page
@user_passes_test(lambda u: u.is_staff)
def admin_user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'custom/admin_customuser_list.html', {'users': users})

from django.shortcuts import render
from .models import LandProperty, LegalCase, OwnershipHistory
from django.shortcuts import render
from .models import LandProperty, LegalCase, OwnershipHistory, LandImage

from django.db.models import Prefetch

def home(request):
    # Prefetch legal_cases and ownership_history with ordering and related user for ownership_history if needed
    legal_cases_prefetch = Prefetch('legalcase_set', queryset=LegalCase.objects.all())
    ownership_history_prefetch = Prefetch(
        'ownershiphistory_set',
        queryset=OwnershipHistory.objects.all().order_by('ownership_order')
    )
    # Prefetch images from land_record relation
    land_properties = LandProperty.objects.all()\
        .select_related('land_record')\
        .prefetch_related(
            'sellers',
            legal_cases_prefetch,
            ownership_history_prefetch,
            Prefetch('land_record__images')
        )


    property_data = []
    for land in land_properties:
        legal_cases = getattr(land, 'legalcase_set', []).all()
        ownership_history = getattr(land, 'ownershiphistory_set', []).all()

        images = land.land_record.images.all() if land.land_record else []

        property_data.append({
            'land': land,
            'legal_cases': legal_cases,
            'ownership_history': ownership_history,
            'images': images,
        })

    return render(request, 'dashboard/home.html', {'property_data': property_data})



# Registration with Web3 Verification
def register_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')  # Replace with your actual login URL name
        else:
            messages.error(request, 'Form validation failed. Please check the input.')
    else:
        form = CustomUserForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})





from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # important, to keep user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'users/send_message.html', {'form': form})

@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'users/inbox.html', {'messages': messages})

@login_required
def view_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id, receiver=request.user)
    if not msg.is_read:
        msg.is_read = True
        msg.save()
    return render(request, 'users/view_message.html', {'msg': msg})

# Utility decorator

def verified_user_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'sellerprofile') or not request.user.sellerprofile.verified_by_admin:
            messages.error(request, "Access denied. Admin verification required.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# LandProperty CRUD

@login_required
@verified_user_required
def landproperty_list(request):
    properties = LandProperty.objects.all()
    return render(request, 'land/landproperty_list.html', {'properties': properties})

@login_required
@verified_user_required
def landproperty_create(request):
    if request.method == 'POST':
        form = LandPropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Property added successfully.")
            return redirect('landproperty_list')
    else:
        form = LandPropertyForm()
    return render(request, 'land/landproperty_form.html', {'form': form})

@login_required
@verified_user_required
def landproperty_update(request, pk):
    property = get_object_or_404(LandProperty, pk=pk)
    if request.method == 'POST':
        form = LandPropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated successfully.")
            return redirect('landproperty_list')
    else:
        form = LandPropertyForm(instance=property)
    return render(request, 'land/landproperty_form.html', {'form': form})

@login_required
@verified_user_required
def landproperty_delete(request, pk):
    property = get_object_or_404(LandProperty, pk=pk)
    if request.method == 'POST':
        property.delete()
        messages.success(request, "Property deleted successfully.")
        return redirect('landproperty_list')
    return render(request, 'legal/confirm_delete.html', {'object': property, 'title': 'Delete Property'})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import LegalCase, OwnershipHistory, BuyerProfile, SellerProfile
from .forms import LegalCaseForm, OwnershipHistoryForm, BuyerProfileForm, SellerProfileForm

# Utility: Check if user is verified seller

def is_verified(user):
    return hasattr(user, 'sellerprofile') and user.sellerprofile.verified_by_admin

# LEGAL CASE CRUD

@login_required
@user_passes_test(is_verified)
def legalcase_list(request):
    cases = LegalCase.objects.all()
    return render(request, 'legal/legalcase_list.html', {'cases': cases})

@login_required
@user_passes_test(is_verified)
def legalcase_create(request):
    form = LegalCaseForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('legalcase_list')
    return render(request, 'legal/form_template.html', {'form': form, 'title': 'Add Legal Case'})

@login_required
@user_passes_test(is_verified)
def legalcase_update(request, pk):
    case = get_object_or_404(LegalCase, pk=pk)
    form = LegalCaseForm(request.POST or None, request.FILES or None, instance=case)
    if form.is_valid():
        form.save()
        return redirect('legalcase_list')
    return render(request, 'legal/form_template.html', {'form': form, 'title': 'Edit Legal Case'})

@login_required
@user_passes_test(is_verified)
def legalcase_delete(request, pk):
    case = get_object_or_404(LegalCase, pk=pk)
    if request.method == 'POST':
        case.delete()
        return redirect('legalcase_list')
    return render(request, 'legal/confirm_delete.html', {'object': case, 'title': 'Delete Legal Case'})

# OWNERSHIP HISTORY CRUD

@login_required
@user_passes_test(is_verified)
def ownershiphistory_list(request):
    history = OwnershipHistory.objects.all()
    return render(request, 'owner/ownershiphistory_list.html', {'history': history})

@login_required
@user_passes_test(is_verified)
def ownershiphistory_create(request):
    form = OwnershipHistoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('ownershiphistory_list')
    return render(request, 'legal/form_template.html', {'form': form, 'title': 'Add Ownership History'})

@login_required
@user_passes_test(is_verified)
def ownershiphistory_update(request, pk):
    record = get_object_or_404(OwnershipHistory, pk=pk)
    form = OwnershipHistoryForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('ownershiphistory_list')
    return render(request, 'legal/form_template.html', {'form': form, 'title': 'Edit Ownership History'})

@login_required
@user_passes_test(is_verified)
def ownershiphistory_delete(request, pk):
    record = get_object_or_404(OwnershipHistory, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('ownershiphistory_list')
    return render(request, 'legal/confirm_delete.html', {'object': record, 'title': 'Delete Ownership History'})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserForm  # You need to create this form based on CustomUser

# views.py
from .forms import CustomUserEditForm
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserEditForm

@staff_member_required
def admin_customuser_edit(request, user_id):
    user_obj = get_object_or_404(CustomUser, pk=user_id)

    if request.method == "POST":
        form = CustomUserEditForm(request.POST, request.FILES, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"User '{user_obj.username}' updated successfully.")
            return redirect('admin_customuser_list')  # Ensure this URL name exists
    else:
        form = CustomUserEditForm(instance=user_obj)

    return render(request, 'custom/customuser_edit.html', {'form': form, 'user_obj': user_obj})



# BUYER PROFILE

@login_required
def buyer_profile(request):
    try:
        profile = BuyerProfile.objects.get(user=request.user)
    except BuyerProfile.DoesNotExist:
        profile = None

    form = BuyerProfileForm(request.POST or None, instance=profile)
    if form.is_valid():
        form.save()
    return render(request, 'legal/form_template.html', {'form': form, 'title': 'Buyer Profile'})

# SELLER PROFILE

@login_required
def seller_profile(request):
    profile, created = SellerProfile.objects.get_or_create(user=request.user)
    form = SellerProfileForm(request.POST or None, instance=profile)
    if form.is_valid():
        form.save()
    return render(request, 'legal/form_template.html', {'form': form, 'title': 'Seller Profile'})

































