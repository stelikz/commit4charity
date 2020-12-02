from django.contrib import admin
from django.urls import include, path
"""project_1_37 URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('accounts/', include('allauth.urls')),

    path('profile/',views.profile,name='profile'),
    path('profile/<int:u_id>/', views.profile, name='profile'),
    path('profile/volunteering/', views.profile_volunteering, name='my_volunteering'),
    path('profile/donations/', views.profile_donation, name='my_donations'),
    path('profile/donations/checkout/<int:id>', views.profile_checkout, name='donate'),
    path('profile/created_volunteering/', views.profile_created_volunteering, name='created_volunteering'),
    path('profile/created_donations/', views.profile_created_donations, name='created_donations'),
    path('profile/created_donations/checkout/<int:id>', views.profile_checkout, name='donate'),
    
    path('save_settings/', views.save_settings, name='save'),
    path('settings/', views.user_settings, name='settings'),
    path('leaderboard/',views.leaderboard,name='leaderboard'),

    path('apply/<int:id>', views.apply, name='signup'),
    path('remove/<int:id>', views.remove_signup, name='un_signup'),
    path('delete/<int:id>', views.delete_event, name='delete_event'),

    path('volunteer_post/', views.volunteer_post, name='volunteer_post'),
    path('volunteer_list/', views.volunteer_list, name='volunteer_list'),

    path('donation_post/', views.donation_post, name='donation_post'),
    path('donation_list/', views.donation_list, name='donation_list'),
    path('donation_list/checkout/<int:id>', views.profile_checkout, name='donate'),
    path('checkout/<int:id>/confirm', views.profile_checkout_confirm, name='confirm'),
    
]