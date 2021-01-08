# Generated by Django 3.1.4 on 2021-01-05 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_option_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.BooleanField(default=False)),
                ('option_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.option')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
            ],
        ),
    ]
