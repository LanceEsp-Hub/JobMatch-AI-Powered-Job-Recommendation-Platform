# Generated by Django 5.1.3 on 2024-12-01 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_jobmatch_resume_resume_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobmatch',
            name='matched_at',
        ),
    ]
