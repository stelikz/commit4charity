from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from multiselectfield import MultiSelectField #import multiple selection

d_causes_choices = (('Children', 'Children'),
                    ('Elderly', 'Elderly'),
                    ('Environmental', 'Environmental'),
                    ('Animals', 'Animals'),
                    ('Homelessness', 'Homelessness'),
                    ('Poverty', 'Poverty'),
                    ('Disabilities', 'Disabilities'),
                    ('Medical Philanthropy','Medical Philanthropy'))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=200, blank=True)
    points = models.PositiveIntegerField(default=0)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class VolunteerOpportunity(models.Model):
    """ Model for user-posted volunteer opportunities """
    event_name = models.CharField(max_length=50)
    start_datetime = models.DateTimeField()
    hours = models.TimeField(default=datetime.time(hour=1))
    location = models.CharField(max_length=75)
    description = models.TextField()
    volunteers_needed = models.PositiveIntegerField() # Allows 0
    volunteers = models.ManyToManyField(User)
    created_by = models.ForeignKey(User, related_name ='created_by' ,on_delete=models.CASCADE)
    def open_event(self):
        """ Whether an event still has volunteer spots open 
            and whether the event is in the future """
        in_future = self.start_datetime > timezone.now()
        return (self.volunteers_needed > 0) and in_future

class DonationOpportunity(models.Model):
    d_org = models.CharField(max_length=75) #name of org posting donation opp
    d_description = models.TextField() #description of donation opp
    d_date = models.DateField() #posted date of donation opp ------- NOT USING IT SEEMS -------
    d_created_by = models.ForeignKey(User, related_name ='d_created_by' ,on_delete=models.CASCADE)

    d_causes = MultiSelectField(choices = d_causes_choices)
    d_total_received = models.DecimalField(max_digits=8, decimal_places=2, default=0)

class DonationTransaction(models.Model):
    donator = models.ForeignKey(User, related_name = 'donator', on_delete=models.CASCADE)
    amount_donated = models.DecimalField(max_digits=6, decimal_places=2)
    donated_to = models.ForeignKey(DonationOpportunity, related_name = 'donated_to', on_delete=models.CASCADE)
    transaction_date = models.DateField()


