# Generated by Django 3.1.1 on 2020-10-20 21:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationOpportunity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_org', models.TextField()),
                ('d_description', models.TextField()),
                ('d_date', models.DateField()),
                ('d_amount', models.FloatField()),
                ('d_causes', multiselectfield.db.fields.MultiSelectField(choices=[('Children1', 'Children'), ('Elderly1', 'Elderly'), ('Environmental1', 'Environmental'), ('Animals1', 'Animals'), ('Homelessness1', 'Homelessness'), ('Poverty1', 'Poverty'), ('SpecialOlympics1', 'Special Olmypics')], max_length=82)),
            ],
        ),
        migrations.CreateModel(
            name='VolunteerOpportunity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField()),
                ('hours', models.DurationField()),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=75)),
                ('volunteers_needed', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=200)),
                ('points', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
