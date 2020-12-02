###############################################################################
#   REFERENCES
#   Title: Bootstrap Datepicker Plus
#   Author: Munim Munna
#   Date: 9/14/18
#   Code version: 3.0.5
#   URL: https://pypi.org/project/django-bootstrap-datepicker-plus/ 
#   Software License: Apache Software License (2.0)
###############################################################################

from django.contrib import admin
from django.urls import include, path

from django import forms
from django.forms import ModelForm
from django.forms import ValidationError

from django.contrib.auth.models import User
from .models import VolunteerOpportunity
from .models import DonationOpportunity, DonationTransaction

from bootstrap_datepicker_plus import DateTimePickerInput, TimePickerInput
from django.core import validators
from django.utils import timezone
import string

class NameForm(forms.Form):
    name1 = forms.CharField(label='Name 1:', max_length=100)
    name2 = forms.CharField(label='Name 2:', max_length=100)
    name3 = forms.CharField(label='Name 3:', max_length=100)

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = VolunteerOpportunity
        fields = '__all__'
        #fields = ('start_datetime', 'hours', 'description', 'location', 'volunteers_needed')
        #volunteers_needed = forms.IntegerField(validators=[validators.MinValueValidator(1,"The number of volunteers needed must be at least one.")])
        exclude = ['volunteers', 'created_by']
        labels = {
            'start_datetime': 'Date and Time',
            'event_name': 'Event Name',
            'hours': 'Volunteering Hours',
            'description': 'Event Description',
            'location': 'Location',
            'volunteers_needed': 'Volunteers Needed',
        }
        widgets = {
            'start_datetime': DateTimePickerInput(), # leave as military time for now - format="MM/DD/YYYY HH:mm A"
            'hours': TimePickerInput(),
        }

    def clean_volunteers_needed(self):
        ''' Do not save an event with 0 volunteers needed '''
        num_volunteers = self.cleaned_data["volunteers_needed"]
        if num_volunteers < 1:
            raise forms.ValidationError("The number of volunteers needed at the event must be at least one.", code='invalid')
        return num_volunteers

    def clean_start_datetime(self):
        ''' Do not save an event that is scheduled to occur in the past '''
        start_date_time = self.cleaned_data["start_datetime"]
        current_time = timezone.now()
        if start_date_time <= current_time: # in past 
            raise forms.ValidationError("You cannot create an event that occurs in the past.")
        return start_date_time

class TransactionForm(forms.ModelForm):
    class Meta:
        model = DonationTransaction
        fields = '__all__'
        exclude = ['donator','donated_to','transaction_date']
        labels = {
            'amount_donated' : 'Amount (in US dollars)',
        }

class DonationForm(forms.ModelForm):
    class Meta:
        model = DonationOpportunity
        exclude = ['d_date', 'd_amount', 'd_donator', 'd_created_by', 'd_total_received']
        # fields = ('d_org', 'd_description', 'd_causes', )
        labels = {
            'd_org': 'Organization Name',
            'd_description': 'Donation Opportunity Description',
            'd_causes': "Relevant Causes"
        }

class PayForm(forms.ModelForm):
    class Meta:
        model = DonationOpportunity
        exclude = ['d_org', 'd_description', 'd_date', 'd_donator', 'd_created_by', 'd_causes']
        labels = {
            'd_amount': 'Donation Amount',
        }  
 
class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
    def clean_username(self):
        username = self.cleaned_data['username']
        allowed = set(string.ascii_lowercase + string.ascii_uppercase + string.digits + '@.+-_')
        if not set(username) <= allowed:
            raise ValidationError('Username contains invalid characters. Please select a different Username.')
        return username
    def clean_first_name(self):
        fname = self.cleaned_data['first_name']
        allowed = set(string.ascii_lowercase + string.ascii_uppercase + '.- ')
        if not set(fname) <= allowed:
            raise ValidationError('First name should contain letters and ./- only.')
        return fname
    def clean_last_name(self):
        lname = self.cleaned_data['last_name']
        allowed = set(string.ascii_lowercase + string.ascii_uppercase + '.- ')
        if not set(lname) <= allowed:
            raise ValidationError('Last name should contain letters and ./- only.')
        return lname