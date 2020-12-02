###############################################################################
#   REFERENCES
#   Title: Django RequestFactory
#   Author: Tim Graham, Adrian Holovaty, Claude Paroz, et. al.
#   Date: August 2020
#   Code version: 3.1.3
#   URL: https://docs.djangoproject.com/en/3.1/topics/testing/advanced/#the-request-factory 
#   Software License: MIT
#
#   REFERENCES
#   Title: How to Unit Test a Django Form
#   Author: Adam Johnson
#   Date Created: 06/15/2020
#   Date Accessed: November 2020
#   Code version: 3.1.3
#   URL: https://adamj.eu/tech/2020/06/15/how-to-unit-test-a-django-form/
#   Software License: MIT
#
#   REFERENCES
#   Title: Django Tutorial Part 10: Testing a Django web application
#   Date Accessed: November 2020
#   Code version: 3.1.3
#   URL: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
#   Software License: MIT
###############################################################################

from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
import datetime
from django.utils import timezone
from django.contrib.auth.models import User, AnonymousUser

from .models import Profile, VolunteerOpportunity, DonationOpportunity, DonationTransaction

from .forms import VolunteerForm, UserSettingsForm
from .views import index, profile, leaderboard, volunteer_post, volunteer_list, apply, profile_donation, remove_signup, donation_list, donation_post, profile_checkout, delete_event
from .views import donation_list, donation_post, profile_checkout, user_settings, save_settings

from http import HTTPStatus

class CreateUserTests(TestCase):
    def test_create_user_normal(self):
        test_user = User.objects.create_user(username='tester', email='cjk0021@gmail.com', password='password')
        self.assertIs(test_user.profile.bio, '')
        self.assertIs(test_user.profile.points, 0)
    def test_negative_user_points(self):
        test_user = User.objects.create_user(username='tester', email='cjk0021@gmail.com', password='password')
        self.assertIs(test_user.profile.bio, '')
        self.assertIs(test_user.profile.points, 0)

class VolunteerOpportunitiesModelTests(TestCase):

    def test_open_event_with_no_volunteers_needed(self):
        """ open_event() returns False when no more volunteers are needed """
        time = timezone.now() + timezone.timedelta(days=1)
        closed_opp = VolunteerOpportunity(volunteers_needed=0, start_datetime=time)
        self.assertIs(closed_opp.open_event(), False)

    def test_open_event_with_valid(self):
        """ open_event() returns True when any volunteers are needed and
            opportunity is scheduled for the future """
        time = timezone.now() + timezone.timedelta(days=1)
        open_opp = VolunteerOpportunity(volunteers_needed=1, start_datetime=time)
        self.assertIs(open_opp.open_event(), True)

    def test_invalid_start_datetime(self):
        """ open_event() returns False when start_datetime is past """
        time = timezone.now() - timezone.timedelta(seconds=1)
        past_opp = VolunteerOpportunity(volunteers_needed=1, start_datetime=time)
        self.assertIs(past_opp.open_event(), False)

    def test_invalid_volunteers(self):
        """ VolunteerOpportunity should not allow negative volunteers """
        with self.assertRaises(ValidationError):
            VolunteerOpportunity(volunteers_needed=(-1)).full_clean()

class VolunteerPostFormTests(TestCase):

    # Good data for testing purposes
    # data = {'event_name': 'Event Name',
    #         'hours': datetime.time(hour=1),
    #         'start_datetime': timezone.now() + timezone.timedelta(days=1),
    #         'location': 'Test Location',
    #         'description': 'Test Description',
    #         'volunteers_needed': 5,
    #         'created_by': self.user}
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='alanna',email='az5dd@virginia.edu',password='passwd')

    def test_past_event(self):
        ''' An event that occurs in the past should raise a validation error '''
        data = {'event_name': 'Event Name',
                'hours': datetime.time(hour=1),
                'start_datetime': timezone.now() - timezone.timedelta(seconds=1), # Specific to this test
                'location': 'Test Location',
                'description': 'Test Description',
                'volunteers_needed': 5,
                'created_by': self.user}
        form = VolunteerForm(data)
        self.assertEqual(form.is_valid(), False)

    def test_zero_volunteers(self):
        ''' An event that specifies 0 volunteers needed should raise a validation error '''
        data = {'event_name': 'Event Name',
                'hours': datetime.time(hour=1),
                'start_datetime': timezone.now() + timezone.timedelta(days=1),
                'location': 'Test Location',
                'description': 'Test Description',
                'volunteers_needed': 0, # Specific to this test
                'created_by': self.user}
        form = VolunteerForm(data)
        self.assertEqual(form.is_valid(), False)

    def test_valid(self):
        ''' Test that a valid event is interpretted as valid '''
        data = {'event_name': 'Event Name',
                'hours': datetime.time(hour=1),
                'start_datetime': timezone.now() + timezone.timedelta(days=1),
                'location': 'Test Location',
                'description': 'Test Description',
                'volunteers_needed': 1,
                'created_by': self.user}
        form = VolunteerForm(data)
        self.assertEqual(form.is_valid(), True)

    def test_access_volunteer_post(self):
        ''' Test that a normal user can access the volunteer_post '''
        request = self.factory.get('/volunteer_post')
        request.user = self.user # Simulates logged in user
        response = volunteer_post(request)
        self.assertEqual(response.status_code,200)

    def test_forbid_access_volunteer_post(self):
        ''' Test that someone who is not logged in cannot access the volunteer_post '''
        request = self.factory.get('/volunteer_post')
        request.user = AnonymousUser() # Has is_authenticated set to false
        response = volunteer_post(request) # Send in anonymous request

        self.assertEqual(response.status_code,302) # Check that it redirected

class VolunteerListTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='alanna',email='az5dd@virginia.edu',password='passwd')

    # Had thrown a ValueError: Missing staticfiles manifest entry for 'project-1-37/styles.css'
    # Run python manage.py collectstatic and then test works
    def test_access_volunteer_list(self):
        ''' Test that a normal user can access the volunteer_list '''
        request = self.factory.get('/volunteer_list')
        request.user = self.user # Simulates logged in user
        response = volunteer_list(request)
        self.assertEqual(response.status_code,200)

    def test_forbid_access_volunteer_list(self):
        ''' Test that someone who is not logged in cannot access the volunteer_list '''
        request = self.factory.get('/volunteer_list')
        request.user = AnonymousUser() # Has is_authenticated set to false
        response = volunteer_list(request) # Send in anonymous request

        self.assertEqual(response.status_code,302) # Check that it redirected    

class TestDonationOpportunity(TestCase):
    
    def test_valid_d_org(self):
        """ Returns TRUE when valid org name was given """
        test1 = DonationOpportunity(d_org="Animal Adopt Org")
        self.assertIs(test1.d_org, "Animal Adopt Org")
        self.assertIsNot(test1.d_org, "WRONG WRONG WRONG")
        # print("test1")
        # print(test1.d_org)


    def test_valid_d_description(self):
        """ Returns TRUE when valid org desc was given """
        test1 = DonationOpportunity(d_description="We help advertise animals for adoption!")
        self.assertIs(test1.d_description, "We help advertise animals for adoption!")
        self.assertIsNot(test1.d_description, "WRONG WRONG WRONG")
        # print("test22")

    def test_valid_d_date(self):
        test1 = DonationOpportunity(d_date="10/20/20")
        self.assertIs(test1.d_date, "10/20/20")
        # self.assertIs(datetime.date.today(), "2020-10-20")
        # print(datetime.date.today())

class TestLeaderboard(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='alanna',email='az5dd@virginia.edu',password='passwd')

    # Had thrown a ValueError: Missing staticfiles manifest entry for 'project-1-37/styles.css'
    # Run python manage.py collectstatic and then test works
    def test_access_leaderboard(self):
        ''' Test that a normal user can access the leaderboard '''
        request = self.factory.get('/leaderboard')
        request.user = self.user # Simulates logged in user
        response = leaderboard(request)
        self.assertEqual(response.status_code,200)

    def test_forbid_access_leaderboard(self):
        ''' Test that someone who is not logged in cannot access the leaderboard '''
        request = self.factory.get('/leaderboard')
        request.user = AnonymousUser() # Has is_authenticated set to false
        response = leaderboard(request) # Send in anonymous request

        self.assertEqual(response.status_code,302) # Check that it redirected

class ProfileDonations(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='erwin1',email='ew9nd@virginia.edu',password='passwd')
        self.donation = DonationOpportunity.objects.create(d_org="Animal Adopt Org", d_date=timezone.now(), d_created_by= self.user)
        self.transaction = DonationTransaction.objects.create(donator=self.user, amount_donated=10, donated_to=self.donation, transaction_date = timezone.now())

    # Had thrown a ValueError: Missing staticfiles manifest entry for 'project-1-37/styles.css'
    # Run python manage.py collectstatic and then test works
    def test_access_profile_donation(self):
        ''' Test that a normal user can access the their donation history '''
        request = self.factory.get('/profile/donations')
        request.user = self.user # Simulates logged in user
        response = profile_donation(request)
        # print(response)
        self.assertEqual(response.status_code,200)

    def test_forbid_access_profile_donation(self):
        ''' Test that someone who is not logged in cannot access the volunteer_list '''
        request = self.factory.get('/profile/donations')
        request.user = AnonymousUser() # Has is_authenticated set to false
        response = profile_donation(request) # Send in anonymous request

