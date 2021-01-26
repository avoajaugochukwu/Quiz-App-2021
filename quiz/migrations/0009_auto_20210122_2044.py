# Generated by Django 3.1.4 on 2021-01-22 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_auto_20210122_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choice_question', to='quiz.question'),
        ),
        migrations.AlterField(
            model_name='quizanswer',
            name='choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizAnswer_choice', to='quiz.choice'),
        ),
        migrations.AlterField(
            model_name='quizanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizAnswer_question', to='quiz.question'),
        ),
        migrations.AlterField(
            model_name='quizanswer',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizAnswer_quiz', to='quiz.quiz'),
        ),
    ]