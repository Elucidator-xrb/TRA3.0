# Generated by Django 4.0.3 on 2022-05-29 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_shieldingwords'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='related_schedule',
        ),
        migrations.AddField(
            model_name='message',
            name='related_flight',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.flight'),
        ),
        migrations.AddField(
            model_name='message',
            name='related_scheduleitem',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.scheduleitem'),
        ),
    ]