class TestDonation(TestCase):
    # Referenced Alanna's TestLeaderboard as a template for the following test cases

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='tester1',email='email1@gmail.com',password='password1')

    def test_access_donation_list(self):
        ''' Test that a normal user can access the donation list page; (Returns TRUE if valid access) '''
        request = self.factory.get('/donation_list')
        request.user = self.user # Simulates logged in user
        response = donation_list(request)
        self.assertEqual(response.status_code,200)

    def test_forbid_access_donation_list(self):
        ''' Test that a non-logged-in user cannot access the donation list page; (Returns TRUE if invalid access) '''
        request = self.factory.get('/donation_list')
        request.user = AnonymousUser() # Has is_authenticated set to false
        response = donation_list(request) # Send in anonymous request
        self.assertEqual(response.status_code,302) # Check that it redirected


    def test_access_donation_post(self):
        ''' Test that a normal user can access the donation post page; (Returns TRUE if valid access) '''
        request = self.factory.get('/donation_post')
        request.user = self.user # Simulates logged in user
        response = donation_post(request)
        self.assertEqual(response.status_code,200)

    def test_forbid_access_donation_post(self):
        ''' Test that a non-logged-in user cannot access the donation post page; (Returns TRUE if invalid access) '''
        request = self.factory.get('/donation_post')
        request.user = AnonymousUser() # Has is_authenticated set to false
        response = donation_post(request) # Send in anonymous request
        self.assertEqual(response.status_code,302) # Check that it redirected


    def test_access_checkout(self):
        ''' Test that a normal user can access the donation checkout page; (Returns TRUE if valid access) '''
        request = self.factory.get('/checkout')
        id = 1
        request.user = self.user # Simulates logged in user
        response = profile_checkout(request, id)
        self.assertEqual(response.status_code,200)

    def test_forbid_access_checkout(self):
        ''' Test that a non-logged-in user cannot access the checkout page; (Returns TRUE if invalid access) '''
        request = self.factory.get('/checkout')
        id = 1
        request.user = AnonymousUser() # Has is_authenticated set to false
        response = profile_checkout(request, id) # Send in anonymous request
        self.assertEqual(response.status_code,302) # Check that it redirected

class TestUserSettings(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='clara',email='cjk8ad@virginia.edu',password='password', first_name='Clara', last_name='K.')
        anotherUser = User.objects.create_user(username='claraAgain',email='cjk0021@gmail.com',password='password', first_name='Clara', last_name='K.')
        self.client = Client()
        self.client.login(username="clara", password="password")

    def test_access_user_settings(self):
        ''' Test that a normal user can access their settings '''
        request = self.factory.get('/settings')
        request.user = self.user # Simulates logged in user
        response = user_settings(request)
        self.assertEqual(response.status_code,200)

    def test_forbid_access_user_settings(self):
        ''' Test that someone who is not logged in cannot access settings '''
        request = self.factory.get('/settings')
        request.user = AnonymousUser() # Has is_authenticated set to false
        response = user_settings(request) # Send in anonymous request
        self.assertEqual(response.status_code,302) # Check that it redirected

    def test_all_fields_same(self):
        ''' Form should be considered invalid if username stays the same '''
        data = {'username': self.user.username,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,}
        form = UserSettingsForm(data)
        self.assertEqual(form.is_valid(), False)

    def test_all_fields_same_redirect(self):
        ''' Form should be considered invalid if username stays the same, but should still redirect '''
        data = {'username': self.user.username,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,}
        form = UserSettingsForm(data)
        response = self.client.post(
            "/save_settings", data = data, content_type='application/json'
        )
        self.assertEqual(response.status_code, 301)

    def test_change_username_valid(self):
        ''' No errors should be raised if all field inputs are valid'''
        data = {'username': "clara2",
                'first_name': "Valid",
                'last_name': "Valid",}
        form = UserSettingsForm(data)
        self.assertEqual(form.is_valid(), True)
    
    def test_change_username_invalid(self):
        ''' An error should be raised if the user attempts to change their username to one already in use '''
        data = {'username': "claraAgain",
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,}
        form = UserSettingsForm(data)
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors["username"], ['A user with that username already exists.'])

    def test_change_username_invalid_chars(self):
        ''' An error should be raised if the user attempts to change their username to one with invalid characters '''
        data = {'username': "clara username",
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,}
        form = UserSettingsForm(data)
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors["username"], ['Username contains invalid characters. Please select a different Username.'])

    def test_change_username_invalid_length(self):
        ''' An error should be raised if the user attempts to change their username to one that is too long (i.e. greater than 150 characters) '''
        longStr = "0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"
        data = {'username': longStr,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,}
        form = UserSettingsForm(data)
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors["username"], ['Ensure this value has at most 150 characters (it has 160).'])

    def test_change_fname_invalid(self):
        ''' An error should be raised if the user attempts to change their name to one with invalid characters '''
        data = {'username': "clara2",
                'first_name': "SomethingWithNumber1",
                'last_name': self.user.last_name,}
        form = UserSettingsForm(data)
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors["first_name"], ['First name should contain letters and ./- only.'])
    
    def test_change_lname_invalid(self):
        ''' An error should be raised if the user attempts to change their name to one with invalid characters '''
        data = {'username': "clara2",
                'first_name': self.user.first_name,
                'last_name': "SomethingWithNumber1",}
        form = UserSettingsForm(data)
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors["last_name"], ['Last name should contain letters and ./- only.'])

