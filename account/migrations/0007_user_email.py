# Generated by Django 4.2.4 on 2023-09-03 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_rename_expration_date_start_otp_expration_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='آدرس ایمیل'),
        ),
    ]
