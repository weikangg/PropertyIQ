# Generated by Django 4.1.7 on 2023-03-05 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='realtor',
        ),
    ]
