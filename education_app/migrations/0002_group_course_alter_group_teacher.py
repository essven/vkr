# Generated by Django 4.0.4 on 2022-04-28 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='course',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='education_app.course'),
        ),
        migrations.AlterField(
            model_name='group',
            name='teacher',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='education_app.employee'),
        ),
    ]
