from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile, VolunteerOpportunity, DonationOpportunity, DonationTransaction
# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'
class UserAdmin(BaseUserAdmin): # Define a new User admin
    inlines = (ProfileInline,)
    readonly_fields = ('id',)

class VolunteerOpportunityAdmin(admin.ModelAdmin):
    search_fields = ['description']
class DonationOpportunityAdmin(admin.ModelAdmin):
    search_fields = ['description']
class DonationTransactionAdmin(admin.ModelAdmin):
    search_fields = ['description']
    
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(VolunteerOpportunity, VolunteerOpportunityAdmin)
admin.site.register(DonationOpportunity, DonationOpportunityAdmin)
admin.site.register(DonationTransaction, DonationTransactionAdmin)