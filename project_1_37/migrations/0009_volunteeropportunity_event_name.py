# Generated by Django 3.1.1 on 2020-11-05 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_1_37', '0008_donationopportunity_d_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteeropportunity',
            name='event_name',
            field=models.CharField(default='Event', max_length=50),
            preserve_default=False,
        ),
    ]
