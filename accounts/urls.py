from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', base, name='base'),
    path('home/', home, name='home'),
    
    # Authentication
    path('register/', register_user, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('adminUser/', admin_user_list, name='admin_customuser_list'),
    
    path('admincustom-users/edit/<int:user_id>/',
            admin_customuser_edit,
            name='admin_customuser_edit'),
    # Profile
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/change-password/', change_password, name='change_password'),
    
    # Messaging
    path('messages/send/', send_message, name='send_message'),
    path('messages/inbox/', inbox, name='inbox'),
    path('messages/<int:message_id>/', view_message, name='view_message'),

    # Land Property CRUD
    path('land/list/', landproperty_list, name='landproperty_list'),
    path('land/add/', landproperty_create, name='landproperty_create'),
    path('land/update/<int:pk>/', landproperty_update, name='landproperty_update'),
    path('land/delete/<int:pk>/', landproperty_delete, name='landproperty_delete'),

    # Legal Case CRUD
    path('legalcase/list/', legalcase_list, name='legalcase_list'),
    path('legalcase/add/', legalcase_create, name='legalcase_create'),
    path('legalcase/update/<int:pk>/', legalcase_update, name='legalcase_update'),
    path('legalcase/delete/<int:pk>/', legalcase_delete, name='legalcase_delete'),

    # Ownership History CRUD
    path('ownershiphistory/list/', ownershiphistory_list, name='ownershiphistory_list'),
    path('ownershiphistory/add/', ownershiphistory_create, name='ownershiphistory_create'),
    path('ownershiphistory/update/<int:pk>/', ownershiphistory_update, name='ownershiphistory_update'),
    path('ownershiphistory/delete/<int:pk>/', ownershiphistory_delete, name='ownershiphistory_delete'),

    # Buyer and Seller Profiles
    path('buyer/profile/', buyer_profile, name='buyer_profile'),
    path('seller/profile/', seller_profile, name='seller_profile'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)