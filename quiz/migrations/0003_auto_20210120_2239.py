# Generated by Django 3.1.4 on 2021-01-20 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20210118_2134'),
    ]

    operations = [
        migrations.RenameField(
            model_name='option',
            old_name='question_id',
            new_name='question',
        ),
    ]