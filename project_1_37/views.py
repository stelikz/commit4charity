from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.contrib.auth.decorators import login_required

# additional imports from here-down
from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User, AnonymousUser
from django.db import IntegrityError

from .models import DonationOpportunity, VolunteerOpportunity, Profile, DonationTransaction
from .forms import NameForm, ContactForm, DonationForm, VolunteerForm, UserSettingsForm, TransactionForm

from django.utils import timezone

from decimal import *

def apply(request, id):
    v1 = VolunteerOpportunity.objects.get(id=id)
    v1.volunteers.add(request.user)
    v1.volunteers_needed = v1.volunteers_needed - 1
    v1.save(update_fields=['volunteers_needed'])

    user = Profile.objects.get(id=request.user.id)
    user.points += v1.hours.hour*10
    user.save(update_fields=['points'])

    return redirect(reverse('my_volunteering'))
def remove_signup(request, id):
    v1 = VolunteerOpportunity.objects.get(id=id)
    v1.volunteers.remove(request.user)
    v1.volunteers_needed = v1.volunteers_needed + 1
    v1.save(update_fields=['volunteers_needed'])

    user = Profile.objects.get(id=request.user.id)
    user.points -= v1.hours.hour*10
    user.save(update_fields=['points'])
    
    return redirect(reverse('my_volunteering'))
def delete_event(request, id):
    v1 = VolunteerOpportunity.objects.get(id=id)
    
    for volunteer in v1.volunteers.all():
        user = Profile.objects.get(id = volunteer.id)
        user.points -= v1.hours.hour*10
        user.save(update_fields=['points'])

    if(v1.created_by == request.user):
        v1.delete()

    return redirect(reverse('created_volunteering'))

def index(request):
    template_name='project-1-37/index.html'
    leading_users = Profile.objects.order_by('-points', '-user')[:10]
    context = {
        'page_title' : "Welcome",
        'leading_users' : leading_users,
    }
    if not request.user.is_anonymous:
        context['user_profile'] = Profile.objects.get(user=request.user)
    return render(request,template_name,context)

@login_required(redirect_field_name=None)
def leaderboard(request):
    template_name = 'project-1-37/leaderboard.html'
    leading_users = Profile.objects.order_by('-points', '-user')[:10]
    context = {
        'page_title' : "Leaderboard",
        'leading_users' : leading_users,
    }
    return render(request,template_name,context)

@login_required(redirect_field_name=None)
def profile(request, u_id=None):
    template_name = 'project-1-37/profile.html'
    if u_id is not None:
        other_user = get_object_or_404(User, pk=u_id)
        context = {
            'page_title' : "Profile",
            'user' : other_user,            
            'user_profile' : Profile.objects.get(user=other_user),
        }
    else:
        context = {
            'page_title' : "Profile",
            'user_profile' : Profile.objects.get(user=request.user),
        }
    return render(request,template_name,context)
@login_required(redirect_field_name=None)
def save_settings(request):
    form = UserSettingsForm(request.POST)
    usernameSame = (request.user.username == request.POST['username'])
    # this is a mess but the username validation is not a good time
    if form.is_valid() or (usernameSame and 'username' in form.errors and len(form.errors["username"])==1 and "exists" in form.errors["username"][0]):
        if request.method == 'POST' and 'settings_save' in request.POST:
            request.user.username = request.POST['username']
            request.user.first_name = request.POST['first_name']
            request.user.last_name = request.POST['last_name']
            try:
                request.user.save()
            except (IntegrityError):
                return user_settings(request, error_msg="Username taken. Please select a different username.")
            return HttpResponseRedirect(reverse('profile'))
    else:
        errors = []
        if('username' in form.errors):
            for usernameErr in form.errors['username']:
                if("exists" in usernameErr and usernameSame):
                    continue
                errors.append(usernameErr)
        if('first_name' in form.errors):
            errors.extend(form.errors['first_name'])
        if('last_name' in form.errors):
            errors.extend(form.errors['last_name'])
        if(len(errors)==0):
            return HttpResponseRedirect(reverse('profile'))
        else:
            # shows one error at a time
            return user_settings(request, error_msg=errors[0])
@login_required(redirect_field_name=None)
def user_settings(request, error_msg=None):
    template_name = 'project-1-37/user_settings.html' 
    form = UserSettingsForm(initial={'username': request.user.username, 'first_name': request.user.first_name, 'last_name': request.user.last_name})
    context = {
        'page_title' : "Settings",
        'form' : form,
        'error_message' : error_msg,
    }
    return render(request,template_name,context)
