# Generated by Django 5.0.7 on 2024-10-19 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientmodels',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='DoctorModels',
        ),
        migrations.DeleteModel(
            name='PatientModels',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]