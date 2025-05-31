# decorators.py
from django.shortcuts import redirect
from django.contrib import messages

def seller_verified_required(view_func):
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'sellerprofile') and request.user.sellerprofile.verified_by_admin:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied. Seller is not verified.")
        return redirect('home')
    return wrapper