class TestProfileCreatedVolunteering(TestCase):
    def setUp(self):
        time = timezone.now() + timezone.timedelta(days=1)
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='clara',email='cjk8ad@virginia.edu',password='password')
        self.user.save()
        self.client = Client()
        self.client.login(username='clara', password='password')
        self.myEvent = VolunteerOpportunity.objects.create(event_name = "A TEST EVENT",volunteers_needed=1, start_datetime=time,created_by = self.user)
        anotherUser = User.objects.create_user(username='claraDifferent',email='cjk0021@gmail.com',password='password')
        anotherEvent = VolunteerOpportunity.objects.create(event_name = "A DIFFERENT TEST EVENT",volunteers_needed=1, start_datetime=time,created_by = anotherUser)
    
    def test_profile_volunteering_created_template(self):
        response = self.client.get('/profile/created_volunteering/')
        self.assertTemplateUsed(response, 'project-1-37/volunteer_list.html')
    
    def test_profile_volunteering_created(self):
        ''' A user's created_volunteering profile should render the the event(s) created by the user on the page, but not other events '''
        response = self.client.get('/profile/created_volunteering/')
        self.assertContains(response, 'A TEST EVENT')
        self.assertNotContains(response, 'A DIFFERENT TEST EVENT')
    
    def test_profile_volunteering_delete_event(self):
        ''' Once a User deletes an event they have created, a user's created_volunteering profile should not render the the event any longer '''
        request = self.factory.get('/delete/'+str(self.myEvent.id))
        request.user = self.user # Simulates logged in user
        response = delete_event(request, self.myEvent.id)
        response = self.client.get('/profile/created_volunteering/')
        self.assertNotContains(response, 'A TEST EVENT')

class Points(TestCase):
    def setUp(self):
        time = timezone.now() + timezone.timedelta(days=1)
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='erwin1',email='ew9nd@virginia.edu',password='passwd')
        self.volunteer = VolunteerOpportunity.objects.create(event_name='test1', volunteers_needed=2, start_datetime=time, created_by=self.user)
        self.user.profile.points += 10
        self.user.save()

    # Had thrown a ValueError: Missing staticfiles manifest entry for 'project-1-37/styles.css'
    # Run python manage.py collectstatic and then test works
    def test_apply_user_added(self):
        ''' Test for apply user has been added '''
        request = self.factory.get('/apply/'+str(self.volunteer.id))
        request.user = self.user # Simulates logged in user
        response = apply(request, self.volunteer.id)
        self.volunteer.refresh_from_db()
        self.assertEqual(self.volunteer.volunteers.get(), self.user)
    
    def test_apply_user_added(self):
        ''' Test for apply volunteer needed decreased '''
        request = self.factory.get('/apply/'+str(self.volunteer.id))
        request.user = self.user # Simulates logged in user
        response = apply(request, self.volunteer.id)
        self.volunteer.refresh_from_db()
        self.assertEqual(self.volunteer.volunteers_needed, 1)
    
    def test_apply_user_point_increased(self):
        ''' Test for apply user point increased by the hour '''
        request = self.factory.get('/apply/'+str(self.volunteer.id))
        request.user = self.user # Simulates logged in user
        response = apply(request, self.volunteer.id)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.points, 20)
    
    def test_remove_signup_user_point_deducted(self):
        ''' Test for remove sign up user point reduced by the hour '''
        self.volunteer.volunteers.add(self.user)
        request = self.factory.get('/remove/'+str(self.volunteer.id))
        request.user = self.user # Simulates logged in user
        response = remove_signup(request, self.volunteer.id)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.points, 0)

    def test_remove_signup_volunteers_needed(self):
        ''' Test for remove sign up volunteer needed increases '''
        self.volunteer.volunteers.add(self.user)
        request = self.factory.get('/remove/'+str(self.volunteer.id))
        request.user = self.user # Simulates logged in user
        response = remove_signup(request, self.volunteer.id)
        self.user.refresh_from_db()
        self.assertEqual(self.volunteer.volunteers_needed, 2)
    