"""
# In case it's better to separate out current user from other user cases...
@login_required(redirect_field_name=None)
def profile_other(request, u_id):
    template_name = 'project-1-37/profile.html'
    other_user = get_object_or_404(User, pk=u_id)
    context = {
        'page_title' : "Profile",
        'user' : other_user,
    }
    return render(request, template_name, context)
"""
@login_required(redirect_field_name=None)
def profile_volunteering(request):
    template_name = 'project-1-37/volunteer_list.html'
    context = {
        'page_title' : "Events I've Signed Up for",
        'v1' : VolunteerOpportunity.objects.filter(volunteers = request.user).order_by('start_datetime'),
        'type' : 'remove_self',
    }         
    return render(request,template_name,context)  

@login_required(redirect_field_name=None)
def profile_donation(request):
    template_name = 'project-1-37/donation_list.html'
    transactions = DonationTransaction.objects.filter(donator= request.user)
    history = []
    for transaction in transactions:
        donation = DonationOpportunity.objects.get(id = transaction.donated_to.id)
        x = {}
        x['id'] = donation.id
        x['d_org'] = donation.d_org
        x['d_description'] = donation.d_description
        x['d_causes'] = donation.d_causes
        x['d_created_by'] = donation.d_created_by
        x['transaction_date'] = transaction.transaction_date
        x['amount_donated'] = transaction.amount_donated
        history.append(x)
    context = {
        'page_title' : "Donation History",
        'v1' : history,
        'profile' : True,
    }         
    return render(request,template_name,context)  

@login_required(redirect_field_name=None)
def profile_created_volunteering(request):
    template_name = 'project-1-37/volunteer_list.html'
    context = {
        'page_title' : "Events I've Created",
        'v1' : VolunteerOpportunity.objects.filter(created_by = request.user).order_by('start_datetime'),
        'type' : 'delete',
    }         
    return render(request,template_name,context) 

@login_required(redirect_field_name=None)
def profile_created_donations(request):
    template_name = 'project-1-37/donation_list.html'
    context = {
        'page_title' : "Donation Opportunities I've Created",
        'v1' : DonationOpportunity.objects.filter(d_created_by = request.user),
        'type': 'created_d',
    }
    return render(request,template_name,context)  

@login_required(redirect_field_name=None)
def profile_checkout(request, id):
    template_name = 'project-1-37/checkout.html'
    form = TransactionForm()
    context = {
        'page_title' : "Donation Checkout Page",
        'form' : form,
        'id': id,
    }
    return render(request,template_name,context) 

@login_required(redirect_field_name=None)
@csrf_exempt
def profile_checkout_confirm(request, id):
    amount = request.body.decode('utf-8')
    amount = Decimal(amount)
    d1 = DonationOpportunity.objects.get(id = id)
    d1.d_total_received += amount
    d1.save(update_fields=['d_total_received'])
    t = DonationTransaction(donator=request.user, amount_donated=amount, donated_to=d1, transaction_date=timezone.now())
    t.save()
    
    user = Profile.objects.get(id=request.user.id)
    user.points += round(amount)
    user.save(update_fields=['points'])
    
    return HttpResponse(status=200)


@login_required(redirect_field_name=None)
def volunteer_post(request):
    template_name = 'project-1-37/volunteer_post.html'
    form = VolunteerForm()
    context = {
        'page_title' : "Create Volunteering Opportunity",
        'form': form,
    }
    return render(request, template_name, context)

@login_required(redirect_field_name=None)
def volunteer_list(request):
    template_name = 'project-1-37/volunteer_list.html'
    page_title = "Volunteering Opportunities"
    v1 = VolunteerOpportunity.objects.exclude(volunteers=request.user).exclude(volunteers_needed__lt=1).exclude(start_datetime__lt=timezone.now()).order_by('start_datetime')
    context = {
        'page_title' : page_title,
        'v1' : v1,
    }            
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            # Sets the volunteer opportunity's "created_by" to the current user
            form.instance.created_by = request.user
            form.save()
            return redirect(reverse("volunteer_list"))
    else:
        form = VolunteerForm()
    return render(request,template_name,context)


@login_required(redirect_field_name=None)
def donation_post(request):
    template_name = 'project-1-37/donation_post.html'
    form = DonationForm()
    context = {
        'page_title' : "Create Donation Opportunity",
        'form' : form,
    }
    return render(request, template_name, context)

@login_required(redirect_field_name=None)
def donation_list(request):
    template_name = 'project-1-37/donation_list.html'
    context = {
        'page_title' : "Donation Opportunities",
        'v1' : DonationOpportunity.objects.all(),
    }
    if request.method == 'POST':
        exclusions = DonationOpportunity(d_date=timezone.now())
        form = DonationForm(request.POST, instance=exclusions)
        if form.is_valid():
            # Sets the donation's "created_by" to the current user
            form.instance.d_created_by = request.user
            form.save()
            return redirect(reverse('donation_list'))
    else:
        form = DonationForm()
    return render(request,template_name,context)