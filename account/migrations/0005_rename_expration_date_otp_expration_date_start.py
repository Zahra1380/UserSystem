# Generated by Django 4.2.4 on 2023-09-02 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_otp_options_otp_token_alter_otp_code_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otp',
            old_name='expration_date',
            new_name='expration_date_start',
        ),
    ]
