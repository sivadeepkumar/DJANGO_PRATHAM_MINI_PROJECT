# Generated by Django 4.2.4 on 2023-09-04 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('noticeboard', '0002_remove_noticeboard_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NoticeBoard',
        ),
    ]
